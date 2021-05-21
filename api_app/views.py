from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.core.exceptions import ObjectDoesNotExist

from api_app.exceptions import ImageDoesNotExist, OriginalImageTypeDoesNotExist
from api_app.models import Image, ThumbnailType
from api_app.permissions import CreateExpiredLinkPermission, HasUserAccountTier
from api_app.serializers import ImageListSerializer, ExpiredLinkCreateSerializer, ImageSerializer
from api_app.services import resize_image, set_link_expiring_datetime, get_base64_encode_image
from api_image_links.settings import domen_and_port_for_link


class CreateImage(CreateAPIView):
    """Allows to upload image by POST request to 'upload/' """

    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        try:
            image_type = ThumbnailType.objects.get(is_original=True)
        except ObjectDoesNotExist:
            raise OriginalImageTypeDoesNotExist
        _serializer = serializer.save(user=self.request.user, type=image_type)
        thumbnails_heigth_sizes_and_types = resize_image(_serializer.image)
        for size_and_type in thumbnails_heigth_sizes_and_types:
            new_thumbnail_image, new_thumbnail_type = size_and_type
            Image.objects.create(image=new_thumbnail_image, type=new_thumbnail_type, user=self.request.user,
                                 title=_serializer.title)


class ImageListView(APIView):
    """Allows to get list of all user's images according to account tier by GET request to 'images/' """

    permission_classes = [IsAuthenticated, HasUserAccountTier]

    def get(self, request):
        user = request.user
        images = Image.objects.filter(user=user, type__in=user.account_tier.allowed_image_types.all())
        serializer = ImageListSerializer(images, many=True)
        return Response(serializer.data)


class ExpiredLinkCreateView(CreateAPIView):
    """Allows to generate expiry link by POST request to 'exp_link_create/<image_id>/' """

    serializer_class = ExpiredLinkCreateSerializer
    permission_classes = [IsAuthenticated, CreateExpiredLinkPermission]

    def perform_create(self, serializer):
        try:
            image = Image.objects.get(id=self.kwargs['pk'])
        except ObjectDoesNotExist:
            raise ImageDoesNotExist

        user_exp_time_seconds = serializer.validated_data['user_exp_time_seconds']
        link_exp_datetime = set_link_expiring_datetime(user_exp_time_seconds)
        title = f'{image.title}_{image.type.title}_expiry'
        image_base_64 = get_base64_encode_image(image.image.url)
        _serializer = serializer.save(
            user=self.request.user,
            expiry_date_time=link_exp_datetime,
            image=image,
            user_exp_time_seconds=user_exp_time_seconds,
            title=title,
            image_base_64=image_base_64
        )
        _serializer.expiry_link = f'{domen_and_port_for_link}/temp/{_serializer.uuid_link}'
        _serializer.save()

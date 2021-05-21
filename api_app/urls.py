from django.urls import path

from api_app.views import CreateImage, ImageListView, ExpiredLinkCreateView

urlpatterns = [
    path('upload/', CreateImage.as_view()),
    path('images/', ImageListView.as_view()),
    path('exp_link_create/<int:pk>/', ExpiredLinkCreateView.as_view()),

]
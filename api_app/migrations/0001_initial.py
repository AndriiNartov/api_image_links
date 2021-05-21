# Generated by Django 3.2.3 on 2021-05-21 08:25

import api_app.models
from django.conf import settings
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('username', models.CharField(error_messages={'unique': 'A user with that username already exists.'}, help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150, unique=True, validators=[django.contrib.auth.validators.UnicodeUsernameValidator()], verbose_name='username')),
                ('first_name', models.CharField(blank=True, max_length=150, verbose_name='first name')),
                ('last_name', models.CharField(blank=True, max_length=150, verbose_name='last name')),
                ('email', models.EmailField(blank=True, max_length=254, verbose_name='email address')),
                ('is_staff', models.BooleanField(default=False, help_text='Designates whether the user can log into this admin site.', verbose_name='staff status')),
                ('is_active', models.BooleanField(default=True, help_text='Designates whether this user should be treated as active. Unselect this instead of deleting accounts.', verbose_name='active')),
                ('date_joined', models.DateTimeField(default=django.utils.timezone.now, verbose_name='date joined')),
            ],
            options={
                'verbose_name': 'user',
                'verbose_name_plural': 'users',
                'abstract': False,
            },
            managers=[
                ('objects', django.contrib.auth.models.UserManager()),
            ],
        ),
        migrations.CreateModel(
            name='ThumbnailType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Name of thumbnail')),
                ('heigth_size_in_pixels', models.PositiveSmallIntegerField(blank=True, null=True)),
                ('is_original', models.BooleanField(default=True, verbose_name='Image has original size')),
            ],
        ),
        migrations.CreateModel(
            name='Image',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Image title')),
                ('image', models.ImageField(upload_to=api_app.models.upload_image, validators=[django.core.validators.FileExtensionValidator(['png', 'jpeg', 'jpg'])])),
                ('type', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='thumbnail_links', to='api_app.thumbnailtype', verbose_name='Type of thumbnail')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='images', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='ExpiredLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=100, verbose_name='Name of link')),
                ('uuid_link', models.UUIDField(default=uuid.uuid4, editable=False, unique=True)),
                ('expiry_link', models.URLField(null=True, verbose_name='Expiry link for user')),
                ('user_exp_time_seconds', models.PositiveSmallIntegerField(default=300, validators=[django.core.validators.MinValueValidator(300, message='Value must be between 300 and 30000 seconds'), django.core.validators.MaxValueValidator(30000, message='Value must be between 300 and 30000 seconds')], verbose_name='Expiry time in seconds')),
                ('expiry_date_time', models.DateTimeField(blank=True, null=True, verbose_name='Expiry date and time')),
                ('image_base_64', models.BinaryField(verbose_name='Image in base64 format')),
                ('image', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='expired_links', to='api_app.image', verbose_name='Image')),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='expired_links', to=settings.AUTH_USER_MODEL, verbose_name='User')),
            ],
        ),
        migrations.CreateModel(
            name='AccountTier',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30, verbose_name='Name of account tier')),
                ('has_ability_create_expiry_link', models.BooleanField(default=False)),
                ('allowed_image_types', models.ManyToManyField(to='api_app.ThumbnailType', verbose_name='Allowed types of images')),
            ],
        ),
        migrations.AddField(
            model_name='user',
            name='account_tier',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='api_app.accounttier', verbose_name='Account tier'),
        ),
        migrations.AddField(
            model_name='user',
            name='groups',
            field=models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.Group', verbose_name='groups'),
        ),
        migrations.AddField(
            model_name='user',
            name='user_permissions',
            field=models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.Permission', verbose_name='user permissions'),
        ),
    ]

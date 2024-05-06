# Generated by Django 5.0.4 on 2024-05-06 00:19

import datetime
import django.contrib.auth.models
import django.contrib.auth.validators
import django.core.validators
import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
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
            name='Listing',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=50, verbose_name='Title')),
                ('description', models.CharField(max_length=1000, verbose_name='Description')),
                ('imageLink', models.URLField(blank=True, verbose_name='Image')),
                ('categories', models.CharField(blank=True, choices=[('AR', 'Armor'), ('PT', 'Potions'), ('RN', 'Rings'), ('RD', 'Rods'), ('SL', 'Scrolls'), ('SF', 'Staffs'), ('WN', 'Wands'), ('WP', 'Weapons'), ('WI', 'Wondrous Items'), ('OT', 'Other')], default='Other', max_length=2, verbose_name='Category')),
                ('active', models.BooleanField(default=True, verbose_name='Is Active')),
                ('created_at', models.DateTimeField(default=datetime.datetime.now, verbose_name='Created at')),
                ('updated_at', models.DateTimeField(default=datetime.datetime.now, verbose_name='Updated at')),
                ('lister', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='lister', to=settings.AUTH_USER_MODEL, verbose_name='Listed By')),
                ('watchlist', models.ManyToManyField(blank=True, null=True, related_name='listingWatchlist', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Comments',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('comment', models.CharField(max_length=500, verbose_name='Comment')),
                ('commented_at', models.DateField(default=datetime.datetime(2024, 5, 6, 0, 19, 17, 811015), verbose_name='Comment created at')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commented_by', to=settings.AUTH_USER_MODEL, verbose_name='Commented By')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='commented_on', to='auctions.listing', verbose_name='Commented On')),
            ],
        ),
        migrations.CreateModel(
            name='Offers',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('offer_amount', models.PositiveIntegerField(default=1, validators=[django.core.validators.MinValueValidator(1)], verbose_name='Offer')),
                ('offered_at', models.DateTimeField(default=datetime.datetime.now, verbose_name='Offer created at')),
                ('offerer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='offered_by', to=settings.AUTH_USER_MODEL, verbose_name='Offered By')),
            ],
        ),
        migrations.AddField(
            model_name='listing',
            name='price',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='price', to='auctions.offers', verbose_name='Price'),
        ),
        migrations.CreateModel(
            name='Winners',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateField(default=datetime.datetime.now, verbose_name='Product winned at')),
                ('item', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='product_winned', to='auctions.listing', verbose_name='Product Winned')),
                ('winned_by', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='winned_by', to=settings.AUTH_USER_MODEL, verbose_name='Winned by')),
            ],
        ),
    ]

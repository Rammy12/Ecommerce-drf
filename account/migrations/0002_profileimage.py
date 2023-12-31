# Generated by Django 4.2.1 on 2023-06-13 21:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ProfileImage',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('image', models.ImageField(upload_to='Profile')),
                ('userprofile', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='P_Image', to='account.profile')),
            ],
        ),
    ]

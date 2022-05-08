from django.contrib.auth.models import User
from django.db import migrations


def create_superuser(apps, schema_editor):
    user = User(
        username='root',
        email='root@gmail.com',
    )
    user.set_password('root')
    user.is_superuser = True
    user.is_staff = True
    user.save()

    return user


class Migration(migrations.Migration):
    dependencies = [('moviesApi', '0002_add_movies')]

    operations = [
        migrations.RunPython(create_superuser)
    ]

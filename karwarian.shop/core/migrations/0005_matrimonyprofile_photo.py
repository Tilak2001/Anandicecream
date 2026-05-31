from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0004_matrimonyprofile'),
    ]

    operations = [
        migrations.AddField(
            model_name='matrimonyprofile',
            name='photo',
            field=models.ImageField(blank=True, null=True, upload_to='matrimony/profiles/'),
        ),
    ]

# Generated manually for function services filtering

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('services', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='service',
            name='function_segment',
            field=models.CharField(
                blank=True,
                choices=[
                    ('decoration', 'Decoration'),
                    ('catering', 'Catering'),
                    ('photography', 'Photography'),
                ],
                help_text='Function Services category (decoration, catering, photography)',
                max_length=20,
            ),
        ),
        migrations.AddField(
            model_name='service',
            name='function_subcategory',
            field=models.CharField(
                blank=True,
                help_text='e.g. marriage, haldi, veg-thali, wedding',
                max_length=50,
            ),
        ),
    ]

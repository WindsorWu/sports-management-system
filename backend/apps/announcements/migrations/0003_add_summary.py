from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('announcements', '0002_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='announcement',
            name='summary',
            field=models.CharField(blank=True, default='', max_length=200, verbose_name='摘要'),
        ),
    ]

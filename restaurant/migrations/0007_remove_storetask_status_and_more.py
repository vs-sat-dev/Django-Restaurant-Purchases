# Generated by Django 4.0.4 on 2022-06-13 09:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('restaurant', '0006_alter_telegramnotification_status_storetask'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='storetask',
            name='status',
        ),
        migrations.AlterField(
            model_name='telegramnotification',
            name='status',
            field=models.CharField(choices=[('FreeTask', 'free_task'), ('BusyTask', 'busy_task'), ('ProcessTask', 'process_task')], default='free_task', max_length=32),
        ),
    ]

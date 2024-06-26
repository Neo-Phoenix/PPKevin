# Generated by Django 4.2.3 on 2024-06-09 06:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0007_alter_event_eventtype_alter_eventtype_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='ItemType',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naam', models.CharField(max_length=255)),
            ],
        ),
        migrations.RemoveField(
            model_name='event',
            name='description',
        ),
        migrations.RemoveField(
            model_name='event',
            name='title',
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('naam', models.CharField(max_length=255)),
                ('beschrijving', models.CharField(max_length=255)),
                ('itemTypeID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='app.itemtype')),
            ],
        ),
        migrations.AddField(
            model_name='event',
            name='itemid',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='app.item'),
            preserve_default=False,
        ),
    ]

# Generated by Django 4.0.5 on 2022-08-10 02:04

from django.db import migrations, models
import mdeditor.fields


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_editor_content'),
    ]

    operations = [
        migrations.CreateModel(
            name='Editor_md',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('content', mdeditor.fields.MDTextField()),
            ],
        ),
        migrations.DeleteModel(
            name='editor',
        ),
    ]
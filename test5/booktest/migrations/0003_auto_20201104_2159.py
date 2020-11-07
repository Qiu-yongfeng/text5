# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('booktest', '0002_areainfo'),
    ]

    operations = [
        migrations.CreateModel(
            name='PicTest',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('goods_pic', models.ImageField(upload_to='booktest')),
            ],
        ),
        migrations.AlterField(
            model_name='areainfo',
            name='aname',
            field=models.CharField(verbose_name='标题', max_length=20),
        ),
    ]

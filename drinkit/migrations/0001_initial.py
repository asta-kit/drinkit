# -*- coding: utf-8 -*-

# Drinkit – The drinker management used by the AStA at the KIT
#
# Written in 2015 by Michael Tänzer <neo@nhng.de>
#
# This stuff is beer-ware (CC0 flavour): If you meet one of the authors some
# day, and you think the stuff is worth it, you may buy them a beer in return,
# if you want to. Also you can do anything you want with the stuff (and we
# encourage that you do) because the stuff is formally licensed according to the
# following terms:
#
# To the extent possible under law, the author(s) have dedicated all copyright
# and related and neighboring rights to this software to the public domain
# worldwide. This software is distributed without any warranty.
#
# You should have received a copy of the CC0 Public Domain Dedication along with
# this software. If not, see <http://creativecommons.org/publicdomain/zero/1.0/>.

from __future__ import unicode_literals

from django.db import models, migrations
import datetime


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Consumption',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('count', models.PositiveSmallIntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Drink',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('name', models.CharField(max_length=255)),
                ('price', models.DecimalField(max_digits=6, decimal_places=2)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('price',),
            },
        ),
        migrations.CreateModel(
            name='Drinker',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('firstname', models.CharField(max_length=20)),
                ('lastname', models.CharField(max_length=20)),
                ('email', models.EmailField(max_length=254)),
                ('active', models.BooleanField(default=True)),
            ],
            options={
                'ordering': ('firstname', 'lastname'),
            },
        ),
        migrations.CreateModel(
            name='Transaction',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, primary_key=True, auto_created=True)),
                ('date', models.DateField(default=datetime.date.today)),
                ('amount', models.DecimalField(max_digits=6, decimal_places=2)),
                ('comment', models.CharField(max_length=255, blank=True)),
                ('drinker', models.ForeignKey(to='drinkit.Drinker')),
                ('reckoning', models.ManyToManyField(to='drinkit.Drink', through='drinkit.Consumption')),
            ],
            options={
                'ordering': ('-date', 'drinker'),
            },
        ),
        migrations.AddField(
            model_name='consumption',
            name='drink',
            field=models.ForeignKey(to='drinkit.Drink'),
        ),
        migrations.AddField(
            model_name='consumption',
            name='transaction',
            field=models.ForeignKey(to='drinkit.Transaction'),
        ),
        migrations.AlterUniqueTogether(
            name='consumption',
            unique_together=set([('drink', 'transaction')]),
        ),
    ]

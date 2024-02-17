# -*- coding: utf-8 -*-
# Generated by Django 1.11.29 on 2022-06-19 22:05
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("leprikon", "0069_question_slug"),
    ]

    operations = [
        migrations.AlterField(
            model_name="question",
            name="slug",
            field=models.SlugField(unique=True, verbose_name="unique identifier"),
        ),
        migrations.AddField(
            model_name="leprikonsite",
            name="decision_print_setup",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="leprikon.PrintSetup",
                verbose_name="default decision print setup",
            ),
        ),
        migrations.AddField(
            model_name="subject",
            name="decision_print_setup",
            field=models.ForeignKey(
                blank=True,
                help_text="Only use to set value specific for this subject.",
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="leprikon.PrintSetup",
                verbose_name="registration print setup",
            ),
        ),
        migrations.AddField(
            model_name="subjecttype",
            name="decision_print_setup",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name="+",
                to="leprikon.PrintSetup",
                verbose_name="decision print setup",
            ),
        ),
    ]

# -*- coding: utf-8 -*-
# Generated by Django 1.11.2 on 2017-06-16 07:18
from __future__ import unicode_literals

from django.db import migrations


def rename_position_names_to_side_names(apps, schema_editor):
    rename_preference(apps, "debate_rules", "position_names", "side_names")


def rename_side_names_to_position_names(apps, schema_editor):
    rename_preference(apps, "debate_rules", "side_names", "position_names")


def rename_preference(apps, section, old_name, new_name):
    TournamentPreferenceModel = apps.get_model("options", "TournamentPreferenceModel")

    old_prefs = TournamentPreferenceModel.objects.filter(section=section, name=old_name)

    for pref in old_prefs:
        # Can't use the value attribute, since it's not a real field.
        value = pref.raw_value

        # If there already exists a preference, leave it alone.
        if not TournamentPreferenceModel.objects.filter(section=section,
                name=new_name, instance_id=pref.instance_id).exists():
            TournamentPreferenceModel.objects.create(section=section,
                    name=new_name, instance_id=pref.instance_id, raw_value=value)

        # The checkpreferences command would do this, but since this preference
        # doesn't exist anymore, we may as well delete it now.
        pref.delete()


class Migration(migrations.Migration):

    dependencies = [
        ('options', '0007_convert_show_institutions'),
    ]

    operations = [
        migrations.RunPython(rename_position_names_to_side_names,
            reverse_code=rename_side_names_to_position_names),
    ]
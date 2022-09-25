import datetime

from django import forms
from django.forms import ModelForm

from .models import SiteConf, ConfigValues


class SiteConfCreateForm(ModelForm):
    class Meta:
        model = SiteConf
        fields = [
            'name',
            'scraper_name',
            'icon',
            'base_url',
            'extra_data_json',
            'enabled',
            'is_locked'
        ]


class ConfigValuesCreateForm(ModelForm):
    class Meta:
        model = ConfigValues
        fields = [
            'key',
            'val'
        ]
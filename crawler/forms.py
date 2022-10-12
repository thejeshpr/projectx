import datetime
import json

from django import forms
from django.core.exceptions import ValidationError
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


class SiteConfFormByJSON(forms.Form):
    json_data = forms.CharField(widget=forms.Textarea)

    def clean(self):
        cleaned_data = super().clean()
        json_data = self.cleaned_data.get("json_data")
        if json_data:
            try:
                _ = json.loads(json_data)
            except Exception as e:
                self.add_error(None, ValidationError(f"Invalid JSON Data: {e}"))
        return cleaned_data

    def create_site_conf(self):
        json_data = json.loads(self.cleaned_data.get("json_data"))
        SiteConf.objects.create(
            name=json_data.get("name"),
            scraper_name=json_data.get("scraper_name"),
            icon=json_data.get("icon"),
            base_url=json_data.get("base_url"),
            extra_data_json=json_data.get("extra_data_json"),
            enabled=json_data.get("enabled"),
            is_locked=json_data.get("enabled")
        )

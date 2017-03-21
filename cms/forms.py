from django import forms
from cms.models import (
    Partner,
    Text,
)


class PartnerForm(forms.ModelForm):
    class Meta:
        model = Partner
        fields = '__all__'

    def clean_logo(self):
        data = self.cleaned_data['logo']
        if 'https://' not in data:
            raise forms.ValidationError("Please only use https:// images.")
        return data


class TextForm(forms.ModelForm):
    class Meta:
        model = Text
        fields = '__all__'

    def clean_image_url(self):
        data = self.cleaned_data['image_url']
        if 'https://' not in data:
            raise forms.ValidationError("Please only use https:// images.")
        return data

    def clean_video_url(self):
        data = self.cleaned_data['video_url']
        if 'https://' not in data:
            raise forms.ValidationError("Please only use https:// links.")
        return data

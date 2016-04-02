from django.forms import ModelForm

from tests.testapp.models import EmptyVIESModel, VIESModel


class VIESModelForm(ModelForm):
    class Meta:
        model = VIESModel
        exclude = []


class EmptyVIESModelForm(ModelForm):
    class Meta:
        model = EmptyVIESModel
        exclude = []

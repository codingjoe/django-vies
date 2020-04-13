from django.db.models import CharField, Model

from vies import models


class VIESModel(Model):
    vat = models.VATINField()


class EmptyVIESModel(Model):
    name = CharField(default="John Doe", max_length=50)
    vat = models.VATINField(blank=True, null=True)

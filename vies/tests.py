from django.utils import unittest
from django.db.models import Model
from django.forms import Form, ModelForm

from vies import fields
from vies import models


class VIESModel(Model):
    vat = models.VIESField()


class VIESModelForm(ModelForm):
    class Meta:
        model = VIESModel


class VIESForm(Form):
    vat = fields.VIESField()


class ModelTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_create(self):
        """Object is correctly created."""
        vies = VIESModel.objects.create(vat='GB802311782')
        self.assertNotEqual(VIESModel.objects.count(), 0)
        self.assertEqual(vies.vat, 'GB802311782')

    def test_save(self):
        """Object is correctly saved."""
        vies_saved = VIESModel()
        vies_saved.vat = 'GB802311782'
        vies_saved.save()

        vies_received = VIESModel.objects.get(pk=vies_saved.pk)
        self.assertNotEqual(VIESModel.objects.count(), 0)
        self.assertEqual(vies_received.vat, 'GB802311782')


class ModelFormTestCase(unittest.TestCase):
    def test_is_valid(self):
        """Form is valid"""
        form = VIESModelForm({'vat_0': 'GB', 'vat_1': '802311782'})
        self.assertTrue(form.is_valid())

        vies = form.save()
        self.assertEqual(vies.vat, 'GB802311782')

    def test_is_not_valid_country(self):
        """Invalid country"""
        form = VIESModelForm({'vat_0': 'xx', 'vat_1': '802311782'})
        self.assertFalse(form.is_valid())

    def test_is_not_valid_numbers(self):
        """Invalid number"""
        form = VIESModelForm({'vat_0': 'GB', 'vat_1': 'xx123+-'})
        self.assertFalse(form.is_valid())

    def test_is_not_valid_numbers(self):
        """Invalid number"""
        form = VIESModelForm({'vat_0': 'GB', 'vat_1': '000000000'})
        self.assertFalse(form.is_valid())

    def test_save(self):
        """Form is valid"""
        form = VIESModelForm({'vat_0': 'GB', 'vat_1': '802311782'})
        vies_saved = form.save()

        vies_received = VIESModel.objects.get(pk=vies_saved.pk)
        self.assertEqual(vies_received, vies_saved)
        self.assertNotEqual(VIESModel.objects.count(), 0)
        self.assertEqual(vies_received.vat, 'GB802311782')
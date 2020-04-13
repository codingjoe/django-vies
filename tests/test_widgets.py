# -*- coding: utf-8 -*-
import pytest
from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from tests import VALID_VIES, VALID_VIES_COUNTRY_CODE, VALID_VIES_NUMBER
from tests.testapp.forms import EmptyVIESModelForm, VIESModelForm
from tests.testapp.models import VIESModel
from vies.forms import VATINWidget


class ModelTestCase(TestCase):
    def setUp(self):
        pass

    def test_create(self):
        """Object is correctly created."""
        vies = VIESModel.objects.create(vat=VALID_VIES)
        self.assertNotEqual(VIESModel.objects.count(), 0)
        self.assertEqual(vies.vat, VALID_VIES)

    def test_save(self):
        """Object is correctly saved."""
        vies_saved = VIESModel()
        vies_saved.vat = VALID_VIES
        vies_saved.save()

        vies_received = VIESModel.objects.get(pk=vies_saved.pk)
        self.assertNotEqual(VIESModel.objects.count(), 0)
        self.assertEqual(vies_received.vat, VALID_VIES)


class ModelFormTestCase(TestCase):
    def test_is_valid(self):
        """Form is valid."""
        form = VIESModelForm(
            {"vat_0": VALID_VIES_COUNTRY_CODE, "vat_1": VALID_VIES_NUMBER}
        )
        self.assertTrue(form.is_valid())

        vies = form.save()
        self.assertEqual(vies.vat, VALID_VIES)

    def test_is_not_valid_country(self):
        """Invalid country."""
        form = VIESModelForm({"vat_0": "xx", "vat_1": VALID_VIES_NUMBER})
        self.assertFalse(form.is_valid())

    def test_is_not_valid_numbers(self):
        """Invalid number."""
        form = VIESModelForm({"vat_0": VALID_VIES_COUNTRY_CODE, "vat_1": "xx123+-"})
        self.assertFalse(form.is_valid())

    def test_save(self):
        """Form is saved."""
        form = VIESModelForm(
            {"vat_0": VALID_VIES_COUNTRY_CODE, "vat_1": VALID_VIES_NUMBER}
        )
        self.assertTrue(form.is_valid())
        vies_saved = form.save()

        vies_received = VIESModel.objects.get(pk=vies_saved.pk)
        self.assertEqual(vies_received, vies_saved)
        self.assertNotEqual(VIESModel.objects.count(), 0)
        self.assertEqual(vies_received.vat, VALID_VIES)

    def test_empty(self):
        form = EmptyVIESModelForm({"name": "Eva"})
        self.assertTrue(form.is_valid())

    def test_is_valid_and_has_vatin_data(self):
        """Valid VATINFields' vatin_data() return result dict."""
        form = VIESModelForm({"vat_0": "CZ", "vat_1": "24147931"})

        assert form.is_valid()
        data = form.cleaned_data["vat"].data
        assert data["name"] == "Braiins Systems s.r.o."


class TestWidget(object):
    @pytest.mark.parametrize(
        "given_value",
        [
            [VALID_VIES_COUNTRY_CODE, VALID_VIES_NUMBER],
            ["", "%s%s" % (VALID_VIES_COUNTRY_CODE, VALID_VIES_NUMBER)],
            [
                VALID_VIES_COUNTRY_CODE,
                "%s%s" % (VALID_VIES_COUNTRY_CODE, VALID_VIES_NUMBER),
            ],
        ],
    )
    def test_value_from_datadict(self, given_value):
        widget = VATINWidget()
        data = {"my_field_%s" % i: value for i, value in enumerate(given_value)}
        v = widget.value_from_datadict(data, [], "my_field")
        assert v == [VALID_VIES_COUNTRY_CODE, VALID_VIES_NUMBER]

    def test_decompress(self):
        assert (VALID_VIES_COUNTRY_CODE, VALID_VIES_NUMBER) == VATINWidget().decompress(
            "%s%s" % (VALID_VIES_COUNTRY_CODE, VALID_VIES_NUMBER)
        )
        assert (VALID_VIES_COUNTRY_CODE, VALID_VIES_NUMBER) == VATINWidget().decompress(
            [VALID_VIES_COUNTRY_CODE, VALID_VIES_NUMBER]
        )
        assert (None, None) == VATINWidget().decompress(None)


class MockRequest(object):
    pass


request = MockRequest()


class AdminTestCase(TestCase):
    def setUp(self):
        self.site = AdminSite()

    def test_vatin_field_admin(self):
        """Admin form is generated."""
        ma = ModelAdmin(VIESModel, self.site)

        try:
            ma.get_form(request)
        except Exception as e:
            self.fail(e.message)

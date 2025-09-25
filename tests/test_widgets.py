from types import SimpleNamespace
from unittest.mock import patch

import pytest
from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.sites import AdminSite
from django.test import TestCase

from tests import VALID_VIES, VALID_VIES_COUNTRY_CODE, VALID_VIES_NUMBER
from tests.testapp.forms import EmptyVIESModelForm, VIESModelForm
from tests.testapp.models import VIESModel
from vies.forms import VATINWidget
from vies.forms.fields import VATINField


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

    @patch("vies.types.Client")
    def test_is_valid_and_has_vatin_data(self, mock_client):
        """Valid VATINFields' vatin_data() return result dict."""
        mock_client.return_value.service.checkVat.return_value = SimpleNamespace(
            countryCode="CZ",
            vatNumber="24147931",
            name="Braiins Systems s.r.o.",
            valid=True,
        )

        form = VIESModelForm({"vat_0": "CZ", "vat_1": "24147931"})

        assert form.is_valid()
        data = form.cleaned_data["vat"].data
        assert data.name == "Braiins Systems s.r.o."


class TestWidget:
    @pytest.mark.parametrize(
        "given_value",
        [
            [VALID_VIES_COUNTRY_CODE, VALID_VIES_NUMBER],
            ["", f"{VALID_VIES_COUNTRY_CODE}{VALID_VIES_NUMBER}"],
            [
                VALID_VIES_COUNTRY_CODE,
                f"{VALID_VIES_COUNTRY_CODE}{VALID_VIES_NUMBER}",
            ],
        ],
    )
    def test_value_from_datadict(self, given_value):
        widget = VATINWidget()
        data = {f"my_field_{i:d}": value for i, value in enumerate(given_value)}
        v = widget.value_from_datadict(data, [], "my_field")
        assert v == [VALID_VIES_COUNTRY_CODE, VALID_VIES_NUMBER]

    def test_decompress(self):
        assert VATINWidget().decompress(
            f"{VALID_VIES_COUNTRY_CODE}{VALID_VIES_NUMBER}"
        ) == (VALID_VIES_COUNTRY_CODE, VALID_VIES_NUMBER)
        assert VATINWidget().decompress(
            [VALID_VIES_COUNTRY_CODE, VALID_VIES_NUMBER]
        ) == (VALID_VIES_COUNTRY_CODE, VALID_VIES_NUMBER)
        assert VATINWidget().decompress(None) == (None, None)

    def test_no_attrs(self):
        widget = VATINWidget()
        assert "class" not in widget.attrs
        assert "class" not in widget.widgets[0].attrs
        assert "class" not in widget.widgets[1].attrs

    def test_attrs(self):
        widget = VATINWidget(attrs={"class": "someclass"})
        assert widget.attrs["class"] == "someclass"
        assert widget.widgets[0].attrs["class"] == "someclass"
        assert widget.widgets[1].attrs["class"] == "someclass"


class TestField:
    def test_no_attrs(self):
        field = VATINField()
        assert "class" not in field.widget.attrs
        assert "class" not in field.widget.widgets[0].attrs
        assert "class" not in field.widget.widgets[1].attrs

    def test_attrs(self):
        field = VATINField(attrs={"class": "someclass"})
        assert field.widget.attrs["class"] == "someclass"
        assert field.widget.widgets[0].attrs["class"] == "someclass"
        assert field.widget.widgets[1].attrs["class"] == "someclass"

    def test_attrs_from_widget(self):
        field = VATINField(widget=VATINWidget(attrs={"class": "otherclass"}))
        assert field.widget.attrs["class"] == "otherclass"
        assert field.widget.widgets[0].attrs["class"] == "otherclass"
        assert field.widget.widgets[1].attrs["class"] == "otherclass"


class MockRequest:
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

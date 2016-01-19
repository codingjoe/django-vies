# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

import logging

from django import get_version
from django.contrib.admin.options import ModelAdmin
from django.contrib.admin.sites import AdminSite
from django.db.models import CharField, Model
from django.forms import Form, ModelForm
from django.test import override_settings
from django.utils import unittest
from mock import patch
from suds import WebFault

from . import VATIN, VIES_COUNTRY_CHOICES, fields, models

VALID_VIES = 'DE284754038'
VALID_VIES_COUNTRY_CODE = 'DE'
VALID_VIES_NUMBER = '284754038'
VALID_VIES_IE = ['1234567X', '1X23456X', '1234567XX', ]


class VIESModel(Model):
    vat = models.VATINField()


class EmptyVIESModel(Model):
    name = CharField(default='John Doe', max_length=50)
    vat = models.VATINField(blank=True, null=True)


class VIESModelForm(ModelForm):
    class Meta:
        model = VIESModel
        exclude = []


class EmptyVIESModelForm(ModelForm):
    class Meta:
        model = EmptyVIESModel
        exclude = []


class VIESForm(Form):
    vat = fields.VATINField()


class EmptyVIESForm(Form):
    vat = fields.VATINField(required=False)


custom_error = {
    'invalid_vat': 'This VAT number is not valid'
}


class VIESFormCustomError(Form):
    vat = fields.VATINField(error_messages=custom_error)


custom_error_16 = {
    'invalid_vat': '%(value)s is not a valid European VAT.'
}


class VIESFormCustomError16(Form):
    vat = fields.VATINField(error_messages=custom_error_16)


class VIESTestCase(unittest.TestCase):
    def setUp(self):
        pass

    def test_creation(self):
        try:
            VATIN(VALID_VIES_COUNTRY_CODE, VALID_VIES_NUMBER)
        except Exception as e:
            self.fail(e.message)

    def test_verified(self):
        with self.assertRaises(ValueError):
            VATIN('xx', VALID_VIES_NUMBER)

    def test_country_code_getter(self):
        v = VATIN(VALID_VIES_COUNTRY_CODE.lower(), VALID_VIES_NUMBER)
        self.assertEqual(v.country_code, VALID_VIES_COUNTRY_CODE)

    def test_is_valid(self):
        v = VATIN(VALID_VIES_COUNTRY_CODE, VALID_VIES_NUMBER)

        self.assertTrue(v.is_valid())

    def test_result(self):
        v = VATIN(VALID_VIES_COUNTRY_CODE, VALID_VIES_NUMBER)

        self.assertFalse(hasattr(v, 'result'))
        self.assertTrue(v.is_valid())

        # v should have a result now
        self.assertTrue(hasattr(v, 'result'))

        self.assertEqual(v.result['countryCode'], VALID_VIES_COUNTRY_CODE)
        self.assertEqual(v.result['vatNumber'], VALID_VIES_NUMBER)

    def test_ie_regex_validation(self):
        import re
        search_match_type = type(re.match("", ""))

        for vn in VALID_VIES_IE:
            v = VATIN('IE', vn)
            assert isinstance(
                v._validate(),
                search_match_type), 'Validation failed for {}'.format(vn)

    @patch('vies.Client')
    def test_raises_when_suds_web_fault(self, mock_client):
        """Raise an error if suds raises a WebFault."""
        mock_check_vat = mock_client.return_value.service.checkVat
        mock_check_vat.side_effect = WebFault(500, 'error')

        v = VATIN(VALID_VIES_COUNTRY_CODE, VALID_VIES_NUMBER)

        logging.getLogger('vies').setLevel(logging.CRITICAL)

        with self.assertRaises(WebFault):
            v.is_valid()

        logging.getLogger('vies').setLevel(logging.NOTSET)

        mock_check_vat.assert_called_with(
            VALID_VIES_COUNTRY_CODE,
            VALID_VIES_NUMBER)


class ModelTestCase(unittest.TestCase):
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


class FieldTestCase(unittest.TestCase):

    @patch('vies.Client')
    @override_settings(INSTALLED_APPS=['vies.apps.ViesDisallowServerErrorConfig'])  # noqa
    def test_not_raises_when_suds_web_fault_exception(self, mock_client):
        """Do not raise if WebFault exception and allow_server_error=False."""
        mock_check_vat = mock_client.return_value.service.checkVat
        mock_check_vat.side_effect = WebFault(500, 'error')

        logging.getLogger('vies').setLevel(logging.CRITICAL)

        v = fields.VATINField(VIES_COUNTRY_CHOICES)
        out = v.clean([VALID_VIES_COUNTRY_CODE, VALID_VIES_NUMBER])
        self.assertEqual(out, '')

        logging.getLogger('vies').setLevel(logging.NOTSET)


class ModelFormTestCase(unittest.TestCase):
    def test_is_valid(self):
        """Form is valid."""
        form = VIESModelForm({
            'vat_0': VALID_VIES_COUNTRY_CODE,
            'vat_1': VALID_VIES_NUMBER})
        self.assertTrue(form.is_valid())

        vies = form.save()
        self.assertEqual(vies.vat, VALID_VIES)

    def test_is_not_valid_country(self):
        """Invalid country."""
        form = VIESModelForm({
            'vat_0': 'xx',
            'vat_1': VALID_VIES_NUMBER})
        self.assertFalse(form.is_valid())

    def test_is_not_valid_numbers(self):
        """Invalid number."""
        form = VIESModelForm({
            'vat_0': VALID_VIES_COUNTRY_CODE,
            'vat_1': 'xx123+-'})
        self.assertFalse(form.is_valid())

    def test_is_not_valid(self):
        """Invalid number."""
        form = VIESModelForm({'vat_0': 'GB', 'vat_1': '000000000'})
        self.assertFalse(form.is_valid())

    def test_save(self):
        """Form is saved."""
        form = VIESModelForm({
            'vat_0': VALID_VIES_COUNTRY_CODE,
            'vat_1': VALID_VIES_NUMBER})
        self.assertTrue(form.is_valid())
        vies_saved = form.save()

        vies_received = VIESModel.objects.get(pk=vies_saved.pk)
        self.assertEqual(vies_received, vies_saved)
        self.assertNotEqual(VIESModel.objects.count(), 0)
        self.assertEqual(vies_received.vat, VALID_VIES)

    def test_empty(self):
        form = EmptyVIESModelForm({'name': 'Eva'})
        self.assertTrue(form.is_valid())

    def test_is_valid_and_has_vatin_data(self):
        """Valid VATINFields' vatin_data() return result dict."""
        form = VIESModelForm({'vat_0': 'NL', 'vat_1': '124851903B01'})

        self.assertEqual(form.fields['vat'].vatin_data(), None)

        form.is_valid()
        data = form.fields['vat'].vatin_data()

        self.assertEqual(data['name'], 'JIETER')

    def test_invalid_error_message(self):
        form = VIESForm({'vat_0': 'NL', 'vat_1': '0000000000'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['vat'][0],
                         'Not a valid European VAT number.')

    def test_custom_invalid_error_message(self):
        form = VIESFormCustomError({'vat_0': 'NL',
                                    'vat_1': '0000000000'})
        self.assertFalse(form.is_valid())
        self.assertEqual(form.errors['vat'][0],
                         'This VAT number is not valid')

    def test_custom_invalid_error_message_with_value(self):
        form = VIESFormCustomError16({'vat_0': 'NL', 'vat_1': '0000000000'})
        self.assertFalse(form.is_valid())
        if get_version() > '1.6':
            self.assertEqual(form.errors['vat'][0],
                             'NL0000000000 is not a valid European VAT.')


class MockRequest(object):
    pass

request = MockRequest()


class AdminTestCase(unittest.TestCase):
    def setUp(self):
        self.site = AdminSite()

    def test_vatin_field_admin(self):
        """Admin form is generated."""
        ma = ModelAdmin(VIESModel, self.site)

        try:
            ma.get_form(request)
        except Exception as e:
            self.fail(e.message)

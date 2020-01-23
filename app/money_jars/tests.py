# -*- coding: utf-8 -*-
"""
description: simple functional test
todo: test should be rewritten to use factories and generic tests classes should be made
"""

from django.urls import reverse
from django.contrib.auth.models import User

from rest_framework import status
from rest_framework.test import APITestCase

from money_jars.models import Currency, Jar, Operation


def create_hyperlink(relative_path, pk, server="testserver"):
    return f"http://{server}{relative_path}{pk}/"


class Test(APITestCase):
    def setUp(self):
        self.test_user = User.objects.create_superuser(username='t', password='t')
        self.client.force_authenticate(user=self.test_user)

        self.currency_url = reverse('currency-list')
        self.jar_url = reverse('jar-list')
        self.operation_url = reverse('operation-list')
        self.transaction_url = reverse('transaction-list')

    def test_create_currency(self):
        data_currency1 = {
            'name': 'curr1',
            'symbol': 'C1',
            'code': 'CR1',
            'value': 1
        }
        data_currency2 = {
            'name': 'curr2',
            'code': 'CR2',
            'value': 2
        }

        response1 = self.client.post(self.currency_url, data_currency1, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Currency.objects.count(), 1)
        self.assertEqual(Currency.objects.get().name, 'curr1')

        response2 = self.client.post(self.currency_url, data_currency2, format='json')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Currency.objects.count(), 2)
        self.assertEqual(Currency.objects.get(name='curr2').name, 'curr2')

    def test_create_jar(self):
        self.test_create_currency()

        data_jar1 = {
            'name': 'jar1',
            # 'amount': 0,
            'currency': create_hyperlink(relative_path=self.currency_url, pk=1),
        }
        data_jar2 = {
            'name': 'jar2',
            'amount': 0,
            'currency': create_hyperlink(relative_path=self.currency_url, pk=1),
        }
        data_jar3 = {
            'name': 'jar3',
            'currency': create_hyperlink(relative_path=self.currency_url, pk=2),
        }

        response1 = self.client.post(self.jar_url, data_jar1, format='json')

        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Jar.objects.count(), 1)
        self.assertEqual(Jar.objects.get().name, 'jar1')

        response2 = self.client.post(self.jar_url, data_jar2, format='json')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)

        response3 = self.client.post(self.jar_url, data_jar3, format='json')
        self.assertEqual(response3.status_code, status.HTTP_201_CREATED)

    def test_create_operation(self):
        self.test_create_jar()

        data_operation1 = {
            'jar': create_hyperlink(relative_path=self.jar_url, pk=1),
            'amount_operation': 1
        }

        data_operation2 = {
            'jar': create_hyperlink(relative_path=self.jar_url, pk=1),
            'amount_operation': -1
        }

        response1 = self.client.post(self.operation_url, data_operation1, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Operation.objects.count(), 1)
        self.assertEqual(Jar.objects.get(name='jar1').amount, 1)

        response2 = self.client.post(self.operation_url, data_operation2, format='json')
        self.assertEqual(response2.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Jar.objects.get(name='jar1').amount, 0)

        # test debit ban
        response3 = self.client.post(self.operation_url, data_operation2, format='json')
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Jar.objects.get(name='jar1').amount, 0)

    def test_create_transaction(self):
        self.test_create_jar()

        data_transaction1 = {
            "deposit": {
                "amount_operation": 1,
                "jar": create_hyperlink(relative_path=self.jar_url, pk=2)
            },
            "withdraw": {
                "amount_operation": -1,
                "jar": create_hyperlink(relative_path=self.jar_url, pk=1)
            },
            "title": "transaction1",
            "currency": create_hyperlink(relative_path=self.currency_url, pk=1)
        }
        data_transaction2 = {
            "deposit": {
                "amount_operation": 1,
                "jar": create_hyperlink(relative_path=self.jar_url, pk=2)
            },
            "withdraw": {
                "amount_operation": -1,
                "jar": create_hyperlink(relative_path=self.jar_url, pk=1)
            },
            "title": "transaction2",
            "currency": create_hyperlink(relative_path=self.currency_url, pk=2)
        }
        data_transaction3 = {
            "deposit": {
                "amount_operation": -1,
                "jar": create_hyperlink(relative_path=self.jar_url, pk=2)
            },

            "title": "transaction3",
            "currency": create_hyperlink(relative_path=self.currency_url, pk=2)
        }
        data_transaction4 = {
            "withdraw": {
                "amount_operation": 1,
                "jar": create_hyperlink(relative_path=self.jar_url, pk=2)
            },

            "title": "transaction3",
            "currency": create_hyperlink(relative_path=self.currency_url, pk=2)
        }

        # test correct transaction
        Jar.objects.filter(name='jar1').update(amount=1)
        response1 = self.client.post(self.transaction_url, data_transaction1, format='json')
        self.assertEqual(response1.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Operation.objects.count(), 2)
        self.assertEqual(Jar.objects.get(name='jar1').amount, 0)
        self.assertEqual(Jar.objects.get(name='jar2').amount, 1)

        # test debit ban
        Jar.objects.filter(name='jar1').update(amount=0)
        response2 = self.client.post(self.transaction_url, data_transaction1, format='json')
        self.assertEqual(response2.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Operation.objects.count(), 2)

        # test incorrect currency ban
        Jar.objects.filter(name='jar1').update(amount=10)
        Jar.objects.filter(name='jar2').update(amount=10)
        response3 = self.client.post(self.transaction_url, data_transaction2, format='json')
        self.assertEqual(response3.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Operation.objects.count(), 2)

        # test negative deposit ban
        response4 = self.client.post(self.transaction_url, data_transaction3, format='json')
        self.assertEqual(response4.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Operation.objects.count(), 2)

        # test positive withdraw ban
        response4 = self.client.post(self.transaction_url, data_transaction4, format='json')
        self.assertEqual(response4.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(Operation.objects.count(), 2)

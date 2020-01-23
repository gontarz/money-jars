# -*- coding: utf-8 -*-
"""
description: provide filters for views
"""

from django.db.models import Q

from django_filters.rest_framework import FilterSet, ModelChoiceFilter, BooleanFilter

from money_jars.models import Transaction


class TransactionFilter(FilterSet):
    withdraw = BooleanFilter(field_name='withdraw_id', method='filter_not_empty')
    deposit = BooleanFilter(field_name='deposit_id', method='filter_not_empty')
    transaction = BooleanFilter(label='transaction', method='filter_transaction')

    def filter_not_empty(self, queryset, name, value):
        """
        check value exists in row (is null or not)
        """
        lookup = '__'.join([name, 'isnull'])
        return queryset.filter(**{lookup: not value})

    def filter_transaction(self, queryset, name, value):
        f_bool = not value
        if value:
            return queryset.filter(deposit_id__isnull=f_bool, withdraw_id__isnull=f_bool)

        return queryset.filter(Q(deposit_id__isnull=f_bool) | Q(withdraw_id__isnull=f_bool))

    class Meta:
        model = Transaction
        fields = [
            'currency',
            'deposit',
            'withdraw',
            'transaction',
            'title',
            'created',
            'updated',
        ]

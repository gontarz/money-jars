# -*- coding: utf-8 -*-
"""
description: money_jars serializers
"""

from rest_framework import serializers

from money_jars.models import Currency, Jar, Operation, Transaction


class CurrencySerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Currency
        fields = '__all__'


class JarSerializer(serializers.HyperlinkedModelSerializer):
    def validate(self, data):
        """
        check resource enough
        """
        if data.get("amount") and data.get("amount") < 0:
            raise serializers.ValidationError("you can't go debit")

        return data

    class Meta:
        model = Jar
        fields = '__all__'


class OperationSerializer(serializers.HyperlinkedModelSerializer):
    def create(self, validated_data):
        """
        generate amounts and update jar amount
        """
        JarSerializer().update(
            instance=validated_data['jar'],
            validated_data={'amount': validated_data['amount_after']}
        )

        return Operation.objects.create(**validated_data)

    def validate(self, data):
        """
        check is jar resource enough and create amount variables
        """
        amount_before = data['jar'].amount
        amount_after = amount_before + data['amount_operation']

        if amount_after < 0:
            raise serializers.ValidationError("you can't withdraw more than you have")

        data['amount_before'] = amount_before
        data['amount_after'] = amount_after

        return data

    class Meta:
        model = Operation

        read_only_fields = [
            'created',
            'updated',
            'amount_before',
            'amount_after'
        ]
        fields = [
            'amount_operation',
            'amount_before',
            'amount_after',
            'jar',
            'created',
            'updated'
        ]


class TransactionSerializer(serializers.HyperlinkedModelSerializer):
    deposit = OperationSerializer(required=False)
    withdraw = OperationSerializer(required=False)

    def create(self, validated_data):
        operation_serializer = OperationSerializer()

        if deposit := validated_data.get('deposit'):
            validated_data['deposit'] = operation_serializer.create(deposit)

        if withdraw := validated_data.get('withdraw'):
            validated_data['withdraw'] = operation_serializer.create(withdraw)

        transaction = Transaction.objects.create(
            **validated_data
        )

        return transaction

    def validate(self, data):
        """
        check is operation in jar currency
        """
        if deposit := data.get('deposit'):
            if deposit['jar'].currency.code != data['currency'].code:
                raise serializers.ValidationError("deposit currency code must be same as in jar")
            if deposit['amount_operation'] < 0:
                raise serializers.ValidationError("deposit value must be positive")

        if withdraw := data.get('withdraw'):
            if withdraw['jar'].currency.code != data['currency'].code:
                raise serializers.ValidationError("withdraw currency code must be same as in jar")
            if withdraw['amount_operation'] > 0:
                raise serializers.ValidationError("withdraw value must be negative")

        if withdraw and deposit:
            if withdraw.get('amount_operation') != deposit.get('amount_operation'):
                raise serializers.ValidationError("withdraw and deposit value must be equal to accomplish transaction")

        return data

    class Meta:
        model = Transaction
        fields = '__all__'

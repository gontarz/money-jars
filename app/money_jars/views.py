# Create your views here.
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import OrderingFilter

from money_jars.models import Currency, Jar, Operation, Transaction
from money_jars.serializers import CurrencySerializer, JarSerializer, OperationSerializer, TransactionSerializer
from money_jars.filters import TransactionFilter


class CurrencyViewSet(viewsets.ModelViewSet):
    queryset = Currency.objects.all().order_by('-updated')
    serializer_class = CurrencySerializer
    filterset_fields = ('code', 'name', 'created', 'updated')
    ordering_fields = ('created', 'updated', 'code', 'name', 'value')


class JarViewSet(viewsets.ModelViewSet):
    queryset = Jar.objects.all().order_by('-updated')
    serializer_class = JarSerializer
    filterset_fields = ('currency', 'name', 'created', 'updated')
    ordering_fields = ('created', 'updated', 'amount', 'name', 'currency')

    @action(methods=['get'], detail=True,
            # permission_classes=[IsAdminOrIsSelf]
            )
    def operations(self, request, pk=None):

        jar_operations = Operation.objects.filter(jar=pk)

        return Response([o.amount_operation for o in jar_operations])

        if jar_operations is not None:
            serializer = OperationSerializer(data=jar_operations)

            if serializer.is_valid():
                return Response(serializer)
                return self.get_paginated_response(serializer.data)

            print(serializer, serializer.data)
            return Response(serializer.data)


class OperationViewSet(viewsets.ModelViewSet):
    queryset = Operation.objects.all().order_by('-updated')
    serializer_class = OperationSerializer

    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter
    ]

    filterset_fields = ('jar', 'amount_operation', 'created', 'updated')
    ordering_fields = ('created', 'updated', 'amount_operation', 'jar')


class TransactionViewSet(viewsets.ModelViewSet):
    queryset = Transaction.objects.all().order_by('-updated')
    serializer_class = TransactionSerializer

    filter_backends = [
        DjangoFilterBackend,
        OrderingFilter
    ]

    filterset_class = TransactionFilter
    ordering_fields = ('created', 'updated', 'currency', 'title')

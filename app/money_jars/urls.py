from django.urls import include, path

from rest_framework import routers

from money_jars.views import CurrencyViewSet, JarViewSet, OperationViewSet, TransactionViewSet


router = routers.DefaultRouter()

router.register(r'currencies', CurrencyViewSet)
router.register(r'jars', JarViewSet)
router.register(r'operations', OperationViewSet)
router.register(r'transactions', TransactionViewSet)


urlpatterns = [
    path(r"money-jars/", include(router.urls)),
]

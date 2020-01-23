"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, re_path, include

from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="money-jars API",
      default_version='v1',
      description="Keep your jars money in money-jars",
      contact=openapi.Contact(email="python.backend.dev@gmail.com"),
      license=openapi.License(name="MIT"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)


urlpatterns = [
    path('admin/', admin.site.urls),
    re_path(r'^api-auth/', include('rest_framework.urls', namespace='rest_framework')),

    path("doc/docs/", schema_view.with_ui("swagger"), name="api_docs"),
    path("doc/redoc/", schema_view.with_ui("redoc"), name="api_redocs"),
    re_path(
        "^doc/swagger(?P<format>.json|.yaml)$",
        schema_view.without_ui(),
        name="schema_swagger",
    ),

    path("", include("money_jars.urls")),
]

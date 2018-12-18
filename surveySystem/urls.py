"""surveySystem URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.urls import path
from django.urls import include
from django.contrib import admin

from django.shortcuts import HttpResponse


def sentry(request):
    from sentry_sdk import capture_exception

    try:
        a_potentially_failing_function()
    except Exception as e:
        # Alternatively the argument can be omitted
        capture_exception(e)

    return HttpResponse("ok")


urlpatterns = [
    path(r'admin/', admin.site.urls),

    path('api/', include('api.urls')),
    path(r'', include('web.urls')),
    path(r'', include('jwt_demo.urls')),

    path(r'sentry/', sentry)
]

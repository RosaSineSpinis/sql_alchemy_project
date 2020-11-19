"""hypercar URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, re_path
from tickets.views import (
    WelcomeView,
    Menu,
    Inflate_tires,
    # Inflate_tires2,
    ProcessingView,
    Next_view,
)
from django.views.generic import RedirectView

urlpatterns = [
    path('welcome/', WelcomeView.as_view(), name='welcome'),
    path('menu/', Menu.as_view(), name='menu'),
    path('get_ticket/<str:link>/', Inflate_tires.as_view(), name='inflate_tires'),
    path('get_ticket/<str:link>/', Inflate_tires.as_view(), name='change_oil'),
    path('get_ticket/<str:link>/', Inflate_tires.as_view(), name='diagnostic'),
    # path('processing/',  RedirectView.as_view(), name='processing'),
    # path('processing/', RedirectView.as_view(url='/processing')),
    re_path('processing', ProcessingView.as_view(), name='/processing'),
    path('next/', Next_view.as_view(), name='/processing'),

    # re_path('processing/?', ProcessingView.as_view()),


    # path('menu/get_ticket/inflate_tires', Inflate_tires.as_view(), name='inflate_tires'),

]

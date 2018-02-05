from django.urls import path,re_path
from . import views
from django.contrib import admin

urlpatterns = [
    path("",views.overview, name="overview"),
    path("ausgabe/",views.ausgabe, name="ausgabe"),
    path("ausgleichszahlung/",views.ausgleichszahlung),
    path("ausgabe/post_ausgabe/", views.post_ausgabe, name="post_ausgabe"),
    path("ausgleichszahlung/post_ausgleichszahlung/", views.post_ausgleichszahlung, 
                                                    name="post_ausgleichszahlung"),
    re_path("user/(\w+)",views.profile,name="profile"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
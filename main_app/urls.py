from django.urls import path,re_path
from . import views
from django.contrib import admin

urlpatterns = [
    path("",views.overview, name="overview"),
    path("ausgabe/",views.ausgabe, name="ausgabe"),
    path("ausgleichszahlung/",views.ausgleichszahlung, name="ausgleichszahlung"),
    path("ausgabe/post_ausgabe/", views.post_ausgabe, name="post_ausgabe"),
    path("ausgleichszahlung/post_ausgleichszahlung/", views.post_ausgleichszahlung, 
                                                    name="post_ausgleichszahlung"),
    re_path("user/(\w+)",views.profile,name="profile"),
    path("delete_ausgabe/<int:ausgabe_id>/<str:origin_id>", views.delete_ausgabe, name="delete_ausgabe"),
    path("delete_agz/<int:agz_id>/<str:origin_id>", views.delete_agz, name="delete_agz"),
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
]
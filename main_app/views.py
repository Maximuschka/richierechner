from django.shortcuts import render
# from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from .models import Ausgabe,Ausgleichszahlung
from .forms import AusgabeForm, AusgleichszahlungForm, LoginForm, OverviewForm
from .richierechner import *

@login_required(login_url='/login/')
def overview(request):
    # if not request.user.is_authenticated:
    #     return redirect('%s?next=%s' % (settings.LOGIN_URL, request.path))

    if request.method == "POST":
        form = OverviewForm(request.POST)
        if form.is_valid():
            sd = form.cleaned_data[ "start_datum" ]
            ed = form.cleaned_data[ "end_datum" ]
    else:
        try:
            sd = getStartDatum()
            ed= getEndDatum()
        except: 
            sd = None
            ed = None

    mitbewohnis = User.objects.all().exclude(is_superuser=True)
    ausgaben = Ausgabe.objects.filter(datum__range=[sd, ed]).order_by("datum")

    agzs = Ausgleichszahlung.objects.filter(datum__range=[sd, ed]).order_by("datum")

    summe_ausgaben = summiereAusgaben(ausgaben)
    MBW_ausgaben = getMBWAusgabenDJANGO(mitbewohnis,ausgaben,agzs)

    summe_MBW_ausgaben = 0
    for item in MBW_ausgaben:
        summe_MBW_ausgaben += item[1]

    form = OverviewForm(initial={"start_datum":sd, "end_datum": ed})

    return render(request, "overview.html", {"form": form,
                                                "mitbewohnis":mitbewohnis,
                                                "ausgaben": ausgaben,
                                                "agzs": agzs,
                                                "summe_ausgaben": summe_ausgaben,
                                                "MBW_ausgaben": MBW_ausgaben,
                                                "summe_MBW_ausgaben": summe_MBW_ausgaben})

@login_required(login_url='/login/')
def ausgabe(request):
    letzte_ausgaben = Ausgabe.objects.filter().order_by("-datum")[:5]

    user = request.user
    mitbewohnis = User.objects.all().exclude(is_superuser=True)
    ausgaben = Ausgabe.objects.all().order_by("datum")
    agzs = Ausgleichszahlung.objects.all().order_by("datum")

    form = AusgabeForm(initial={"mitbewohni":user})

    return render(request, "ausgabe.html",{"letzte_ausgaben": letzte_ausgaben,
                                            "form": form})

@login_required(login_url='/login/')
def ausgleichszahlung(request):
    letzte_agzs = Ausgleichszahlung.objects.filter().order_by("-datum")[:5]

    mitbewohnis = User.objects.all().exclude(is_superuser=True)
    ausgaben = Ausgabe.objects.all().order_by("datum")
    agzs = Ausgleichszahlung.objects.all().order_by("datum")
    noetige_agzs = getNoetigeAusgleichszahlungen2(mitbewohnis,ausgaben,agzs)

    form = AusgleichszahlungForm()
    return render(request, "ausgleichszahlung.html",{"letzte_agzs": letzte_agzs,
                                                        "form": form,
                                                        "noetige_agzs": noetige_agzs})

@login_required(login_url='/login/')
def profile(request,username):
    user = User.objects.get(username=username)
    ausgaben = Ausgabe.objects.filter(mitbewohni=user)
    return render(request, "profile.html",{"username": username,
                                            "ausgaben": ausgaben})

def post_ausgabe(request):
    form = AusgabeForm(request.POST)
    if form.is_valid():
        form.save(commit=True)
    return HttpResponseRedirect("/ausgabe")

def post_ausgleichszahlung(request):
    form = AusgleichszahlungForm(request.POST)
    if form.is_valid():
        form.save(commit=True)
    return HttpResponseRedirect("/ausgleichszahlung/")

def login_view(request):
    if request.method == "POST":
        form = LoginForm(request.POST)
        if form.is_valid():
            u = form.cleaned_data[ "username" ]
            p = form.cleaned_data[ "password" ]
            user = authenticate(username = u, password = p)
            if user is not None:
                if user.is_active:
                    print("User is valid, active and authenticated")
                    login(request, user)
                    return HttpResponseRedirect("/")
                else:
                    print("The account has been disabled!")
            else:
                print("The username and/or password were incorrect.")

    else:
        form = LoginForm()
        return render(request, "login.html", {"form": form})

def logout_view(request):
    logout(request)
    return HttpResponseRedirect("/")
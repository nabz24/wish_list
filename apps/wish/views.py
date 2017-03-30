from django.shortcuts import render, HttpResponse, redirect
from datetime import datetime
from django.contrib import messages
from .models import Users, Wish
from django.db.models import Count
import bcrypt

def index(request):

    return render(request, "wish/index.html")

def register(request):

    regCheck = Users.objects.register(request.POST)

    if regCheck['success']:
        messages.success(request, "Succesful Registrations")
        request.session['user_id'] = regCheck['user_id']
        user = Users.objects.get(id = regCheck['user_id'])

        return redirect('/')
    else:
        for error in regCheck['errors']:
            messages.error(request, error)
        return redirect('/')

def login(request):

    logCheck = Users.objects.login(request.POST)
    if logCheck['success']:
        request.session['user_id'] = logCheck['user_id']


        return redirect('/dashboard')
    else:
        for error in logCheck['errors']:
            messages.error(request, error)
        return redirect('/')

def dashboard(request):

    context = {

    'user' : Users.objects.get(id = request.session['user_id']),
    'wishs' : Wish.objects.all()

    }
    return render(request, "wish/dashboard.html", context)


def addWish(request):

    wish_form = {

    'item' : request.POST['item'],
    'user_id' : request.session['user_id'],

    }

    quoteCheck = Wish.objects.quoteReg(wish_form)

    if quoteCheck['success']:

        return redirect('/dashboard')
    else:
        for error in quoteCheck['errors']:
            messages.error(request, error)
        return redirect('/create')


def create(request):
    thisUser = Users.objects.get(id = request.session['user_id'])
    return render(request, 'wish/create.html')

def wish_item(request, id):
    thisuser = Users.objects.get(id = request.session['user_id'])
    wish = Wish.objects.get(id = id)
    wish.wish_item.add(thisuser)
    return redirect('/dashboard')

def logout(request):
    request.session.pop('user_id')
    messages.success(request, "You are logged out")
    return redirect('/')


def remove(request, id):
    this_user = Users.objects.get(id = request.session['user_id'])
    wish = Wish.objects.get(id = id)
    wish.wish_item.remove(this_user)
    return redirect('/dashboard')

def delete(request, id):
    Wish.objects.get(id=id).delete()
    return redirect('/dashboard')


def item(request, id):
    thisuser = Users.objects.get(id = request.session['user_id'])
    wish = Wish.objects.get(id = id)
    context = {

    'user': thisuser,
    'wishs': wish

    }
    return render(request, "wish/item.html", context)

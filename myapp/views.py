from django.shortcuts import render, redirect
from django.contrib import messages
from .models import User, Quote
import bcrypt

def index(request):
    return render(request, "index.html")

def register(request):
    print(request.POST)
    errors = User.objects.registration_validator(request.POST)
    print(errors)
    print(len(errors))
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        password = request.POST['password']
        print(password)
        hash1 = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        print(hash1)
        user = User.objects.create(name = request.POST['name'], alias = request.POST['alias'], email = request.POST['email'], password = hash1.decode())
        print(user)
        request.session['id'] = user.id   #put logged_in_user into a session variable so we can access info later in another function
    return redirect("/quotes")

def login(request):
    errors_from_login_validator = User.objects.login_validator(request.POST)
    if len(errors_from_login_validator) > 0:
        for key, value in errors_from_login_validator.items():
            messages.error(request, value)
        return redirect("/")
    user = User.objects.filter(email= request.POST['email'])[0]
    print(user.id)
    request.session['id'] = User.objects.filter(email= request.POST['email'])[0].id
    return redirect("/quotes")

def quoteDashboard(request):
    if 'id' not in request.session:
        return redirect("/")
    else:
        user = User.objects.get(id = request.session['id'])
        context = {
            "user": user,
            "all_my_favorites": Quote.objects.filter(joiner = user),
            "all_other_quotes": Quote.objects.exclude(joiner = user)
        }
    return render(request, "quotes.html", context)

def addQuote(request):
    print(request.POST)
    errors = User.objects.addQuote_validator(request.POST)
    print(errors)
    print(len(errors))
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/quotes')
    else:
        user = User.objects.get(id = request.session['id'])
        quote = Quote.objects.create(quoteBy = request.POST['quoteBy'], quoteMessage = request.POST['quoteMessage'], creator = user)
        return redirect('/quotes')

def addToFavorites(request, quote_id):
    quoteToAddToFavorites = Quote.objects.get(id = quote_id)
    loggedinuser = User.objects.get(id = request.session['id'])
    loggedinuser.joiner.add(quoteToAddToFavorites)
    return redirect('/quotes')

def removeFromFavorites(request, quote_id):
    quoteToRemoveFromFavorites = Quote.objects.get(id = quote_id)
    loggedinuser = User.objects.get(id = request.session['id'])
    loggedinuser.joiner.remove(quoteToRemoveFromFavorites)
    return redirect('/quotes')

def userPage(request, quote_creator_id):
    if 'id' not in request.session:
        return redirect("/")
    user = User.objects.get(id = quote_creator_id)
    context = {
        "user": user,
        "number_of_quotes": len(user.QuotesCreated.all())
    }
    return render(request, "userPage.html", context)

def deleteQuote(request, quote_id):
    quote_to_delete = Quote.objects.get(id = quote_id)
    quote_to_delete.delete()
    return redirect('/quotes')

def editQuote(request, quote_id):
    if 'id' not in request.session:
        return redirect("/")
    quote = Quote.objects.get(id = quote_id)
    context = {
        "quote": quote
    }
    return render(request, "editQuote.html", context)

def updateQuote(request, quote_id):
    user = User.objects.get(id=request.session['id'])
    errors = User.objects.updateQuote_validator(request.POST)
    print(errors)
    print(len(errors))
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/quotes/{{quote.id}}")
    else:
        update = Quote.objects.get(id = quote_id)
        update.quoteMessage = request.POST['quoteMessage']
        update.quoteBy = request.POST['quoteBy']
        update.creator = user
        update.save()
        return redirect('/quotes')

def logout(request):
    request.session.clear()
    return redirect('/')
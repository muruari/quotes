from __future__ import unicode_literals
import bcrypt, time
from django.shortcuts import render, redirect, HttpResponse
from .models import *
from django.contrib import messages
from datetime import datetime

def current_user(request):
	return User.objects.get(id = request.session['user_id'])


def registration(request):
	return render(request, 'exam/registration.html')


def register(request):
    check = User.objects.validate(request.POST)
    if request.method != 'POST':
		return redirect('/')

    #Validates User Registration
    if len(check) > 0:
        for error in check:
            messages.add_message(request, messages.INFO, error, extra_tags="registration")
            return redirect('/')

    #Hashes password before new user is entered into DB.
    passwd = request.POST['password']
    if len(check) == 0:
		hashed_pw = bcrypt.hashpw(str(passwd).encode(), bcrypt.gensalt())

    #Creates a new user in the database:
		user = User.objects.create(
			name = request.POST['name'],
			alias = request.POST['alias'],
			email = request.POST['email'],
			date_of_birth = request.POST['date_of_birth'],
			password = hashed_pw
		)

    email = request.POST['email']
    user = User.objects.get(email = email) # THIS LINE results in JSON serializable error because I was capturing the ENTIRE user object into session.
    request.session['user_id'] = user.id
    request.session['name'] = user.name

    return redirect('/dashboard')


def login(request):

    if request.method != 'POST':
        return redirect('/')

    user = User.objects.filter(email = request.POST.get('email')).first()

    #Validates User Login    
    if user and bcrypt.checkpw(request.POST.get('password').encode(), user.password.encode()):
        request.session['user_id'] = user.id
        request.session['name'] = user.name
        return redirect('/dashboard')
    
    #Returns Errors if Login Validation Fails
    else: 
        messages.add_message(request, messages.INFO, 'Your credentials are invalid! Please try again.', extra_tags="login")
        return redirect('/')
    return redirect('/dashboard')


def logout(request):
		request.session.clear()
		return redirect('/')


def dashboard(request):
    user = User.objects.get(id = request.session['user_id'])
    my_quotes = Quote.objects.filter(quotes = user)
    all_quotes = Quote.objects.exclude(quotes = user)

    #Creates context dictionary to pass to dashboard.html.  
    context = {
        'user_name' : user.name,
        'all_quotes' : all_quotes,
        'my_quotes' : my_quotes
    }
    return render(request, 'exam/dashboard.html', context)


def create_quote (request):

    # Validates Quote Submission.
    check = Quote.objects.validate_quote(request.POST)
    if len(check) > 0:
        for error in check:
            messages.add_message(request, messages.INFO, error, extra_tags="create_quote")
            return redirect('/dashboard')


    if len(check) == 0:
        
        #Creates a new user in the database:
        user = User.objects.get(id=request.session['user_id'])
        quote = Quote.objects.create(
            quoter = request.POST['quote_by'],
            quote_text = request.POST['quote_text_input'],
            posted_by = user,
        )

    return redirect('/dashboard')

# Adds quote to loggeddd users list of favorite quotes.
def add_quote (request, id):
    user = User.objects.get(id = request.session['user_id'])
    quote = Quote.objects.get (id = id)
    quote.quotes.add(user)
    quote.save()
    return redirect('/dashboard')

#Removes quote from logged user's list of favorite quotes.
def remove_quote (request, id):
    user = User.objects.get(id = request.session['user_id'])
    quote = Quote.objects.get (id = id)
    quote.quotes.remove(user)
    return redirect('/dashboard')


#Displays Quote Information Page
def quote_info(request, id):
    user = User.objects.get(id = id)
    my_quotes = Quote.objects.filter(posted_by = user)
    quote_count = len(Quote.objects.filter(posted_by = user))
    context = {
        'user_name' : user.name,
        'quote_count' : quote_count,
        'my_quotes' : my_quotes,
    }
    return render(request, 'exam/quotes.html', context)


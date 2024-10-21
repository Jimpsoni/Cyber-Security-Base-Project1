from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from . import models
from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError

import logging

# logging.basicConfig(level=logging.INFO, filename='activities.log', encoding="utf-8", filemode='a', format='%(asctime)s: %(levelname)s - %(name)s - %(message)s')

@login_required(login_url='login')
def index(request):
    # Serve image urls to user
    return render(request, 'index.html', 
                  {
                    "username": request.user.username, 
                    'images': models.Image.objects.filter(owner=request.user)
                   }
                )


def logout_view(request):
    # logging.info(f"Logged '{request.user.username}' out")
    logout(request)
    return redirect('login')


def create_user(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        try:
            # Validate users' passwords
            # validate_password(password)

            user = User.objects.create_user(
                                            username=username,
                                            password=password
                                            )

            # logging.info(f"Created a new user '{username}'")
            login(request, user)
            return redirect('/')
        
        except ValidationError:
            print("Val error")
            return render(request, 'signup.html', {"error": "Bad password"})

        except:
            # logging.debug('Tried to create a username that already exists')
            return render(request, 'signup.html', {"error": "username that already exists"})
    else:
        return render(request, 'signup.html', {'error': ''})


@login_required(login_url='login')
def search(request):
    # Search from database
    searchterm = request.GET['term']

    query = f"SELECT * FROM 'src_image' WHERE owner_id = {request.user.id} AND name LIKE '%{searchterm}%'"
    result = models.Image.objects.raw(query)
    
    """
    Problem: SQL INJECTION
    You can query {%' OR 1=1 OR NAME LIKE '%} and it will return every image in the database regardless of owner

    THE FIX TO INJECTION:
    to fix the issue, django provides sanitization to raw inputs

    Solution:
    query = f"SELECT * FROM 'src_image' WHERE owner_id = %s AND name LIKE %s"
    result = models.Image.objects.raw(query, [request.user.id, "%" + searchterm + "%"])

    This way injection doesn't work
    """

    return render(request, 'search.html', {'searchterm': searchterm, 
                                           'imagecount': len(result), 
                                           'images': result})


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            # logging.info(f"Logged '{user}' in")
            return redirect('/')
        else:
            # logging.warning('A Failed Authentication')
            return render(request, 'login.html', {'error': "Wrong password or username"})
        
    else:
        return render(request, 'login.html', {'error': ''})
    

@login_required(login_url='login')
def upload(request):
    if request.method == 'POST':
        form = models.ImageForm(request.POST, request.FILES)

        if form.is_valid():
            # logging.info(f"New media uploaded")
            name = form.cleaned_data.get("name")
            img = form.cleaned_data.get("file")
            owner = request.user

            obj = models.Image.objects.create(name=name, file=img, owner=owner)
            obj.save()

            return redirect('/')
        else:
            # logging.warning(f"Invalid media upload")
            return render(request, 'upload_form.html', {})
    else:
        return render(request, 'upload_form.html', {})


@login_required(login_url='login')
def usersettings(request):
    return render(request, 'usersettings.html', {})


@login_required(login_url='login')
def deleteuser(request):
    try:
        u = User.objects.get(id = request.user.id)
        u.delete()
        # logging.warning(f"Deleted user '{request.user.username}'")

        return redirect('/login')

    except Exception as e: 
        # logging.critical(f"Tried to delete a user that doesn't exist!!")
        return redirect('/')

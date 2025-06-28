from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Recipe
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required


def home(request):
  if request.method == "GET":
    data = request.GET
    searchKey = data.get('search')
    if searchKey:
        queryset = Recipe.objects.filter(name__icontains=searchKey)
        context = {'recipes': queryset}
        return render(request, 'home.html', context)
    else:
        queryset = Recipe.objects.all()
        context = {'recipes': queryset}
        return render(request, 'home.html', context)

  queryset = Recipe.objects.all()
  context = {'recipes': queryset}
  return render(request, 'home.html', context)

def loginPage(request):
  if request.user.is_authenticated:
    logout(request)
  if request.method == "POST":
    data = request.POST
    username = data.get('username')
    password = data.get('password')
    if User.objects.filter(username=username).exists():
      user = authenticate(username=username, password=password)
      if user is not None:
        login(request, user)
        return redirect('/')
      else:
        messages.info(request, 'Incorrect password')
        return redirect('/login/',messages=messages)
    else:
      messages.info(request, 'Username does not exist')
      return redirect('/login/',messages=messages)

  return render(request, 'Login.html')

@login_required(login_url='/login/')
def logoutPage(request):
    if request.user.is_authenticated:
        logout(request)
        messages.info(request, 'Logged out successfully')
    return redirect('/login/', messages=messages)

def registerPage(request):
    if request.method == "POST":
        data = request.POST
        firstname = data.get('firstname')
        lastname = data.get('lastname')
        username = data.get('username')
        password = data.get('password')

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username already exists')
            return redirect('/register/')

        user = User.objects.create_user(
            first_name=firstname,
            last_name=lastname,
            username=username)
        user.set_password(password)
        user.save()
        messages.info(request, 'Account created successfully. Please login to continue')
        return redirect('/register/')
    return render(request, 'Register.html')

@login_required(login_url='/login/')
def addRecipe(request):
  if request.method == "POST":
      data = request.POST
      name = data.get('name')
      description = data.get('description')
      image = request.FILES.get('image')
      Recipe.objects.create(
          name=name,
          description=description,
          image=image,
      )
      return redirect('/')
  return render(request, 'AddRecipe.html')

@login_required(login_url='/login/')
def deleteRecipe(request, id):
    queryset = Recipe.objects.get(id=id)
    queryset.delete()
    return redirect('/')

@login_required(login_url='/login/')
def updateRecipe(request, id):
  queryset = Recipe.objects.get(id=id)
  if request.method == "POST":
    data = request.POST
    name = data.get('name')
    description = data.get('description')
    image = request.FILES.get('image')
    queryset.name = name
    queryset.description = description
    if image:
      queryset.image = image
    queryset.save()
    return redirect('/')
  return render(request, 'UpdateRecipe.html', {'recipe': queryset})

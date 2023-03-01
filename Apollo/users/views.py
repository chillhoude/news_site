from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .forms import *
from navigation.models import *
from django.contrib.auth import login, logout
from django.db.models import Q

def login_user(request):
    if request.method == 'POST':
        form = LoginUser(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request,user)
            return redirect('home')
    else:
        form = LoginUser()
    return render(request,'users/login.html',{'form':form})

def register(request):
    if request.method == "POST":
        form = UserRegistrForm(request.POST)
        if form.is_valid():
            user = form.save()
            user.is_active = True
            user.save()
            messages.success(request,'Вы успешно зарегистрировались!')
            return redirect('home')
        else:
            messages.error(request, 'Ошибка регистрации')
    else:
        form =  UserRegistrForm()

    return render(request,'users/register.html', {'form':form})

def cabinet(request):
    MainUser = get_object_or_404(CustomUser, id=request.user.id)
    users = CustomUser.objects.filter(Q(first_name__isnull=False)&Q(last_name__isnull=False)&Q(email__isnull=False))
    #personal data form
    if request.method == 'POST':
        MainUser.first_name = request.POST.get("first_name")
        MainUser.last_name = request.POST.get("last_name")
        MainUser.email = request.POST.get("email")
        for player in users:
            if request.POST.get(f"{player.username}") == 'on':
                player.is_journalist = True
            else:
                player.is_journalist = False
            player.save()
    #comment auth user
    comment = Comment_user.objects.filter(user=request.user).prefetch_related('like').select_related('user')
    context = {'users':users,
                'comments':comment,
                #'form':form
                'MainUser':MainUser
                }
    return render(request,'users/cabinet.html',context)

def logout_user(request):
    logout(request)
    return redirect('login')

def create_superuser(request):
    return redirect()
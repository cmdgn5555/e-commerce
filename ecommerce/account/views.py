from django.shortcuts import render, redirect
from .forms import CreateUserForm, LoginForm, UpdateUserForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
# Create your views here.


def register(request):
    form = CreateUserForm()

    if request.method == 'POST':
        form = CreateUserForm(request.POST)

        if form.is_valid():
            user = form.save()
            user.save()

            return redirect('my_login')

    return render(
        request=request,
        template_name='register.html',
        context={
            'form': form
        }
    )


def my_login(request):
    form = LoginForm()

    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = request.POST.get('username')
            password = request.POST.get('password')

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('dashboard')

    return render(
        request=request,
        template_name='my-login.html',
        context={
            'form': form
        }
    )


def user_logout(request):
    logout(request)
    messages.success(request, 'Logout has been success')
    return redirect('store')


@login_required(login_url='my_login')
def profile_management(request):
    user_form = UpdateUserForm(instance=request.user)

    if request.method == 'POST':
        user_form = UpdateUserForm(request.POST, instance=request.user)

        if user_form.is_valid():
            user_form.save()

            messages.info(request, 'update has been success')

            return redirect('dashboard')

    return render(
        request=request,
        template_name='profile-management.html',
        context={
            'user_form': user_form
        }
    )


@login_required(login_url='my_login')
def delete_account(request):
    user = User.objects.get(id=request.user.id)

    if request.method == 'POST':
        user.delete()

        messages.error(request, 'Account has been deleted')

        return redirect('store')

    return render(
        request=request,
        template_name='delete-account.html'
    )


@login_required(login_url='my_login')
def dashboard(request):
    return render(request, 'dashboard.html')
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.db import transaction, IntegrityError
from django.contrib.auth.decorators import login_required
from .forms import RegisterForm, LoginForm

def index(request):
    register_form = RegisterForm()
    login_form = LoginForm()
    register_error = ''
    login_error = ''

    if request.method == 'POST':
        if 'register' in request.POST:
            register_form = RegisterForm(request.POST)
            if register_form.is_valid():
                try:
                    with transaction.atomic():
                        user = User.objects.create_user(
                            username=register_form.cleaned_data['username'],
                            password=register_form.cleaned_data['password'],
                            first_name=register_form.cleaned_data['first_name'],
                            last_name=register_form.cleaned_data['last_name'],
                        )
                        # Save middle name in user profile or another model if needed
                        login(request, user)
                        return redirect('dashboard')
                except IntegrityError:
                    register_error = 'Username already exists.'
                except Exception as e:
                    register_error = str(e)
            else:
                register_error = register_form.errors.as_text()
        elif 'login' in request.POST:
            login_form = LoginForm(request.POST)
            if login_form.is_valid():
                user = authenticate(
                    request,
                    username=login_form.cleaned_data['username'],
                    password=login_form.cleaned_data['password']
                )
                if user is not None:
                    login(request, user)
                    return redirect('dashboard')
                else:
                    login_error = 'Invalid username or password.'
            else:
                login_error = login_form.errors.as_text()

    return render(request, 'index.html', {
        'register_form': register_form,
        'login_form': login_form,
        'register_error': register_error,
        'login_error': login_error,
    })

@login_required
def dashboard(request):
    # Dummy values for now, replace with real queries later
    context = {
        'total_income': 0,
        'total_expenses': 0,
        'balance': 0,
        'monthly_salary': 0,
    }
    return render(request, 'dashboard.html', context)

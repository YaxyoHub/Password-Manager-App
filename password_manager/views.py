from django.shortcuts import render, redirect

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.core.mail import send_mail

from .models import App_Password, User, OTP_codes
from .forms import SignUp_Form, App_Password_Form, OTP_Code_Form

# Create your views here.

"""
!1. signin

!2. signup

3. signout

4. verify_email_tosign

!5. home_view ( passwords ) 

!6. add_password

!7. edit_password

!8. delete_password

10. change_email_view

11. verify_email_tochange

12. verify_email_toupdate

13. change_password

14. verify_email_tochangepassword

15. verify_email_tosignout

16. delete_and_signout

17. verify_email_todeleteandsignout

18. forgot_password

19. 
"""

# 1) sign in view
def signin(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(
            username=username,
            password=password
        )
        if user:
            login(
                request, user
            )
            messages.success(
                request,
                'Signed In Successfully!'
            )
            return redirect(
                'home'
            )
        else:
            messages.error(
                request,
                'Username or password is incorrect!'
            )
            return redirect(
                'signin'
            )
    

    return render(
        request,
        'signin.html'
    )

# 2) sign up view
def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        form = SignUp_Form(data=request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False
            user.save()

            user_email = user.email
            request.session['email'] = user_email
            # email otp 

            import random
            code = random.randint(100000, 999999)
            OTP_codes.objects.create(
                user_id=user,
                email=user_email,
                code=str(code)
            )
            send_mail(
                subject='Tasdiqlash kodi',
                message=f'Sizning tasdiqlash kodingiz: {code}',
                from_email=None,
                recipient_list=[user_email]
            )
            messages.success(
                request,
                'Emailingizga tasdiqlash kodiu yuborildi'
            )
            return redirect(
                'verify_email'
            )
            # login(request, user)
            # messages.success(
            #     request,
            #     'Signed Up successfully!'
            # )
            # return redirect('home')
        else:
            messages.error(
                request,
                form.errors
            )

    empty_form = SignUp_Form()
    return render(
        request,
        'signup.html',
        context={'form': empty_form}
    )

def verify_email(request):

    if request.method == 'POST':
        form = OTP_Code_Form(data=request.POST)

        email = request.session.get('email')
        code = OTP_codes.objects.filter(email=email).first()
        user = User.objects.get(email=email)
        user_code = form.cleaned_data.get('code')
        if code.code == user_code:
            user.is_active = True
            user.save()
            login(request, user)
            messages.success(
                request,
                'Signed Up successfully!'
            )
            return redirect('home')
        else:
            messages.error(
                request,
                'Tasdiqlash kodi noto`g`ri'
            )
            return redirect(
                'verify_email'
            )

    bush_form = OTP_Code_Form()
    return render(
        request,
        'verify_email.html',
        context={
            'form': bush_form
        }
    )

# 3) signout view

@login_required(login_url='signin')
def signout(request):
    logout(request)
    return redirect('signin')

# 4) home view
@login_required(login_url='signin')
def home_view(request):
    passwords = App_Password.objects.all()

    return render(
        request,
        'home.html',
        context={
            'passwords': passwords
        }
    )

# 6) add password

@login_required(login_url='signin')
def add_password_view(request):

    if request.method == 'POST':
        form = App_Password_Form(data=request.POST)
        if form.is_valid():
            new_password = form.save(commit=False)
            new_password.user_id = request.user
            new_password.save()
            messages.success(
                request,
                'Parol saqlandi'
            )
            return redirect(
                'home'
            )
        else:
            messages.error(
                request,
                form.errors
            )
            return redirect(
                'add_password'
            )

    bush_form = App_Password_Form()
    return render(
        request,
        'add_password.html',
        context={
            'form': bush_form
        }
    )

@login_required(login_url='signin')
def edit_password_view(request, password_id):
    app_password = App_Password.objects.get(id=password_id)
    form = App_Password_Form(instance=app_password)

    if request.method == 'POST':
        new_form = App_Password_Form(data=request.POST, instance=app_password)
        if new_form.is_valid():
            new_form.save()
            messages.success(
                request,
                'Parol yangilandi!'
            )
            return redirect(
                'home'
            )
        else:
            messages.error(
                request,
                new_form.errors
            )
            return redirect(
                'edit_password',
                password_id=app_password.id
            )
            


    return render(
        request,
        'edit_password.html',
        context={
            'form': form
        }
    )

@login_required(login_url='signin')
def delete_password_view(request, password_id):
    app_password = App_Password.objects.get(id=password_id)
    app_password.delete()
    messages.success(
        request,
        'Parol o`chirildi'
    )
    return redirect(
        'home'
    )

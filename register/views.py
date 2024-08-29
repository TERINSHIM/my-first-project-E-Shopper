import random
import uuid
from django.shortcuts import render, redirect, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login  # Alias the built-in login function
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.contrib.auth import authenticate, logout as auth_logout
from allauth.account.views import LogoutView

from .models import Profile
from .helper import MessageHandler
from e_commerce import settings

def home1(request):
    if request.COOKIES.get('verified'):
        return HttpResponse("verified.")
    else:
        return HttpResponse("Not verified.")

def register(request):
    if request.method == "POST":
        username = request.POST['username']
        phone = request.POST['phone']

       
        user = User.objects.filter(username__iexact=username).first()
        if not user:
            messages.error(request, "Invalid username")
            return render(request, 'register.html')

        
        profile = Profile.objects.filter(user=user, phone_number=phone).first()
        if not profile:
            messages.error(request, "Invalid phone number")
            return render(request, 'register.html')

        
        otp = random.randint(1000, 9999)
        profile.otp = str(otp)
        profile.save()

        
        MessageHandler(phone, otp).send_otp_via_message()

        
        red = redirect(f'/register/otp/{profile.uid}/')
        red.set_cookie("can_otp_enter", True, max_age=600)
        return red

    return render(request, 'register.html')


def otpVerify(request, uid):
    if request.method == "POST":
        try:
            profile = Profile.objects.get(uid=uid)
        except Profile.DoesNotExist:
            return HttpResponse("Profile does not exist")

        if request.COOKIES.get('can_otp_enter') is not None:
            if profile.otp == request.POST['otp']:
               
                user = profile.user
                user.backend = 'django.contrib.auth.backends.ModelBackend'  
                auth_login(request, user, backend=user.backend)
                
                red = redirect('home')
                red.set_cookie('verified', True)
                return red
            return HttpResponse("Wrong OTP")
        return HttpResponse("10 minutes passed")
    
    return render(request, "otp.html", {'id': uid})



def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(username=username, password=password)
        if user is not None:
            auth_login(request, user)  
            return redirect('home')
        else:
            messages.info(request, "Invalid login")
            return redirect('user_login')

    return render(request, 'loginn.html')


def generate_email_otp():
    return str(random.randint(100000, 999999))

def signup(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        phone = request.POST.get('phone')
        password = request.POST.get('password')
        confpassword = request.POST.get('confpassword')

        if User.objects.filter(username=username).exists():
            messages.info(request, 'Username already exists')
            return redirect('signup')
        elif User.objects.filter(email=email).exists():
            messages.info(request, 'Email already exists')
            return redirect('signup')
        elif password == confpassword:
            
            otp = generate_email_otp()

            request.session['otp'] = otp
            request.session['email'] = email
            request.session['username'] = username
            request.session['phone'] = phone
            request.session['password'] = password

         
            send_mail(
                'Your OTP Code',
                f'Your OTP code is {otp}',
                settings.EMAIL_HOST_USER,  
                [email],
                fail_silently=False,
            )

            return redirect('verify_email_otp')
        else:
            messages.info(request, 'Passwords do not match')
            return redirect('signup')

    return render(request, 'signup.html')

def verify_email_otp(request):
    if request.method == 'POST':
        entered_otp = request.POST.get('otp')
        session_otp = request.session.get('otp')
        
        if entered_otp == session_otp:
           
            user = User.objects.create_user(
                username=request.session['username'], 
                email=request.session['email'], 
                password=request.session['password'],
            )

            
            Profile.objects.create(
                user=user,
                phone_number=request.session['phone'],
                uid=str(uuid.uuid4())  
            )

           
            del request.session['otp']
            del request.session['email']
            del request.session['username']
            del request.session['phone']
            del request.session['password']

            messages.success(request, 'Your account has been created successfully! Please log in.')
            return redirect('user_login')
        else:
            messages.error(request, 'Invalid OTP. Please try again.')
            return redirect('verify_email_otp')

    return render(request, 'verify_email_otp.html')




class CustomLogoutView(LogoutView):
    def get_next_page(self):
        next_page = super().get_next_page()
        
        google_logout_url = 'https://accounts.google.com/Logout'
        return redirect(f'{google_logout_url}?continue={next_page}')

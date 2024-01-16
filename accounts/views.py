from typing import Any
from django.forms.forms import BaseForm
from django.http.response import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from . import forms
from django.contrib.auth import login, authenticate, logout, update_session_auth_hash
from django.contrib.auth.forms import AuthenticationForm, PasswordChangeForm, SetPasswordForm
from django.contrib import messages


from django.contrib.auth.mixins import UserPassesTestMixin
from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import CreateView, UpdateView, DetailView, DetailView
from django.views import View

from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, LogoutView

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
# Create your views here.


from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.utils.encoding import force_bytes, force_str
from QuizMaster import settings
from django.core.mail import EmailMessage, send_mail, EmailMultiAlternatives
from django.contrib.sites.shortcuts import get_current_site


from django.contrib.auth.tokens import default_token_generator
# from django.utils.encoding import force_text


def activate(request, uid64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uid64))
        user = User._default_manager.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(
            request, "Your account has been activated. You can now log in.")
        return redirect('login')
    else:
        messages.error(request, "Invalid activation link.")
        return redirect('register')


def signup(request):
    if not request.user.is_authenticated:
        form = forms.RegisterForm()
        if request.method == 'POST':
            form = forms.RegisterForm(request.POST)
            if form.is_valid():
                user = form.save()
                user.is_active = False  # The user is inactive until activation
                user.save()

                # Generate activation link
                token = default_token_generator.make_token(user)
                uid = urlsafe_base64_encode(force_bytes(user.pk))
                confirm_link = f'http://127.0.0.1:8000/accounts/activate/{uid}/{token}'

                # Send activation email
                email_subject = "Confirm your email"
                email_body = render_to_string(
                    'email_templates/email_confirmation.html',
                    {'user': user, 'confirm_link': confirm_link}
                )
                email = EmailMultiAlternatives(
                    subject=email_subject, body=email_body, to=[user.email]
                )
                email.attach_alternative(email_body, 'text/html')
                email.send()

                messages.success(
                    request, 'Check your email and click on the link to activate your account.')
                # return redirect('login')
                return redirect('signup')

        else:
            form = forms.RegisterForm()

        return render(request, 'form.html', {'form': form, 'title': 'Sign Up', 'button_text': 'Sign Up', 'button_class': 'btn-success'})
    else:
        return redirect('home')


def user_login(request):
    if not request.user.is_authenticated:
        if request.method == 'POST':
            form = AuthenticationForm(request, request.POST)
            if form.is_valid():
                username = form.cleaned_data.get('username')
                password = form.cleaned_data.get('password')
                user = authenticate(username=username, password=password)
                if user is not None:
                    login(request, user)

                    messages.success(request, 'Logged In Successfully')
                    messages.info(
                        request, f"You are now logged in as {username}")

                    # Redirect to the appropriate page after login
                    return redirect('privacy_settings')
                else:
                    messages.error(request, 'Invalid username or password')

        else:
            form = AuthenticationForm()

        return render(request, 'form.html', {'form': form, 'title': 'Login', 'button_text': 'Login', 'button_class': 'btn-primary'})
    else:
        return redirect('home')


# def profile(request):
#     if request.user.is_authenticated:
#         bought_cars = Car.objects.filter(buyers=request.user)
#         # print(bought_cars)
#         # for car in bought_cars:
#         #     print(car.quantity)

#         return render(request, 'profile.html', {'bought_cars': bought_cars})
#     else:
#         return redirect('login')

@login_required
def list_profiles(request):
    if not request.user.is_staff:
        return redirect('home')  # Redirect non-admin users

    users = User.objects.all()
    return render(request, 'list_profiles.html', {'users': users})

def privacy_settings(request):
    if request.user.is_authenticated:
        return render(request, 'profile_settings.html', {'title': 'Privacy Settings', 'user': request.user})
    else:
        return redirect('login')


# def signup(request):
#     if not request.user.is_authenticated:
#         form = forms.RegisterForm()
#         if request.method == 'POST':
#             form = forms.RegisterForm(request.POST)
#             if form.is_valid():
#                 # username = form.cleaned_data.get('username')
#                 # first_name = form.cleaned_data.get('first_name')
#                 # last_name = form.cleaned_data.get('last_name')
#                 # is_active = form.cleaned_data.get('is_active')

#                 # messages.success(request, 'Account created successfully')
#                 # form.save()


#                 # # send email
#                 # subject = 'Activate Your Account'
#                 # message = 'success'
#                 # email_from = settings.EMAIL_HOST_USER
#                 # send_mail(subject, message, email_from, [form.cleaned_data.get('email')])

#                 # # email address confirmation link
#                 # current_site = get_current_site(request)
#                 # email_subject = "Confirm your email"
#                 # message2 = render_to_string('email_confirmation.html', {

#                 #     'name': form.cleaned_data.get('username'),
#                 #     'domain': current_site.domain,
#                 #     'uid': urlsafe_base64_encode(force_bytes(form.cleaned_data.get('username'))),
#                 #     'token': generate_token.make_token(myuser)
#                 # })

#                 user = request.user
#                 token = default_token_generator.make_token(user)
#                 uid = urlsafe_base64_encode(force_bytes(user.pk))
#                 # link = reverse('activate', kwargs={'uidb64': uid, 'token': token})
#                 print('uid: ',uid,' token:', token)
#                 confirm_link = f'http://127.0.0.1:8000/accounts/activate/{uid}/{token}'
#                 email_subject = "Confirm your email"
#                 email_body = render_to_string(
#                     'accounts/email_templates/email_confirmation.html',{
#                         'user': user, 'confirm_link': confirm_link
#                     }
#                 )
#                 email = EmailMultiAlternatives(
#                     # email_subject, email_body, settings.EMAIL_HOST_USER, [form.cleaned_data.get('email')]
#                     subject=email_subject, body=email_body, to=[user.email]
#                 )
#                 email.attach_alternative(email_body, 'text/html')
#                 email.send()
#                 return HttpResponse('Check your email and click on the link to activate your account')
#                 # return redirect('login')
#                 # return redirect('home')
#                 # return redirect('profile')

#         else:
#             form = forms.RegisterForm()
#         return render(request, 'form.html', {'form': form, 'title': 'Sign Up', 'button_text': 'Sign Up', 'button_class': 'btn-success'})
#     else:
#         return redirect('home')
#         # return redirect('profile')


class UserSignUpView(SuccessMessageMixin, CreateView):
    form_class = forms.RegisterForm
    template_name = 'form.html'
    success_url = reverse_lazy('login')
    success_message = "Account created successfully"

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Sign Up'
        context['button_text'] = 'Sign Up'
        context['button_class'] = 'btn-success'
        return context


# def user_login(request):
#     if not request.user.is_authenticated:
#         if request.method == 'POST':
#             # form = AuthenticationForm(data=request.POST)
#             form = AuthenticationForm(request, request.POST)
#             if form.is_valid():
#                 username = form.cleaned_data.get('username')
#                 password = form.cleaned_data.get('password')
#                 user = authenticate(username=username, password=password)
#                 if user is not None:
#                     token, created = Token.objects.get_or_create(user=user)
#                     print('token: ', token, 'created: ', created)
#                     login(request, user)
#                     messages.success(request, 'Logged In Successfully')
#                     messages.info(
#                         request, f"You are now logged in as {username}")
#                     # return redirect('home')
#                     return redirect('privacy_settings')
#                 else:
#                     messages.error(request, 'Invalid username or password')

#         else:
#             form = AuthenticationForm()
#         return render(request, 'form.html', {'form': form, 'title': 'Login', 'button_text': 'Login', 'button_class': 'btn-primary'})
#     else:
#         return redirect('home')
#         # return redirect('profile')


class UserLoginView(SuccessMessageMixin, LoginView):
    template_name = 'form.html'

    def get_success_url(self):
        return reverse_lazy('privacy_settings')

    def form_valid(self, form):
        messages.success(self.request, 'Logged In Successfully')
        return super().form_valid(form)

    def form_invalid(self, form):
        messages.error(self.request, 'Invalid username or password')
        return super().form_invalid(form)

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home')
        return super().dispatch(request, *args, **kwargs)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Login'
        context['button_text'] = 'Login'
        context['button_class'] = 'btn-primary'
        return context


def user_logout(request):
    logout(request)
    messages.info(request, "Logged Out Successfully")
    return redirect('home')


# class UserLogoutView(LogoutView):
#     next_page = 'home'

#     def dispatch(self, request, *args, **kwargs):
#         response = super().dispatch(request, *args, **kwargs)
#         messages.info(self.request, "Logged Out Successfully")
#         return response

class UserLogoutView(View):

    def get(self, request):
        logout(request)
        messages.info(request, "Logged Out Successfully")
        return redirect('home')


def password_change(request):
    if request.user.is_authenticated:
        form = PasswordChangeForm(request.user)
        if request.method == 'POST':
            form = PasswordChangeForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(
                    request, 'Your password was successfully updated!')
                # return redirect('home')
                # return redirect('profile')
                return redirect('privacy_settings')
            else:
                messages.error(request, 'Please correct the error below.')
        return render(request, 'form.html', {'form': form, 'title': 'Change Your Password', 'button_text': 'Change Password', 'button_class': 'btn-warning'})
    else:
        return redirect('home')
        # return redirect('profile')


def password_change_without_old_password(request):
    if request.user.is_authenticated:
        form = SetPasswordForm(request.user)
        if request.method == 'POST':
            form = SetPasswordForm(request.user, request.POST)
            if form.is_valid():
                user = form.save()
                update_session_auth_hash(request, user)  # Important!
                messages.success(
                    request, 'Your password was successfully updated!')
                # return redirect('home')
                # return redirect('profile')
                return redirect('privacy_settings')
            else:
                messages.error(request, 'Please correct the error below.')
        return render(request, 'form.html', {'form': form, 'title': 'Change Your Password without Old Password', 'button_text': 'Change Password', 'button_class': 'btn-danger'})
    else:
        return redirect('home')
        # return redirect('profile')


def edit_privacy_settings(request):
    if request.user.is_authenticated:
        form = forms.EditProfileForm(instance=request.user)
        if request.method == 'POST':
            form = forms.EditProfileForm(request.POST, instance=request.user)
            if form.is_valid():
                messages.success(
                    request, 'Your user data was successfully updated.')
                form.save()
                # return redirect('home')
                # return redirect('profile')
                return redirect('privacy_settings')
            else:
                messages.error(request, 'Please correct the error below.')
        else:
            form = forms.EditProfileForm(instance=request.user)
        return render(request, 'form.html', {'form': form, 'title': 'Edit Your Profile', 'button_text': 'Update Profile', 'button_class': 'btn-info'})
    else:
        return redirect('home')
        # return redirect('profile')

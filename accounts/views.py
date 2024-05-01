from django.shortcuts import render, redirect
from django.views import View
from .forms import UserRegistrationForm, UserLoginForm
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.mixins import LoginRequiredMixin
from home.models import Post
class RegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            User.objects.create_user(cd['username'], cd['email'], cd['password1'])
            messages.success(request, 'Account created successfully')
            return redirect('home:home')
        return render(request, self.template_name, {'form': form})


class LoginView(View):
    template_name = 'accounts/login.html'
    form_class = UserLoginForm

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('home:home')
        return super().dispatch(request, *args, **kwargs)

    def get(self, request):
        forms = self.form_class
        return render(request, self.template_name, {'forms': forms})

    def post(self, request):
        forms = self.form_class(request.POST)
        if forms.is_valid():
            cd = forms.cleaned_data
            user = authenticate(request, username=cd['username'], password=cd['password'])
            if user is not None:
                login(request, user)
                messages.success(request, 'you login successfully')
                return redirect('home:home')
            messages.error(request, 'username or password is wrong')
            return render(request, self.template_name, {'forms': forms})



class LogoutView(LoginRequiredMixin,View):
    def get(self,request):
        logout(request)
        messages.success(request,'logout successfully')
        return redirect('home:home')


class ProfileView(LoginRequiredMixin,View):
    def get(self,request,user_id):
        user = User.objects.get(id=user_id)
        posts = Post.objects.filter(user= user)
        return render(request,'accounts/profile.html',{'user':user,"posts":posts})
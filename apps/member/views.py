from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from apps.member.forms import RegisterUserForm
from django.views.generic.edit import CreateView
from django.views.generic import View


class LoginUser(CreateView):
    template_name = 'authenticate/login.html'
    success_message = "You logged in successfully"
    error_message = "Error logging in"

    def get(self, request):
        return render(request, self.template_name, {})

    def post(self, request):
        if not request.method == "POST":
            return render(request, self.template_name, {})
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, email=email, password=password)
        if user is None:
            messages.error(request, self.error_message)
            return redirect('member:login')
        login(request, user)
        messages.success(request, self.success_message)
        return redirect('poll:index')


class LogoutUser(View):
    success_message = "You were logged out"

    def get(self, request):
        logout(request)
        messages.success(request, self.success_message)
        return redirect('poll:index')


class RegisterUser(CreateView):
    template_name = 'authenticate/register_user.html'
    form_class = RegisterUserForm
    success_message = "Registration successful"

    def post(self, request):
        form = self.form_class(request.POST)
        if not request.method == "POST":
            form = RegisterUserForm()
        if form.is_valid():
            form.save()
            email = form.cleaned_data['email']
            password = form.cleaned_data['password1']
            user = authenticate(email=email, password=password)
            login(request, user)
            messages.success(request, self.success_message)
            return redirect('poll:index')

        return render(request, self.template_name, {
            'form': form,
        })

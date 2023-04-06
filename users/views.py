from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View

from users.forms import RegisterForm


class RegisterView(View):
    form_class = RegisterForm
    template_name = 'users/register.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(to="quote:index")

        return super(RegisterView, self).dispatch(request, *args, **kwargs)

    def get(self, request, *args, **kwargs):
        return render(request, self.template_name, {"form": self.form_class()})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if not form.is_valid():
            return render(request, self.template_name, {"form": form})

        form.save()
        messages.success(request, f'Ваш акаунт успішно створено: {form.cleaned_data["username"]}')

        return redirect(to="users:login")

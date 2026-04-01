from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy


def home(request):
    return render(request, "core/home.html")


class CustomLoginView(LoginView):
    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect(self.get_success_url())
        return super().dispatch(request, *args, **kwargs)
    def get_success_url(self):
        user = self.request.user
        if user.groups.filter(name='Editores').exists():
            return reverse_lazy('editor')
        if user.groups.filter(name='Gestores').exists():
            return reverse_lazy('gestor')
        return reverse_lazy('home')

    def form_valid(self, form):
        user = form.get_user()
        auth_login(self.request, user)
        return redirect(self.get_success_url())

    def get_form(self, form_class=None):
        form = super().get_form(form_class)
        cls = "w-full px-3 py-2 border border-gray-300 rounded shadow-sm bg-white focus:outline-none focus:ring-2 focus:ring-yellow-300"
        if 'username' in form.fields:
            form.fields['username'].widget.attrs.update({'class': cls, 'placeholder': form.fields['username'].label or 'Usuário'})
        if 'password' in form.fields:
            form.fields['password'].widget.attrs.update({'class': cls, 'placeholder': form.fields['password'].label or 'Senha'})
        return form


@login_required
def editor(request):
    if not request.user.groups.filter(name='Editores').exists():
        return HttpResponseForbidden('Acesso restrito a Editores')
    return render(request, 'core/editor.html')


@login_required
def gestor(request):
    if not request.user.groups.filter(name='Gestores').exists():
        return HttpResponseForbidden('Acesso restrito a Gestores')
    return render(request, 'core/gestor.html')

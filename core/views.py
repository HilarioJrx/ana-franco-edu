from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import LoginView
from django.contrib.auth import login as auth_login
from django.http import HttpResponseForbidden
from django.urls import reverse_lazy
from django.contrib import messages
from django.conf import settings
import os
from .models import Feed, UniformItem, UniformOrder, UniformOrderItem
from .forms import UniformOrderForm, UniformOrderItemFormSet


def home(request):
    return render(request, "core/home.html")


def news_list(request):
    feeds = Feed.objects.all().order_by('-created_at').prefetch_related('categories')
    return render(request, 'core/news_list.html', {'feeds': feeds})


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
            form.fields['username'].widget.attrs.update({'class': cls, 'placeholder': 'Seu login'})
        if 'password' in form.fields:
            form.fields['password'].widget.attrs.update({'class': cls, 'placeholder': 'Senha'})
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


def uniform_catalog(request):
    items = UniformItem.objects.filter(available=True)
    
    # Permitir Alunos OU Superusuários (para você conseguir testar)
    is_aluno = request.user.is_authenticated and (
        request.user.groups.filter(name='Alunos').exists() or 
        request.user.is_superuser
    )

    order_form = None
    item_formset = None
    order_success = False

    if is_aluno:
        if request.method == 'POST':
            order_form = UniformOrderForm(request.POST)
            item_formset = UniformOrderItemFormSet(request.POST)

            if order_form.is_valid() and item_formset.is_valid():
                order = order_form.save(commit=False)
                order.user = request.user
                order.save()

                for form in item_formset:
                    if form.cleaned_data and not form.cleaned_data.get('DELETE', False):
                        UniformOrderItem.objects.create(
                            order=order,
                            uniform_item=form.cleaned_data['uniform_item'],
                            size=form.cleaned_data['size'],
                            quantity=form.cleaned_data['quantity'],
                        )

                messages.success(request, 'Pedido realizado com sucesso!')
                return redirect('uniform_catalog')
            else:
                messages.error(request, 'Erro ao processar o pedido. Verifique os campos abaixo.')
        else:
            order_form = UniformOrderForm()
            item_formset = UniformOrderItemFormSet()

    user_orders = None
    if request.user.is_authenticated:
        user_orders = UniformOrder.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'core/uniform_catalog.html', {
        'items': items,
        'is_aluno': is_aluno,
        'order_form': order_form,
        'item_formset': item_formset,
        'user_orders': user_orders,
    })

def document_list(request):
    doc_dir = os.path.join(settings.MEDIA_ROOT, 'documentos')
    documents = []
    
    if os.path.exists(doc_dir):
        for filename in os.listdir(doc_dir):
            if filename == '.gitkeep':
                continue
            
            file_path = os.path.join(doc_dir, filename)
            if os.path.isfile(file_path):
                ext = os.path.splitext(filename)[1].lower()
                documents.append({
                    'name': filename,
                    'url': settings.MEDIA_URL + 'documentos/' + filename,
                    'extension': ext,
                    'size_mb': round(os.path.getsize(file_path) / (1024 * 1024), 2)
                })
    
    return render(request, 'core/document_list.html', {'documents': documents})

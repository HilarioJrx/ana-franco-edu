from django.urls import path, include
from .views import home, CustomLoginView, editor, gestor

urlpatterns = [
    path('', home, name='home'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('editor/', editor, name='editor'),
    path('gestor/', gestor, name='gestor'),
]
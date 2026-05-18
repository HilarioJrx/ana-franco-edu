from django.urls import path, include
from .views import home, CustomLoginView, editor, gestor, news_list, uniform_catalog, document_list, my_orders

urlpatterns = [
    path('', home, name='home'),
    path('news/', news_list, name='news_list'),
    path('uniformes/', uniform_catalog, name='uniform_catalog'),
    path('documentos/', document_list, name='document_list'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('editor/', editor, name='editor'),
    path('gestor/', gestor, name='gestor'),
    path('meus-pedidos/', my_orders, name='my_orders'),
]
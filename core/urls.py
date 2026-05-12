from django.urls import path, include
from .views import home, CustomLoginView, editor, gestor, news_list, uniform_catalog

urlpatterns = [
    path('', home, name='home'),
    path('news/', news_list, name='news_list'),
    path('uniformes/', uniform_catalog, name='uniform_catalog'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('editor/', editor, name='editor'),
    path('gestor/', gestor, name='gestor'),
]
from django.urls import path, include
from .views import home, CustomLoginView, editor, gestor, news_list

urlpatterns = [
    path('', home, name='home'),
    path('news/', news_list, name='news_list'),
    path('accounts/login/', CustomLoginView.as_view(), name='login'),
    path('accounts/', include('django.contrib.auth.urls')),
    path('editor/', editor, name='editor'),
    path('gestor/', gestor, name='gestor'),
]
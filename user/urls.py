from django.urls import path
from . import views
# from django.views.generic import LogoutView

urlpatterns = [
    path('consultation', views.consultation, name='consultation'),
    path('applicationForm', views.application, name='applicationForm'),
    path('login', views.user_login, name='login'),
    path('loginForApp', views.user_login_before_app, name='loginForApp'),
    path('loginForFeedback', views.user_login_before_feedback, name='loginForFeedback'),
    path('register', views.register, name='register'),
    path('registerForApp', views.register_before_app, name='registerForApp'),
    path('account_view', views.account_view, name='account_view'),
    path('sendOfConsForm', views.sendOfConsForm, name='sendOfConsForm'),
    path('sendOfAppForm', views.sendOfAppForm, name='sendOfAppForm'),
    # path('logout/', views.LogoutView.as_view(), name='logout'),
    path('addStatus/', views.addStatus, name='addStatus'),
    path('appOfClient/<int:pk>', views.appOfClient, name='appOfClient'),
    path('edit/', views.edit, name='edit'),
    path('update/', views.update, name='update'),
    path('user/list/', views.list, name='list'),
    path('listStatus/', views.listStatus, name='listStatus'),
]


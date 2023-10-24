from django.contrib.auth.models import User
from django.urls import path
from . import views
from staff.views import ClientsListView
from django.views.generic import DetailView

urlpatterns = [
    path('baseOfClients/', ClientsListView.as_view(), name='user'),
    path('<int:pk>', DetailView.as_view(model=User, template_name="staff/aboutClient.html")),
    path('delete/<int:id>', views.delete, name='delete'),
]
from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.models import User
from .models import Status


class ClientsListView(ListView):
    model = User
    template_name = 'staff/baseOfClients.html'
    context_object_name = 'user'

    def get_success_url(self):
        return reverse_lazy('accounts:list_messages', kwargs={'uname': self.request.user.username })

def delete(request, id):
    obj = Status.objects.get(id=id)
    obj.delete()
    myList = {"allStatuses": Status.objects.all()
              }
    return render(request, 'staff/createNewStatus.html', context=myList)
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, request
from django.contrib.auth import authenticate, login
from .forms import ConsultationForm, ApplicationForm, LoginForm, UserRegistrationForm
from django.contrib.auth.models import User, Group
from .models import Application
from staff.models import Status


class ProfileActive():
    u = 0
    def __init__(self,user):
        self.user_active = user

class ClientActive():
    a = 0
    def __init__(self,client):
        self.client = client

def accountOfUser(request):
    return render(request, 'user/usersAccount.html')


def sendOfConsForm(request):
    return render(request, 'user/sendOfConsForm.html')


def sendOfAppForm(request):
    return render(request, 'user/sendOfAppForm.html')

def user_login_before_app(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/applicationForm')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
        return render(request, 'user/loginForApp.html', {'form': form})

def user_login_before_feedback(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponseRedirect('/feedback/createFB')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
        return render(request, 'feedback/loginForFeedback.html', {'form': form})

def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(username=cd['username'], password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    if request.user.is_active:
                        current_user = request.user
                        ProfileActive.u = int(current_user.id)
                    return HttpResponseRedirect('/account_view')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
        return render(request, 'user/login.html', {'form': form})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            new_user.groups.add(Group.objects.get(name='clients'))
            return render(request, 'user/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'user/register.html', {'user_form': user_form})

def register_before_app(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            new_user.groups.add(Group.objects.get(name='clients'))
            return render(request, 'user/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'user/registerForApp.html', {'user_form': user_form})

def consultation(request):
    error = ''
    if request.method == 'POST':
        form = ConsultationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/sendOfConsForm')
        else:
            error = "Ошибка валидации"
    form = ConsultationForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'user/consultation.html', data)


def application(request):
    error = ''
    if request.method == 'POST':
        form = ApplicationForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/sendOfAppForm')
        else:
            error = "Ошибка валидации"
    form = ApplicationForm()
    data = {
        'form': form,
        'error': error
    }
    return render(request, 'user/applicationForm.html', data)

def account_view(request):
    try:
        if not request.user.is_authenticated:
            return HttpResponseRedirect('/register')

        if request.user.is_staff:
            template = 'staff/managersAccount.html'
            return render(request, template)
        else:
            product = Application.objects.get(user=User.objects.get(pk=ProfileActive.u))
            template = 'user/usersAccount.html'

            INFO = {
            'nameOfClient': product.nameOfClient,
            'kindOfEvent': product.kindOfEvent,
            'phoneOfClient': product.phoneOfClient,
            'purposeOfEvent': product.purposeOfEvent,
            'dateTimeOfEvent': product.dateTimeOfEvent,
            'budgetOfEvent': product.budgetOfEvent,
            'placeOfEvent': product.placeOfEvent,
            'numberOfGuests': product.numberOfGuests,
            'ageOfGuests': product.ageOfGuests,
            'periodOfPreparation': product.periodOfPreparation,
            'addInfo': product.addInfo,
            }
            contex = {}
            contex.update(INFO)
            return render(request, template, contex)
    except Application.DoesNotExist:
        return HttpResponse('Заявка еще не создана')


def appOfClient(request, pk):
    try:
        product = Application.objects.get(user=User.objects.get(pk=pk))
        template = 'staff/appOfClient.html'
        ClientActive.a = pk

        INFO = {
        'id_app': product.id,
        'nameOfClient': product.nameOfClient,
        'kindOfEvent': product.kindOfEvent,
        'phoneOfClient': product.phoneOfClient,
        'purposeOfEvent': product.purposeOfEvent,
        'dateTimeOfEvent': product.dateTimeOfEvent,
        'budgetOfEvent': product.budgetOfEvent,
        'placeOfEvent': product.placeOfEvent,
        'numberOfGuests': product.numberOfGuests,
        'ageOfGuests': product.ageOfGuests,
        'periodOfPreparation': product.periodOfPreparation,
        'addInfo': product.addInfo,
        }
        contex = {}
        contex.update(INFO)
        return render(request, template, contex)
    except Application.DoesNotExist:
        return HttpResponse('Заявка еще не создана')

def edit(request):
    obj = Application.objects.get(user=User.objects.get(pk=ProfileActive.u))
    myList = {
        "nameOfClient": obj.nameOfClient,
        "phoneOfClient": obj.phoneOfClient,
        "kindOfEvent": obj.kindOfEvent,
        "purposeOfEvent": obj.purposeOfEvent,
        "dateTimeOfEvent": obj.dateTimeOfEvent,
        "budgetOfEvent": obj.budgetOfEvent,
        "placeOfEvent": obj.placeOfEvent,
        "numberOfGuests": obj.numberOfGuests,
        "ageOfGuests": obj.ageOfGuests,
        "periodOfPreparation": obj.periodOfPreparation,
        "addInfo": obj.addInfo,
    }
    return render(request,'user/edit.html', context=myList)

def update(request):
    obj = Application.objects.get(user=User.objects.get(pk=ProfileActive.u))
    obj.nameOfClient = request.GET['nameOfClient']
    obj.phoneOfClient = request.GET['phoneOfClient']
    obj.kindOfEvent = request.GET['kindOfEvent']
    obj.purposeOfEvent = request.GET['purposeOfEvent']
    obj.dateTimeOfEvent = request.GET['dateTimeOfEvent']
    obj.budgetOfEvent = request.GET['budgetOfEvent']
    obj.placeOfEvent = request.GET['placeOfEvent']
    obj.numberOfGuests = request.GET['numberOfGuests']
    obj.ageOfGuests = request.GET['ageOfGuests']
    obj.periodOfPreparation = request.GET['periodOfPreparation']
    obj.addInfo = request.GET['addInfo']
    import datetime
    updated_at = datetime.datetime.now()
    obj.created_et = updated_at
    obj.save()
    myList = {"allApps": Application.objects.all()
              }
    return render(request, 'user/update.html', context=myList)


def addStatus(request):
    template = 'staff/listStatus.html'
    obj = Status()
    obj.title = request.GET['title']
    obj.application = Application.objects.get(user=User.objects.get(pk=ClientActive.a))
    obj.save()
    myList = {'allStatuses': Status.objects.all(),
                }
    return render(request, template, context=myList)

def list(request):
    try:
        template = 'user/list.html'
        obj = Status.objects.get(application=Application.objects.get(user=User.objects.get(pk=ProfileActive.u)))
        myList = {"allStatuses": Status.objects.filter(application=obj.application)
                    }
        return render(request, template, context=myList)
    except Status.DoesNotExist:
        return HttpResponse('Статус еще не создан')

def listStatus(request):
    try:
        template = 'staff/listStatus.html'
        obj = Status.objects.get(application=Application.objects.get(user=User.objects.get(pk=ClientActive.a)))
        myList = {"allStatuses": Status.objects.filter(application=obj.application)
                    }
        return render(request, template, context=myList)
    except Status.DoesNotExist:
        return render(request, 'staff/createNewStatus.html')

from django.contrib.auth import login, authenticate, logout
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from .models import *
from .AppFiles.LengualeOut import WorkFile

class EnterView(View):
    template_name = 'Enter.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('Autentificate'))
        else:
            try:
                lenguage = request.COOKIES['lenguage']
            except:
                lenguage = "RU"
            return render(request, self.template_name, {
                'LengObj': WorkFile.outLenguage("EnterPage"),
                'lenguage': lenguage
            })

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse_lazy('Autentificate'))
        else:
            username = request.POST.get("username")
            password = request.POST.get("password")
            flagAuth = authenticate(username=username, password=password)
            if flagAuth is not None:
                login(request, flagAuth)
                return HttpResponseRedirect(reverse_lazy('Autentificate'))
            else:
                try:
                    lenguage = request.COOKIES['lenguage']
                except:
                    lenguage = "RU"
                return render(request, self.template_name, {
                    'error' : 'Не верный логин или пароль',
                    'LengObj': WorkFile.outLenguage("EnterPage"),
                    'lenguage': lenguage
                })

class ChangeLengEnterPage(View):

    def post(self, request):
        request.session['Currentpage'] = "Enter"
        request.session['inLenluage'] = request.POST.get('Len')
        return HttpResponseRedirect(reverse_lazy('ChangeLenguage'))


class NavigationPermision(View):

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            user = User.objects.get(username=request.user.username)
            try:
                groupName = str(user.groups.all()[0])
            except:
                raise Http404
            try:
                request.COOKIES['lenguage']
            except:
                request.session['Currentpage'] = "Autentificate"
                return HttpResponseRedirect(reverse_lazy('ChangeLenguage'))
            if groupName == "Managers":
                return HttpResponseRedirect(reverse_lazy('Admin'))
            elif groupName == "UserSimply":
                return HttpResponseRedirect(reverse_lazy('Client'))
            else:
                raise Http404
        else:
            return HttpResponseRedirect(reverse_lazy('Enter'))

class LogOut(View):

    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('Enter'))

    def post(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect(reverse_lazy('Enter'))



# Create your views here.

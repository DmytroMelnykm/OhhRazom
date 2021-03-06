import traceback

from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render
from django.views import View

from .AppFiles.LengualeOut import WorkFile
from .AppFiles.OutColorFile import WorkFiels
from django.urls import reverse_lazy
from .models import *

class ClientPage(View):
    template_name = 'FinallyClient.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            try:
                request.COOKIES['lenguage']
            except:
                request.session['Currentpage'] = 'Admin'
                return HttpResponseRedirect(reverse_lazy('ChangeLenguage'))
            try:
                dataAll = RkCompany.objects.filter(rk=int(request.session['currentOutAC']))
                try:
                    if request.session['advancedSearchType'] == "doors":
                        dataAll = dataAll.filter(Razom_number__doors__in = request.session['advancedSearchCodes'])
                    elif request.session['advancedSearchType'] == "Self_number":
                        dataAll = dataAll.filter(Razom_number__Self_number__in=request.session['advancedSearchCodes'])
                    elif request.session['advancedSearchType'] == "Razom_number":
                        dataAll = dataAll.filter(Razom_number__Razom_number__in=request.session['advancedSearchCodes'])
                except Exception as e:
                    print(traceback.format_exc())
                try:
                    dataAll = dataAll.filter(Razom_number__city_standart__id__in=request.session['filterCity'])
                    paramCity = CityPlanes.objects.filter(id__in=request.session['filterCity'])
                except:
                    paramCity = None

                try:
                    dataAll = dataAll.filter(Razom_number__type__id__in=request.session['filterType'])
                    paramType = FormatPlanes.objects.filter(id__in=request.session['filterType'])
                except:
                    paramType = None

                try:
                    dataAll = dataAll.filter(Razom_number__format__id__in=request.session['filterFormat'])
                    paramFormat = FormatPlanes.objects.filter(id__in=request.session['filterFormat'])
                except:
                    paramFormat = None

                try:
                    dataAll = dataAll.filter(story__id__in=request.session['filterStory'])
                    paramStory = Story.objects.filter(id__in=request.session['filterStory'])
                except:
                    paramStory = None

                outCity = []
                for i in dataAll.values('Razom_number__city_standart').distinct():
                    outCity.append(CityPlanes.objects.get(id=i['Razom_number__city_standart']))

                outType = []
                for i in dataAll.values('Razom_number__type').distinct():
                    outType.append(TypePlanes.objects.get(id=i['Razom_number__type']))

                outFormat = []
                for i in dataAll.values('Razom_number__format').distinct():
                    outFormat.append(FormatPlanes.objects.get(id=i['Razom_number__format']))

                outStory = []
                for i in dataAll.values('story').distinct():
                    outStory.append(Story.objects.get(id=i['story']))

                CountAC = {
                    "AllAC": len(RkCompany.objects.filter(rk=int(request.session['currentOutAC']))),
                    "like": len(RkCompany.objects.filter(rk=int(request.session['currentOutAC'])).filter(Grade=1)),
                    "Dislike": len(RkCompany.objects.filter(rk=int(request.session['currentOutAC'])).filter(Grade=2))
                }

                appFilter = {
                    "City": paramCity,
                    "Format": paramFormat,
                    "Type": paramType,
                    "Story": paramStory,
                    "Product": Rk.objects.get(id=request.session['currentOutAC'])

                }
                NameAgency = PermisionUsersClient.objects.get(userId=request.user.id)
                request.session['currentDataOut'] = list(dataAll.values())
                return render(request, self.template_name, {
                    "color": WorkFiels.colorFile(str(NameAgency.client.agancy)),
                    'lenguage': request.COOKIES['lenguage'],
                    'MyAC': Rk.objects.filter(client=NameAgency.client.id),
                    'CurrentAC': dataAll,
                    'filterCity': outCity,
                    'filterType': outType,
                    'filterFormat': outFormat,
                    'filterStory': outStory,
                    'Program': dataAll,
                    'tableNameHead': WorkFile.outLenguage("tableHead"),
                    "CountAboutAC": CountAC,
                    "ParamFilter": appFilter,
                    'TranslateBody': WorkFile.outLenguage("MainMapPage"),
                    'TranslateModalWindow': WorkFile.outLenguage("ModalWindow"),
                    'TranslateHead': WorkFile.outLenguage("HeadMain"),
                    'NameAgancy': PermisionUsersClient.objects.get(userId=request.user.id),
                    'Reach': ReachCity.objects.filter(rk=int(request.session['currentOutAC']))
                })
            except Exception as e:
                print('????????????:\n', traceback.format_exc())
                NameAgency = PermisionUsersClient.objects.get(userId=request.user.id)
                return render(request, self.template_name, {
                    "color": WorkFiels.colorFile(str(NameAgency.client.agancy)),
                    'lenguage': request.COOKIES['lenguage'],
                    'MyAC': Rk.objects.filter(client=NameAgency.client.id),
                    'tableNameHead': WorkFile.outLenguage("tableHead"),
                    'TranslateBody': WorkFile.outLenguage("MainMapPage"),
                    'TranslateModalWindow': WorkFile.outLenguage("ModalWindow"),
                    'TranslateHead': WorkFile.outLenguage("HeadMain"),
                    'NameAgancy' : PermisionUsersClient.objects.get(userId=request.user.id)
                })

        else:
            return HttpResponseRedirect(reverse_lazy('Enter'))
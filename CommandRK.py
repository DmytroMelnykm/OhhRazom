from django.http import HttpResponseRedirect, Http404
from django.urls import reverse_lazy
from django.views import View
from .models import *
from django.contrib import messages
import traceback


class OutputWindow:

    @staticmethod
    def numberIn(text):
        outList = []
        for i in (str(text).replace("\n", " ")).split():
            outList.append(i.strip())
        return outList

class CommandWork(View):

    def post(self, request, utils):
        if utils == "AddMark":
            errorNumb = "Ошибка с такими кодами : "
            try:
                if request.POST.get("story") == "":
                    story = "Основной сюжет"
                else:
                    story = request.POST.get("story")
                try:
                    infStory = Story.objects.filter(rk=request.session['SettingRKName']).get(story=story)
                except:
                    try:
                        if request.POST.get("color_begin") == "":
                            color = "#191970"
                        else:
                            color = request.POST.get("color_begin")
                        infStory = Story(
                            rk= Rk.objects.get(id=request.session['SettingRKName']),
                            story= story,
                            color= color
                        )
                        infStory.save()
                    except Exception as e:
                        print('Ошибка:\n', traceback.format_exc())
                if request.POST.get("choise_type") == "doors":
                    for i in OutputWindow.numberIn(request.POST.get("area_mark")):
                        print(i)
                        try:
                            RkCompany.objects.filter(rk=request.session['SettingRKName']).get(Razom_number__doors=i)
                            errorNumb += str(i) + " "
                        except:
                            try:
                                tmpNumb = Totalplanes.objects.get(doors=i)
                                RkCompany(
                                    rk= Rk.objects.get(id=request.session['SettingRKName']),
                                    Razom_number= tmpNumb,
                                    story= infStory
                                ).save()
                            except Exception as e:
                                print('Ошибка:\n', traceback.format_exc())
                                print(f"Нет такого {i}")
                                errorNumb += str(i) + " "

                elif request.POST.get("choise_type") == "Razom_number":
                    for i in OutputWindow.numberIn(request.POST.get("area_mark")):
                        try:
                            RkCompany.objects.filter(rk=request.session['SettingRKName']).get(Razom_number__Razom_number=int(i))
                            errorNumb += str(i) + " "
                        except:
                            try:
                                tmpNumb = Totalplanes.objects.get(Razom_number=int(i))
                                RkCompany(
                                    rk=Rk.objects.get(id=request.session['SettingRKName']),
                                    Razom_number=tmpNumb,
                                    story=infStory
                                ).save()
                            except Exception as e:
                                print('Ошибка:\n', traceback.format_exc())
                                print(f"Нет такого {i}")
                                errorNumb += str(i) + " "
                else:
                    print("Not Work")
                if errorNumb != "":
                    print("hello")
                    messages.success(request, errorNumb)
            except Exception as e:
                print('Ошибка:\n', traceback.format_exc())
                messages.success(request, 'Ошибка')
            finally:
                return HttpResponseRedirect(reverse_lazy('CurrentRK'))
        elif utils == "Changecolor":
            errorNumb = "Ошибка с такими кодами : "
            try:
                if request.POST.get("story") == "":
                    story = "Основной сюжет"
                else:
                    story = request.POST.get("story")
                try:
                    infStory = Story.objects.filter(rk=request.session['SettingRKName']).get(story=story)
                except:
                    try:
                        if request.POST.get("color_begin") == "":
                            color = "#191970"
                        else:
                            color = request.POST.get("color_begin")
                        infStory = Story(
                            rk=Rk.objects.get(id=request.session['SettingRKName']),
                            story=story,
                            color=color
                        )
                        infStory.save()
                    except Exception as e:
                        print('Ошибка:\n', traceback.format_exc())
                if request.POST.get("choise_type") == "doors":
                    for i in OutputWindow.numberIn(request.POST.get("area_mark")):
                        try:
                            tmpRKNumb = RkCompany.objects.get(Razom_number__doors=i)
                            tmpRKNumb.story = infStory
                            tmpRKNumb.save()
                        except Exception as e:
                            print('Ошибка:\n', traceback.format_exc())
                            print(f"Нет такого {i}")
                            errorNumb = str(i) + " ы"
                elif request.POST.get("choise_type") == "Razom_number":
                    for i in OutputWindow.numberIn(request.POST.get("area_mark")):
                        try:
                            tmpRKNumb = RkCompany.objects.get(Razom_number__Razom_number=int(i))
                            tmpRKNumb.story = infStory
                            tmpRKNumb.save()
                        except Exception as e:
                            print('Ошибка:\n', traceback.format_exc())
                            print(f"Нет такого {i}")
                            errorNumb = str(i) + " "
                else:
                    print("Not Work")
                if errorNumb != "":
                    messages.success(request, errorNumb)
            except Exception as e:
                print('Ошибка:\n', traceback.format_exc())
                messages.success(request, 'Ошибка')
            finally:
                return HttpResponseRedirect(reverse_lazy('CurrentRK'))
        elif utils == "DeleteMark":
            try:
                if request.POST.get("choise_type") == "doors":
                    for i in OutputWindow.numberIn(request.POST.get("area_mark")):
                        try:
                            tmpRKNumb = RkCompany.objects.get(Razom_number__doors=i)
                            tmpRKNumb.delete()
                        except Exception as e:
                            print('Ошибка:\n', traceback.format_exc())
                            print(f"Нет такого {i}")
                            errorNumb = str(i) + " "
                elif request.POST.get("choise_type") == "Razom_number":
                    for i in OutputWindow.numberIn(request.POST.get("area_mark")):
                        try:
                            tmpRKNumb = RkCompany.objects.get(Razom_number__Razom_number=int(i))
                            tmpRKNumb.delete()
                        except Exception as e:
                            print('Ошибка:\n', traceback.format_exc())
                            print(f"Нет такого {i}")
                            errorNumb = str(i) + " "
                else:
                    print("Not Work")
                if errorNumb != "":
                    messages.success(request, errorNumb)
            except Exception as e:
                print('Ошибка:\n', traceback.format_exc())
                messages.success(request, 'Ошибка')
        elif utils == "ChangeLenguage":
            request.session['Currentpage'] = "CurrentRK"
            request.session['inLenluage'] = request.POST.get('Len')
            return HttpResponseRedirect(reverse_lazy('ChangeLenguage'))
        elif utils == "ShowMap":
            request.session['currentOutAC'] = request.session['SettingRKName']
            del request.session['SettingRKName']
            return HttpResponseRedirect(reverse_lazy('Admin'))
        elif utils == "ResetColorStory":
            try:
                instanceStory = Story.objects.filter(rk=request.session['SettingRKName']).get(story='Основной сюжет')
            except:
                instanceStory = Story(
                    rk=Rk.objects.get(id=request.session['SettingRKName']),
                    story='Основной сюжет',
                    color='#191970'
                )
                instanceStory.save()
            allObjsectInAC = RkCompany.objects.filter(rk=request.session['SettingRKName'])
            for i in allObjsectInAC:
                i.story = instanceStory
                i.save()
            return HttpResponseRedirect(reverse_lazy('CurrentRK'))
        elif utils == "ClearAC":
            instanceAC = RkCompany.objects.filter(rk=request.session['SettingRKName'])
            for i in instanceAC:
                i.delete()
            return HttpResponseRedirect(reverse_lazy('CurrentRK'))
        elif utils == "back":
            return HttpResponseRedirect(reverse_lazy('setting'))
        elif utils == "AddReach":
            try :
                inst = ReachCity.objects.filter(rk=int(request.session['SettingRKName'])).get(city=int(request.POST.get('ChooseCity')))
                inst.reach=  request.POST.get('TextForReach')
                inst.frequency =  request.POST.get('TextForFrequency')
                inst.period =  request.POST.get('TextForPeriod')
                inst.save()
            except:
                Instance = ReachCity(
                    rk = Rk.objects.get(id=request.session['SettingRKName']),
                    city = CityPlanes.objects.get(id=int(request.POST.get('ChooseCity'))),
                    reach = request.POST.get('TextForReach'),
                    frequency=request.POST.get('TextForFrequency'),
                    period=request.POST.get('TextForPeriod')
                )
                Instance.save()
            return HttpResponseRedirect(reverse_lazy('CurrentRK'))
        else:
            raise Http404
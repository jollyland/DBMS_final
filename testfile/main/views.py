from django.http import HttpResponse
from django.shortcuts import render
from main.models import *
from django.core.exceptions import ObjectDoesNotExist

# Create your views here.

def main(request):
#    uni = Academy.objects.all()
    return render(request, 'index.html')

def search_uni(request):
#    return HttpResponse('依大學')
    place = ['基隆市','臺北市','新北市','宜蘭市','桃園市','新竹市','新竹縣','苗栗縣','台中市','彰化縣','南投縣','雲林縣','嘉義市','嘉義縣','屏東縣','花蓮縣','台東縣','澎湖縣']

    return render(request, 's_uni.html', {'region': place})

def search_apt(request):
    return render(request, 's_dpt.html')


def search_gp(request):
    gplist = Academy.objects.all()
    return render(request, 'gp_main.html', {'gplist': gplist})

def list_all(request):
    alldpt = Department.objects.all()
    uni = University.objects.all()
    return render(request, 'dpt_list.html', {'dpt':alldpt,'uni':uni})


def gp_each(request, name):
    gplist = Academy.objects.get(name=name)
    gpapt = []
    gpapt = Maindepartment.objects.filter(academy=name)
    context = {
        'gp': gplist,
        'apt': gpapt
    }
    return render(request, 'gp_each.html', context)


def dprt_each(request, dprtid):
    dpt = Department.objects.get(id=dprtid)
    uni = University.objects.get(id=dpt.university_id)
    try:
        career = Career.objects.get(id=dprtid)
    except ObjectDoesNotExist:
        career = Career()

    try:
        G = Gsat.objects.get(id=dprtid)
    except ObjectDoesNotExist:
        G = Gsat()
    try:
        A = Ast.objects.get(id=dprtid)
    except ObjectDoesNotExist:
        A = Ast()
    context = {
        'dpt': dpt,
        'uni': uni,
        'career': career,
        'gsat': G,
        'ast': A,
    }
    return render(request, 'dprt_each.html', context)

def uni_result(request):
    if 'uni_keyword' in request.GET and request.GET['uni_keyword'] != '' and 'uni_s_con' in request.GET and request.GET['uni_s_con'] !='' :
        if request.GET['uni_s_con'] == '0':
            result = University.objects.filter(name__contains=request.GET['uni_keyword'])
            return render(request, 'uni_result.html', {'result': result, 'keyword':request.GET['uni_keyword']})
        elif request.GET['uni_s_con'] == '1':
            result = University.objects.filter(id__contains=request.GET['uni_keyword'])
            return render(request, 'uni_result.html', {'result': result, 'keyword':request.GET['uni_keyword']})
        else:
            return HttpResponse('sthwrong')
    elif 'region' in request.GET and request.GET['region'] !='':
        result = University.objects.filter(position__contains=request.GET['region'])
        return render(request, 'uni_result.html', {'result': result, 'keyword':request.GET['region']})

    else:
        return HttpResponse('badinput')


def dpt_result(request):
    if 'dpt_keyword' in request.GET and request.GET['dpt_keyword'] != '' :
        result = Department.objects.filter(name__contains=request.GET['dpt_keyword'])
        return render(request, 'dpt_result.html', {'result': result, 'keyword': request.GET['dpt_keyword']})

    else:
        return HttpResponse('badinput')


from django.core.checks import messages
from django.shortcuts import render
from django.http import HttpResponse, response
from .models import group,Server
import json
from django.views.decorators.csrf import csrf_exempt
# Create your views here.
def get_pack(request):
    PackNumber=request.GET.get("pack")
    g=group.objects.get(pk=PackNumber)
    question=g.questions_set.all().order_by('published_date')
    # for question in Questions:
    #     print(question)
    i=1
    #just a commit
    response_data={}
    response_data["ok"]={}
    response_data["ok"][g.title]={}
    for q in question:
        response_data["ok"][g.title][i]=q.question
        i += 1
    return HttpResponse(json.dumps(response_data), content_type="application/json")
@csrf_exempt
def get_pack_by_server(request):
    response_data={}
    server_giuld=""
    if not request.method == "POST":
         response_data["error"]="please use a post request"
         return HttpResponse(json.dumps(response_data), content_type="application/json",status=405)
    server_giuld=request.POST.get('server')
    print(server_giuld)
    if 'number_of_packs' not in request.POST or request.POST["number_of_packs"]== 1:
        try:
            s=Server.objects.get(giuld=server_giuld)
        except:
            response_data["error"]="this server does not registerd! please register server"
            return HttpResponse(json.dumps(response_data), content_type="application/json",status=404)
        pack=s.pack
        g=group.objects.get(pk=pack)
        question=g.questions_set.all().order_by('published_date')
        s.pack=pack + 1
        s.save()
        i=1
        response_data['ok'][g.title]={}
        response_data['ok']={}
        for q in question:
            response_data['ok'][g.title][i]=q.question
            i += 1
    elif int(request.POST["number_of_packs"]) > 3 or int(request.POST["number_of_packs"]) < 1:
        response_data["error"]="Please use a number in the range 1 to 3"
        return HttpResponse(json.dumps(response_data), content_type="application/json",status=400)
    else:
        try:
            s=Server.objects.get(giuld=server_giuld)
        except:
            response_data["error"]="this server does not registerd! please register server"
            return HttpResponse(json.dumps(response_data),status=404, content_type="application/json")
        number_of_packs=request.POST["number_of_packs"]
        response_data['ok']={}
        for z in range(1,int(number_of_packs)+1):
            pack=s.pack
            g=group.objects.get(pk=pack)
            question=g.questions_set.all().order_by('published_date')
            s.pack=pack + 1
            s.save()
            i=1
            response_data['ok'][g.title]={}
            for q in question:
                response_data['ok'][g.title][i]=q.question
                i += 1
    return HttpResponse(json.dumps(response_data), content_type="application/json")
@csrf_exempt
def register_server(request):
    response_data={}
    if not request.method == "POST":
        response_data["error"]="please use a post request"
        return HttpResponse(json.dumps(response_data), content_type="application/json",status=405)
    try:
        server=request.POST["server"]
        name=request.POST["server_name"]
    except:
        response_data["error"]="You have not sent some required parameters!"
        return HttpResponse(json.dumps(response_data), content_type="application/json",status=400)
    s=Server(name=name,giuld=server,pack=1)
    s.save()
    response_data['message']='Successful,registerd'
    return HttpResponse(json.dumps(response_data), content_type="application/json")
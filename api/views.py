from django.core.checks import messages
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, response
from .models import group,Server
import json
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
# Create your views here.
def get_pack(request,pack):
    # PackNumber=request.GET.get("pack")
    print(f"pack is {pack}")
    g=get_object_or_404(group, pk=pack)
    question=g.questions_set.all().order_by('published_date')
    # for question in Questions:
    #     print(question)
    i=1
    # just a commit
    response_data={}
    response_data["ok"]={}
    response_data["ok"]["title"]=g.title
    for q in question:
        response_data["ok"][i]=q.question
        i += 1
    return HttpResponse(json.dumps(response_data), content_type="application/json")
@csrf_exempt
@require_POST
def get_pack_by_server(request):
    response_data={}
    server_giuld=""
    server_giuld=request.POST.get('server')
    print(server_giuld)
    if 'number_of_packs' not in request.POST or request.POST["number_of_packs"]== 1:
        s=get_object_or_404(Server,giuld=server_giuld)
        pack=s.pack
        try:
            g=group.objects.get(pk=pack)
        except:
            response_data["error"]="There isnt new pack for you!please wait for new packs"
            return HttpResponse(json.dumps(response_data),status=456, content_type="application/json")
        question=g.questions_set.all().order_by('published_date')
        s.pack=pack + 1
        s.save()
        i=1
        response_data["ok"]={}
        response_data["ok"]["title"]=g.title
        for q in question:
            response_data["ok"][i]=q.question
            i += 1
    elif int(request.POST["number_of_packs"]) > 3 or int(request.POST["number_of_packs"]) < 1:
        response_data["error"]="Please use a number in the range 1 to 3"
        return HttpResponse(json.dumps(response_data), content_type="application/json",status=400)
    else:
        s=get_object_or_404(Server,giuld=server_giuld)
        number_of_packs=request.POST["number_of_packs"]
        for z in range(1,int(number_of_packs)+1):
            pack=s.pack
            try:
                g=group.objects.get(pk=pack)
            except:
                response_data["error"]="There isnt new pack for you!please wait for new packs"
                return HttpResponse(json.dumps(response_data),status=456, content_type="application/json")
            question=g.questions_set.all().order_by('published_date')
            s.pack=pack + 1
            s.save()
            i=1
            response_data["ok"]={}
            response_data["ok"]["title"]=g.title
            for q in question:
                response_data["ok"][i]=q.question
                i += 1
    return HttpResponse(json.dumps(response_data), content_type="application/json")
@csrf_exempt
@require_POST
def register_server(request):
    response_data={}
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
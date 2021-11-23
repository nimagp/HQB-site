from django.core.checks import messages
from django.shortcuts import get_object_or_404, render
from django.http import HttpResponse, response
from django.utils import timezone
from .models import Pack, Question,Server
import json
from django.core import serializers
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from django.contrib.auth.decorators import login_required
# Create your views here.
def get_pack(request,pack):
    # PackNumber=request.GET.get("pack")
    print(f"pack is {pack}")
    g=get_object_or_404(Pack, pk=pack)
    question=g.Question_set.all().order_by('published_date')
    # for question in Question:
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
                g=Pack.objects.get(pk=pack)
            except:
                response_data["error"]="There isnt new pack for you!please wait for new packs"
                return HttpResponse(json.dumps(response_data),status=456, content_type="application/json")
            question=g.Question_set.all().order_by('published_date')
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
def add_question_pack(request):
    if request.method == "POST":
        try:
            request.POST["pack_name"]
            request.POST["q1"]
            request.POST["q2"]
            request.POST["q3"]
            request.POST["q4"]
            request.POST["q5"]
        except:
            response_data="You have not sent some required parameters!"
            return render(request, 'blog/post_edit.html', {'returned': response_data})
        p=Pack(title=request.POST["pack_name"])
        p.save()
        q1=Question(question=request.POST["q1"],Pack=p,published_date = timezone.now())
        q1.save()
        del q1
        q2=Question(question=request.POST["q2"],Pack=p,published_date = timezone.now())
        q2.save()
        del q2
        q3=Question(question=request.POST["q3"],Pack=p,published_date = timezone.now())
        q3.save()
        del q3
        q4=Question(question=request.POST["q4"],Pack=p,published_date = timezone.now())
        q4.save()
        del q4
        q5=Question(question=request.POST["q5"],Pack=p,published_date = timezone.now())
        q5.save()
        del q5
        del p
        response_data="Successful,added"
        return render(request, 'blog/post_edit.html', {'returned': response_data})
    
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
    ResponseData={}
    QuestionPack=get_object_or_404(Pack, pk=pack)
    try:
        ResponseData["Status"] = "OK"
        ResponseData["Pack"] = QuestionPack.title
        ResponseData["Questions"] = []
        Questions=QuestionPack.question_set.all().order_by('published_date')
        for Question in Questions:
            ResponseData["Questions"].append(Question.question)
    except Exception as e:
        ResponseData["Status"] = "Error"
        ResponseData["Error"] = str(e)
    return HttpResponse(json.dumps(ResponseData), content_type="application/json")
@csrf_exempt
@require_POST
def get_pack_by_server(request):
    ResponseData={}
    ResponseCode=200
    try:
        ServerID=request.POST.get('server')
        if 'number_of_packs' not in request.POST or request.POST["number_of_packs"]== 1:
            ServerModel=Server.objects.get_or_create(giuld=ServerID)
            QuestionPack=get_object_or_404(Pack,pk=ServerModel.pack)
            Questions=QuestionPack.question_set.all().order_by('published_date')
            ServerModel.pack = ServerModel.pack + 1
            ServerModel.save()
            ResponseData["Status"] = "OK"
            ResponseData["Pack"] = QuestionPack.title
            ResponseData["Questions"] = []
            for Question in Questions:
                ResponseData["Questions"].append(Question.question)
        elif int(request.POST["number_of_packs"]) > 3 or int(request.POST["number_of_packs"]) < 1:
            ResponseCode = 400
            raise Exception("Please use a number in the range 1 to 3")
        else:
            #get packs in the amount of number_of_packs parameter
            ResponseData["Packs"] = {}
            for i in range(int(request.POST["number_of_packs"])):
                ServerModel=get_object_or_404(Server,giuld=ServerID)
                QuestionPack=get_object_or_404(Pack,pk=ServerModel.pack)
                Questions=QuestionPack.question_set.all().order_by('published_date')
                ServerModel.pack = ServerModel.pack + 1
                ServerModel.save()
                ResponseData["Packs"][QuestionPack.title] = {}
                ResponseData["Packs"][QuestionPack.title]["Questions"] = []
                for Question in Questions:
                    ResponseData["Packs"][QuestionPack.title]["Questions"].append(Question.question)
                

        

    except Exception as e:
        ResponseData["Status"] = "Error"
        ResponseData["Error"] = str(e)
    return HttpResponse(json.dumps(ResponseData), content_type="application/json",status=ResponseCode)
@require_POST
@csrf_exempt
def add_question_pack(request):
    ResponseData={}
    try:
        if ('pack_name',"q1","q2","q3","q4","q5") not in request.POST:
            ResponseCode = 400
            raise Exception("Some parameters are missing")
        PackModel = Pack(title=request.POST["pack_name"])
        PackModel.save()
        QuestionModel1 = Question(question=request.POST["q1"],pack=PackModel)
        QuestionModel1.save()
        QuestionModel2 = Question(question=request.POST["q2"],pack=PackModel)
        QuestionModel2.save()
        QuestionModel3 = Question(question=request.POST["q3"],pack=PackModel)
        QuestionModel3.save()
        QuestionModel4 = Question(question=request.POST["q4"],pack=PackModel)
        QuestionModel4.save()
        QuestionModel5 = Question(question=request.POST["q5"],pack=PackModel)
        QuestionModel5.save()
        ResponseData["Status"] = "OK"
    except Exception as e:
        ResponseData["Status"] = "Error"
        ResponseData["Error"] = str(e)
    return HttpResponse(json.dumps(ResponseData), content_type="application/json",status=ResponseCode)
    
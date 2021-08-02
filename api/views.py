from django.shortcuts import render
from django.http import HttpResponse
from .models import group, questions
import json
# Create your views here.
def get_pack(request):
    PackNumber=request.GET.get("pack")
    g=group.objects.get(pk=PackNumber)
    question=g.questions_set.all().order_by('published_date')
    # for question in Questions:
    #     print(question)
    i=1
    #just a commit :)
    response_data = {"title":g.title}
    for q in question:
        response_data[i]=q.question
        i += 1
    return HttpResponse(json.dumps(response_data), content_type="application/json")

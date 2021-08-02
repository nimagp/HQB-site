from django.urls import path
from . import views

urlpatterns = [
  path("",views.get_pack,name="question_get"),
]
from django.urls import path
from . import views

urlpatterns = [
  path("v1/get_pack_by_id/",views.get_pack,name="question_get"),
  path("v1/get_pack_by_server/",views.get_pack_by_server,name="pack_get"),
  path("v1/register_server/",views.register_server,name="register_server"),
]
from django.contrib import admin
from .models import group
from .models import questions,Server
# Register your models here.
admin.site.register(group)
admin.site.register(questions)
admin.site.register(Server)
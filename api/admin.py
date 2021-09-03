from django.contrib import admin
from .models import Pack
from .models import Question,Server
# Register your models here.
admin.site.register(Pack)
admin.site.register(Question)
admin.site.register(Server)
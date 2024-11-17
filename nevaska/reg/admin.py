from django.contrib import admin
from .models import Empresa, User
from django.contrib.auth.admin import UserAdmin

# Register your models here.

admin.site.register(Empresa)
admin.site.register(User)

from django.contrib import admin

# Register your models here.
from .models import Chama, Member, Membership

admin.site.register(Chama)
admin.site.register(Member)
admin.site.register(Membership) 
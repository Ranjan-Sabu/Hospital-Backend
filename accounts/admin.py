from django.contrib import admin
from accounts.models import User,Doctors

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display = ['id','username','email','is_doctor']
admin.site.register(User,UserAdmin)

class DoctorAdmin(admin.ModelAdmin):
    list_display = ['id']
admin.site.register(Doctors,DoctorAdmin)




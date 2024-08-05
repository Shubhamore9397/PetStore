from django.contrib import admin
from petapp.models import Pet

# Register your models here.
class PetAdmin(admin.ModelAdmin):
    list_display = ['id','name','type','breed','gender','age','price','description']
    list_filter = ['type','breed','price']
    
admin.site.register(Pet,PetAdmin)

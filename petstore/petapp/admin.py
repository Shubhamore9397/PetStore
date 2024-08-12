from django.contrib import admin
from petapp.models import Pet,Cart

# Register your models here.
class PetAdmin(admin.ModelAdmin):
    list_display = ['id','name','type','breed','gender','age','price','description','petimage']
    list_filter = ['type','breed','price']
    
admin.site.register(Pet,PetAdmin)

class CartAdmin(admin.ModelAdmin):
    list_display = ['id','pid','uid','quantity']
    list_filter = ['uid']
    
admin.site.register(Cart, CartAdmin)

from django.contrib import admin
from ustawi.models import *

class CropAdmin(admin.ModelAdmin):
	list_display=['id','crop','code']
	
class CropSalesAdmin(admin.ModelAdmin):
	list_display=['id','farm','crop','weight','price']

class CoordinatorAdmin(admin.ModelAdmin):
	list_display=['id','alias','first_name','last_name']

admin.site.register(Crop,CropAdmin)
admin.site.register(CropSales,CropSalesAdmin)
admin.site.register(Farm)
admin.site.register(Coordinator,CoordinatorAdmin)

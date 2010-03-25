from django.contrib import admin
from ustawi.models import *

class CropAdmin(admin.ModelAdmin):
	list_display=['crop','code']
	
admin.site.register(Crop,CropAdmin)
admin.site.register(Farmer)
admin.site.register(Farm)

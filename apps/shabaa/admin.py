from django.contrib import admin
from shabaa.models import *


class EnterpriseAdmin(admin.ModelAdmin):
    list_display = ('id','reporter','industry','jobs_created','location')
    list_filter = []    

class ShabaaReporterAdmin(admin.ModelAdmin):
    list_display = ('id','alias','first_name', 'last_name')
    list_filter = []    


class ActivityAdmin(admin.ModelAdmin):
    list_display = ('id','reporter','activitytype','male_attendees','female_attendees','location')
    list_filter = []    

admin.site.register(ShabaaReporter,ShabaaReporterAdmin)
admin.site.register(Enterprise,EnterpriseAdmin)
admin.site.register(Industry)
admin.site.register(Organisation)
admin.site.register(Activity,ActivityAdmin)
admin.site.register(ActivityType)
admin.site.register(VisitorType)


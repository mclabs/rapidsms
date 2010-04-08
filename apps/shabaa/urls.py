from django.conf.urls.defaults import *
import shabaa.views as views

urlpatterns = patterns('',
    url(r'^shabaa/$',            views.index),
    url(r'^shabaa/map$',            views.map),
    url(r'^shabaa/reports$',            views.reports),

)

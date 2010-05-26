from django.conf.urls.defaults import *
import shabaa.views as views

urlpatterns = patterns('',
    url(r'^shabaa/$',            views.index),
    url(r'^shabaa/map$',            views.map),
    url(r'^shabaa/reports$',            views.reports),
    url(r'^shabaa/to_json$',            views.to_json),
    url(r'^shabaa/graphs$',            views.graphs),

)

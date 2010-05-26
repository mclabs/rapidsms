from django.conf.urls.defaults import *
import ustawi.views as views

urlpatterns = patterns('',
    url(r'^ustawi/$',            views.index),
    url(r'^ustawi/map$',            views.map),
    url(r'^ustawi/reports$',            views.reports),
    url(r'^ustawi/graphs$',            views.graphs),

)

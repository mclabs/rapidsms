from django.conf.urls.defaults import *
import ustawi.views as views

urlpatterns = patterns('',
    url(r'^ustawi/$',            views.index),
)

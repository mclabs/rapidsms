from django.conf.urls.defaults import *
import ecd.views as views

urlpatterns = patterns('',
    url(r'^ecd/$',            views.index),
)

from django.conf.urls.defaults import *
import shabaa.views as views

urlpatterns = patterns('',
    url(r'^shabaa/$',            views.index),
)

from django.conf.urls.defaults import *
import girlchild.views as views

urlpatterns = patterns('',
    url(r'^girlchild/$',            views.index),
)

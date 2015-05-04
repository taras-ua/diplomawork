from django.conf import settings
from django.conf.urls import patterns, url
# from django.contrib import admin

urlpatterns = patterns('',
    url(r'^$', 'app.views.home', name='home'),
    url(r'^graph/$', 'app.views.graph', name='graph'),
    url(r'^probabilities/$', 'app.views.probabilities', name='probabilities'),
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),

    # url(r'^admin/', include(admin.site.urls)),
)
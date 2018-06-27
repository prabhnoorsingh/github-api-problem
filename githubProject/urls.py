from django.conf.urls import url, include
from django.contrib import admin
# Local Imports
from githubUsers.views import schema_view

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^users/', include('githubUsers.urls')),
    url(r'^$', schema_view),
]

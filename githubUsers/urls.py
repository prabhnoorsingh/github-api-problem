from django.conf.urls import url
#Local imports
from githubUsers import views


urlpatterns = [
    url(r'^fetchAndStoreAllUsers/$', views.fetch_and_store_all_users),
    url(r'^sendFilteredUsers/$', views.send_filtered_users),
    ]
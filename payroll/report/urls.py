from django.urls import path
from . import views
from rest_framework.urlpatterns import format_suffix_patterns

urlpatterns = [
    path('', views.index, name='home'),
    path('report/', views.timelog_list),
    path('upload/', views.upload, name='upload'),
]

urlpatterns = format_suffix_patterns(urlpatterns)
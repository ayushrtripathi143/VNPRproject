from django.contrib import admin
from django.urls import path,include
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # path('',views.index,name="index"),
    path('',views.index1111,name="index1111"),
    path('index',views.index,name="index"),
    path('upload',views.uploadImage,name="uploadImage"),
    path('output/',views.output,name='output'),
    path("about",views.about,name='about'),
    path("services",views.services,name='services'),
    path("contact",views.contact,name='contact'),
    path('project1',views.project1,name='project1'),
    path('output',views.output,name='output'),

]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
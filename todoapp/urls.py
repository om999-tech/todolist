from django.urls import path
from todoapp import views

urlpatterns = [
    path("", views.task_list, name="task_list"),
    path('apidocumnets',views.apidocumnets,name='apidocumnets')
   
]

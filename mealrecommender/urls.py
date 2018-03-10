from django.urls import include, path
from . import views

urlpatterns = [
    path('', views.get_meal_plan, name='get_meal_plan'),

]
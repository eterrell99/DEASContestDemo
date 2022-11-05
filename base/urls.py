from django.urls import path
from . import views

urlpatterns = [
    path('',views.index.as_view()),
    path('calendar/<int:year>/<int:month>/', views.updateCalendarView.as_view(),name='updateCalendar')





]
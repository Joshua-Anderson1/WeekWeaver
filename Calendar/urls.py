from django.urls import path

from . import views

app_name = "calendar"

urlpatterns = [
    path("calendar/add/", views.CalendarCreateView.as_view(), name='create-calendar'),
    path("calendar/", views.CalendarListView.as_view(), name='calendar-list'),
    path("calendar/<int:pk>/", views.CalendarDetailView.as_view(), name="calendar-detail"),
    path("calendar/<int:pk>/edit/", views.CalendarUpdateView.as_view(), name="update-calendar"),
    path("calendar/<int:pk>/delete/", views.CalendarDeleteView.as_view(), name="delete-calendar")

]

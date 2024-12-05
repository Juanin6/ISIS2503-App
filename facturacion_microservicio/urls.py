from django.urls import path
from .views import AdminDashboard, StudentDashboard

urlpatterns = [
    path('admin/dashboard/', AdminDashboard.as_view(), name='admin_dashboard'),
    path('student/dashboard/', StudentDashboard.as_view(), name='student_dashboard'),
]

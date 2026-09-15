from django.urls import path
from . import views


urlpatterns = [
    path('login/',views.student_login,name='student_login'),
    path("dashboard/",views.student_dashboard,name="student_dashboard"),
    path("forgot-password/",views.forgot_password,name="forgot_password"),
    path("courses/",views.course_search, name="course_search"),
    path("courses/signup/<int:course_id>/",views.signup_course,name="signup_course"),
    path("picked-courses/",views.picked_courses,name="picked_courses"),
    path("profile/",views.student_profile,name="student_profile"),
    path("profile/edit/",views.edit_profile,name="edit_profile"),
    path("change-password/",views.change_password,name="change_password"),
    path("logout/",views.student_logout,name="student_logout"),


]

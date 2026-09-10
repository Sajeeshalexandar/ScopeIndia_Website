from django.urls import path
from . import views

urlpatterns = [
    # path('course',views.course,name='course'),

    # COURSE

    path("", views.course_list, name="course_list"),
    path("add/", views.course_create, name="course_create"),
    path("<int:course_id>/", views.course_detail, name="course_detail"),
    path("<int:course_id>/edit/", views.course_update, name="course_update"),
    path("<int:course_id>/delete/", views.course_delete, name="course_delete"),

    # SYLLABUS

    path("syllabus/", views.syllabus_list, name="syllabus_list"),
    path("syllabus/add/", views.syllabus_create, name="syllabus_create"),
    path("syllabus/<int:syllabus_id>/edit/",views.syllabus_update,name="syllabus_update"),
    path("syllabus/<int:syllabus_id>/delete/",views.syllabus_delete,name="syllabus_delete"),


    path('courseSection/',views.Course_Section,name='courseSection'),
    path('courseDetails/<int:c_id>/',views.Course_Details,name='courseDetails'),

]

from django.shortcuts import render

# Create your views here.


def course(request):

    return render(request, "pages/courses.html")


from django.shortcuts import render, redirect, get_object_or_404

from .models import CourseList, Syllabus
from .forms import CourseForm, SyllabusForm

# =========================================================
# COURSE CRUD
# =========================================================


# READ - All Courses
def course_list(request):

    courses = CourseList.objects.all()

    return render(request, "admin/course_list.html", {"courses": courses})


# READ - Single Course + Syllabus
def course_detail(request, course_id):

    course = get_object_or_404(CourseList, id=course_id)

    syllabus = course.course_syllabus.all()

    return render(
        request, "admin/course_detail.html", {"course": course, "syllabus": syllabus}
    )


# CREATE - Course
def course_create(request):

    if request.method == "POST":

        form = CourseForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("course_list")

    else:

        form = CourseForm()

    return render(
        request, "admin/course_form.html", {"form": form, "title": "Add Course"}
    )


# UPDATE - Course
def course_update(request, course_id):

    course = get_object_or_404(CourseList, id=course_id)

    if request.method == "POST":

        form = CourseForm(request.POST, instance=course)

        if form.is_valid():

            form.save()

            return redirect("course_detail", course_id=course.id)

    else:

        form = CourseForm(instance=course)

    return render(
        request, "admin/course_form.html", {"form": form, "title": "Edit Course"}
    )


# DELETE - Course
def course_delete(request, course_id):

    course = get_object_or_404(CourseList, id=course_id)

    if request.method == "POST":

        course.delete()

        return redirect("course_list")

    return render(request, "admin/course_delete.html", {"course": course})


# =========================================================
# SYLLABUS CRUD
# =========================================================


# READ - All Syllabus
def syllabus_list(request):

    syllabus = Syllabus.objects.all()

    return render(request, "admin/syllabus_list.html", {"syllabus": syllabus})


# CREATE - Syllabus
def syllabus_create(request):

    if request.method == "POST":

        form = SyllabusForm(request.POST)

        if form.is_valid():

            form.save()

            return redirect("syllabus_list")

    else:

        form = SyllabusForm()

    return render(
        request, "admin/syllabus_form.html", {"form": form, "title": "Add Syllabus"}
    )


# UPDATE - Syllabus
def syllabus_update(request, syllabus_id):

    syllabus = get_object_or_404(Syllabus, id=syllabus_id)

    if request.method == "POST":

        form = SyllabusForm(request.POST, instance=syllabus)

        if form.is_valid():

            form.save()

            return redirect("syllabus_list")

    else:

        form = SyllabusForm(instance=syllabus)

    return render(
        request, "admin/syllabus_form.html", {"form": form, "title": "Edit Syllabus"}
    )


# DELETE - Syllabus
def syllabus_delete(request, syllabus_id):

    syllabus = get_object_or_404(Syllabus, id=syllabus_id)

    if request.method == "POST":

        syllabus.delete()

        return redirect("syllabus_list")

    return render(request, "admin/syllabus_delete.html", {"syllabus": syllabus})

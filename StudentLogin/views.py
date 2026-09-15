import random
import string

from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.contrib.auth.decorators import login_required
from Registration.models import StudentRegistration

from django.db.models import Q

from django.shortcuts import render, redirect, get_object_or_404
from .models import StudentAccount, PickedCourse
from Courses.models import CourseList

from .forms import StudentProfileForm

from django.contrib.auth import logout


@login_required(login_url="student_login")
def student_logout(request):

    logout(request)

    return redirect("student_login")

@login_required(login_url="student_login")
def change_password(request):

    if request.method == "POST":

        current_password = request.POST.get("current_password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        user = request.user

        # Check current password
        if not user.check_password(current_password):
            return render(
                request,
                "pages/change_password.html",
                {
                    "error": "Current password is incorrect."
                }
            )

        # Check new passwords
        if new_password != confirm_password:
            return render(
                request,
                "pages/change_password.html",
                {
                    "error": "New passwords do not match."
                }
            )

        # Password length
        if len(new_password) < 8:
            return render(
                request,
                "pages/change_password.html",
                {
                    "error": "Password must contain at least 8 characters."
                }
            )

        # Set new password
        user.set_password(new_password)
        user.save()

        # Logout after password change
        logout(request)

        return render(
            request,
            "pages/change_password.html",
            {
                "success": "Password changed successfully. Please login again."
            }
        )

    return render(
        request,
        "pages/change_password.html"
    )

@login_required(login_url="student_login")
def edit_profile(request):

    student_account = request.user.student_account
    student = student_account.student

    if request.method == "POST":

        form = StudentProfileForm(
            request.POST,
            instance=student
        )

        if form.is_valid():

            form.save()

            return redirect("student_profile")

    else:

        form = StudentProfileForm(
            instance=student
        )

    return render(
        request,
        "pages/edit_profile.html",
        {
            "form": form,
            "student": student
        }
    )

@login_required(login_url="student_login")
def student_profile(request):

    student_account = request.user.student_account
    student = student_account.student

    return render(
        request,
        "pages/profile.html",
        {
            "student": student,
            "student_account": student_account,
        }
    )

@login_required(login_url="student_login")
def picked_courses(request):

    student_account = request.user.student_account

    courses = PickedCourse.objects.filter(
        student=student_account
    ).select_related("course")

    return render(
        request,
        "pages/picked_courses.html",
        {
            "courses": courses
        }
    )

@login_required(login_url="student_login")
def signup_course(request, course_id):

    student_account = request.user.student_account

    course = get_object_or_404(
        CourseList,
        id=course_id
    )

    picked_course, created = PickedCourse.objects.get_or_create(
        student=student_account,
        course=course
    )

    if created:
        message = "Course signed up successfully."
    else:
        message = "You have already signed up for this course."

    return render(
        request,
        "pages/course_signup.html",
        {
            "course": course,
            "message": message,
            "picked_course": picked_course,
        }
    )

@login_required(login_url="student_login")
def course_search(request):

    query = request.GET.get("q", "").strip()

    courses = CourseList.objects.all()

    if query:
        courses = courses.filter(
            Q(course_name__icontains=query) |
            Q(course_description__icontains=query)
        )

    return render(
        request,
        "pages/course_search.html",
        {
            "courses": courses,
            "query": query,
        }
    )


@login_required(login_url="student_login")
def student_dashboard(request):

    student_account = request.user.student_account
    student = student_account.student

    return render(
        request,
        "pages/dashboard.html",
        {
            "student": student,
            "student_account": student_account,
        }
    )

def generate_temp_password(length=8):

    characters = string.ascii_letters + string.digits

    return ''.join(
        random.choice(characters)
        for _ in range(length)
    )


def student_login(request):

    if request.method == "POST":

        email = request.POST.get("email")
        password = request.POST.get("password")
        remember_me = request.POST.get("remember_me")

        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        email = email.strip().lower()

        try:

            student = StudentRegistration.objects.get(
                email=email
            )

            student_account = StudentAccount.objects.get(
                student=student
            )

            user = student_account.user

            # --------------------------------
            # FIRST LOGIN
            # --------------------------------

            if student_account.is_first_login:

                # Send temporary password
                if not password and not new_password:

                    temp_password = generate_temp_password()

                    user.set_password(temp_password)
                    user.save()

                    send_mail(
                        subject="Your Student Login Password",
                        message=f"""
Hello {student.full_name},

Your temporary password is:

{temp_password}

Use this password to continue your first login.

Regards,
Student Portal
""",
                        from_email=None,
                        recipient_list=[student.email],
                    )

                    return render(
                        request,
                        "pages/login.html",
                        {
                            "first_login_password_sent": True,
                            "student": student,
                        }
                    )

                # Verify temporary password
                if password and not new_password:

                    authenticated_user = authenticate(
                        request,
                        username=email,
                        password=password
                    )

                    if authenticated_user is not None:

                        login(request, authenticated_user)

                        if remember_me:

                            # Keep the session for 30 days
                            request.session.set_expiry(60 * 60 * 24 * 30)

                        else:

                            # Session expires when browser is closed
                            request.session.set_expiry(0)

                        return redirect("student_dashboard")

                    else:

                        return render(
                            request,
                            "pages/login.html",
                            {
                                "first_login_password_sent": True,
                                "student": student,
                                "error": "Invalid temporary password."
                            }
                        )

                # Create permanent password
                if new_password:

                    if new_password != confirm_password:

                        return render(
                            request,
                            "pages/login.html",
                            {
                                "new_password_required": True,
                                "student": student,
                                "error": "Passwords do not match."
                            }
                        )

                    if len(new_password) < 8:

                        return render(
                            request,
                            "pages/login.html",
                            {
                                "new_password_required": True,
                                "student": student,
                                "error": "Password must contain at least 8 characters."
                            }
                        )

                    user.set_password(new_password)
                    user.save()

                    student_account.is_first_login = False
                    student_account.save()

                    return render(
                        request,
                        "pages/login.html",
                        {
                            "message": "Password created successfully. You can now login."
                        }
                    )

            # --------------------------------
            # NORMAL LOGIN
            # --------------------------------

            else:

                authenticated_user = authenticate(
                    request,
                    username=email,
                    password=password
                )

                if authenticated_user is not None:

                    # Create Django session
                    login(request, authenticated_user)

                    return redirect("student_dashboard")

                else:

                    return render(
                        request,
                        "pages/login.html",
                        {
                            "show_password": True,
                            "student": student,
                            "error": "Invalid password."
                        }
                    )

        except StudentRegistration.DoesNotExist:

            return render(
                request,
                "pages/login.html",
                {
                    "error": "No student account found with this email."
                }
            )

        except StudentAccount.DoesNotExist:

            return render(
                request,
                "pages/login.html",
                {
                    "error": "Student account is not properly configured."
                }
            )

    return render(
        request,
        "pages/login.html"
    )
def forgot_password(request):

    if request.method == "POST":

        email = request.POST.get("email", "").strip().lower()

        password = request.POST.get("password")
        new_password = request.POST.get("new_password")
        confirm_password = request.POST.get("confirm_password")

        try:

            student = StudentRegistration.objects.get(
                email=email
            )

            student_account = StudentAccount.objects.get(
                student=student
            )

            user = student_account.user

            # --------------------------------
            # STEP 1: SEND TEMPORARY PASSWORD
            # --------------------------------

            if not password and not new_password:

                temp_password = generate_temp_password()

                user.set_password(temp_password)
                user.save()

                send_mail(
                    subject="Password Reset - Student Portal",
                    message=f"""
Hello {student.full_name},

Your temporary password for resetting your account is:

{temp_password}

Use this password to continue resetting your password.

Regards,
Student Portal
""",
                    from_email=None,
                    recipient_list=[student.email],
                )

                return render(
                    request,
                    "pages/forgot_password.html",
                    {
                        "password_sent": True,
                        "student": student,
                    }
                )

            # --------------------------------
            # STEP 2: VERIFY TEMPORARY PASSWORD
            # --------------------------------

            if password and not new_password:

                authenticated_user = authenticate(
                    request,
                    username=email,
                    password=password
                )

                if authenticated_user is not None:

                    return render(
                        request,
                        "pages/forgot_password.html",
                        {
                            "new_password_required": True,
                            "student": student,
                        }
                    )

                else:

                    return render(
                        request,
                        "pages/forgot_password.html",
                        {
                            "password_sent": True,
                            "student": student,
                            "error": "Invalid temporary password."
                        }
                    )

            # --------------------------------
            # STEP 3: CREATE NEW PASSWORD
            # --------------------------------

            if new_password:

                if new_password != confirm_password:

                    return render(
                        request,
                        "pages/forgot_password.html",
                        {
                            "new_password_required": True,
                            "student": student,
                            "error": "Passwords do not match."
                        }
                    )

                if len(new_password) < 8:

                    return render(
                        request,
                        "pages/forgot_password.html",
                        {
                            "new_password_required": True,
                            "student": student,
                            "error": "Password must contain at least 8 characters."
                        }
                    )

                user.set_password(new_password)
                user.save()

                # Make sure the account is now a normal-login account
                student_account.is_first_login = False
                student_account.save()

                return render(
                    request,
                    "pages/forgot_password.html",
                    {
                        "success": "Password reset successfully. You can now login."
                    }
                )

        except StudentRegistration.DoesNotExist:

            return render(
                request,
                "pages/forgot_password.html",
                {
                    "error": "No student account found with this email."
                }
            )

        except StudentAccount.DoesNotExist:

            return render(
                request,
                "pages/forgot_password.html",
                {
                    "error": "Student account is not properly configured."
                }
            )

    return render(
        request,
        "pages/forgot_password.html"
    )
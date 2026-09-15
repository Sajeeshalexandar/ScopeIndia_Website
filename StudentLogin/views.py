import random
import string
import secrets

from django.contrib.auth import authenticate, login
from django.core.mail import send_mail
from django.core.exceptions import ObjectDoesNotExist
from django.contrib.auth.decorators import login_required
from Registration.models import StudentRegistration

from django.db.models import Q

from django.shortcuts import render, redirect, get_object_or_404
from .models import StudentAccount, PickedCourse
from Courses.models import CourseList

from .forms import StudentProfileForm

from django.contrib.auth import logout


# ---------------------------------------------------------------------------
# UTILITIES
# ---------------------------------------------------------------------------

def generate_temp_password(length=10):
    """Generate a secure random temporary password."""
    alphabet = string.ascii_letters + string.digits + "!@#$"
    # Ensure at least one digit and one letter
    password = (
        random.choice(string.ascii_uppercase)
        + random.choice(string.ascii_lowercase)
        + random.choice(string.digits)
        + ''.join(random.choice(alphabet) for _ in range(length - 3))
    )
    return ''.join(random.sample(password, len(password)))


def _send_temp_password_email(student, temp_password, subject_prefix="Login"):
    """Send a branded temporary password email. Returns (success, error_msg)."""
    subject = f"Your Temporary Password — Scope India Student Portal"
    if subject_prefix == "Reset":
        subject = f"Password Reset — Scope India Student Portal"

    message = f"""Hello {student.full_name},

{'You have requested a password reset for your Scope India Student Portal account.' if subject_prefix == 'Reset' else 'Welcome to Scope India Student Portal! To complete your first login, a temporary password has been generated for you.'}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
  Temporary Password: {temp_password}
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

This password is valid for your current session only. You will be asked to set a new permanent password after verifying this temporary password.

If you did not request this, please ignore this email or contact support.

Regards,
Scope India Student Portal
https://www.scopeindia.com
"""
    try:
        send_mail(
            subject=subject,
            message=message,
            from_email=None,           # uses DEFAULT_FROM_EMAIL from settings
            recipient_list=[student.email],
            fail_silently=False,
        )
        return True, None
    except Exception as e:
        return False, str(e)


# ---------------------------------------------------------------------------
# STUDENT LOGIN
# ---------------------------------------------------------------------------

def student_login(request):
    """
    Multi-step login flow:

    Step 0 (GET / initial POST):
        - User enters email → submit
        - If first_login: send temp password → go to Step 1a
        - If normal login: show password field → go to Step 1b

    Step 1a (first login — verify temp password):
        - User enters temp password → submit
        - If correct: show "set new password" form → go to Step 2

    Step 2 (first login — set permanent password):
        - User sets new password → mark is_first_login=False → redirect to login

    Step 1b (normal login — enter password):
        - User enters password → if correct: login → redirect to dashboard
    """

    # If already logged in, go straight to dashboard
    if request.user.is_authenticated:
        try:
            _ = request.user.student_account
            return redirect("student_dashboard")
        except ObjectDoesNotExist:
            pass

    if request.method != "POST":
        return render(request, "pages/login.html")

    email = request.POST.get("email", "").strip().lower()
    password = request.POST.get("password", "")
    new_password = request.POST.get("new_password", "")
    confirm_password = request.POST.get("confirm_password", "")
    remember_me = request.POST.get("remember_me")
    login_step = request.POST.get("login_step", "")  # hidden field for state

    # --- Look up student ---
    try:
        student = StudentRegistration.objects.get(email=email)
        student_account = StudentAccount.objects.get(student=student)
        user = student_account.user
    except StudentRegistration.DoesNotExist:
        return render(request, "pages/login.html", {
            "error": "No student account found with this email.",
            "email": email,
        })
    except StudentAccount.DoesNotExist:
        return render(request, "pages/login.html", {
            "error": "Student account is not properly configured. Please contact support.",
            "email": email,
        })

    # -----------------------------------------------------------------------
    # FIRST LOGIN FLOW
    # -----------------------------------------------------------------------
    if student_account.is_first_login:

        # Step 0 → send temp password
        if login_step == "" or login_step == "email_submitted":
            temp_password = generate_temp_password()
            user.set_password(temp_password)
            user.save()

            success, err = _send_temp_password_email(student, temp_password, "Login")

            if not success:
                return render(request, "pages/login.html", {
                    "error": f"Could not send email: {err}. Please contact support.",
                    "email": email,
                })

            return render(request, "pages/login.html", {
                "first_login_step": "temp_password_sent",
                "student": student,
                "info": f"A temporary password has been sent to {student.email}. Please check your inbox.",
            })

        # Step 1a → verify temp password
        if login_step == "temp_password_sent":
            if not password:
                return render(request, "pages/login.html", {
                    "first_login_step": "temp_password_sent",
                    "student": student,
                    "error": "Please enter the temporary password.",
                })

            authenticated_user = authenticate(request, username=email, password=password)

            if authenticated_user is None:
                return render(request, "pages/login.html", {
                    "first_login_step": "temp_password_sent",
                    "student": student,
                    "error": "Incorrect temporary password. Please try again.",
                })

            # Temp password verified — now ask for a permanent password
            # Store flag in session so Step 2 can't be bypassed
            request.session["first_login_verified_email"] = email
            return render(request, "pages/login.html", {
                "first_login_step": "set_new_password",
                "student": student,
                "info": "Temporary password verified! Now set your permanent password.",
            })

        # Step 2 → set permanent password
        if login_step == "set_new_password":
            # Verify session token (prevent bypass)
            verified_email = request.session.get("first_login_verified_email")
            if verified_email != email:
                return render(request, "pages/login.html", {
                    "error": "Session expired. Please start again.",
                })

            if not new_password:
                return render(request, "pages/login.html", {
                    "first_login_step": "set_new_password",
                    "student": student,
                    "error": "Please enter a new password.",
                })

            if new_password != confirm_password:
                return render(request, "pages/login.html", {
                    "first_login_step": "set_new_password",
                    "student": student,
                    "error": "Passwords do not match.",
                })

            if len(new_password) < 8:
                return render(request, "pages/login.html", {
                    "first_login_step": "set_new_password",
                    "student": student,
                    "error": "Password must be at least 8 characters long.",
                })

            user.set_password(new_password)
            user.save()

            student_account.is_first_login = False
            student_account.save()

            # Clear session token
            request.session.pop("first_login_verified_email", None)

            return render(request, "pages/login.html", {
                "success": "Password created successfully! You can now log in with your new password.",
            })

    # -----------------------------------------------------------------------
    # NORMAL LOGIN FLOW
    # -----------------------------------------------------------------------
    else:

        # Step 0 — email submitted, show password field
        if login_step == "" or login_step == "email_submitted":
            return render(request, "pages/login.html", {
                "show_password": True,
                "student": student,
                "email": email,
            })

        # Step 1b — password submitted, authenticate
        if login_step == "password_submitted":
            if not password:
                return render(request, "pages/login.html", {
                    "show_password": True,
                    "student": student,
                    "email": email,
                    "error": "Please enter your password.",
                })

            authenticated_user = authenticate(request, username=email, password=password)

            if authenticated_user is None:
                return render(request, "pages/login.html", {
                    "show_password": True,
                    "student": student,
                    "email": email,
                    "error": "Incorrect password. Please try again.",
                })

            login(request, authenticated_user)

            if remember_me:
                # Keep session for 30 days
                request.session.set_expiry(60 * 60 * 24 * 30)
            else:
                # Session expires when browser closes
                request.session.set_expiry(0)

            return redirect("student_dashboard")

    return render(request, "pages/login.html")


# ---------------------------------------------------------------------------
# FORGOT PASSWORD
# ---------------------------------------------------------------------------

def forgot_password(request):
    """
    3-step password reset:
    Step 1: Enter email → send temp password
    Step 2: Verify temp password (stored in session so Step 3 can't be bypassed)
    Step 3: Set new permanent password
    """

    if request.method != "POST":
        return render(request, "pages/forgot_password.html")

    email = request.POST.get("email", "").strip().lower()
    password = request.POST.get("password", "")
    new_password = request.POST.get("new_password", "")
    confirm_password = request.POST.get("confirm_password", "")
    reset_step = request.POST.get("reset_step", "")

    # --- Look up student ---
    try:
        student = StudentRegistration.objects.get(email=email)
        student_account = StudentAccount.objects.get(student=student)
        user = student_account.user
    except StudentRegistration.DoesNotExist:
        return render(request, "pages/forgot_password.html", {
            "error": "No student account found with this email.",
        })
    except StudentAccount.DoesNotExist:
        return render(request, "pages/forgot_password.html", {
            "error": "Student account is not properly configured. Please contact support.",
        })

    # -----------------------------------------------------------------------
    # STEP 1: Send temporary password
    # -----------------------------------------------------------------------
    if reset_step == "" or reset_step == "email_submitted":
        temp_password = generate_temp_password()
        user.set_password(temp_password)
        user.save()

        success, err = _send_temp_password_email(student, temp_password, "Reset")

        if not success:
            return render(request, "pages/forgot_password.html", {
                "error": f"Could not send email: {err}. Please contact support.",
            })

        # Clear any previous reset token
        request.session.pop("password_reset_verified_email", None)

        return render(request, "pages/forgot_password.html", {
            "reset_step": "temp_password_sent",
            "student": student,
        })

    # -----------------------------------------------------------------------
    # STEP 2: Verify temporary password
    # -----------------------------------------------------------------------
    if reset_step == "temp_password_sent":
        if not password:
            return render(request, "pages/forgot_password.html", {
                "reset_step": "temp_password_sent",
                "student": student,
                "error": "Please enter the temporary password.",
            })

        authenticated_user = authenticate(request, username=email, password=password)

        if authenticated_user is None:
            return render(request, "pages/forgot_password.html", {
                "reset_step": "temp_password_sent",
                "student": student,
                "error": "Incorrect temporary password. Please try again.",
            })

        # Mark Step 2 as complete via session token
        request.session["password_reset_verified_email"] = email

        return render(request, "pages/forgot_password.html", {
            "reset_step": "set_new_password",
            "student": student,
        })

    # -----------------------------------------------------------------------
    # STEP 3: Set new password (requires session token from Step 2)
    # -----------------------------------------------------------------------
    if reset_step == "set_new_password":
        verified_email = request.session.get("password_reset_verified_email")

        if verified_email != email:
            return render(request, "pages/forgot_password.html", {
                "error": "Session expired or invalid. Please start the password reset again.",
            })

        if not new_password:
            return render(request, "pages/forgot_password.html", {
                "reset_step": "set_new_password",
                "student": student,
                "error": "Please enter a new password.",
            })

        if new_password != confirm_password:
            return render(request, "pages/forgot_password.html", {
                "reset_step": "set_new_password",
                "student": student,
                "error": "Passwords do not match.",
            })

        if len(new_password) < 8:
            return render(request, "pages/forgot_password.html", {
                "reset_step": "set_new_password",
                "student": student,
                "error": "Password must be at least 8 characters long.",
            })

        user.set_password(new_password)
        user.save()

        student_account.is_first_login = False
        student_account.save()

        # Clear session token
        request.session.pop("password_reset_verified_email", None)

        return render(request, "pages/forgot_password.html", {
            "success": "Your password has been reset successfully! You can now log in.",
        })

    return render(request, "pages/forgot_password.html")


# ---------------------------------------------------------------------------
# LOGOUT
# ---------------------------------------------------------------------------

@login_required(login_url="student_login")
def student_logout(request):
    logout(request)
    return redirect("student_login")


# ---------------------------------------------------------------------------
# CHANGE PASSWORD
# ---------------------------------------------------------------------------

@login_required(login_url="student_login")
def change_password(request):

    if request.method == "POST":
        current_password = request.POST.get("current_password", "")
        new_password = request.POST.get("new_password", "")
        confirm_password = request.POST.get("confirm_password", "")
        user = request.user

        if not user.check_password(current_password):
            return render(request, "pages/change_password.html", {
                "error": "Current password is incorrect.",
            })

        if new_password != confirm_password:
            return render(request, "pages/change_password.html", {
                "error": "New passwords do not match.",
            })

        if len(new_password) < 8:
            return render(request, "pages/change_password.html", {
                "error": "Password must be at least 8 characters long.",
            })

        if user.check_password(new_password):
            return render(request, "pages/change_password.html", {
                "error": "New password must be different from your current password.",
            })

        user.set_password(new_password)
        user.save()

        logout(request)

        return render(request, "pages/change_password.html", {
            "success": "Password changed successfully. Please log in with your new password.",
        })

    return render(request, "pages/change_password.html")


# ---------------------------------------------------------------------------
# EDIT PROFILE
# ---------------------------------------------------------------------------

@login_required(login_url="student_login")
def edit_profile(request):
    student_account = request.user.student_account
    student = student_account.student

    if request.method == "POST":
        form = StudentProfileForm(request.POST, instance=student)
        if form.is_valid():
            form.save()
            return redirect("student_profile")
    else:
        form = StudentProfileForm(instance=student)

    return render(request, "pages/edit_profile.html", {
        "form": form,
        "student": student,
    })


# ---------------------------------------------------------------------------
# STUDENT PROFILE
# ---------------------------------------------------------------------------

@login_required(login_url="student_login")
def student_profile(request):
    student_account = request.user.student_account
    student = student_account.student

    return render(request, "pages/profile.html", {
        "student": student,
        "student_account": student_account,
    })


# ---------------------------------------------------------------------------
# PICKED COURSES
# ---------------------------------------------------------------------------

@login_required(login_url="student_login")
def picked_courses(request):
    student_account = request.user.student_account
    courses = PickedCourse.objects.filter(
        student=student_account
    ).select_related("course")

    return render(request, "pages/picked_courses.html", {
        "courses": courses,
    })


# ---------------------------------------------------------------------------
# COURSE SIGNUP
# ---------------------------------------------------------------------------

@login_required(login_url="student_login")
def signup_course(request, course_id):
    student_account = request.user.student_account
    course = get_object_or_404(CourseList, id=course_id)

    picked_course, created = PickedCourse.objects.get_or_create(
        student=student_account,
        course=course,
    )

    if created:
        message = "Course signed up successfully."
    else:
        message = "You have already signed up for this course."

    return render(request, "pages/course_signup.html", {
        "course": course,
        "message": message,
        "picked_course": picked_course,
    })


# ---------------------------------------------------------------------------
# COURSE SEARCH
# ---------------------------------------------------------------------------

@login_required(login_url="student_login")
def course_search(request):
    query = request.GET.get("q", "").strip()
    courses = CourseList.objects.all()

    if query:
        courses = courses.filter(
            Q(course_name__icontains=query) |
            Q(course_description__icontains=query)
        )

    return render(request, "pages/course_search.html", {
        "courses": courses,
        "query": query,
    })


# ---------------------------------------------------------------------------
# STUDENT DASHBOARD
# ---------------------------------------------------------------------------

@login_required(login_url="student_login")
def student_dashboard(request):
    student_account = request.user.student_account
    student = student_account.student

    picked_count = PickedCourse.objects.filter(student=student_account).count()

    return render(request, "pages/dashboard.html", {
        "student": student,
        "student_account": student_account,
        "picked_count": picked_count,
    })
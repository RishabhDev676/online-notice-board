from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.core.mail import send_mail

from notices.models import Notice, Category, Department
from subscriptions.models import EmailSubscription
from django.utils.text import slugify
from django.contrib.auth.models import User
from django.contrib import messages

from .models import AdminProfile


def admin_register(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")

        # Password match check
        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect('admin_register')

        # Username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken")
            return redirect('admin_register')

        # Create admin user, but will be staff before approval
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )

        user.is_staff = True
        user.save()

        AdminProfile.objects.create(
            user=user,
            is_approved=False
        )

        messages.success(request,
            "Registration successful! Your account is pending approval by Super Admin. You can login once approved."
        )
        return redirect('admin_login')


    return render(request, "admin/register.html")

#################### NOTICE MANAGEMENT ####################

@login_required
def notice_list(request):
    notices = Notice.objects.all().order_by('-created_at')
    return render(request, 'admin/notices/notice_list.html', {
        'notices': notices
    })


@login_required
def notice_add(request):
    categories = Category.objects.all()
    departments = Department.objects.all()

    if request.method == "POST":

        is_published = bool(request.POST.get("is_published"))

        notice = Notice.objects.create(
            title=request.POST.get("title"),
            description=request.POST.get("description"),
            category_id=request.POST.get("category"),
            department_id=request.POST.get("department") or None,
            file=request.FILES.get("file"),
            is_published=is_published,
            published_at=timezone.now() if is_published else None,
        )

        # SEND EMAIL IF NEW NOTICE IS PUBLISHED
        if is_published:
            emails = list(
                EmailSubscription.objects
                .filter(is_active=True)
                .values_list('email', flat=True)
            )

            if emails:
                send_mail(
                    subject=f"New Notice Published: {notice.title}",
                    message=(
                        f"A new notice '{notice.title}' has been published.\n\n"
                        f"Visit the notice board to view details."
                    ),
                    from_email=None,
                    recipient_list=emails,
                    fail_silently=False,
                )

        return redirect('admin_notice_list')

    return render(request, 'admin/notices/notice_form.html', {
        'categories': categories,
        'departments': departments
    })


@login_required
def notice_edit(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    categories = Category.objects.all()
    departments = Department.objects.all()

    if request.method == "POST":

        old_publish_status = notice.is_published

        notice.title = request.POST.get("title")
        notice.description = request.POST.get("description")
        notice.category_id = request.POST.get("category")
        notice.department_id = request.POST.get("department") or None

        if request.FILES.get("file"):
            notice.file = request.FILES.get("file")


        is_published = bool(request.POST.get("is_published"))

        # Detect first publish
        first_publish = is_published and not old_publish_status

        if first_publish:
            notice.published_at = timezone.now()

        notice.is_published = is_published

        # Update Logic
        send_email = False
        email_subject = ""
        email_message = ""

        if first_publish:
            send_email = True
            email_subject = f"New Notice Published: {notice.title}"
            email_message = (
                f"A new notice '{notice.title}' has been published.\n\n"
                f"Please visit the notice board to view details."
            )

        if request.POST.get("major_update"):
            notice.updated_at = timezone.now()
            notice.show_updated_badge = True
            notice.send_update_email = True

            send_email = True
            email_subject = f"Updated Notice: {notice.title}"
            email_message = (
                f"The notice '{notice.title}' has been updated.\n\n"
                f"Please visit the notice board to view the latest details."
            )
        else:
            notice.show_updated_badge = False
            notice.send_update_email = False

        # Send Email
        if send_email:
            emails = list(
                EmailSubscription.objects
                .filter(is_active=True)
                .values_list('email', flat=True)
            )

            if emails:
                send_mail(
                    subject=email_subject,
                    message=email_message,
                    from_email=None,
                    recipient_list=emails,
                    fail_silently=False,
                )

        notice.save()
        return redirect('admin_notice_list')

    return render(request, 'admin/notices/notice_edit.html', {
        'notice': notice,
        'categories': categories,
        'departments': departments
    })


@login_required
def notice_delete(request, pk):
    notice = get_object_or_404(Notice, pk=pk)
    notice.delete()
    return redirect('admin_notice_list')


#################### CATEGORY MANAGEMENT ####################

@login_required
def category_list(request):
    categories = Category.objects.all()
    return render(request, 'admin/categories/category_list.html', {
        'categories': categories
    })


@login_required
def category_add(request):
    if request.method == "POST":
        name = request.POST.get("name")

        Category.objects.create(
            name=name,
            slug=slugify(name)
        )

        return redirect('admin_category_list')

    return render(request, 'admin/categories/category_form.html')



@login_required
def category_delete(request, pk):
    category = get_object_or_404(Category, pk=pk)
    category.delete()
    return redirect('admin_category_list')


@login_required
def category_edit(request, pk):
    category = get_object_or_404(Category, pk=pk)

    if request.method == "POST":
        name = request.POST.get("name")

        category.name = name
        category.slug = slugify(name)
        category.save()

        return redirect('admin_category_list')

    return render(request, 'admin/categories/category_form.html', {
        'category': category
    })


#################### DEPARTMENT MANAGEMENT ####################

@login_required
def department_list(request):
    departments = Department.objects.all()
    return render(request, 'admin/departments/department_list.html', {
        'departments': departments
    })


@login_required
def department_add(request):
    if request.method == "POST":
        name = request.POST.get("name")

        Department.objects.create(
            name=name,
            slug=slugify(name)
        )

        return redirect('admin_department_list')

    return render(request, 'admin/departments/department_form.html')



@login_required
def department_delete(request, pk):
    department = get_object_or_404(Department, pk=pk)
    department.delete()
    return redirect('admin_department_list')


@login_required
def department_edit(request, pk):
    department = get_object_or_404(Department, pk=pk)

    if request.method == "POST":
        name = request.POST.get("name")

        department.name = name
        department.slug = slugify(name)
        department.save()

        return redirect('admin_department_list')

    return render(request, 'admin/departments/department_form.html', {
        'department': department
    })



#################### SUBSCRIPTION MANAGEMENT ####################

@login_required
def subscription_list(request):
    subscriptions = EmailSubscription.objects.all()
    return render(request, 'admin/subscriptions/subscription_list.html', {
        'subscriptions': subscriptions
    })


@login_required
def subscription_delete(request, pk):
    sub = get_object_or_404(EmailSubscription, pk=pk)
    sub.delete()
    return redirect('admin_subscription_list')


#################### ADMIN AUTH ####################

def admin_login(request):
    error_message = ""

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)

        if user is not None and user.is_staff:
            try:
                if not user.adminprofile.is_approved:
                    error_message = "Admin account pending approval"
                    return render(request, "admin/login.html", {
                        "error_message": error_message
                    })
            except:
                pass

            login(request, user)
            return redirect('admin_dashboard')

        else:
            error_message = "Invalid credentials or not an admin user"

    return render(request, "admin/login.html", {
        "error_message": error_message
    })


@login_required
def pending_admins(request):

    if not request.user.is_superuser:
        messages.error(request, "Access Denied: Only Super Admin can view pending approvals.")
        return redirect('admin_dashboard')

    pending = AdminProfile.objects.filter(is_approved=False)

    return render(request, "admin/pending_admins.html", {
        "pending_admins": pending
    })



@login_required
def approve_admin(request, pk):

    if not request.user.is_superuser:
        messages.error(request, "Access Denied.")
        return redirect('admin_dashboard')

    profile = get_object_or_404(AdminProfile, pk=pk)
    profile.is_approved = True
    profile.save()

    messages.success(request, "Admin approved successfully.")
    return redirect('admin_pending_admins')


@login_required
def admin_list(request):

    if not request.user.is_superuser:
        messages.error(request, "Access Denied: Only Super Admin can manage admins.")
        return redirect('admin_dashboard')

    admins = AdminProfile.objects.filter(is_approved=True)

    return render(request, "admin/admin_list.html", {
        "admins": admins
    })


@login_required
def remove_admin(request, pk):

    if not request.user.is_superuser:
        messages.error(request, "Access Denied.")
        return redirect('admin_dashboard')

    profile = get_object_or_404(AdminProfile, pk=pk)

    if profile.user == request.user:
        messages.error(request, "You cannot remove yourself.")
        return redirect('admin_admin_list')

    if profile.user.is_superuser:
        messages.error(request, "Cannot remove another Super Admin.")
        return redirect('admin_admin_list')

    profile.user.delete()

    messages.success(request, "Admin removed successfully.")
    return redirect('admin_admin_list')



@login_required
def dashboard(request):
    return render(request, "admin/dashboard_home.html", {
        "total_notices": Notice.objects.count(),
        "published_notices": Notice.objects.filter(is_published=True).count(),
        "unpublished_notices": Notice.objects.filter(is_published=False).count(),
        "total_subscribers": EmailSubscription.objects.filter(is_active=True).count(),
    })


@login_required
def admin_logout(request):
    logout(request)
    return redirect('admin_login')

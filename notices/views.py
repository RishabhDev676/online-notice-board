from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Notice, Category, Department


# -------------------------
# HOME PAGE – ALL NOTICES
# -------------------------
def home(request):

    notices = Notice.objects.filter(
        is_published=True,
        published_at__lte=timezone.now()
    )

    year = request.GET.get("year")
    month = request.GET.get("month")
    sort = request.GET.get("sort")

    # YEAR FILTER
    if year and year != "all":
        notices = notices.filter(published_at__year=year)

    # MONTH FILTER
    if month and month != "all":
        notices = notices.filter(published_at__month=month)

    # SORTING
    if sort == "oldest":
        notices = notices.order_by("published_at")
    else:
        notices = notices.order_by("-published_at")  # default newest

    return render(request, "public/home.html", {
        "notices": notices,
        "selected_year": year,
        "selected_month": month,
        "selected_sort": sort,
    })


# -------------------------
# CATEGORY LIST PAGE
# -------------------------
def categories(request):
    categories = Category.objects.all().order_by('name')

    return render(request, 'public/categories.html', {
        'categories': categories
    })


# -------------------------
# CATEGORY-WISE NOTICES
# -------------------------
def category_notices(request, slug):
    category = get_object_or_404(Category, slug=slug)

    notices = Notice.objects.filter(
        is_published=True,
        category=category,
        published_at__lte=timezone.now()
    ).order_by('-published_at')

    return render(request, 'public/category_notices.html', {
        'category': category,
        'notices': notices
    })


# -------------------------
# DEPARTMENT LIST PAGE
# -------------------------
def departments(request):
    departments = Department.objects.all().order_by('name')

    return render(request, 'public/departments.html', {
        'departments': departments
    })


# -------------------------
# DEPARTMENT-WISE NOTICES
# -------------------------
def department_notices(request, slug):
    department = get_object_or_404(Department, slug=slug)

    notices = Notice.objects.filter(
        is_published=True,
        department=department,
        published_at__lte=timezone.now()
    ).order_by('-published_at')

    return render(request, 'public/department_notices.html', {
        'department': department,
        'notices': notices
    })

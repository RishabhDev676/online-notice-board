from django.shortcuts import render, redirect
from django.contrib import messages

from .models import EmailSubscription
from notices.models import Category, Department


def subscribe(request):
    """
    Handles email subscription form submission
    """

    if request.method == "POST":
        email = request.POST.get("email")
        category_ids = request.POST.getlist("categories")
        department_ids = request.POST.getlist("departments")

        if not email:
            messages.error(request, "Email is required")
            return redirect("subscribe")

        subscription, created = EmailSubscription.objects.get_or_create(
            email=email
        )

        # Clear old selections
        subscription.categories.clear()
        subscription.departments.clear()

        # Add selected categories
        if category_ids:
            subscription.categories.add(*Category.objects.filter(id__in=category_ids))

        # Add selected departments
        if department_ids:
            subscription.departments.add(*Department.objects.filter(id__in=department_ids))

        subscription.is_active = True
        subscription.save()

        messages.success(request, "Subscription saved successfully!")
        messages.success(request, "You have subscribed successfully!")
        return redirect("home")


    # GET request → show subscription form
    categories = Category.objects.all()
    departments = Department.objects.all()

    return render(request, "public/subscribe.html", {
        "categories": categories,
        "departments": departments
    })

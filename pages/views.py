from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db.models import Q
from course.models import Course


def get_all_user_courses(user):
    courses = Course.objects.filter(Q(owners__in=[user]) | Q(teachers__in=[user]) | Q(students__in=[user]) | Q(observers__in=[user]) | Q(user_query__in=[user])).distinct().all()

    return courses

def index(request):
    context = {}
    if request.user.is_authenticated:
        context["courses"] = get_all_user_courses(request.user)
    
    return render(request, "pages/index.html", context)
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.urls import reverse
from django.db.models import Q
from .models import Course, Task, Solution, File, Link
from account.models import User

def check_admin_course(user, course_uuid, context):
    try:
        course = Course.objects.get(pk=course_uuid)
    except Course.DoesNotExist:
        return True, redirect(reverse("courses"), context)
    
    if not user in course.owners.all() and not user.is_superuser:
        return True, redirect(reverse("course", kwargs={"course_uuid": course_uuid}), context)

    return False, course

def check_admin_course_user(user, course_uuid, user_uuid, context):
    try:
        course = Course.objects.get(pk=course_uuid)
    except Course.DoesNotExist:
        return True, redirect(reverse("courses"), context), None
    
    if not user in course.owners.all() and not user.is_superuser:
        return True, redirect(reverse("course", kwargs={"course_uuid": course_uuid}), context), None

    try:
        user = User.objects.get(pk=user_uuid)
    except Course.DoesNotExist:
        return True, redirect(reverse("admin-course", kwargs={"course_uuid": course_uuid}), context), None

    return False, course, user

def get_all_user_courses(user):
    courses = Course.objects.filter(Q(owners__in=[user]) | Q(teachers__in=[user]) | Q(students__in=[user]) | Q(observers__in=[user]) | Q(user_query__in=[user])).distinct().all()

    return courses

def delete_user_from_course(course, user):
    if user in course.owners.all():
        course.owners.remove(user)
        
    if user in course.teachers.all():
        course.teachers.remove(user)
        
    if user in course.students.all():
        course.students.remove(user)
        
    if user in course.observers.all():
        course.observers.remove(user)
        
    if user in course.user_query.all():
        course.user_query.remove(user)
    
    course.save()
    return

def search(request):
    context = {}
    courses = get_all_user_courses(request.user)
    context["courses"] = courses
    
    if request.method == "POST":
        course = request.POST.get("course", context)
    
    return redirect(reverse("home"), context)

def course(request, course_uuid):
    context = {}
    courses = get_all_user_courses(request.user)
    context["courses"] = courses
    
    try:
        course = Course.objects.get(pk=course_uuid)
        context["course"] = course
        
        return render(request, "course/course.html", context)
    except ValidationError:
        return redirect(reverse("courses"), context)
    except Course.DoesNotExist:
        return redirect(reverse("courses"), context)

@login_required()
def admin_course(request, course_uuid):
    context = {}
    courses = get_all_user_courses(request.user)
    context["courses"] = courses
    
    error, first = check_admin_course(request.user, course_uuid, context)
    if error:
        return first
    course = first
    context["course"] = course
    
    members = {}
    members["owners"] = course.owners.all()
    members["teachers"] = course.teachers.all()
    members["students"] = course.students.all()
    members["observers"] = course.observers.all()
    context["members"] = members
    
    user_query = course.user_query.all()
    context["user_query"] = user_query
    
    return render(request, "course/admin-course.html", context)

@login_required()
def change_name_course(request, course_uuid):
    context = {}
    courses = get_all_user_courses(request.user)
    context["courses"] = courses
    
    error, first = check_admin_course(request.user, course_uuid, context)  
    if error:
        return first
    course = first
    
    if request.method == "POST":
        name = request.POST.get("name")
        
        if name is None:
            return redirect(reverse("admin-course", kwargs={"course_uuid": course_uuid}), context)
        
        course.name = name
        course.save()
    
    return redirect(reverse("admin-course", kwargs={"course_uuid": course_uuid}), context)

@login_required()
def change_description_course(request, course_uuid):
    context = {}
    courses = get_all_user_courses(request.user)
    context["courses"] = courses
    
    error, first = check_admin_course(request.user, course_uuid, context)  
    if error:
        return first
    course = first
    
    if request.method == "POST":
        description = request.POST.get("description")
        
        if description is None:
            return redirect(reverse("admin-course", kwargs={"course_uuid": course_uuid}), context)
        
        course.description = description
        course.save()
    
    return redirect(reverse("admin-course", kwargs={"course_uuid": course_uuid}), context)

@login_required()
def accept_user(request, course_uuid, user_uuid):
    context = {}
    courses = get_all_user_courses(request.user)
    context["courses"] = courses

    error, first, second = check_admin_course_user(request.user, course_uuid, user_uuid, context)  
    if error:
        return first
    course, user = first, second
    
    delete_user_from_course(course, user)
    course.students.add(user)
    course.save()
    
    return redirect(reverse("admin-course", kwargs={"course_uuid": course_uuid}), context)

@login_required()
def reject_user(request, course_uuid, user_uuid):
    context = {}
    courses = get_all_user_courses(request.user)
    context["courses"] = courses
    
    error, first, second = check_admin_course_user(request.user, course_uuid, user_uuid, context)  
    if error:
        return first
    course, user = first, second
    
    delete_user_from_course(course, user)   
    return redirect(reverse("admin-course", kwargs={"course_uuid": course_uuid}), context)

@login_required()
def add_user_to_owners(request, course_uuid, user_uuid):
    context = {}
    courses = get_all_user_courses(request.user)
    context["courses"] = courses
    
    error, first, second = check_admin_course_user(request.user, course_uuid, user_uuid, context)  
    if error:
        return first
    course, user = first, second
    
    delete_user_from_course(course, user)
    course.owners.add(user)
    course.save()
    
    return redirect(reverse("admin-course", kwargs={"course_uuid": course_uuid}), context)

@login_required()
def add_user_to_teachers(request, course_uuid, user_uuid):
    context = {}
    courses = get_all_user_courses(request.user)
    context["courses"] = courses
    
    error, first, second = check_admin_course_user(request.user, course_uuid, user_uuid, context)  
    if error:
        return first
    course, user = first, second
    
    delete_user_from_course(course, user)
    course.teachers.add(user)
    course.save()

    return redirect(reverse("admin-course", kwargs={"course_uuid": course_uuid}), context)

@login_required()
def add_user_to_students(request, course_uuid, user_uuid):
    context = {}
    courses = get_all_user_courses(request.user)
    context["courses"] = courses
    
    error, first, second = check_admin_course_user(request.user, course_uuid, user_uuid, context)  
    if error:
        return first
    course, user = first, second
    
    delete_user_from_course(course, user)
    course.students.add(user)
    course.save()
    
    return redirect(reverse("admin-course", kwargs={"course_uuid": course_uuid}), context)

@login_required()
def add_user_to_observers(request, course_uuid, user_uuid):
    context = {}
    courses = get_all_user_courses(request.user)
    context["courses"] = courses
    
    error, first, second = check_admin_course_user(request.user, course_uuid, user_uuid, context)  
    if error:
        return first
    course, user = first, second

    delete_user_from_course(course, user)
    course.observers.add(user)
    course.save()

    return redirect(reverse("admin-course", kwargs={"course_uuid": course_uuid}), context)

@login_required()
def delete_user_from_course_view(request, course_uuid, user_uuid):
    context = {}
    courses = get_all_user_courses(request.user)
    context["courses"] = courses
    
    error, first, second = check_admin_course_user(request.user, course_uuid, user_uuid, context)  
    if error:
        return first
    course, user = first, second

    delete_user_from_course(course, user)
    return redirect(reverse("admin-course", kwargs={"course_uuid": course_uuid}), context)

@login_required()
def courses(request):
    context = {}
    courses = get_all_user_courses(request.user)
    context["courses"] = courses
    
    return render(request, "course/courses.html", context)

@login_required()
def create_course(request):
    context = {}
    courses = get_all_user_courses(request.user)
    context["courses"] = courses
    
    if request.method == "POST":
        name = request.POST.get("course")
        description = request.POST.get("description")
        
        newcourse = Course.objects.create(name=name, description=description)
        newcourse.teachers.add(request.user)
        newcourse.save()
        
        return redirect(reverse("course", kwargs={"course_uuid": newcourse.uuid}), context)
        
    return render(request, "course/create-course.html", context)

@login_required()
def add_course(request, course_uuid=None):
    context = {}
    courses = get_all_user_courses(request.user)
    context["courses"] = courses
    
    if request.method == "POST":
        uuid = request.POST.get("course")
        
        try:
            course = Course.objects.get(pk=uuid)
            if not course.owners.contains(request.user) and not course.teachers.contains(request.user) and not course.students.contains(request.user) and \
                not course.observers.contains(request.user) and not course.user_query.contains(request.user):
                course.user_query.add(request.user)
            course.save()
            
            context["course"] = course
            
            return redirect(reverse("course", kwargs={"course_uuid": uuid}), context)
        except ValidationError:
            return redirect("/courses/add-course/", context)

    if course_uuid is None:
        return render(request, "course/add-course.html", context)
    
    try:
        course = Course.objects.get(pk=course_uuid)
        if not course.teachers.contains(request.user) and not course.students.contains(request.user) and \
            not course.observers.contains(request.user) and not course.user_query.contains(request.user):
            course.user_query.add(request.user)
        context["course"] = course
        
        return redirect(reverse("course", kwargs={"course_uuid": course_uuid}), context)
    except ValidationError:
        return redirect(reverse("courses"), context)
    except Course.DoesNotExist:
        return redirect(reverse("courses"), context)
    
@login_required()
def delete_course(request, course_uuid):
    context = {}
    courses = get_all_user_courses(request.user)
    context["courses"] = courses
    
    error, first = check_admin_course(request.user, course_uuid, context)  
    if error:
        return first
    course = first
    
    course.delete()
    return redirect(reverse("courses"), context)




@login_required()
def task(request, task_uuid):
    context = {}
    courses = get_all_user_courses(request.user)
    context["courses"] = courses
    
    try:
        task = Task.objects.get(pk=task_uuid)
        context["task"] = task
        course = Course.objects.get(pk=task.course.uuid)
        context["course"] = course
 
        if request.user in course.owners.all() or request.user in course.teachers() or request.user.is_superuser: 
            students = course.students.all()
            solutions = list(map(lambda student: (student, Solution.objects.filter(task=task_uuid, owner=student, status=True).first()), students))
            context["solutions"] = solutions
        
        if request.user in course.students.all():
            context["solution"] = Solution.objects.filter(owner=request.user).first()
        
        return render(request, "task/task.html", context)
    except Task.DoesNotExist:
        return redirect(reverse("courses"), context)
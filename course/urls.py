from django.urls import path
from .views import *

urlpatterns = [
    path("", courses, name="courses"),
    path("course/<uuid:course_uuid>/", course, name="course"),
    path("search/", search, name="search"),
    path("create-course/", create_course, name="create-course"),
    path("add-course/", add_course, name="add-course"),
    path("add-course/<uuid:course_uuid>/", add_course, name="add-course"),
    path("course/<uuid:course_uuid>/admin/", admin_course, name="admin-course"),
    path("course/change-name/<uuid:course_uuid>/", change_name_course, name="change-name-course"),
    path("course/change-description/<uuid:course_uuid>/", change_description_course, name="change-description-course"),
    path("course/<uuid:course_uuid>/accept-user/<uuid:user_uuid>/", accept_user, name="accept-user"),
    path("course/<uuid:course_uuid>/reject-user/<uuid:user_uuid>/", reject_user, name="reject-user"),
    path("course/<uuid:course_uuid>/add-to-owners/<uuid:user_uuid>/", add_user_to_owners, name="add-to-owners"),
    path("course/<uuid:course_uuid>/add-to-teachers/<uuid:user_uuid>/", add_user_to_teachers, name="add-to-teachers"),
    path("course/<uuid:course_uuid>/add-to-students/<uuid:user_uuid>/", add_user_to_students, name="add-to-students"),
    path("course/<uuid:course_uuid>/add-to-observers/<uuid:user_uuid>/", add_user_to_observers, name="add-to-observers"),
    path("course/<uuid:course_uuid>/delete-from-course/<uuid:user_uuid>/", delete_user_from_course_view, name="delete-from-course"),
    path("course/<uuid:course_uuid>/delete/", delete_course, name="delete-course"),
    
    path("task/<uuid:task_uuid>/", task, name="task"),
    path("task/<uuid:task_uuid>/", task, name="admin-task"),
    path("task/<uuid:task_uuid>/", task, name="solution"),
    # path("courses/editcourse", editcourse, name="editcourse"),
    # path("courses/deletecourse", deletecourse, name="deletecourse"),
    # path("courses/course?course_id=<str:course_id>", course, name="course"),
    # path("courses/course?course_id=<str:course_id>/addtask", addtask, name="addtask"),
    # path("courses/course?course_id=<str:course_id>/addtask", edittask, name="edittask"),
    # path("courses/course?course_id=<str:course_id>/addtask", deletetask, name="deletetask"),
    # path("courses/course?=<str:course_id>?task=<task_id>", task, name="task"),
]
from django.urls import path
from . import views


urlpatterns = [

    path(
        '',
        views.student_list,
        name='student_list'
    ),

    path(
        'create/',
        views.create_student,
        name='create_student'
    ),
    
    path(
        "edit-status/<int:student_id>/",
          views.edit_status,
            name="edit_status"
        ),
]
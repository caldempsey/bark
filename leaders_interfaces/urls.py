from django.conf import settings
from django.conf.urls import url
from django.conf.urls.static import static

from leaders_interfaces import views

app_name = 'leaders_interfaces'

# URL Patterns for the leaders interface.

urlpatterns = [
                  # If the url is equal to "" then call views.home.

                  url(r'^leaders/?$', views.CoursesView.as_view(), name="courses"),

                  url(r'^leaders/courses/create/?$', views.CoursesCreateView.as_view(),
                      name="courses_create"),
                  url(r'^leaders/courses/delete/?$', views.CoursesDeleteView.as_view(),
                      name="courses_delete"),

                  url(r'^leaders/courses/(?P<course_id>[0-9]+)/?$', views.CoursesLessonsView.as_view(),
                      name='courses_lessons'),
                  url(r'^leaders/courses/(?P<course_id>[0-9]+)/edit/?$', views.CoursesEditView.as_view(),
                      name='courses_edit'),
                  url(r'^leaders/courses/(?P<course_id>[0-9]+)/lesson/create/?$', views.LessonCreateView.as_view(),
                      name='lesson_create'),

                  url(r'^leaders/courses/(?P<course_id>[0-9]+)/lessons/delete/?$', views.LessonsDeleteView.as_view(),
                      name='lessons_delete'),

                  url(r'^leaders/courses/(?P<course_id>[0-9]+)/lessons/(?P<lesson_id>[0-9]+)/?$',
                      views.LessonsResourcesView.as_view(),
                      name='lessons_resources'),

                  url(r'^leaders/courses/(?P<course_id>[0-9]+)/lessons/(?P<lesson_id>[0-9]+)/edit/?$',
                      views.LessonsEditView.as_view(),
                      name='lessons_edit'),

                  url(r'^leaders/courses/(?P<course_id>[0-9]+)/lessons/(?P<lesson_id>[0-9]+)/resources/create/?$',
                      views.LessonsResourceCreateView.as_view(),
                      name='lessons_resources_create'),

                  url(r'^leaders/courses/(?P<course_id>[0-9]+)/lessons/(?P<lesson_id>[0-9]+)/resources/delete/?$',
                      views.LessonsResourceDeleteView.as_view(),
                      name='lessons_resources_delete'),

                  url(
                      r'^leaders/courses/(?P<course_id>[0-9]+)/lessons/(?P<lesson_id>[0-9]+)/resources/(?P<learning_resource_id>[0-9]+)/edit?$',
                      views.LessonsResourceEditView.as_view(),
                      name='lessons_resources_delete'),
              ] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

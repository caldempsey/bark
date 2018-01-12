from django.conf.urls import url

from students_interfaces import views

app_name = 'students_interfaces'

# URL Patterns for the students interface.

urlpatterns = [

    # /bark/courses
    url(r'^courses/?$', views.CoursesView.as_view(), name='courses'),

    # /bark/courses/lesson/
    url(r'^courses/(?P<course_id>[0-9]+)/?$', views.CoursesLessonsView.as_view(),
        name='courses_lessons'),

    url(r'^courses/(?P<course_id>[0-9]+)/lessons/(?P<lesson_id>[0-9]+)/?$',
        views.CoursesLessonsResourcesView.as_view(),
        name='courses_lessons_resources'),

    url(r'^courses/(?P<course_id>[0-9]+)/lessons/(?P<lesson_id>[0-9]+)/complete/?$',
        views.CoursesLessonsMakeProgressView.as_view(),
        name='courses_lessons_progress'),

    url(r'^courses/(?P<course_id>[0-9]+)/purge_progress/?$',
        views.CoursesLessonsPurgeProgressView.as_view(),
        name='courses_purge_progress'),

    url(
        r'^courses/(?P<course_id>[0-9]+)/lessons/(?P<lesson_id>[0-9]+)/resource/(?P<learning_resource_id>[0-9]+)/interface/?$',
        views.RenderResource.as_view(),
        name='get_resource'),

    url(r'^settings/?$', views.LearningStylesConfigurationView.as_view(), name="settings"),

]

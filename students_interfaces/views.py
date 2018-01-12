from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.views import View

from communicate.exceptions.courses_exceptions import CourseNotFoundException
from communicate.exceptions.learning_resources_exceptions import NoLearningResourcesExistException
from communicate.exceptions.learning_styles_exceptions import NoLearningStylesException
from communicate.exceptions.lessons_exceptions import LessonNotFoundException
from communicate.exceptions.static_containers import RenderResourceFailedException
from communicate.static_containers import lessonslearningstyleresource_to_nginx_alpine_static_container
from communicate.students import get_all_courses, get_course_lesson, get_learning_resources, \
    get_all_learning_resources_except_learningstyles_from_list, get_course, get_lesson_resource
from communicate.students import get_student_course_completion_percentages, get_student_learning_styles, \
    has_student_completed_lesson, delete_course_student_progress, update_student_learning_styles, \
    delete_all_student_progress
from learning_styles.forms import LearningStylesConfigurationForm
from students_interfaces.exceptions.context_exceptions import UndefinedContextException
from students_interfaces.exceptions.template_exceptions import TemplateDoesNotExistException
from students_interfaces.exceptions.update_exceptions import InvalidUserLessonProgressRequestException
from students_interfaces.generator.register_template_context_rules import generate_template_context
from students_interfaces.generator.template import get_learning_styles_template
from students_interfaces.update.register_progress_update_rules import update_user_lesson_progress_protocols

courses_template = "students/courses.html"
lessons_resources_template = "students/lessons_resources.html"
learning_style_settings_template = 'students/settings.html'
render_resources_template = "students/resources_render.html"


class CoursesView(View):
    """
    View for Student Courses
    """
    def get(self, request):
        user = request.user
        # Get the users user_profile
        context = {}
        try:
            courses = get_all_courses()
        except:
            messages.error(request,
                           'An error has occurred (^・x・^). Looks like we do not have any courses right about now! '
                           'Sorry about that!')
            return redirect("/")
        completion_percentages = get_student_course_completion_percentages(user, courses)
        context.update({'courses': courses})
        context.update({'course_completion_percentages': completion_percentages})
        return render(request, courses_template, context)


class CoursesLessonsView(View):
    """
    View for Student Courses Lessons
    """
    def get(self, request, course_id):
        # Get the user
        student = request.user
        # Get the course
        try:
            course = get_course(course_id)
        except CourseNotFoundException:
            messages.error(request,
                           'An error has occurred (^・x・^). We can not find the course you wanted. Sorry about that!')
            # Redirect to the home page
            return redirect("/")
        try:
            learning_styles = get_student_learning_styles(student)
        except NoLearningStylesException:
            messages.error(request,
                           'An error has occurred (^・x・^). We are unable to display lesson content for you until '
                           'you have set your learning styles. Please use the settings menu to provide this.')
            # Redirect to the home page
            return redirect("/")
        try:
            template = get_learning_styles_template(learning_styles)
        except TemplateDoesNotExistException:
            messages.error(request,
                           'An error has occurred (^・x・^). '
                           'We simply do not have any courses associable with your learning style choices. '
                           'Please contact us with this information so we can fix the problem right away!')
            return HttpResponse(status=500)

        # Update with the context necessary for all courses (the course object)
        # At this point we can get the context associated with that learning styles template.
        try:
            context = generate_template_context(template, student, course)
        except UndefinedContextException:
            messages.error(request,
                           'An error has occurred (^・x・^). We are unable to process a context for your '
                           'learning style. Please contact us with this information so we can fix the problem '
                           'right away!')
            return HttpResponse(status=500)
        context.update({"course": course})
        return render(request, template, context)


class CoursesLessonsResourcesView(View):
    """
    View for Students Lessons Resources
    """
    def get(self, request, course_id, lesson_id):
        student = request.user
        try:
            course = get_course(course_id)
        except CourseNotFoundException:
            messages.error(request,
                           'An error has occurred (^・x・^). We are unable to find the course you wanted. Sorry about '
                           'that!')
            return redirect("students_interfaces:courses")
        # Identify if the requested lesson *belongs to* the requested course. If not, return a 404.
        try:
            lesson = get_course_lesson(lesson_id, course)
        except LessonNotFoundException:
            messages.error(request,
                           'An error has occurred (^・x・^). We are unable to find the lesson you wanted. Sorry about '
                           'that!')
            return redirect("students_interfaces:courses_lessons", course_id)

        # Check if student has any learning styles
        try:
            learning_styles = get_student_learning_styles(student)
        except NoLearningStylesException:
            messages.error(request,
                           'An error has occurred (^・x・^). We could not find any learning styles associated with your '
                           'account. Please try assigning some in the settings menu, or get in touch!')
            return redirect("/")

        try:
            student_resources = get_learning_resources(learning_styles, lesson)
        except NoLearningResourcesExistException:
            messages.error(request,
                           '(^・x・^). Looks like we do not have any resources suited for you for this lesson! Sorry '
                           'about that!')
            student_resources = []
        additional_lesson_resources = []
        try:
            additional_lesson_resources = get_all_learning_resources_except_learningstyles_from_list(learning_styles,
                                                                                                     lesson)
        except NoLearningResourcesExistException:
            messages.error(request,
                           '(^・x・^). We could not find any additional resources for this '
                           'lesson! Sorry '
                           'about that!')
        # We also send whether the user has completed the lesson (or not) as this is used in the template.
        lesson_completed = has_student_completed_lesson(student, lesson)
        return render(request, lessons_resources_template,
                      {'users_resources': student_resources,
                       'additional_resources': additional_lesson_resources,
                       'course': course, "lesson": lesson, "lesson_completed": lesson_completed
                       })


class CoursesLessonsMakeProgressView(View):
    """
    Function View, passed when students want to make progress.
    """
    def post(self, request, course_id, lesson_id):
        student = request.user
        try:
            course = get_course(course_id)
        except CourseNotFoundException:
            messages.error(request,
                           'A serious error has occurred (^・x・^). '
                           'We were unable to update a course with some details for you.'
                           'Please contact us so we can fix this right away!')
            # Redirect to the home page
            return HttpResponse(status=500)
            # Identify if the requested lesson *belongs to* the requested course. If not, return a 404.
        try:
            lesson = get_course_lesson(lesson_id, course)
        except LessonNotFoundException:
            messages.error(request,
                           'A serious error has occurred (^・x・^). '
                           'We were unable to update a lesson with some details for you.'
                           'Please contact us so we can fix this right away!')
            return HttpResponse(status=500)
        try:
            learning_styles = get_student_learning_styles(student)
        except NoLearningStylesException:
            messages.error(request,
                           'An error has occurred (^・x・^). We are unable to display lesson content for you until '
                           'you have set your learning styles. Please use the settings menu to provide this.')
            return redirect("/")

        # Execute the rule set for that learning style. Request is passed to execute custom error messages in
        # subsequent methods (a limitation of python is there is no "throws" declaration).
        try:
            update_user_lesson_progress_protocols(student=student,
                                                  learning_styles=learning_styles, lesson=lesson)
        except (InvalidUserLessonProgressRequestException or LessonNotFoundException or CourseNotFoundException):
            messages.error(request,
                           'An error has occurred (^・x・^). We are unable to save your lesson progress. If you '
                           'feel this is in error please raise this with an administrator.')
            # Redirect to the home page
            return redirect("/")

        # Redirect to the course lessons view if the operation was successful so users can see the results.
        return redirect("students_interfaces:courses_lessons",
                        course.id)  # Performs the function of purging user progress of a given course


class LearningStylesConfigurationView(View):
    """
    View to configure LearningStyles
    """
    def get(self, request):
        config_form = LearningStylesConfigurationForm(request.POST or None)
        return render(request, learning_style_settings_template, {'config_form': config_form,
                                                                  })

    def post(self, request):
        student = request.user
        config_form = LearningStylesConfigurationForm(request.POST)
        learning_styles = []
        if config_form.is_valid():
            delete_all_student_progress(student)
            # Define a new list of the learning_styles to update with.
            # Add any desired updates to this list.
            learning_styles = [config_form.cleaned_data["active_reflective"],
                               config_form.cleaned_data["visual_verbal"],
                               config_form.cleaned_data["sensing_intuitive"],
                               config_form.cleaned_data["sequential_global"],
                               ]
            string = ""
            for learning_style in learning_styles:
                string = string + learning_style.name + " "
            # Append to learning styles list cleaned data [no injections].
            # Get the user we will be updating.
            # Update learning styles
            update_student_learning_styles(student, learning_styles)
            messages.success(request,
                             'We have updated your learning styles ฅ^•ﻌ•^ฅ We can see you are an ' + str(
                                 string) + " learner! Happy Learning!")
        else:
            messages.error(request,
                           'Sorry, we cannot update your learning styles if you do not complete the form (^・x・^)')
            config_form = LearningStylesConfigurationForm(instance=request.user)
        # Return to same page, user will see the changes.
        return render(request, learning_style_settings_template,
                      {'config_form': config_form, 'learning-styles': learning_styles
                       })


class CoursesLessonsPurgeProgressView(View):
    """
    View for CoursesLessons
    """
    def post(self, request, course_id):
        student = request.user
        try:
            course = get_course(course_id)
        except CourseNotFoundException:
            return HttpResponse(status=404)
        # Purge the progress
        delete_course_student_progress(student=student, course=course)
        # Prompt
        messages.success(request,
                         "We have removed all your progress for this course ฅ^•ﻌ•^ฅ Stay tough! Happy learning!")
        # Return user back to the courses page where the changes will be reflected.

        return redirect("students_interfaces:courses")


class RenderResource(View):
    """
    View for RenderingResources
    """
    def get(self, request, course_id, lesson_id, learning_resource_id):
        try:
            course = get_course(course_id)
        except CourseNotFoundException:
            messages.error(request,
                           'A serious error has occurred (^・x・^). '
                           'We were unable to find the course for you.'
                           'Please contact us so we can fix this right away!')
            # Redirect to the home page
            return HttpResponse(status=500)
            # Identify if the requested lesson *belongs to* the requested course. If not, return a 404.
        try:
            lesson = get_course_lesson(lesson_id, course)
        except LessonNotFoundException:
            messages.error(request,
                           'A serious error has occurred (^・x・^). '
                           'We were unable to find the lesson for you.'
                           'Please contact us so we can fix this right away!')
            return HttpResponse(status=500)
        try:
            learning_resource = get_lesson_resource(learning_resource_id, lesson, course)
        except NoLearningResourcesExistException:
            messages.error(request,
                           'A serious error has occurred (^・x・^). '
                           'We were unable to find the resource for you.'
                           'Please contact us so we can fix this right away!')
            raise HttpResponse(status=500)
        try:
            host_port = lessonslearningstyleresource_to_nginx_alpine_static_container(
                learning_resource=learning_resource)
        except RenderResourceFailedException:
            messages.error(request,
                           'An error has occurred (^・x・^). '
                           'We were unable to interface the resource you requested. '
                           'Please contact us with this information so we can fix it right away!')
            raise HttpResponse(status=500)
        return render(request, render_resources_template, {'host_port': host_port})

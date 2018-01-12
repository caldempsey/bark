from django.contrib import messages
from django.shortcuts import render, redirect
from django.views import View

from communicate.exceptions.courses_exceptions import CourseNotFoundException
from communicate.exceptions.learning_resources_exceptions import LearningResourceNotFoundException
from communicate.exceptions.lessons_exceptions import LessonNotFoundException
from communicate.leaders import get_leaders_course, remove_courses_list, \
    remove_lessons_list, \
    remove_learning_resources_list, get_leaders_learning_resource, get_leaders_lesson, \
    get_maximum_lesson_sequence_number
from courses.forms import CoursesCreateForm, CoursesEditForm, LessonsCreateForm, LessonsEditForm
from courses.forms import LessonsLearningStylesResourcesCreateForm, LessonsLearningStylesResourcesEditForm

# Static Templates #
# Courses Goals #
courses_template = 'leaders/courses.html'
courses_delete_template = 'leaders/courses_delete.html'
courses_create_template = 'leaders/courses_create.html'
courses_edit_template = 'leaders/courses_edit.html'
courses_lessons_template = 'leaders/courses_lessons.html'
# Lessons Goals
lesson_create_template = 'leaders/lessons_create.html'
lessons_edit_template = 'leaders/lessons_edit.html'
lessons_delete_template = 'leaders/lessons_delete.html'
# Lesson resources goals #
lessons_resources_template = 'leaders/lessons_resources.html'
lessons_resources_create_template = 'leaders/resources_create.html'
resources_delete_template = 'leaders/resources_delete.html'
lessons_resources_edit_template = 'leaders/resources_edit.html'


# Views #

class CoursesView(View):
    """
    The Courses view is responsible for providing the interface of all of the courses a leader owns.
    """

    def get(self, request):
        """
        The get method of the courses view is responsible for providing the user interface view courses.

        :param request: the HTTP request object passed.
        :return returns a HTTP response object coupled with the leaders courses as context.
        """
        # Validation
        # Get the user object.
        leader = request.user
        # Get all the courses objects associated with the user objects.
        courses = leader.courses.all()
        # If there are no lessons pass a message.
        if not courses:
            messages.error(request,
                           'It looks like there are no courses for us to display (^・x・^). Please populate '
                           'courses so students have something to see!')

        return render(request, courses_template, {'courses': courses})


class CoursesDeleteView(View):
    """
    The Courses Delete view is responsible for providing the interface from which Bark leaders are able to delete courses.
    This is facilitated by rendering the courses_delete template specified.  "that belong" to the user [test_author]).
    """

    def get(self, request):
        """
        The get method of the leaders courses delete view is responsible for providing the user interface to HTTP get
        requests to delete courses.

        :param request: the HttpRequest object passed.
        :return returns a HttpResponse of the courses delete template coupled with the leaders courses as context.
        """
        # Get the user object.
        leader = request.user
        # Get all the courses objects associated with the user objects.
        courses = leader.courses_set.all()
        # If there are no lessons pass a message.
        if not courses:
            messages.error(request,
                           'It looks like there are no courses for us to display (^・x・^). Please populate '
                           'courses so students have something to see!')
        return render(request, courses_delete_template, {'courses': courses})

    def post(self, request):
        """
        The post method of the leaders courses delete view is responsible for processing the requests from the leaders
        courses delete interface.

        :param request: the HttpRequest object passed.
        :return returns a HttpResponse of the courses delete template coupled with the leaders courses as context.
        """
        # Validation
        # Get the user object.
        leader = request.user
        # Get the POST data "checks" associated with the request.
        course_ids = request.POST.getlist('checks')
        # Contact the interface_communicator library to do the removal work for us.
        remove_courses_list(leader, course_ids)
        # Get all the courses objects associated with the user objects.
        courses = leader.courses_set.all()
        # If there are no lessons pass a message.
        if not courses:
            messages.error(request,
                           'It looks like there are no courses for us to display (^・x・^). Please populate '
                           'courses so students have something to see!')
        return render(request, courses_delete_template, {'courses': courses})


class CoursesCreateView(View):
    """
    The Courses Create View is responsible for providing an interface which allows users to create new
    courses. This is facilitated by rendering the courses_create_template specified.
    """

    def get(self, request):
        """
        The get method of the leaders courses create view is responsible for providing the user interface to HTTP get
        requests to create courses.
        """
        # Get the courses creation form from the Django generated model form.
        courses_create_form = CoursesCreateForm()
        # Return and interface the courses create template with the model form passed to context.
        return render(request, courses_create_template,
                      {'courses_create_form': courses_create_form,
                       })

    def post(self, request):
        """
        The post method of the leaders courses delete view is responsible for providing the user interface to HTTP get
        requests to create courses.
        """
        # All requests in the Django framework have a user object associated with their request [which is appended
        # with anonymous in the case of non authenticated requests].
        leader = request.user
        # Render a new course create form that includes the user submitted data so we can parse it with Django
        create_form = CoursesCreateForm(request.POST, request.FILES)
        # If the forms fields are valid (as interpreted by the "save()" method in the form)
        if create_form.is_valid():
            # Save the form but do not commit, we need to add some user details.
            course = create_form.save(commit=False)
            course.author = leader
            course.save()
            return redirect('leaders_interfaces:courses')
        else:
            return render(request, courses_create_template,
                          {'courses_create_form': create_form,
                           })


# Users should be redirected if they attempt to view the courses owned by another leader
class CoursesLessonsView(View):
    """
    The Courses Lessons View is responsible for providing an interface which allows users to view lessons for
    courses. This is facilitated by rendering the courses_lessons_template specified.
    """

    def get(self, request, course_id):
        """
        The get method of the courses lessons view is responsible for serving an interface associated with
        viewing lessons for each course. These details are already be passed by the courses object implicitly.
        """
        # Validation
        # Get user details
        leader = request.user
        # Get the course we want to work with.
        try:
            course = get_leaders_course(course_id, leader)
        # Forward error handle back where the user came from with an error message.
        except CourseNotFoundException:
            messages.error(request,
                           'An error has occurred (^・x・^). We cannot find the course you asked for! Sorry about that.')
            return redirect("leaders_interfaces:courses")

        # Render the courses_lessons_template with the course object specified.
        return render(request, courses_lessons_template,
                      {'course': course,
                       })


class CoursesEditView(View):
    """
    The Courses Edit View is responsible for providing an interface which allows users to create new
    courses. This is facilitated by rendering the courses_edit_template specified.
    """

    def get(self, request, course_id):
        """
        The get method of the courses edit view is responsible for providing the user interface to HTTP get
        requests to edit courses.
        """
        # Validation
        # Get user details
        leader = request.user
        # Get the course we want to work with.
        try:
            course = get_leaders_course(course_id, leader)
        # Forward error handle back where the user came from with an error message.
        except CourseNotFoundException:
            messages.error(request,
                           'An error has occurred (^・x・^). We cannot find the course you asked for! Sorry about that.')
            return redirect("leaders_interfaces:courses")

        # Get form from Django Forms and construct with initial values.
        edit_form = CoursesEditForm(
            initial={'title': course.title, 'description': course.description, 'logo': course.logo})
        return render(request, courses_edit_template,
                      {'courses_edit_form': edit_form,
                       'course': course})

    def post(self, request, course_id):
        """
        The post method of the courses edit view is responsible for interacting with the POST request sent by the
        interface associated with the get request of editing courses.
        """
        # Validation
        # Get user details
        leader = request.user
        # Get the course we want to work with.
        try:
            course = get_leaders_course(course_id, leader)
        # Forward error handle back where the user came from with an error message.
        except CourseNotFoundException:
            messages.error(request,
                           'An error has occurred (^・x・^). We cannot find the course you asked for! Sorry about that.')
            return redirect("leaders_interfaces:courses")

        # Get edit form post data
        edit_form = CoursesEditForm(request.POST, request.FILES)
        # If the forms fields are valid (as interpreted by the "save()" method in the form)
        if edit_form.is_valid():
            # Save the form but do not commit, we need to add the user details not sent by the form.
            edit_form = edit_form.save(
                commit=False)  # Create a courses object but do not commit it to the database.
            edit_form.author = leader  # Overwrite the users user profile as the test_author of the
            # course.
            edit_form.id = course.id  # Overwrite the course object's ID as the course ID sent by POST.
            if edit_form.logo is None:
                edit_form.logo = course.logo
            edit_form.save()  # Commit the form to the database.
            # Redirect the user on successful save of the form to the courses.
            return redirect('leaders_interfaces:courses_lessons', course_id)
        else:
            # If the form is not valid then re-direct the user back to the edit form.
            return render(request, courses_create_template,
                          {'courses_edit_form': edit_form, 'course': course
                           })


class LessonCreateView(View):
    """
    The  Lessons Create View is responsible for providing an interface which allows users to create new
    lessons. This is facilitated by rendering the lessons_create_template specified.
    """

    def get(self, request, course_id):
        """
        The get method of the leaders lessons create view is responsible for serving an interface associated with
        creating lessons for the course id specified.
        """
        # Validation
        # Get user details
        leader = request.user
        # Get the course we want to work with.
        try:
            course = get_leaders_course(course_id, leader)
        # Forward error handle back where the user came from with an error message.
        except CourseNotFoundException:
            messages.error(request,
                           'An error has occurred (^・x・^). We cannot find the course you asked for! Sorry about that.')
            return redirect("leaders_interfaces:courses")

        # Get form from Django Forms and construct with the maximum sequence number
        # of a lesson. The form is specified to not accept values over the passed value.
        lesson_create_form = LessonsCreateForm(
            # The maximum sequence number is equal to the next possible lesson sequence number (i.e. if
            # Lesson 7 was the last lesson then the value generated will be 8, if there are no lessons then
            # the value generated will be 1).
            maximum_sequence_number=get_maximum_lesson_sequence_number(course), course=course)
        # Render the request
        return render(request, lesson_create_template,
                      {'lesson_create_form': lesson_create_form, 'course': course
                       })

    def post(self, request, course_id):
        """
        The post method of the leaders lessons create view is responsible for interpreting the post data sent by the
        interface associated with creating lessons for the course id specified. This means cleaning the data (
        ensuring that uniqueness is not violated) and ensuring that invalid data i.e. lessons for courses that don't

        belong to the user, are not saved).
        """
        # Validation
        # Get user details
        leader = request.user
        # Get the course we want to work with.
        try:
            course = get_leaders_course(course_id, leader)
        # Forward error handle back where the user came from with an error message.
        except CourseNotFoundException:
            messages.error(request,
                           'An error has occurred (^・x・^). We cannot find the course you asked for! Sorry about that.')
            return redirect("leaders_interfaces:courses")

        # If the user is authenticated as a leader and the course does belong to the leader then we are now
        # in an apt position to handle the form data.
        create_form = LessonsCreateForm(request.POST,
                                        maximum_sequence_number=get_maximum_lesson_sequence_number(course),
                                        course=course)
        if create_form.is_valid():
            create_form.save()
            return redirect('leaders_interfaces:courses_lessons', course.id)
        # If the user form isn't valid return back to the create form having raised an error.
        return render(request, lesson_create_template, {'lesson_create_form': create_form,
                                                        'course': course})


class LessonsDeleteView(View):
    """
    The  Lessons Delete View is responsible for providing an interface which allows users to delete existing
    lessons. This is facilitated by rendering the lessons_delete_template specified. Removal is performed in
    a safe and controlled way by only if statements (only removing the lessons at ids "that belong" to the course).
    """

    def get(self, request, course_id):
        """
        The get method of the leaders lessons delete view is responsible for providing the interface from which users
        can delete existing lessons.
        """
        # Validation
        # Get user details
        leader = request.user
        # Get the course we want to work with.
        try:
            course = get_leaders_course(course_id, leader)
        # Forward error handle back where the user came from with an error message.
        except CourseNotFoundException:
            messages.error(request,
                           'An error has occurred (^・x・^). We cannot find the course you asked for! Sorry about that.')
            return redirect("leaders_interfaces:courses_lessons", course_id)

        # Get all the lessons objects associated with the course objects.
        lessons = course.lessons_set.all()
        # If there are no lessons pass a message.
        if not lessons:
            messages.error(request,
                           'It looks like there are no lessons for us to display (^・x・^). Please populate '
                           'lessons so students have something to see!')
        return render(request, lessons_delete_template,
                      {'lessons': lessons, 'course': course})

    def post(self, request, course_id):
        """
        The post method of the lessons delete view is responsible for requesting for deleting lessons and then updating the interface.
        It is important to ensure that the sequence of lessons is not interrupted by
        the delete operations. For example it could be the case that an existing user takes three lessons of a course
        and the leader of that course deletes the second. In these instances it is necessary to rearrange the material.
        """
        # Validation
        # Get user details
        leader = request.user
        # Get the course we want to work with.
        try:
            course = get_leaders_course(course_id, leader)
        # Forward error handle back where the user came from with an error message.
        except CourseNotFoundException:
            messages.error(request,
                           'An error has occurred (^・x・^). We cannot find the course you asked for! Sorry about that.')
            return redirect("leaders_interfaces:courses_lessons", course_id)

        lesson_ids = request.POST.getlist('checks')
        # Remove the lesson from the course.
        remove_lessons_list(course, lesson_ids)
        # Get all the lessons objects associated with the course objects.
        lessons = course.lessons_set.all()
        # If there are no lessons pass a message.
        if not lessons:
            messages.error(request,
                           'It looks like there are no lessons for us to display (^・x・^). Please populate '
                           'lessons so students have something to see!')

        return render(request, lessons_delete_template,
                      {'lessons': lessons, 'course': course})


class LessonsEditView(View):
    """
    The  Lessons Edit View is responsible for providing an interface which allows users to edit existing
    lessons. This is facilitated by rendering the lessons_edit_template specified.
    """

    def get(self, request, course_id, lesson_id):
        """
        The get method of the leaders lessons edit view is responsible for providing the interface from which users
        can edit existing lessons.
        """

        # Validation
        # Get user details
        leader = request.user
        # Get the lesson and course we want to work with.
        try:
            course = get_leaders_course(course_id, leader)
            lesson = get_leaders_lesson(lesson_id, course, leader)
        # Forward error handle back where the user came from with an error message.
        except CourseNotFoundException:
            messages.error(request,
                           'An error has occurred (^・x・^). We cannot find the course you asked for! Sorry about that.')
            return redirect("leaders_interfaces:courses")
        except LessonNotFoundException:
            messages.error(request,
                           'An error has occurred (^・x・^). We cannot find the lesson you asked for! Sorry about that.')
            return redirect("leaders_interfaces:courses_lessons", course_id)

        edit_form = LessonsEditForm(
            initial={'sequence_number': lesson.sequence_number, 'title': lesson.title,
                     'description': lesson.description},
            maximum_sequence_number=get_maximum_lesson_sequence_number(course), course=course, lesson=lesson)
        # Render the lessons_edit_template passing in the edit form.
        return render(request, lessons_edit_template,
                      {'lessons_edit_form': edit_form, 'lesson': lesson,
                       'course': course
                       })

    def post(self, request, course_id, lesson_id):
        """
        The post method of the leaders lessons edit view is responsible for interpreting the post data sent by the
        interface associated with creating lessons for the course id specified. This means cleaning the data (
        ensuring that uniqueness is not violated) and ensuring that invalid data i.e. lessons for courses that don't
        belong to the user, are not saved).
        """

        # Validation
        # Get user details
        leader = request.user
        # Get the lesson and course we want to work with.
        try:
            course = get_leaders_course(course_id, leader)
            lesson = get_leaders_lesson(lesson_id, course, leader)

        # Forward error handle back where the user came from with an error message.
        except CourseNotFoundException:
            messages.error(request,
                           'An error has occurred (^・x・^). We cannot find the course you asked for! Sorry about that.')
            return redirect("leaders_interfaces:courses")
        except LessonNotFoundException:
            messages.error(request,
                           'An error has occurred (^・x・^). We cannot find the lesson you asked for! Sorry about that.')
            return redirect("leaders_interfaces:courses_lessons", course_id)

        edit_form = LessonsEditForm(request.POST,
                                    maximum_sequence_number=get_maximum_lesson_sequence_number(course), course=course,
                                    lesson=lesson)
        if edit_form.is_valid():
            edit_form.save()
            return redirect('leaders_interfaces:lessons_resources', course.id, lesson.id)
        else:

            return render(request, lessons_edit_template,
                          {'lessons_edit_form': edit_form, 'course': course
                              , 'lesson': lesson})


class LessonsResourcesView(View):
    """
    The  Lessons Resources View is responsible for providing an interface which allows users to view existing
    resources for lessons. This is facilitated by rendering the lessons_resources_template specified. This
    means validating that the resources belong to the lesson.
    """

    def get(self, request, course_id, lesson_id):
        """
        The get method of the leaders lessons resources view is responsible for providing the interface of a lessons
        existing resources. This is achieved by getting all the resources by a particular lesson post validation that
        the lesson belongs to the course and the course belongs to the user.
        """

        # Validation
        # Get user details
        leader = request.user
        # Get the lesson and course we want to work with.
        try:
            course = get_leaders_course(course_id, leader)
            lesson = get_leaders_lesson(lesson_id, course, leader)
        # Forward error handle back where the user came from with an error message.
        except CourseNotFoundException:
            messages.error(request,
                           'An error has occurred (^・x・^). We cannot find the course you asked for! Sorry about that.')
            return redirect("leaders_interfaces:courses")
        except LessonNotFoundException:
            messages.error(request,
                           'An error has occurred (^・x・^). We cannot find the lesson you asked for! Sorry about that.')
            return redirect("leaders_interfaces:courses_lessons", course_id)

        # Get all associated learning_resources objects with the lessons
        learning_resources = lesson.lessonslearningstylesresources_set.all()
        # If there are no resources pass a message.
        if not learning_resources:
            messages.error(request,
                           'It looks like there are no learning resources for us to display (^・x・^). Please '
                           'populate '
                           'some resources so students have something to see!')
        # Render the template of course resources passing the lesson, course, and resources as context.
        return render(request, lessons_resources_template,
                      {'lesson': lesson, 'course': course,
                       'learning_resources': learning_resources})


class LessonsResourceCreateView(View):
    """
    The  Lessons Resources Create View is responsible for providing an interface which allows users to create existing
    resources for lessons. This is facilitated by rendering the lessons_resources_create_template specified.
    """

    def get(self, request, course_id, lesson_id):
        """
        The get method of the leaders lessons resources create view is responsible for providing the interface to
        append a new resource to a lesson. This is achieved by validating that the lesson belongs to the
        course and the course belongs to the user and handling HTTP requests as appropriate.
        """

        # Validation
        # Get user details
        leader = request.user
        # Get the lesson and course we want to work with.
        try:
            course = get_leaders_course(course_id, leader)
            lesson = get_leaders_lesson(lesson_id, course, leader)
        # Forward error handle back where the user came from with an error message.
        except CourseNotFoundException:
            messages.error(request,
                           'An error has occurred (^・x・^). We cannot find the course you asked for! Sorry about that.')
            return redirect("leaders_interfaces:courses")
        except LessonNotFoundException:
            messages.error(request,
                           'An error has occurred (^・x・^). We cannot find the lesson you asked for! Sorry about that.')
            return redirect("leaders_interfaces:courses_lessons", course_id)

        # Get the LessonLearningStylesResources form construct with initial values.
        create_form = LessonsLearningStylesResourcesCreateForm(course=course, lesson=lesson)
        return render(request, lessons_resources_create_template,
                      {'resources_create_form': create_form, 'lesson': lesson,
                       'course': course,
                       })

    def post(self, request, course_id, lesson_id):
        """
        The post method of the leaders lessons resources create view is responsible for handling information passed
        by the interface creating lesson resources. This is achieved by getting the resources sent by the HTTP post
        request, performing validation that the lesson belongs to the course and the course belongs to the user,
        then handling resources as appropriate.
        """

        # Validation
        # Get user details
        leader = request.user
        # Get the lesson and course we want to work with.
        try:
            course = get_leaders_course(course_id, leader)
            lesson = get_leaders_lesson(lesson_id, course, leader)
        # Forward error handle back where the user came from with an error message.
        except CourseNotFoundException:
            messages.error(request,
                           'An error has occurred (^・x・^). We cannot find the course you asked for! Sorry about that.')
            return redirect("leaders_interfaces:courses")
        except LessonNotFoundException:
            messages.error(request,
                           'An error has occurred (^・x・^). We cannot find the lesson you asked for! Sorry about that.')
            return redirect("leaders_interfaces:courses_lessons", course_id)

        create_form = LessonsLearningStylesResourcesCreateForm(request.POST, request.FILES, lesson=lesson,
                                                               course=course)
        if create_form.is_valid():
            create_form.save(commit=True)
            # Get all associated learning_resources objects with the lessons
            learning_resources = lesson.lessonslearningstylesresources_set.all()
            # If there are no resources pass a message.
            if not learning_resources:
                messages.error(request,
                               'It looks like there are no learning resources for us to display (^・x・^). Please '
                               'populate '
                               'some resources so students have something to see!')

            return render(request, lessons_resources_template,
                          {'lesson': lesson, 'course': course,
                           'learning_resources': learning_resources})
        # Re-interface the page with validation errors passed by the form
        else:  # Get all the resources objects associated with the lesson objects.
            learning_resources = lesson.lessonslearningstylesresources_set.all()
            # If there are no resources pass a message.
            if not learning_resources:
                messages.error(request,
                               'It looks like there are no learning resources for us to display (^・x・^). Please '
                               'populate '
                               'some resources so students have something to see!')

            return render(request, lessons_resources_create_template,
                          {'resources_create_form': create_form,
                           'course': course, 'lesson': lesson, 'learning_resources': learning_resources
                           })


class LessonsResourceDeleteView(View):
    """
    The  Lessons Resources Delete View is responsible for providing an interface which allows users to delete existing
    resources for lessons. This is facilitated by rendering the lessons_resources_delete_template specified.
    """

    def get(self, request, course_id, lesson_id):
        """
        The get method of the leaders lessons resources delete view is responsible for providing the interface to
        append a new resource to a lesson. This is achieved by validating that the lesson belongs to the course and
        the course belongs to the user, providing only resources belonging to the lesson and handling HTTP requests
        as appropriate.
        """

        # Validation
        # Get user details
        leader = request.user
        # Get the lesson and course we want to work with.
        try:
            course = get_leaders_course(course_id, leader)
            lesson = get_leaders_lesson(lesson_id, course, leader)
        # Forward error handle back where the user came from with an error message.
        except CourseNotFoundException:
            messages.error(request,
                           'An error has occurred (^・x・^). We cannot find the course you asked for! Sorry about that.')
            return redirect("leaders_interfaces:courses")
        except LessonNotFoundException:
            messages.error(request,
                           'An error has occurred (^・x・^). We cannot find the lesson you asked for! Sorry about that.')
            return redirect("leaders_interfaces:courses_lessons", course_id)

        # Get all the resources objects associated with the lesson objects.
        learning_resources = lesson.lessonslearningstylesresources_set.all()
        # If there are no resources pass a message.
        if not learning_resources:
            messages.error(request,
                           'It looks like there are no learning resources for us to display (^・x・^). Please '
                           'populate '
                           'some resources so students have something to see!')

        return render(request, resources_delete_template,
                      {'course': course, 'lesson': lesson, 'learning_resources': learning_resources})

    def post(self, request, course_id, lesson_id):
        """
        The post method of the leaders lessons resources delete view is responsible for handling information passed
        by the interface to delete lesson resources. This is achieved by getting the resources sent by the HTTP post
        request, performing validation that the lesson belongs to the course and the course belongs to the user,
         and the resource belongs to the lesson then handling resources as appropriate.
        """

        # Validation
        # Get user details
        leader = request.user
        # Get the lesson and course we want to work with.
        try:
            course = get_leaders_course(course_id, leader)
            lesson = get_leaders_lesson(lesson_id, course, leader)
        # Forward error handle back where the user came from with an error message.
        except CourseNotFoundException:
            messages.error(request,
                           'An error has occurred (^・x・^). We cannot find the course you asked for! Sorry about that.')
            return redirect("leaders_interfaces:courses")
        except LessonNotFoundException:
            messages.error(request,
                           'An error has occurred (^・x・^). We cannot find the lesson you asked for! Sorry about that.')
            return redirect("leaders_interfaces:courses_lessons", course_id)

        learning_resource_ids = request.POST.getlist('checks')
        remove_learning_resources_list(lesson, learning_resource_ids)
        # Get all the resources objects associated with the lesson objects.
        learning_resources = lesson.lessonslearningstylesresources_set.all()
        # If there are no resources pass a message.
        if not learning_resources:
            messages.error(request,
                           'It looks like there are no learning resources for us to display (^・x・^). Please '
                           'populate '
                           'some resources so students have something to see!')

        return render(request, resources_delete_template,
                      {'course': course, 'lesson': lesson, 'learning_resources': learning_resources})


class LessonsResourceEditView(View):
    """
    The  Lessons Resources Edit View is responsible for providing an interface which allows users to edit existing
    resources for lessons. This is facilitated by rendering the lessons_resources_edit_template specified.
    """
    def get(self, request, course_id, lesson_id, learning_resource_id):
        """
        The get method of the leaders lessons resources edit view is responsible for providing the interface to
        edit resources of lessons. This is achieved by validating that the lesson belongs to the
        course and the course belongs to the user and the resource belongs to the lesson and handling HTTP requests as appropriate.
        """

        # Validation
        # Get user details
        leader = request.user
        # Get the lesson and course we want to work with.
        try:
            course = get_leaders_course(course_id, leader)
            lesson = get_leaders_lesson(lesson_id, course, leader)
            learning_resource = get_leaders_learning_resource(learning_resource_id, lesson, course, leader)
        # Forward error handle back where the user came from with an error message.
        except CourseNotFoundException:
            messages.error(request,
                           'An error has occurred (^・x・^). We cannot find the course you asked for! Sorry about that.')
            return redirect("leaders_interfaces:courses")
        except LessonNotFoundException:
            messages.error(request,
                           'An error has occurred (^・x・^). We cannot find the lesson you asked for! Sorry about that.')
            return redirect("leaders_interfaces:courses_lessons", course_id)
        except LearningResourceNotFoundException:
            messages.error(request,
                           'An error has occurred (^・x・^). We cannot find the learning resource you asked for! Sorry '
                           'about that.')
            return redirect("leaders_interfaces:lessons_resources", course_id, lesson_id)

        edit_form = LessonsLearningStylesResourcesEditForm(
            initial={'title': learning_resource.title, 'description': learning_resource.description,
                     'learning_style': learning_resource.learning_style}, course=course, lesson=lesson,
            lessonlearningstyleresource=learning_resource)
        # Render the lessons_edit_template passing in the edit form.
        return render(request, lessons_resources_edit_template,
                      {'resources_edit_form': edit_form, 'lesson': lesson,
                       'course': course
                       })

    def post(self, request, course_id, lesson_id, learning_resource_id):

        """
        The get method of the leaders lessons resources edit view is responsible for handling the interface to
        edit resources of lessons. This is achieved by validating that the lesson belongs to the
        course and the course belongs to the user and the resource belongs to the lesson and handling HTTP requests as appropriate.
        """
        leader = request.user
        # Get the lesson and course we want to work with.
        try:
            course = get_leaders_course(course_id, leader)
            lesson = get_leaders_lesson(lesson_id, course, leader)
            learning_resource = get_leaders_learning_resource(learning_resource_id, lesson, course, leader)

        # Forward error handle back where the user came from with an error message.
        except CourseNotFoundException:
            messages.error(request,
                           'An error has occurred (^・x・^). We cannot find the course you asked for! Sorry about that.')
            return redirect("leaders_interfaces:courses")
        except LessonNotFoundException:
            messages.error(request,
                           'An error has occurred (^・x・^). We cannot find the lesson you asked for! Sorry about that.')
            return redirect("leaders_interfaces:courses_lessons", course_id)
        except LearningResourceNotFoundException:
            messages.error(request,
                           'An error has occurred (^・x・^). We cannot find the learning resource you asked for! Sorry '
                           'about that.')
            return redirect("leaders_interfaces:lessons_resources", course_id, lesson_id)

        edit_form = LessonsLearningStylesResourcesEditForm(request.POST, request.FILES, course=course, lesson=lesson,
                                                           lessonlearningstyleresource=learning_resource)
        if edit_form.is_valid():
            edit_form.save(commit=True)
            # Return to resources page, users will see the changes.

            # Get all the resources objects associated with the lesson objects.
            learning_resources = lesson.lessonslearningstylesresources_set.all()
            # If there are none pass a message.
            if not learning_resources:
                messages.error(request,
                               'It looks like there are no learning resources for us to display (^・x・^). Please '
                               'populate '
                               'some resources so students have something to see!')
            return render(request, lessons_resources_template,
                          {'lesson': lesson, 'course': course,
                           'learning_resources': learning_resources})
        # Re-interface the page with validation errors passed by the form
        else:
            return render(request, lessons_resources_edit_template,
                          {'resources_edit_form': edit_form, 'lesson': lesson,
                           'course': course
                           })

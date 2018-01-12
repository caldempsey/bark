from unittest import TestCase

from django.contrib.auth.models import User

from communicate.exceptions.courses_exceptions import NoCoursesExistException, CourseNotFoundException
from communicate.exceptions.learning_resources_exceptions import NoLearningResourcesExistException, \
    LearningResourceNotFoundException
from communicate.exceptions.learning_styles_exceptions import NoLearningStylesException
from communicate.exceptions.lessons_exceptions import LessonNotFoundException, NoLessonsExistException
from communicate.leaders import get_leaders_course, get_leaders_lesson, get_leaders_learning_resource
from communicate.students import has_next_lesson, get_next_lesson, get_all_courses, get_learning_resources, \
    get_all_learning_resources_except_learningstyles_from_list, get_course_lesson, get_student_learning_styles
from courses.models import Courses, Lessons, LessonsLearningStylesResources
from learning_styles.manage.userlearningstyles import purge_user_userlearningstyles, \
    add_to_user_userlearningstyles_collection
from learning_styles.models import LearningStyles, UserLearningStyles
from resources.models import Resources


class StudentsCommunicatorTest(TestCase):
    def setUp(self):
        """
        Create a series of test cases for the Student communicator.
        """
        # Manual assignment of primary key.
        self.test_student = User.objects.create_user(id=1,
                                                     username='MrTest', email='test@test.com', password='test')

        self.course = Courses.objects.create(author=self.test_student, title="", description="")
        self.lesson = Lessons.objects.create(course=self.course, sequence_number=1, title="", description="")

    def test_has_next_lesson(self):
        """
        Tests whether the lesson in test data is correctly identified as having a next sequence member when a lesson
        is added.
        """
        # Add the respective lesson to the test case.
        self.lesson2 = Lessons.objects.create(course=self.course, title="", description="", sequence_number=2)
        self.assertTrue(has_next_lesson(self.lesson))
        self.assertFalse(has_next_lesson(self.lesson2))

    def test_get_next_lesson(self):
        """
        Tests whether given test data the next lesson in the sequence of lessons for a course return the expected
        assertion error. Tests whether LessonNotFound is thrown correctly.
        """
        try:
            self.lesson2 = Lessons.objects.create(course=self.course, title="", description="", sequence_number=2)
            get_next_lesson(lesson=self.lesson2)
        except LessonNotFoundException:
            return True
        self.lesson2 = Lessons.objects.create(course=self.course, title="", description="", sequence_number=2)
        self.assertEqual(get_next_lesson(lesson=self.lesson), self.lesson2)
        self.fail()

    def test_get_all(self):
        """
        Tests the get_all function throws NoCoursesExistException correctly.
        """
        # Get all courses.
        courses = get_all_courses()
        # Test that the QuerySet object contains the valid author defined in setup.
        self.assertTrue(courses.filter(author=self.test_student).exists())
        # Delete all courses
        Courses.objects.all().delete()
        try:
            get_all_courses()
        except NoCoursesExistException:
            return True
        self.fail()

    def test_get_learning_resource(self):
        """
        Tests NoLearningResourcesExistException is thrown correctly.
        """
        style = LearningStyles.objects.create(name="active")
        list = [style]
        try:
            get_learning_resources(list, lesson=self.lesson)
        except NoLearningResourcesExistException:
            return True
        self.fail()

    def test_get_all_learning_resources_except_learningstyles_from_list(self):
        """
        Tests NoLearningResourcesExistException is thrown correctly.
        """
        # Same as above but passing an exclusionary
        style = LearningStyles.objects.create(name="active")
        list = [style]
        try:
            get_all_learning_resources_except_learningstyles_from_list(list, lesson=self.lesson)
        except NoLearningResourcesExistException:
            return True
        self.fail()

    def test_get_course_lesson(self):
        """
        Tests LessonNotFoundException is thrown correctly
        """
        try:
            get_course_lesson(lesson_id=self.lesson.id + 1, course=self.course)
        except LessonNotFoundException:
            return True
        self.fail()

    def test_update_student_learning_styles(self):
        """
        Tests update functionality.
        """
        # Create learning styles.
        a = LearningStyles.objects.create(name="active")
        r = LearningStyles.objects.create(name="reflective")
        # Add them to the user.
        styles = [a, r]
        add_to_user_userlearningstyles_collection(self.test_student, learning_styles=styles)
        purge_user_userlearningstyles(self.test_student)
        # Populate the many to many relationship.
        add_to_user_userlearningstyles_collection(self.test_student, styles)
        # Ensure that the value is the expected value (2, not 4).
        self.assertTrue(UserLearningStyles.objects.filter(user=self.test_student), 2)

    def test_get_student_learning_styles(self):

        """
        Test whether we can successfully get the student learning styles of a student (and error out).
        """
        # Create a collection of learning styles
        self.active_style = LearningStyles.objects.create(name="Active")
        self.reflective_style = LearningStyles.objects.create(name="Reflective")
        collection = [self.active_style, self.reflective_style]
        # Check if each item in styles is equal to the function
        add_to_user_userlearningstyles_collection(self.test_student, collection)
        # Get the collection back assuming its equal to the one passed.
        self.assertEqual(get_student_learning_styles(self.test_student), collection)
        purge_user_userlearningstyles(self.test_student)
        # Test the exception case.
        try:
            get_student_learning_styles(self.test_student)
        except NoLearningStylesException:
            return True
        self.fail()

class LeadersCommunicatorTest(TestCase):
    def setUp(self):
        """
        Create a series of test cases for the Leaders communicator.
        """
        # Manual assignment of primary key.
        self.test_leader = User.objects.create_user(id=1,
                                                     username='MrTest', email='test@test.com', password='test')

        self.course = Courses.objects.create(author=self.test_leader, title="", description="")
    def test_get_leaders_course(self):
        """
        Test whether get_leaders_course returns exceptions correctly.
        """
        try:
            self.test_leader2 = User.objects.create_user(id=2,
                                                        username='MrTest2', email='test@test.com', password='test')
            get_leaders_course(1, self.test_leader2)
        except CourseNotFoundException:
            return True
        try:

            get_leaders_course(2, self.test_leader2)
        except NoCoursesExistException:
            return True
        self.fail()

    def test_get_leaders_lesson(self):
        """
        Tests whether get_leaders_lesson returns exceptions correctly.
        """

        Lessons.objects.create(course=self.course, title="", description="", sequence_number=1)
        test_leader2 = User.objects.create_user(id=2,
                                                     username='MrTest2', email='test@test.com', password='test')
        try:
            get_leaders_lesson(1, self.course, test_leader2)
        except LessonNotFoundException:
            pass
        try:
            get_leaders_lesson(2, self.course, test_leader2)
        except LessonNotFoundException:
            return True
        self.fail()

    def test_get_leaders_learning_resource(self):
        """
        Tests whether get_leaders_learning_resource returns true
        """
        lesson = Lessons.objects.create(course=self.course, title="", description="", sequence_number=1)
        try:
            resource = Resources.objects.create(file='foo')
            learning_style = LearningStyles.objects.create(name="test")
            LessonsLearningStylesResources.objects.create(resource=resource, learning_style=learning_style,lesson=lesson)
            get_leaders_learning_resource(2, lesson=lesson, user=self.test_leader, course=self.course)
        except LearningResourceNotFoundException:
            pass
        try:
            get_leaders_learning_resource(1, lesson=lesson, user=self.test_leader, course=self.course)
        except LearningResourceNotFoundException:
            self.fail()
        return True


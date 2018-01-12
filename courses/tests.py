# Create your tests here.
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from django.test import TestCase
from courses.manage.courses import get_all, get_courses_from_user, has_user_course, has_course_lesson, \
    get_course_from_id, generate_next_lesson_sequence_number, has_course_sequence_number, \
    get_course_lesson_from_sequence_number, remove_courses_ids_from_user
from courses.manage.lessons import get_lesson_from_id, get_next_lesson, has_next_lesson, \
    remove_lessons_ids_from_course, sequence_lessons
from courses.manage.lessonslearningstylesresources import remove_lessonlearningstyleresources_ids_from_lesson, \
    get_excluded_learning_styles_lesson_resources
from courses.manage.userlessonscompleted import add_user_completed_lesson, get_user_course_completion_percentages
from courses.models import Courses, Lessons, LessonsLearningStylesResources
from learning_styles.models import LearningStyles
from resources.models import Resources


class CoursesManagerTest(TestCase):
    """
    Tests for the Courses Manager that can all be neatly performed with the same test case
    """

    # The test cases constructor will create a test database for test cases i.e. make a user 'test_author' and make a
    #  course 'course')
    def setUp(self):
        """
        Create a series of test cases for the manage Courses library.
        """
        # Manual assignment of primary key.
        self.test_author = User.objects.create_user(id=1,
                                                    username='MrTest', email='test@test.com', password='test')
        self.test_not_an_author = User.objects.create_user(id=2,
                                                           username='MrNotACourseAuthor', email='test2@test.com',
                                                           password='test')
        self.course = Courses.objects.create(author=self.test_author, title="", description="")
        self.empty_course = Courses.objects.create(author=self.test_author, title="", description="")
        self.lesson = Lessons.objects.create(course=self.course, sequence_number=1, title="", description="")

    def test_valid_courses_get_all(self):
        """
        Tests the get_all function contains valid data.
        """
        # Get all courses.
        courses = get_all()
        # Test that the QuerySet object contains the valid author defined in setup.
        self.assertTrue(courses.filter(author=self.test_author).exists())

    def test_invalid_courses_getall(self):
        # Get all courses.
        courses = get_all()
        # Test that the QuerySet object does not contain the invalid author defined in the setup
        self.assertFalse(courses.filter(author=self.test_not_an_author).exists())

    def test_valid_get_courses_from_user(self):
        """
        Test the get_courses_from_user function contains valid data.
        """
        # Get all user courses for our test test_author.
        courses = get_courses_from_user(user=self.test_author)
        # Test that the QuerySet object contains the author course defined in setup.
        self.assertTrue(courses.filter(author=self.test_author).exists())

    def test_invalid_get_courses_from_user(self):
        """
        Test the get_courses_from_user function does not contain invalid data.
        """
        # Get all user courses for our test test_author.
        courses = get_courses_from_user(user=self.test_author)
        # Test that the QuerySet object does not contain the invalid author defined in the setup
        self.assertFalse(courses.filter(author=self.test_not_an_author).exists())

    def test_valid_has_user_course(self):
        """
        Test that the has_user_course function is consistent with whether an author has a course.
        """
        # Validate whether the valid author has the course.
        self.assertTrue(has_user_course(user=self.test_author, course=self.course))

    def test_invalid_has_user_course(self):
        """
        Test that the has_user_course function is consistent with whether a non-author does not have a course.
        """
        # Validate whether the invalid author has the course.
        self.assertFalse(has_user_course(user=self.test_not_an_author, course=self.course))

    def test_valid_has_course_lesson(self):
        """
        Test that the has_course_lesson function is consistent with a course which has a lesson.
        """
        # Validate whether the invalid author has the course.
        self.assertTrue(has_course_lesson(course=self.course, lesson=self.lesson))

    def test_invalid_has_course_lesson(self):
        """
        Test that the has_course_lesson function is consistent with a course which has a lesson.
        """
        # Validate whether the invalid author has the course.
        self.assertFalse(has_course_lesson(course=self.empty_course, lesson=self.lesson))

    def test_valid_get_course_from_id(self):
        """
        Tests whether the course in test data can be retrieved by id.
        """
        self.assertTrue(get_course_from_id(id=1))

    def test_invalid_get_course_from_id(self):
        """
        Tests whether a course not in test data is not retrieved by id.
        """
        try:
            get_course_from_id(id=2)
            # We expect this exception as documented.
        except ObjectDoesNotExist:
            return True

    def test_extreme_invalid_get_course_from_id(self):
        """
        Tests whether a course in test data is not retrieved by id passed a more extreme value.
        """
        try:
            get_course_from_id(id=-1)
            # We expect this exception as documented.
        except AssertionError:
            return True
        self.fail()

    def test_valid_generate_next_lesson_sequence_number(self):
        # Since the test case was built with a sequence number "1" the next number should be "2"
        self.assertEqual(generate_next_lesson_sequence_number(course=self.course), 2)
        # The course without a lesson should generate the next lesson sequence number as "1".
        self.assertEqual(generate_next_lesson_sequence_number(course=self.empty_course), 1)

    def test_valid_has_course_sequence_number(self):
        """
        Tests whether has_course_sequence_number evaluates a course which does has a lesson sequence number as true.
        """
        self.assertTrue(has_course_sequence_number(self.course, sequence_number=1))

    def test_invalid_has_course_sequence_number(self):
        """
        Tests whether has_course_sequence_number evaluates a course which does not have a lesson sequence number as false.
        """
        self.assertFalse(has_course_sequence_number(self.course, sequence_number=2))

    def test_extreme_invalid_has_course_sequence_number(self):
        """
        Tests whether has_course_sequence_number a course has an extreme and invalid sequence number does not fail assertion.
        """
        try:
            has_course_sequence_number(self.course, sequence_number=-1)
            # We expect this exception as documented.
        except AssertionError:
            return True
        self.fail()

    def test_valid_get_course_lesson_from_sequence_number(self):
        """
        Tests whether get_course_lesson_from_sequence_number returns the expected course lesson (the one passed into the test data) when given a sequence number.
        """
        lesson = get_course_lesson_from_sequence_number(course=self.course, sequence_number=1)
        if lesson == self.lesson:
            return True
        self.fail()

    def test_invalid_get_course_lesson_from_sequence_number(self):
        """
        Tests whether get_course_lesson_from_sequence_number returns the expected exception when queried for an
        invalid lesson.
        """
        try:
            get_course_lesson_from_sequence_number(course=self.course, sequence_number=2)
        except ObjectDoesNotExist:
            return True
        self.fail()

    def test_extreme_invalid_get_course_lesson_from_sequence_number(self):
        """
        Tests whether get_course_lesson_from_sequence_number returns the expected assertion error when queried for an
        extreme invalid lesson.
        """
        try:
            get_course_lesson_from_sequence_number(course=self.course, sequence_number=-2)
        except AssertionError:
            return True
        self.fail()


class CoursesManagerRemoveCoursesTest(TestCase):
    """
    Courses Manager Remove Courses tests.
    """

    # The test cases constructor will create a test database for test cases i.e. make a user 'test_author' and make a
    #  course 'course')
    def setUp(self):
        """
        Create a series of test cases for the manage Courses library.
        """
        # Manual assignment of primary key.
        self.test_author = User.objects.create_user(id=1,
                                                    username='MrTest', email='test@test.com', password='test')
        # Create some courses appended to the course built into the test-case
        self.course = Courses.objects.create(author=self.test_author, title="", description="")
        self.course2 = Courses.objects.create(author=self.test_author, title="", description="")
        self.course3 = Courses.objects.create(author=self.test_author, title="", description="")

    def test_extreme_valid_remove_course_ids_from_user(self):
        """
        Tests whether remove_course_ids_from_user removes only specified courses ids and gracefully does not error with
        invalid data (as by design).
        """
        # Get the course ids and remove 2 of them and some junk data.
        remove_courses_ids_from_user(self.test_author, [44, 39, self.course.id, self.course2.id])
        # Query the courses in the users courses set from the test data (self.user) and check that the only remaining
        # course is the course we didn't delete.
        courses = get_courses_from_user(self.test_author)
        if len(courses) == 1 and courses[0] == self.course3:
            return True
        self.fail()

    def test_invalid_remove_course_ids_from_user(self):
        """
        Tests whether remove_course_ids_from_user correctly asserts all ids passed must be a numeric value.
        """
        # Get the course ids and remove 2 of them and some junk data.
        try:
            remove_courses_ids_from_user(self.test_author, ["dsa", "dsa", self.course.id, self.course2.id])
        except AssertionError:
            return True
        self.fail()


class LessonsManagerTest(TestCase):
    """
    Generic Lessons Manager Tests
    """

    def setUp(self):
        """
        Create a series of test cases for the Lessons manager.
        """
        # Manual assignment of primary key.
        self.test_author = User.objects.create_user(id=1,
                                                    username='MrTest', email='test@test.com', password='test')

        self.course = Courses.objects.create(author=self.test_author, title="", description="")
        self.lesson = Lessons.objects.create(course=self.course, sequence_number=1, title="", description="")

    def test_valid_get_lesson_from_id(self):
        """
        Tests whether the lesson in test data can be retrieved by id.
        """
        self.assertTrue(get_lesson_from_id(id=1))

    def test_invalid_get_lesson_from_id(self):
        """
        Tests whether a lesson not in test data is not retrieved by id.
        """
        try:
            get_lesson_from_id(id=444)
            # We expect this exception as documented.
        except ObjectDoesNotExist:
            return True
        self.fail()

    def test_extreme_invalid_get_lesson_from_id(self):
        """
        Tests whether a lesson in test data is not retrieved by id passed a more extreme value.
        """
        try:
            get_lesson_from_id(id=-1)
            # We expect this exception as documented.
        except AssertionError:
            return True
        self.fail()

    def test_invalid_has_next_lesson(self):
        """
        Tests whether the lesson in test data is correctly identified as not having a next sequence member.
        """
        self.assertFalse(has_next_lesson(self.lesson))

    def test_valid_has_next_lesson(self):
        """
        Tests whether the lesson in test data is correctly identified as having a next sequence member when a lesson
        is added.
        """
        # Add the respective lesson to the test case.
        self.lesson2 = Lessons.objects.create(course=self.course, title="", description="", sequence_number=2)
        self.assertTrue(has_next_lesson(self.lesson))

    def test_valid_get_next_lesson(self):
        """
        Tests whether given test data the next lesson in the sequence of lessons for a course are returned validly.
        """
        self.lesson2 = Lessons.objects.create(course=self.course, title="", description="", sequence_number=2)
        self.assertEqual(get_next_lesson(lesson=self.lesson), self.lesson2)

    def test_invalid_get_next_lesson(self):
        """
        Tests whether given test data the next lesson in the sequence of lessons for a course return the expected
        assertion error.
        """
        try:
            self.lesson2 = Lessons.objects.create(course=self.course, title="", description="", sequence_number=2)
            get_next_lesson(lesson=self.lesson2)
        except AssertionError:
            return True
        self.fail()


class LessonsManagerRemoveLessonsTest(TestCase):
    """
    Tests for the Lesson Managers sequencing
    """

    def setUp(self):
        """
        Create a series of test cases for the Lessons manager.
        """

        # Manual assignment of primary key.
        self.test_author = User.objects.create_user(id=1,
                                                    username='MrTest', email='test@test.com', password='test')
        self.course = Courses.objects.create(author=self.test_author, title="", description="")
        self.lesson = Lessons.objects.create(course=self.course, title="", description="", sequence_number=1)
        self.lesson2 = Lessons.objects.create(course=self.course, title="", description="", sequence_number=2)
        self.lesson3 = Lessons.objects.create(course=self.course, title="", description="", sequence_number=3)
        self.lesson4 = Lessons.objects.create(course=self.course, title="", description="", sequence_number=4)

    def test_get_next_lesson(self):
        """
        Tests whether given a more extreme set of test data (a number of lessons for a different course) the next
        lesson in the sequence of lessons for a course are returned validly.
        """

        self.assertEqual(get_next_lesson(lesson=self.lesson), self.lesson2)

    def test_remove_lesson_ids_from_course(self):
        """
        Tests whether remove_lesson_ids_from_courses removes only specified lesson ids.
        """
        # Get the lesson ids and remove 3 of them.
        remove_lessons_ids_from_course(self.course, [self.lesson.id, self.lesson2.id, self.lesson3.id])
        # Query the lessons in the courses set from the test data (self.course) and check that the only remaining
        # lesson is the lesson we didn't delete.
        self.assertEqual(self.course.lessons_set.all()[0], self.lesson4)
        self.assertEqual(self.course.lessons_set.count(), 1)


    def test_invalid_remove_lesson_ids_from_course(self):
        """
        Tests whether remove_lesson_ids_from_courses successfully raises an assertion if a non-id data-type is passed.
        """
        # Reset the Courses object
        self.course = Courses.objects.create(author=self.test_author, title="", description="")
        # Create some lessons appended to the courses object
        self.lesson = Lessons.objects.create(course=self.course, title="", description="", sequence_number=1)
        self.lesson2 = Lessons.objects.create(course=self.course, title="", description="", sequence_number=2)
        self.lesson3 = Lessons.objects.create(course=self.course, title="", description="", sequence_number=3)
        self.lesson4 = Lessons.objects.create(course=self.course, title="", description="", sequence_number=4)
        # Ensure the assertion error is raised
        try:
            remove_lessons_ids_from_course(self.course,
                                           ["Invalid", "Invalid", self.lesson.id, self.lesson2.id, self.lesson3.id])
        except AssertionError:
            return True
        self.fail()


class LessonsManagerSequencingTest(TestCase):
    """
    Tests for the Lesson Managers sequencing
    """

    def setUp(self):
        """
        Create a series of test cases
        """
        # Manual assignment of primary key.
        self.test_author = User.objects.create_user(id=1,
                                                    username='MrTest', email='test@test.com', password='test')

        self.course = Courses.objects.create(author=self.test_author, title="", description="")
        self.lesson = Lessons.objects.create(course=self.course, sequence_number=1, title="", description="")
        self.lesson2 = Lessons.objects.create(course=self.course, sequence_number=2, title="", description="")
        self.lesson3 = Lessons.objects.create(course=self.course, sequence_number=4, title="", description="")

    def test_sequence_lessons(self):
        """
        Tests whether the sequence_lessons method validly sequences lessons.
        """
        course = self.course
        sequence_lessons(course)
        # Because the function saves to the *database* we need to get lesson3 back from the database (so Django
        # updates what it has in memory during the test)
        lesson = Lessons.objects.get(id=self.lesson3.id)
        self.assertEqual(lesson.sequence_number, 3)

    def test_extreme_sequence_lessons(self):
        """
        Tests whether the sequence_lessons method validly sequences lessons in an extreme case (with dodgy database data).
        """
        # Load in fresh data
        self.course = Courses.objects.create(author=self.test_author, title="", description="")
        self.lesson = Lessons.objects.create(course=self.course, sequence_number=888, title="", description="")
        self.lesson2 = Lessons.objects.create(course=self.course, sequence_number=-56, title="", description="")
        self.lesson3 = Lessons.objects.create(course=self.course, sequence_number=699, title="", description="")
        sequence_lessons(self.course)
        # Because the function saves to the *database* we need to get lesson3 back from the database (so Django
        # updates what it has in memory during the test)
        self.lesson3 = Lessons.objects.get(id=self.lesson3.id)
        # This should be sequence 2 as the second biggest
        self.assertEqual(self.lesson3.sequence_number, 2)


class LessonsLearningStyleResourcesManagerTest(TestCase):
    """
    Tests for the LessonsLearningStyleResourcesManager
    """

    def setUp(self):
        """
        Create a series of test cases
        """
        # Manual assignment of primary key.
        self.test_author = User.objects.create_user(id=1,
                                                    username='MrTest', email='test@test.com', password='test')
        self.course = Courses.objects.create(author=self.test_author, title="", description="")
        self.lesson = Lessons.objects.create(course=self.course, title="", description="", sequence_number=1)
        # There just isn't a clean way to test Django file fields unfortunately.
        self.file = "foo"
        # Create a resource
        self.resource = Resources.objects.create(file=self.file)
        # Create some learning styles
        self.active_style = LearningStyles.objects.create(name="Active")
        self.reflective_style = LearningStyles.objects.create(name="Reflective")

        # Create lessons learning style resources object
        self.lessonslearningstyleresources = LessonsLearningStylesResources.objects.create(lesson=self.lesson,
                                                                                           learning_style=self.active_style,
                                                                                           resource=self.resource
                                                                                           , title="", description="")

    def test_remove_lessonlearningstyleresources_ids_from_lesson(self):
        """
        Tests for the successful removal of lesson learning style resources from a lesson.
        """
        # Pass in the test case
        ids = [1]
        remove_lessonlearningstyleresources_ids_from_lesson(self.lesson, ids)
        # Value should equal 0 after removing all resources
        self.assertEqual(LessonsLearningStylesResources.objects.all().count(), 0)

    def test_extreme_remove_lessonlearningstyleresources_ids_from_lesson(self):
        """
        Tests for the successful removal of lesson learning style resources from a lesson extemely
        """
        self.resource2 = Resources.objects.create(file=self.file)
        self.resource3 = Resources.objects.create(file=self.file)
        self.resource4 = Resources.objects.create(file=self.file)
        self.resource5 = Resources.objects.create(file=self.file)

        LessonsLearningStylesResources.objects.create(lesson=self.lesson, learning_style=self.active_style,
                                                      resource=self.resource2
                                                      , title="", description="")

        LessonsLearningStylesResources.objects.create(lesson=self.lesson, learning_style=self.active_style,
                                                      resource=self.resource3
                                                      , title="", description="")

        LessonsLearningStylesResources.objects.create(lesson=self.lesson, learning_style=self.active_style,
                                                      resource=self.resource4
                                                      , title="", description="")

        LessonsLearningStylesResources.objects.create(lesson=self.lesson, learning_style=self.active_style,
                                                      resource=self.resource5
                                                      , title="", description="")

        # Pass in the test case
        ids = [1, 2, 3, 4, 5]
        remove_lessonlearningstyleresources_ids_from_lesson(self.lesson, ids)
        # Value should equal 0 after removing all resources
        self.assertEqual(LessonsLearningStylesResources.objects.all().count(), 0)

    def test_get_excluded_learning_styles_lesson_resources(self):
        """
        Tests whether excluded resources are successfully identified
        """
        # Pass in the test case
        self.resource2 = Resources.objects.create(file=self.file)
        self.resource3 = Resources.objects.create(file=self.file)
        self.resource4 = Resources.objects.create(file=self.file)
        self.resource5 = Resources.objects.create(file=self.file)

        LessonsLearningStylesResources.objects.create(lesson=self.lesson, learning_style=self.active_style,
                                                      resource=self.resource2
                                                      , title="", description="")

        LessonsLearningStylesResources.objects.create(lesson=self.lesson, learning_style=self.active_style,
                                                      resource=self.resource3
                                                      , title="", description="")

        LessonsLearningStylesResources.objects.create(lesson=self.lesson, learning_style=self.active_style,
                                                      resource=self.resource4
                                                      , title="", description="")

        LessonsLearningStylesResources.objects.create(lesson=self.lesson, learning_style=self.reflective_style,
                                                      resource=self.resource5
                                                      , title="", description="")

        # Get all the lessons learning style resources except self.resource5.
        learningstyles = [self.active_style]
        # Get resources
        resources = get_excluded_learning_styles_lesson_resources(learningstyles, self.lesson)
        # Check its equal to the expected value
        self.assertEqual(resources.count(), 1)


class UsersLessonsCompletedManagerTest(TestCase):
    """
    Tests for custom methods for UserLessonsProgressManager.
    """

    def setUp(self):
        """
        Create a series of test cases.
        """
        # Manual assignment of primary key.
        self.test_user = User.objects.create_user(id=1,
                                                  username='MrTest', email='test@test.com', password='test')
        # Create some learning styles
        self.active_style = LearningStyles.objects.create(name="Active")
        self.reflective_style = LearningStyles.objects.create(name="Reflective")
        self.course = Courses.objects.create(author=self.test_user, title="", description="")
        self.lesson = Lessons.objects.create(course=self.course, sequence_number=1, title="", description="")
        self.lesson2 = Lessons.objects.create(course=self.course, sequence_number=2, title="", description="")
        self.lesson3 = Lessons.objects.create(course=self.course, sequence_number=3, title="", description="")
        self.lesson4 = Lessons.objects.create(course=self.course, sequence_number=4, title="", description="")
        self.lesson5 = Lessons.objects.create(course=self.course, sequence_number=5, title="", description="")


    def test_get_user_course_completion_percentages(self):
        # Test the course completion percentage is equal to 100
        courses = [self.course]
        # Simple function to add a user has completed a lesson using Django.
        # Iterative validation
        add_user_completed_lesson(self.test_user, self.lesson)
        # Percentages returns a dictionary.
        percentages = get_user_course_completion_percentages(self.test_user, courses)
        self.assertEqual(percentages.get(1), ((1/5)*100))
        add_user_completed_lesson(self.test_user, self.lesson2)
        # Refresh Percentages
        percentages = get_user_course_completion_percentages(self.test_user, courses)
        self.assertEqual(percentages.get(1), ((2/5)*100))
        add_user_completed_lesson(self.test_user, self.lesson3)
        # Refresh Percentages
        percentages = get_user_course_completion_percentages(self.test_user, courses)
        self.assertEqual(percentages.get(1), (3/5)*100)
        add_user_completed_lesson(self.test_user, self.lesson4)
        # Refresh Percentages
        percentages = get_user_course_completion_percentages(self.test_user, courses)
        self.assertEqual(percentages.get(1), (4/5)*100)
        add_user_completed_lesson(self.test_user, self.lesson5)
        # Refresh Percentages
        percentages = get_user_course_completion_percentages(self.test_user, courses)
        self.assertEqual(percentages.get(1), (5/5)*100)



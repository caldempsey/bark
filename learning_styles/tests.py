
from django.contrib.auth.models import User
from django.test import TestCase

from learning_styles.manage.userlearningstyles import add_to_user_userlearningstyles_collection, \
    get_user_learning_styles_from_user
from learning_styles.models import LearningStyles, UserLearningStyles


class UsersLearningStylesManagerTest(TestCase):
    """
    Tests for UserLessonsCompletedManager
    """

    def setUp(self):
        """
        Create a series of test cases.
        """
        # Manual assignment of primary key.
        self.test_user = User.objects.create_user(id=2,
                                                  username='MrTest', email='test@test.com', password='test')
        # Create some learning styles
        self.active_style = LearningStyles.objects.create(name="Active")
        self.reflective_style = LearningStyles.objects.create(name="Reflective")

    def test_add_to_user_userlearningstyles_collection(self):
        """
        Test whether we can add a collection of userlearningstyles to a user.
        """
        # Create a collection of learning styles
        collection = [self.active_style, self.reflective_style]
        # Add the collection
        add_to_user_userlearningstyles_collection(self.test_user, collection)
        # Check if value is expected value.
        self.assertEqual(UserLearningStyles.objects.filter(user=self.test_user).count(), 2)


    def test_get_user_learning_styles_from_user(self):
        """
        Test whether we can successfully get the user learning styles of a user.
        """
        # Create a collection of learning styles
        collection = [self.active_style, self.reflective_style]
        # Check if each item in styles is equal to the function
        add_to_user_userlearningstyles_collection(self.test_user, collection)
        # Get the collection back assuming its equal to the one passed.
        self.assertEqual(get_user_learning_styles_from_user(self.test_user), collection)
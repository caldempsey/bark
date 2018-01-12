from django.contrib.auth.models import User
from django.test import TestCase

from roles.manage.roles import has_user_leader_role
from roles.models import UserRoles


class RoleManagerTest(TestCase):
    """
    Tests for the Roles model.
    """

    def setUp(self):
        User.objects.create()
        # Manual assignment of primary key.
        self.test_user = User.objects.create_user(id=1,
                                                  username='MrTest', email='test@test.com', password='test')

    def test_user_roles_has_leader(self):
        self.assertFalse(has_user_leader_role(self.test_user))
        UserRoles.objects.create(user=self.test_user, role="leader")
        self.assertTrue(has_user_leader_role(self.test_user))

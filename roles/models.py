from django.contrib.auth.models import User
from django.core.validators import MaxLengthValidator
from django.db import models


class UserRoles(models.Model):
    """
    The UserRoles model is responsible for providing a lookup for roles for each user kind.
    This model will correspond to a UserRoles table in the database with associative attributes.
    This is intended for administrative use only.
    """
    # Make the User model a foreign key.
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    # The role (with a max-length validator).
    role = models.CharField(max_length=15, validators=[MaxLengthValidator(15)])

    class Meta:
        """
        Meta tag of the UserRoles model, changes the name in the Django Administrator interface.
        """
        verbose_name_plural = "User Roles"

    def __str__(self):
        """
        The class to a string (similar to the toString method).
        :return: Returns a string representation of the object.
        """
        string = str(self.user)
        return string + " : " + self.role

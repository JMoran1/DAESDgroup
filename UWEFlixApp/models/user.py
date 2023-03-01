from django.contrib.auth.models import AbstractUser, Group
from django.db import models


class User(AbstractUser):
    class Role(models.TextChoices):
        CINEMA_MANAGER = 'M', 'Cinema Manager'
        ACCOUNT_MANAGER = 'A', 'Account Manager'
        CLUB_REP = 'R', 'Club Representative'
        CUSTOMER = 'C', 'Customer'

    role = models.CharField(
        max_length=1,
        choices=Role.choices,
        default=Role.CUSTOMER
    )

    @classmethod
    def get_role_groups(cls):
        """
        Retrieves all the Groups which are specifically for User Roles
        """
        return Group.objects.filter(name__in=(r.label for r in cls.Role))

    def set_correct_groups_for_role(self):
        """
        the easiest way is to just go through the list of Groups for this User
        that are Role Groups and make sure that it only consists of one Group,
        the one for the current Role
        """
        # query current group because we'll reuse it a few times
        current_group = Group.objects.get(name=self.role.label)
        # drop any Groups which are User Role Groups not for our User Role
        self.groups.remove(*Group.objects.exclude(id=current_group.id).union(User.get_role_groups()))
        # make sure our groups include the Group for this User Role
        if not self.groups.contains(current_group):
            self.groups.add(current_group)

    def save(self, *args, **kwargs):
        """
        Override .save() to ensure that this User always has the mandated Group
        for its Role type set, and none of the other Groups for other Role types
        (note that other Groups which are not assigned to Roles are left as-is).
        """
        super().save(*args, **kwargs)  # call super first to get an ID
        # enforce correct group membership
        self.set_correct_groups_for_role()
        # NOTE: there is no need to re-save after this, m2m commits immediately

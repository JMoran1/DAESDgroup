from django.contrib.auth.models import AbstractUser, Group
from django.core.exceptions import ValidationError
from django.db import models
from django.db.models import Q


class Role(models.TextChoices):
    CINEMA_MANAGER = 'M', 'Cinema Manager'
    ACCOUNT_MANAGER = 'A', 'Account Manager'
    CLUB_REP = 'R', 'Club Representative'
    STUDENT = 'S', 'Student'


class User(AbstractUser):
    Role = Role

    role = models.CharField(
        max_length=1,
        choices=Role.choices,
        default=Role.STUDENT
    )
    club = models.ForeignKey(
        'club',
        blank=True,
        null=True,
        on_delete=models.SET_NULL  # deleting a Club unlinks any Users from it
    )

    class Meta:
        constraints = (
            models.CheckConstraint(
                # Logically: (Role EQUALS Club Rep) IMPLIES (Club EXISTS)
                # AKA: (NOT CLUB_REP) OR CLUB EXISTS
                check= ~Q(role=Role.CLUB_REP) | Q(club__isnull=True),
                name='club_reps_have_club',
                violation_error_message='Club Rep must have a Club!'
            ),
        )

    @classmethod
    def get_role_groups(cls):
        """
        Retrieves all the Groups which are specifically for User Roles
        """
        return Group.objects.filter(name__in=(r.label for r in cls.Role))

    @classmethod
    def sanitise_groups(cls, group_qs, role):
        """
        Sanitises a given Group Many-to-Many manager queryset to make sure it
        only contains Role-Groups for the given role
        """
        # query current group because we'll reuse it a few times
        current_group = Group.objects.get(name=role.label)
        # drop any inadvertently-added invalid Role-Groups
        groups_excluding_invalid_roles = group_qs.exclude(
            id__in=User.get_role_groups().exclude(id=current_group.id)
        )
        # force the inclusion of the valid Role-Group in case it was removed
        groups_excluding_invalid_roles |= Group.objects.filter(id=current_group.id)
        return groups_excluding_invalid_roles

    def set_correct_groups_for_role(self):
        """
        the easiest way is to just go through the list of Groups for this User
        that are Role Groups and make sure that it only consists of one Group,
        the one for the current Role
        """
        self.groups.set(User.sanitise_groups(self.groups, User.Role(self.role)))

    def save(self, *args, **kwargs):
        """
        Override .save() to ensure that this User always has the mandated Group
        for its Role type set, and none of the other Groups for other Role types
        (note that other Groups which are not assigned to Roles are left as-is).
        """
        # if creating a new superuser, make them a CINEMA_MANAGER
        if self.id is None and self.is_superuser:
            self.role = User.Role.CINEMA_MANAGER
        super().save(*args, **kwargs)  # call super first to get an ID
        # enforce correct group membership
        self.set_correct_groups_for_role()
        # NOTE: there is no need to re-save after this, m2m commits immediately

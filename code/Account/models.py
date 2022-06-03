from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core.validators import RegexValidator
from django.utils.translation import gettext_lazy as _
from .managers import CustomManager


class User(AbstractBaseUser, PermissionsMixin):
    username = models.CharField(
        max_length=30,
        blank=False,
        null=False,
        unique=True,
        verbose_name=_('Username'),
    )
    email = models.EmailField(
        max_length=75,
        blank=False,
        null=False,
        unique=True,
        verbose_name=_("Email Address")
    )
    phone_regex = RegexValidator(
        regex=r'^(\+\d{1,3})?,?\s?\d{8,13}',
        message=_("Enter Correct Phone Number Format ! 20 digits allowed.")
    )
    phone = models.CharField(
        max_length=20,
        null=True,
        blank=True,
        unique=True,
        validators=[phone_regex],
        verbose_name=_("Phone Number"),
    )
    date_joined = models.DateTimeField(
        auto_now_add=True,
        verbose_name=_("Date Joined")
    )
    last_update = models.DateTimeField(
        auto_now=True,
        verbose_name=_("Last Update")
    )
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = CustomManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['email', ]

    def __str__(self):
        return self.username


class Profile(models.Model):
    CHOICES_GENDER = (
        ("M", "Man"),
        ("F", "Female")
    )
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
        blank=False,
        null=False,
        related_name='profile',
        verbose_name=_("My User")

    )
    first_name = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name=_("First Name")
    )
    last_name = models.CharField(
        max_length=30,
        blank=True,
        null=True,
        verbose_name=_("Last Name")
    )
    date_of_birth = models.DateField(
        blank=True,
        null=True,
        verbose_name=_("Date of Birth")
    )
    image = models.ImageField(
        upload_to='profile_image',
        blank=True,
        null=True,
        verbose_name=_("Profile Image")
    )
    gender = models.CharField(
        max_length=1,
        choices=CHOICES_GENDER,
        null=True,
        blank=True,
        verbose_name=_("Gender")
    )
    last_update = models.DateTimeField(auto_now=True)

    def get_fullname(self):
        return "{} {}".format(self.first_name, self.last_name)

    def __str__(self):
        return "{} {}".format("Profile:", self.user.username)

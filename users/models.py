from django.conf import settings
from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth import models as auth_models
from django.core.mail import send_mail
from django.db import models
from django.utils import timezone
from django.utils.translation import get_language, gettext_lazy as _
from model_utils.choices import Choices
from model_utils.tracker import FieldTracker


class UserManager(BaseUserManager):

    use_in_migrations = True

    def get_by_natural_key(self, email):
        return self.get(email=email)

    def _create_user(self, email, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, **extra_fields)


class AbstractUser(AbstractBaseUser, auth_models.PermissionsMixin):
    """ Get rid of username. """

    first_name = models.CharField(
        _('first name'),
        max_length=250,
        null=True, blank=True,
    )
    middle_name = models.CharField(
        _('middle name'),
        max_length=250,
        null=True, blank=True,
    )
    last_name = models.CharField(
        _('last name'),
        max_length=250,
        null=True, blank=True,
    )
    email = models.EmailField(
        _('email address'),
        unique=True,
    )
    is_email_verified = models.BooleanField(
        _('is email address verified?'),
        default=False,
    )
    is_staff = models.BooleanField(
        _('staff status'),
        default=False,
    )
    is_active = models.BooleanField(
        _('active'),
        default=True,
    )
    date_joined = models.DateTimeField(
        _('date joined'),
        default=timezone.now,
    )

    objects = UserManager()

    EMAIL_FIELD = 'email'
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        abstract = True

    def clean(self):
        super().clean()
        self.email = self.__class__.objects.normalize_email(self.email)

    def get_full_name(self):
        """
        Return the first_name + the middle name + the last_name,
        with a space in between.
        """
        full_name = ' '.join(
            filter(
                lambda x: x is not None, [
                    self.first_name, self.middle_name, self.last_name,
                ]
            )
        )
        return full_name.strip() or self.email

    def get_short_name(self):
        """Return the short name for the user."""
        try:
            return self.get_full_name().split()[0]
        except IndexError:
            return self.email

    def email_user(self, subject, message, from_email=None, **kwargs):
        """Send an email to this user."""
        send_mail(subject, message, from_email, [self.email], **kwargs)


class User(AbstractUser):

    languages = Choices(*settings.LANGUAGES)

    language = models.CharField(
        _('Language'),
        max_length=5,
        choices=languages,
        default=settings.LANGUAGE_CODE,
    )

    tracker = FieldTracker(fields=('language', ))

    def set_language(self, language: str):
        self.language = language
        self.save()


class AnonymousUser(auth_models.AnonymousUser):

    @property
    def language(self):
        return get_language() or settings.LANGUAGE_CODE

    def set_language(self, language: str):
        pass


auth_models.AnonymousUser = AnonymousUser


class Group(auth_models.Group):

    class Meta:
        proxy = True
        verbose_name = _('group')
        verbose_name_plural = _('groups')

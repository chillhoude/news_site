from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from .managers import CustomUserManager



class CustomUser(AbstractBaseUser,PermissionsMixin):
    customuser= None
    username = models.CharField(_("username"),max_length=20,unique=True)
    first_name = models.CharField(_("Фамилия"), max_length=50,null=True, blank=True)
    last_name = models.CharField(_("Имя"), max_length=50,null=True, blank=True)
    reputation = models.IntegerField(_("Репутация"),default = 0)
    avatar = models.ImageField(_("Аватарка"),upload_to='media/avatar',default="avatar_none.png")
    email = models.EmailField(_("email address"), blank=True,null=True)
    is_staff = models.BooleanField(
        _("staff status"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
        )
    is_journalist = models.BooleanField(
        _("Статус журналиста"),
        default=False,
        help_text=_("Designates whether the user can log into this admin site."),
        )
    is_active = models.BooleanField(
        _("active"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
        )
    is_superuser = models.BooleanField(
        _("superuser status"),
        default=False,
        help_text=_(
            "Designates whether this user should be treated as active. "
            "Unselect this instead of deleting accounts."
        ),
        )
    date_joined = models.DateTimeField(
        _("date joined"),
        default=timezone.now
        )

    USERNAME_FIELD = 'username'

    REQUIRED_FIELDS = []

    objects = CustomUserManager()


    class Meta:
        verbose_name= 'User'
        verbose_name_plural= 'User'
    def __str__(self):
        return self.username

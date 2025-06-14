from django.db import models
from django.contrib.auth.models import (BaseUserManager, AbstractBaseUser, PermissionsMixin)
from django.utils.translation import gettext_lazy as _


class UserManager(BaseUserManager):
    def _create_user(self, email, account_id, password, **extra_fields):
        email = self.normalize_email(email)
        user = self.model(email=email, id=account_id, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_user(self, email, account_id, password=None, **extra_fields):
        extra_fields.setdefault('is_active', True)
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(
            email=email,
            id=account_id,
            password=password,
            **extra_fields,
        )

    def create_superuser(self, email, account_id, password, **extra_fields):
        extra_fields['is_active'] = True
        extra_fields['is_staff'] = True
        extra_fields['is_superuser'] = True
        return self._create_user(
            email=email,
            id=account_id,
            password=password,
            **extra_fields,
        )

class User(AbstractBaseUser, PermissionsMixin):
    id = models.AutoField(
        primary_key=True
    )  # わかりやすさ重視でUUIDではなく連番
    email = models.EmailField(
        verbose_name=_("email"),
        unique=True
    )
    name = models.CharField(
        verbose_name=_("name"),
        max_length=150,
        null=True,
        blank=False
    )
    birth_date = models.DateField(
        verbose_name=_("birth_date"),
        blank=True,
        null=True
    )
    is_superuser = models.BooleanField(
        verbose_name=_("is_superuer"),
        default=False
    )
    is_staff = models.BooleanField(
        verbose_name=_('staff status'),
        default=False,
    )
    is_active = models.BooleanField(
        verbose_name=_('active'),
        default=True,
    )
    created_at = models.DateTimeField(
        verbose_name=_("created_at"),
        auto_now_add=True
    )
    updated_at = models.DateTimeField(
        verbose_name=_("updateded_at"),
        auto_now=True
    )

    objects = UserManager()

    # USERNAME_FIELD = 'id' # ログイン時、ユーザー名の代わりにaccount_idを使用
    USERNAME_FIELD = 'email' # ログイン時、ユーザー名の代わりにemailを使用
    REQUIRED_FIELDS = ['email']  # スーパーユーザー作成時にemailも設定する

    def __str__(self):
        return self.id

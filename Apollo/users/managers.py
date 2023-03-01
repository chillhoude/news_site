from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):

    def create_user(self, username, password):
        if not username:
            raise ValueError('Users must have an username')
        user = self.model(
            username=self.normalize_email(username),
        )
        user.is_active = True
        user.is_staff = False
        user.is_journalist = False
        user.is_admin = False
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, password):
        user = self.create_user(
            username,
            password=password,
        )
        user.is_staff = True
        user.is_superuser = True
        user.is_active = True
        user.save(using=self._db)
        return user
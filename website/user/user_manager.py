from django.contrib.auth.base_user import BaseUserManager


class CustomUserManager(BaseUserManager):
    # Uses email as unique identifier and login
    def create_user(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email cannot be empty.")
        email = self.normalize_email(email) #Normalizes email addresses by lowercasing the domain portion of the email address
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **extra_fields):
        if not email:
            raise ValueError("Email cannot be empty.")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.is_superuser = True
        user.save()
        return user

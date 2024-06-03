from django.contrib.auth.models import BaseUserManager as BUM


class UserManager(BUM):
    def create_user(self, phone_number: str, password, date_birth=None, full_name: str = None):
        user = self.model(phone_number=phone_number, date_birth=date_birth, full_name=full_name)
        # email=self.normalize_email(email))
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, phone_number: str, password, date_birth=None, full_name: str = None):
        user = self.create_user(
            # phone_number=phone_number, date_birth=date_birth, name=name, email=self.normalize_email(email),
            phone_number=phone_number, date_birth=date_birth, full_name=full_name, password=password
        )
        user.is_admin = True
        user.save()
        return user

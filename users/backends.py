from django.contrib.auth import get_user_model
from django.contrib.auth.backends import ModelBackend

UserModel = get_user_model()


class EmailBackend(ModelBackend):
    """
    Authenticates against settings.AUTH_USER_MODEL, using email and password.
    """

    def authenticate(self, request, username=None, password=None, **kwargs):
        email = username or kwargs.get(UserModel.EMAIL_FIELD)

        try:
            user = UserModel._default_manager.get(
                **{UserModel.EMAIL_FIELD: email}
            )
        except UserModel.DoesNotExist:
            # Run the default password hasher once to reduce the timing
            # difference between an existing and a nonexistent user (#20760).
            UserModel().set_password(password)
        else:
            if (
                user.check_password(password)
                and self.user_can_authenticate(user)
            ):
                return user

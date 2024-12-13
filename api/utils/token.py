from django.contrib.auth.tokens import PasswordResetTokenGenerator


class CustomTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, value, timestamp):
        return f"{value.pk}{timestamp}"


custom_token_generator = CustomTokenGenerator()

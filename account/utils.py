from django.contrib.auth.tokens import PasswordResetTokenGenerator
from six import text_type

class AccountActivationTokenGenerator(PasswordResetTokenGenerator):
	def _make_hash_value(self, user, timestamp):
		return(
			text_type(user.pk) + text_type(timestamp) + text_type(user.is_active)
		)
class TokenGenerator(PasswordResetTokenGenerator):
	pass

generate_token = TokenGenerator()
account_activation_token = AccountActivationTokenGenerator()
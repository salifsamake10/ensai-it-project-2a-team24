import base64
import hashlib
import hmac
import os


ITERATIONS = 600_000


def hash_password(password: str) -> str:
	salt = os.urandom(16)
	digest = hashlib.pbkdf2_hmac("sha256", password.encode(), salt, ITERATIONS)
	return "pbkdf2_sha256${}${}${}".format(
		ITERATIONS,
		base64.urlsafe_b64encode(salt).decode(),
		base64.urlsafe_b64encode(digest).decode(),
	)


def verify_password(password: str, encoded: str) -> bool:
	try:
		scheme, iterations, salt, expected = encoded.split("$", 3)
		if scheme != "pbkdf2_sha256":
			return False
		digest = hashlib.pbkdf2_hmac(
			"sha256",
			password.encode(),
			base64.urlsafe_b64decode(salt.encode()),
			int(iterations),
		)
		return hmac.compare_digest(
			base64.urlsafe_b64encode(digest).decode(), expected
		)
	except (ValueError, TypeError):
		return False
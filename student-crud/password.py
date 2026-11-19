import string 
import secrets

def password(len):
  all_digits = string.ascii_letters + string.digits + string.punctuation
  password = ''.join(secrets.choice(all_digits) for _ in range(len))
  return password
import re

def password_validation(password):
    # check for minimum length
    if len(password) < 8:
        return False, "password must be at leat 8 characters long"
    # check for at least one uppercase letter
    if not re.search(r'[A-Z]', password):
        return False, "password must contain at least one uppercase letter"
    # check for at least one lowercase letter
    if not re.search(r'[a-z]', password):
        return False, "password must contain at least one lowercase letter"
    # check for at least one digit
    if not re.search(r'\d', password):
        return False, "password must contain at least one digit"
    # check for at least one special character
    if not re.search(r'[!@#$%^&*(),.?":{}/<>]', password):
        return False, "password must contain at least one special character"
    # retur True if all conditions are met
    return True, "Password is valid"


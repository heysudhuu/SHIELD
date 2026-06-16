import secrets
import string

def generate_password(length=16, use_uppercase=True, use_lowercase=True, use_digits=True, use_special=True):
    """
    Generates a cryptographically secure random password based on the selected criteria.
    Ensures that at least one character from each selected class is included in the output.
    """
    if length < 4:
        # Minimum sensible length to satisfy inclusion of all classes if all are selected
        length = 4

    categories = []
    pool = ""

    if use_uppercase:
        categories.append(string.ascii_uppercase)
        pool += string.ascii_uppercase
    if use_lowercase:
        categories.append(string.ascii_lowercase)
        pool += string.ascii_lowercase
    if use_digits:
        categories.append(string.digits)
        pool += string.digits
    if use_special:
        special_chars = "!@#$%^&*()_+-=[]{}|;:,.<>?"
        categories.append(special_chars)
        pool += special_chars

    if not pool:
        raise ValueError("At least one character type must be selected.")

    # Step 1: Ensure at least one character from each selected category is included
    password_chars = [secrets.choice(cat) for cat in categories]

    # Step 2: Fill the rest of the password length from the entire pool
    remaining_length = length - len(password_chars)
    for _ in range(remaining_length):
        password_chars.append(secrets.choice(pool))

    # Step 3: Shuffle the character list using SystemRandom to avoid predictable positions
    sr = secrets.SystemRandom()
    sr.shuffle(password_chars)

    return "".join(password_chars)

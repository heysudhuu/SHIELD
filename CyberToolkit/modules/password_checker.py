import re

def check_password_strength(password):
    """
    Checks the strength of a password based on length, uppercase, lowercase, numbers, and special characters.
    Returns a dictionary containing the score (0-5), strength rating, and detailed feedback checks.
    """
    feedback = {
        "length": False,
        "uppercase": False,
        "lowercase": False,
        "digits": False,
        "special": False
    }
    
    # 1. Length Check (>= 10 characters)
    if len(password) >= 10:
        feedback["length"] = True
        
    # 2. Uppercase Check
    if re.search(r"[A-Z]", password):
        feedback["uppercase"] = True
        
    # 3. Lowercase Check
    if re.search(r"[a-z]", password):
        feedback["lowercase"] = True
        
    # 4. Digits Check
    if re.search(r"\d", password):
        feedback["digits"] = True
        
    # 5. Special Characters Check
    special_pattern = re.compile(r"[!@#$%^&*()_+=\-[\]{}|;:,.<>?]")
    if special_pattern.search(password):
        feedback["special"] = True
        
    # Calculate score
    score = sum(1 for value in feedback.values() if value)
    
    # Map score to strength
    if score <= 2:
        strength = "Weak"
    elif score <= 4:
        strength = "Medium"
    else:
        strength = "Strong"
        
    return {
        "score": score,
        "strength": strength,
        "checks": feedback
    }

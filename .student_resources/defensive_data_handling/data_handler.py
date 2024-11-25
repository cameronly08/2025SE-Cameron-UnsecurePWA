##############################################
# RE = RegExr = Regular Expressions          #
# Read the documentation and tutorials       #
# https://docs.python.org/3/library/re.html  #
# https://docs.python.org/3/howto/regex.html #
##############################################
import re
import html
import bcrypt


# A simple password check function that checks if the password is valid
def example_checker() -> str:
    username = request.form["username"]
    password = request.form["password"]
    isLoggedIn = dbHandler.retrieveUsers(username, password)
    
    if len(password) < 9 or len(password) > 12:
        return "Password must be between 9 and 12 characters."
    if not password.isalnum():
        return "Password must be alphanumeric."
    if len(re.findall(r'[A-Z]', password)) > 4:
        return "Password must not contain more than 4 uppercase letters."
    if len(re.findall(r'[a-z]', password)) > 4:
        return "Password must not contain more than 4 lowercase letters."
    if len(re.findall(r'[0-9]', password)) > 3:
        return "Password must not contain more than 3 digits."
    
    return "Password is valid."


# A more pythonic way to check the password is valid that manages exceptions
def check_password(password: str) -> bytes:
    if not issubclass(type(password), str):
        raise TypeError("Expected a string")
    if len(password) < 8:
        raise ValueError("less than 8 characters")
    if len(password) > 20:
        raise ValueError("more than 10 characters")
    if re.search(r"[ ]", password):
        raise ValueError("contains ' ' space characters")
    if not re.search(r"[A-Z]", password):
        raise ValueError("does not contain uppercase letters")
    if not re.search(r"[a-z]", password):
        raise ValueError("does not contain lowercase letters")
    if not re.search(r"[0-9]", password):
        raise ValueError("does not contain a digit '0123456789'")
    if not re.search(r"[@$!%*?&]", password):
        raise ValueError("does not contain one of '@$!%*?&' special characters")
    # Password is returned encoded so it can't be accidently logged in a human readable format
    return password.encode()


# Function to sanitise text manually
def replace_characters(input_string: str) -> str:
    to_replace = ["<", ">", ";"]
    replacements = ["%3C", "%3E", "%3B"]
    char_list = list(input_string)
    for i in range(len(char_list)):
        if char_list[i] in to_replace:
            index = to_replace.index(char_list[i])
            char_list[i] = replacements[index]


# Function to sanitise text using a library
def make_web_safe(string: str) -> str:
    return html.escape(string)


# Simple function to check if an email is valid
def check_email(email: str) -> bool:
    if re.fullmatch(r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)", email):
        return True
    else:
        return False


# A simple function to check a name is valid
def validate_name(name: str) -> bool:
    # Check if the name is valid (only alphabets allowed).
    if not name.isalpha():
        return False
    return True


# A simple function to check a number is valid
def validate_number(number: str) -> bool:
    # Check if the name is valid (only alphabets allowed).
    if number.isalpha():
        return False
    return True


# Function to salt a hash input
def salt_and_hash(password: str) -> bytes:
    return  # to be implemented


    
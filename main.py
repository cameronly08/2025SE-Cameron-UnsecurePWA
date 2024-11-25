from flask import Flask, render_template, request, redirect
import user_management as dbHandler
import re

app = Flask(__name__)

def replace_characters(input_string: str) -> str:
    to_replace = ["<", ">", ";"]
    replacements = ["%3C", "%3E", "%3B"]
    char_list = list(input_string)
    for i in range(len(char_list)):
        if char_list[i] in to_replace:
            index = to_replace.index(char_list[i])
            char_list[i] = replacements[index]
    return ''.join(char_list)

def example_checker(username: str, password: str) -> str:
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

@app.route("/success.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def addFeedback():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        feedback = request.form["feedback"]
        sanitized_feedback = replace_characters(feedback)
        dbHandler.insertFeedback(sanitized_feedback)
        dbHandler.listFeedback()
        return render_template("/success.html", state=True, value="Back")
    else:
        dbHandler.listFeedback()
        return render_template("/success.html", state=True, value="Back")

@app.route("/signup.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
def signup():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        DoB = request.form["dob"]
        
        # Validate the password
        validation_result = example_checker(username, password)
        print(f"Validation result: {validation_result}")
        if validation_result != "Password is valid.":
            print(f"Validation failed: {validation_result}")
            return render_template("signup.html", error=validation_result)
        
        print(f"Inserting user: {username}")
        try:
            dbHandler.insertUser(username, password, DoB)
            print(f"User {username} inserted successfully")
        except Exception as e:
            print(f"Error inserting user: {e}")
            return render_template("signup.html", error="Error inserting user")
        
        return redirect("/index.html")
    else:
        return render_template("/signup.html")

@app.route("/index.html", methods=["POST", "GET", "PUT", "PATCH", "DELETE"])
@app.route("/", methods=["POST", "GET"])
def home():
    if request.method == "GET" and request.args.get("url"):
        url = request.args.get("url", "")
        return redirect(url, code=302)
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        isLoggedIn = dbHandler.retrieveUsers(username, password)
        if isLoggedIn:
            dbHandler.listFeedback()
            return render_template("/success.html", value=username, state=isLoggedIn)
        else:
            return render_template("/index.html")
    else:
        return render_template("/index.html")

if __name__ == "__main__":
    app.config["TEMPLATES_AUTO_RELOAD"] = True
    app.config["SEND_FILE_MAX_AGE_DEFAULT"] = 0
    app.run(debug=True, host="0.0.0.0", port=5000)
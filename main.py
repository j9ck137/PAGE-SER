from flask import Flask, request, redirect, url_for, session, render_template_string

app = Flask(__name__)
app.secret_key = "d4906e17ce34fc44d39cfb1abea10007dab23a73d393e6f659143b09bea7a553"  # change if you want

# ---- USERS (2-3 users) ----
USERS = {
    "jatin": "xd",
    "samar": "lx",
    "shivu": "lolx"
}

# ---- LOGIN PAGE ----
LOGIN_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>Login</title>
</head>
<body>
    <h2>Login Page</h2>
    <form method="POST">
        <input type="text" name="username" placeholder="Username" required><br><br>
        <input type="password" name="password" placeholder="Password" required><br><br>
        <button type="submit">Login</button>
    </form>
    <p style="color:red;">{{ error }}</p>
</body>
</html>
"""

# ---- HOST PAGE (AFTER LOGIN) ----
HOST_HTML = """
<!DOCTYPE html>
<html>
<head>
    <title>My Host</title>
</head>
<body>
    <h2>Welcome {{ user }}</h2>
    <p>This is my host page</p>
    <h3>Host Link:</h3>
    <a href="de1.bot-hosting.net:21901">de1.bot-hosting.net:21901</a>
    <br><br>
    <a href="/logout">Logout</a>
</body>
</html>
"""

@app.route("/", methods=["GET", "POST"])
def login():
    error = ""
    if request.method == "POST":
        username = request.form.get("username")
        password = request.form.get("password")

        if username in USERS and USERS[username] == password:
            session["user"] = username
            return redirect(url_for("host"))
        else:
            error = "Invalid Username or Password"

    return render_template_string(LOGIN_HTML, error=error)

@app.route("/host")
def host():
    if "user" not in session:
        return redirect(url_for("login"))

    return render_template_string(HOST_HTML, user=session["user"])

@app.route("/logout")
def logout():
    session.pop("user", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=False)

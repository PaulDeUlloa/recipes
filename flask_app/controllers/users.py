from flask_app import app
from flask import flash, redirect, render_template, request, session
from flask_app.models.user import User
from flask_app.models.recipe import Recipe
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route("/")
def index():
    """Display the login and registration forms."""

    return render_template("index.html")


@app.post("/register")
def register_user():
    """Process the registration form."""
    # validate the form first

    # if invalid, redirect user back to form
    if not User.registration_is_valid(request.form):
        return redirect("/")
    # look for user by email on form
    potential_user = User.get_by_email(request.form["email"])
    # if there is a user, redirect to form
    if potential_user:
        flash("Email in use. Please log in.", "register")
        return redirect("/")
    print("Users not found, okay to register.")

    # hash the user's password (encrypt)
    hashed_pw = bcrypt.generate_password_hash(request.form["password"])
    data = {
        "first_name": request.form["first_name"],
        "last_name": request.form["last_name"],
        "email": request.form["email"],
        "password": hashed_pw,
    }
    # saves the user to the database
    user_id = User.create(data)
    # put the user's id into session
    session["user_id"] = user_id
    # message for the users when they successfully register
    flash("Thank you for registering, you're AWESOME!", "register")

    # redirect to the recipes
    return redirect("/recipes")


# THIS IS FOR THE LOGIN BELOW
@app.post("/login")
def login():
    """Processes the LOGIN FORM."""
    # validate FORM first
    if not User.login_is_valid(request.form):
        return redirect("/")
    # check's if user exists by email
    potential_user = User.get_by_email(request.form["email"])
    # if they dont exist, flash message please register and redirect
    if not potential_user:
        flash("Invalid credentials.", "login")
        return redirect("/")
    # check password if they exist
    user = potential_user

    # if password is wrong, flash incorrect and redirect
    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        flash("Invalid credentials.", "login")
        return redirect("/")

    # put the user's id into session
    session["user_id"] = user.id

    # redirect to the recipes page
    flash("Thank you for logging in.", "login")
    return redirect("/recipes")


@app.get("/recipes")
def recipes():
    """Displays the recipes template"""

    if "user_id" not in session:
        flash("Please log in", "login")
        return redirect("/")

    user = User.get_by_user_id(session["user_id"])
    recipes = Recipe.get_all_with_users()

    return render_template("all_recipes.html", user=user, recipes=recipes)


@app.get("/logout")
def logout():
    """Clears session."""

    session.clear()
    flash("You have successfully been logged out.", "login")
    return redirect("/")

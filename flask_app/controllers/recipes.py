import datetime
from flask_app import app
from flask import flash, redirect, render_template, request, session
from flask_app.models.user import User
from flask_app.models.recipe import Recipe


@app.template_filter("format_date")
def format_date(date):
    return date.strftime("%Y-%m-%d")


@app.get("/recipes")
def all_recipes():
    """Display the all_recipes template."""

    if "user_id" not in session:
        flash("Please log in", "login")
        return redirect("/")

    user = User.get_by_user_id(session["user_id"])
    recipes = Recipe.get_all_with_users()

    return render_template("all_recipes.html", user=user, recipes=recipes)


@app.get("/recipes/new")
def new_recipe():
    """Displays the new recipe template"""

    if "user_id" not in session:
        flash("Please log in", "login")
        return redirect("/")

    user = User.get_by_user_id(session["user_id"])
    return render_template("new_recipe.html", user=user)


@app.post("/recipes/create")
def create_recipe():
    """Processes the new recipe table form"""

    if "user_id" not in session:
        flash("Please log in", "login")
        return redirect("/")

    if not Recipe.form_is_valid(request.form):
        return redirect("/recipes/new")

    Recipe.create(request.form)
    return redirect("/recipes")


@app.get("/recipes/<int:recipe_id>")
def recipe_details(recipe_id):
    """Displays the recipe_details.html template."""

    if "user_id" not in session:
        flash("Please log in", "login")
        return redirect("/")

    user = User.get_by_user_id(session["user_id"])
    recipe = Recipe.get_one_with_user(recipe_id)

    return render_template("recipe_details.html", user=user, recipe=recipe)


@app.get("/recipes/<int:recipe_id>/edit")
def edit_recipe(recipe_id):
    """Displays the edit_recipe.html template."""

    if "user_id" not in session:
        flash("Please log in", "login")
        return redirect("/")

    user = User.get_by_user_id(session["user_id"])
    recipe = Recipe.get_one_with_user(recipe_id)

    return render_template("edit_recipe.html", user=user, recipe=recipe)


@app.post("/recipes/<int:recipe_id>/update")
def update_recipe(recipe_id):
    """Process the edit recipe form."""

    if "user_id" not in session:
        flash("Please log in", "login")
        return redirect("/")

    Recipe.update_recipe(request.form)
    return redirect(f"/recipes/{recipe_id}")


@app.post("/recipes/<int:recipe_id>/delete")
def delete_recipe(recipe_id):
    """Deletes a recipe by it's id."""

    if "user_id" not in session:
        flash("Please log in", "login")
        return redirect("/")

    Recipe.delete_recipe(recipe_id)

    return redirect("/recipes")

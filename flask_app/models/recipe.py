from flask import flash
from flask_app.models.user import User
from flask_app.models.like import Like
from flask_app.config.mysqlconnection import connectToMySQL


DATABASE = "users_recipes"

# (*****Change Recipe***)


class Recipe:
    def __init__(self, data):
        self.id = data["id"]
        self.name = data["name"]
        self.description = data["description"]
        self.instructions = data["instructions"]
        self.cooked_at = data["cooked_at"]
        self.is_under_30 = data["is_under_30"]
        self.created_at = data["created_at"]
        self.updated_at = data["updated_at"]
        self.user_id = data["user_id"]
        self.user = None
        # if you are required to display on the page who created that recipe or uploaded that recipe to the website you would switch NONE with

    @staticmethod
    def form_is_valid(form_data):
        """Validates the recipe form."""

        is_valid = True
        # NAME VALIDATION
        if len(form_data["name"].strip()) == 0:
            is_valid = False
            flash("Please enter name.", "name")
        elif len(form_data["name"].strip()) < 3:
            is_valid = False
            flash("Name must be at least three characters.", "name")
        # DESCRIPTION VALIDATION
        if len(form_data["description"].strip()) == 0:
            is_valid = False
            flash("Please enter description.", "name")
        elif len(form_data["description"].strip()) < 3:
            is_valid = False
            flash("Description must be at least three characters.", "name")
        # INSTRUCTIONS VALIDATION
        if len(form_data["instructions"].strip()) == 0:
            is_valid = False
            flash("Please enter instructions.", "name")
        elif len(form_data["instructions"].strip()) < 3:
            is_valid = False
            flash("Instructions must be at least three characters.", "name")
        # COOKED_AT VALIDATION
        if len(form_data["cooked_at"].strip()) == 0:
            is_valid = False
            flash("Please enter cooked at.", "name")
        # UNDER 30 VALIDATION
        if "is_under_30" not in form_data:
            is_valid = False
            flash("Please enter if recipe can be cooked under 30 minutes.", "name")

        return is_valid

    # we reference the class itself and not the object when we have @classmethod as the decorator
    def is_liked_at_by(self, user_id):
        """Will return true or false if user liked a recipe"""

        has_liked = False
        likes = Like.get_all_by_recipe_id(self.id)
        # li = like, just had to rename since app would crash
        for li in likes:
            if li.user_id == user_id:
                has_liked = True
        return has_liked

    @classmethod
    def create(cls, form_data):
        """INSERTS a new recipe in the database."""

        query = """
        INSERT INTO recipes (name, description, instructions, cooked_at, is_under_30, user_id)
        VALUES (%(name)s, %(description)s, %(instructions)s, %(cooked_at)s, %(is_under_30)s, %(user_id)s);
        """
        recipe_id = connectToMySQL(DATABASE).query_db(query, form_data)
        return recipe_id

    @classmethod
    def get_all_with_users(cls):
        """Gets all the recipe rows from the database including the users who created them."""

        query = """
        SELECT * FROM recipes
        JOIN users 
        ON recipes.user_id = users.id;
        """

        results = connectToMySQL(DATABASE).query_db(query)

        recipes = []

        for result in results:
            recipe = Recipe(result)
            creator = User.get_by_user_id(result["user_id"])
            # may need to add new data dictionary instead of creator above^
            # user_data = {
            # roughly by inputting lines 13-21 here
            # }
            recipe.user = creator
            recipes.append(recipe)

        return recipes

    @classmethod
    def get_one_with_user(cls, recipe_id):
        """Gets one recipe row from the database including the individual user who created it."""

        query = """
        SELECT * FROM recipes
        JOIN users
        ON recipes.user_id = users.id
        WHERE recipes.id = %(recipe_id)s;
        """
        # ^^^the reason why its *recipes.id* is because it has to be the name of our table.

        data = {"recipe_id": recipe_id}
        results = connectToMySQL(DATABASE).query_db(query, data)
        recipe = Recipe(results[0])
        creator = User.get_by_user_id(results[0]["user_id"])
        recipe.user = creator

        return recipe

    @classmethod
    def update_recipe(cls, form_data):
        """Updates one recipe row in the database."""

        query = """
        UPDATE recipes
        SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, cooked_at = %(cooked_at)s, is_under_30 = %(is_under_30)s
        WHERE id = %(recipe_id)s;
        """
        connectToMySQL(DATABASE).query_db(query, form_data)
        return

    @classmethod
    def delete_recipe(cls, recipe_id):
        """Deletes one recipe row in the database."""

        query = """
        DELETE FROM recipes
        WHERE id = %(recipe_id)s;
        """

        data = {"recipe_id": recipe_id}

        connectToMySQL(DATABASE).query_db(query, data)
        return

from flask import flash
from flask_app.models.user import User
from flask_app.config.mysqlconnection import connectToMySQL


DATABASE = "users_recipes"

# TODO: would like to add an animation to the like button when a user clicks on it.


class Like:
    def __init__(self, data):
        self.user_id = data["user_id"]
        self.recipe_id = data["recipe_id"]

    @classmethod
    def create_like(cls, form_data):
        """INSERTS a new like in the database."""

        query = """
        INSERT INTO likes (user_id, recipe_id)
        VALUES (%(user_id)s, %(recipe_id)s);
        """
        like_id = connectToMySQL(DATABASE).query_db(query, form_data)
        return like_id

    @classmethod
    def get_all_by_recipe_id(cls, recipe_id):
        """Gets all the like rows from the database including the users who created them."""

        query = """
        SELECT * FROM likes
        WHERE recipe_id = %(recipe_id)s;
        """
        data = {"recipe_id": recipe_id}

        results = connectToMySQL(DATABASE).query_db(query, data)

        likes = []

        for result in results:
            like = Like(result)
            likes.append(like)

        return likes

    @classmethod
    def get_like_count(cls, recipe_id):
        """will return the like count"""

        query = """
        SELECT COUNT(recipe_id) as 'count'
        FROM likes
        WHERE recipe_id = %(recipe_id)s;
        """

        data = {"recipe_id": recipe_id}

        results = connectToMySQL(DATABASE).query_db(query, data)
        return results[0]["count"]

    # @classmethod
    # def get_one_with_user(cls, like_id):
    #     """Gets one like row from the database including the individual user who created it."""

    #     query = """
    #     SELECT * FROM likes
    #     JOIN users
    #     ON likes.user_id = users.id
    #     WHERE likes.id = %(like_id)s;
    #     """
    #     # ^^^the reason why its *likes.id* is because it has to be the name of our table.

    #     data = {"like_id": like_id}
    #     results = connectToMySQL(DATABASE).query_db(query, data)
    #     like = Like(results[0])
    #     creator = User.get_by_user_id(results[0]["user_id"])
    #     like.user = creator

    #     return like

    # @classmethod
    # def update_like(cls, form_data):
    #     """Updates one like row in the database."""

    #     query = """
    #     UPDATE likes
    #     SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, cooked_at = %(cooked_at)s, is_under_30 = %(is_under_30)s
    #     WHERE id = %(like_id)s;
    #     """
    #     connectToMySQL(DATABASE).query_db(query, form_data)
    #     return

    # @classmethod
    # def delete_like(cls, like_id):
    #     """Deletes one like row in the database."""

    #     query = """
    #     DELETE FROM likes
    #     WHERE id = %(like_id)s;
    #     """

    #     data = {"like_id": like_id}

    #     connectToMySQL(DATABASE).query_db(query, data)
    #     return

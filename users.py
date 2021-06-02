 
"""
This is the user module and supports all the REST actions for the
user data
"""

from flask import  abort
from config import db
from models import User, UserSchema


def read_all():
    """
    This function responds to a request for /api/users
    with the complete lists of users
    :return:        json string of list of users
    """
    # Create the list of users from our data
    users = User.query.order_by(User.first_name).all()

    # Serialize the data for the response
    user_schema = UserSchema(many=True)
    data = user_schema.dump(users)
    return data


def read_one(user_id):
    """
    This function responds to a request for /api/users/{user_id}
    with one matching user from users
    :param user_id:   Id of user to find
    :return:            user matching id
    """
    # Get the user requested
    user = User.query.filter(User.user_id == user_id).one_or_none()

    if user is not None:

        # Serialize the data for the response
        user_schema = UserSchema()
        data = user_schema.dump(user)
        return data

    else:
        abort(
            404,
            "User not found for Id: {user_id}".format(user_id=user_id),
        )


def create(user):
    """
    This function creates a new user in the people structure
    based on the passed in user data
    :param user:  user to create in people structure
    :return:        201 on success, 406 on user exists
    """
    first_name = user.get("first_name")
    last_name = user.get("last_name")

    existing_user = (
        User.query.filter(User.first_name == first_name)
        .filter(User.last_name == last_name)
        .one_or_none()
    )

    # New user
    if existing_user is None:

        schema = UserSchema()
        new_user = schema.load(user, session=db.session)

        # Add the user to the database
        db.session.add(new_user)
        db.session.commit()

        # Serialize and return the newly created user in the response
        data = schema.dump(new_user)

        return data, 201

    # Otherwise, nope, person exists already
    else:
        abort(
            409,
            "Person {first_name} {last_name} exists already".format(
                first_name=first_name, last_name=last_name
            ),
        )


def update(user_id, user):
    """
    This function updates an existing user in the people structure
    Throws an error if a user with the name we want to update to
    already exists in the database.
    :param user_id:   Id of the user to update in the people structure
    :param user:      user to update
    :return:            updated user structure
    """
    # Get the user requested from the db into session
    update_user = User.query.filter(
        User.user_id == user_id
    ).one_or_none()

    # Try to find an existing user with the same name as the update
    first_name = user.get("first_name")
    last_name = user.get("last_name")

    existing_user = (
        User.query.filter(User.first_name == first_name)
        .filter(User.last_name == last_name)
        .one_or_none()
    )

    if update_user is None:
        abort(
            404,
            "User not found for Id: {user_id}".format(user_id=user_id),
        )

    elif (
        existing_user is not None and existing_user.user_id != user_id
    ):
        abort(
            409,
            "User {first_name} {last_name} exists already".format(
                first_name=first_name, last_name=last_name
            ),
        )

    # Otherwise go ahead and update!
    else:

        # turn the passed in user into a db object
        schema = UserSchema()
        update = schema.load(user, session=db.session)

        # Set the id to the user we want to update
        update.user_id = update_user.user_id

        # merge the new object into the old and commit it to the db
        db.session.merge(update)
        db.session.commit()

        # return updated user in the response
        data = schema.dump(update_user)

        return data, 200


def delete(user_id):
    """
    This function deletes a user from the people structure
    :param user_id:   Id of the user to delete
    :return:            200 on successful delete, 404 if not found
    """
    # Get the user requested
    user = User.query.filter(User.user_id == user_id).one_or_none()

    if user is not None:
        db.session.delete(user)
        db.session.commit()
        return (
            "User {user_id} deleted".format(user_id=user_id), 200
        )

    else:
        abort(
            404,
            "Person not found for Id: {user_id}".format(user_id=user_id),
        )
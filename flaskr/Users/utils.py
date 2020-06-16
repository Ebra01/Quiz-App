from flaskr import bcrypt
from flaskr.Models.models import Users
from flask_login import login_user


def addUserToDB(body):
    registered_users = [u.display() for u in Users.query.all()]
    registered_emails = [u['email'].lower() for u in registered_users]
    registered_usernames = [u['username'].lower() for u in registered_users]

    # Check if the username & email are not already registered in the Database, and
    # if not, adding the user Credentials to the Database
    if body['email'].lower() not in registered_emails and \
            body['username'].lower() not in registered_usernames:
        hashed_passw = bcrypt.generate_password_hash(body['password']).decode('utf-8')

        new_user = Users(
            username=body['username'],
            email=body['email'],
            password=hashed_passw
        )

        new_user.insert()

        return True

    # In Case of any Credentials Check Errors
    raise Exception("User With Same Credentials is Already Registered!")


def validate_current_user(cred, passw):

    # Check wether the user logged-in with username or email
    user = checkUsernameOrEmail(cred)

    # Check if entered password matches user's hashed password
    if user and bcrypt.check_password_hash(user.password, passw):
        # Logging the user as current_user
        login_user(user)
    else:
        # In Case of Credentials Check Errors
        raise Exception("Wrong Credentials, Try Again!")


def checkUsernameOrEmail(cred):
    try:
        # Check if user Logged-in using his/her username or email

        userByEmail = Users.query.filter(Users.email.ilike(cred)).first()
        userByUsername = Users.query.filter(Users.username.ilike(cred)).first()

        if userByEmail:
            return userByEmail
        elif userByUsername:
            return userByUsername
        else:
            return None

    except Exception as e:
        print(e)

''' API for UniRoute.
    Created by: Chandler Dugan, Christian Hart, and Eric Rivas
'''
import json
from datetime import datetime, timedelta, timezone
import os
import logging
from flask import Flask, request, jsonify, render_template
from flask_jwt_extended import create_access_token, get_jwt, \
    get_jwt_identity, unset_jwt_cookies, jwt_required, JWTManager
from flask_mysqldb import MySQL  # Connects MySQL to Flask
import MySQLdb.cursors
from googleroutes import get_route
from flask_bcrypt import Bcrypt
from itsdangerous import URLSafeTimedSerializer
from flask import flash
from flask_mail import Message
from flask_mail import Mail
from flask import url_for
from utils import userUtils as UserUtils

print(os.getenv('MYSQL_HOST'))
print(os.getenv('MYSQL_USER'))
print(os.getenv('MYSQL_PASSWORD'))

app = Flask(__name__)
bcrypt = Bcrypt(app)


# TOKEN CONFIG

app.config["JWT_SECRET_KEY"] = "super-secret-thingy-that-is-not-best-practice(CHANGE!)"
jwt = JWTManager(app)

# DATABASE CONFIGURATION
app.config['MYSQL_HOST'] = os.getenv('MYSQL_HOST')
app.config['MYSQL_USER'] = os.getenv('MYSQL_USER')
app.config['MYSQL_PASSWORD'] = os.getenv('MYSQL_PASSWORD')
app.config['MYSQL_DB'] = os.getenv('MYSQL_DB')
app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
app.config['SECURITY_PASSWORD_SALT'] = os.getenv('SECURITY_PASSWORD_SALT')
app.config['MAIL_DEFAULT_SENDER'] = os.getenv('MAIL_DEFAULT_SENDER')
app.config['MAIL_SERVER'] = os.getenv('MAIL_SERVER')
app.config['MAIL_PORT'] = os.getenv('MAIL_PORT')
app.config['MAIL_USE_TLS'] = os.getenv('MAIL_USE_TLS')
# app.config['MAIL_USE_SSL'] = os.getenv('MAIL_USE_SSL')
app.config['MAIL_USERNAME'] = os.getenv('MAIL_USERNAME')
app.config['MAIL_PASSWORD'] = os.getenv('MAIL_PASSWORD')

print("Connecting to MySQL DB at " + os.getenv('MYSQL_HOST') + " for user " + os.getenv('MYSQL_USER'))

mail = Mail(app)
mysql = MySQL(app)

# LOGGING CONFIGURATION
log = logging.getLogger("writing-logger")
# logging.basicConfig(level=os.environ.get)()
log.setLevel(logging.INFO)
fh = logging.FileHandler("./mylog.log")
formatting = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatting)
log.addHandler(fh)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/landing')
def landing():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('index.html')


@app.route('/profile')
def profile():
    return render_template('index.html')


@app.route('/register')
def register():
    return render_template('index.html')


# EMAIL VARIFICATION FUNCS
# def generate_confirmation_token(email):
#     serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
#     return serializer.dumps(email, salt=app.config['SECURITY_PASSWORD_SALT'])

# def confirm_token(token, expiration=3600):
#     serializer = URLSafeTimedSerializer(app.config['SECRET_KEY'])
#     try:
#         email = serializer.loads(
#             token,
#             salt=app.config['SECURITY_PASSWORD_SALT'],
#             max_age=expiration
#         )
#     except:
#         return False
#     return email

# def send_email(to, subject, template):
#     msg = Message(
#         subject,
#         recipients=[to],
#         html=template,
#         sender=app.config['MAIL_DEFAULT_SENDER']
#     )
#     mail.send(msg)

# ACCOUNT / SESSION MANAGEMENT

# Add user information to the database
# Basics on how to communicate with MySQL in 5 easy steps
@app.route('/register', methods=['POST'])
def add_user():
    ''' Takes in user account input data from front end and adds it to db as a user's account
        If user already exists, it does not add to db and returns an error msg. 
    '''
    # 1) Create a cursor
    cursor = mysql.connection.cursor()
    # 2) Declare variables for input values, if needed
    # Use input json to populate these variables
    username = request.json["username"]
    password = request.json["password"]
    email = request.json["email"]
    university = request.json["university"]
    first_name = request.json["firstName"]
    last_name = request.json["lastName"]
    confirmed = 0
    date = None
    # Check if username is already in the database
    cursor.execute(
        'SELECT username FROM users WHERE username = %s', [username])
    user = cursor.fetchone()
    if user:
        return 'There is already an account with that username.'
    # Hash the user's password
    hashed_password = UserUtils.hash_password(password, bcrypt)
    # 3) Use cursor.execute() to run a line of MySQL code
    cursor.execute('''INSERT INTO users VALUES(%s,%s,%s,%s,%s,%s)''',
                   (username, hashed_password, email, university, first_name, last_name,))

    # 4) Commit the change to the MySQL database
    mysql.connection.commit()
    # 5) Close the cursor
    cursor.close()

    # token = generate_confirmation_token(email)
    # confirm_url = url_for('confirm_email', token=token, _external=True)
    # print(confirm_url)
    # html = render_template('active.html', confirm_url=confirm_url)
    # subject = "Please confirm your Email"
    # send_email(email, subject, html)
    # flash('A confirmation email has been sent via email.')

    return 'successfully added user to database'


@app.route("/confirm/<token>")
def confirm_email(token):
    try:
        email = confirm_token(token)
    except:
        flash('The confirmation link is invalid or has expired.', 'danger')
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
    cursor.execute('SELECT * from users WHERE email = %s',
                   (email,))
    user = cursor.fetchone()

    cursor.close()

    if user['confirmed']:
        flash('Account already confirmed. Please login.', 'success')
    else:
        username = user['username']
        cursor = mysql.connection.cursor()
        cursor.execute('UPDATE users SET confirmed = true WHERE username = %s',
                       (username,))
        mysql.connection.commit()
        cursor.close()
        flash('You have confirmed your account. Thanks!', 'success')
    return 'You have successfully confirmed your email!'

# Api route for logging in users and creating token


@app.route('/token', methods=["POST"])
def create_token():
    '''
    Takes user login data and checks if thier user and pass is in db.
    if in db, create a JWT Auth token and send to front end.
    else, show an error messgage that the user credentials entered are incorrect.
    '''
    # request json of username and pass from front end
    username = request.json.get("username", None)
    password = request.json.get("password", None)

    # create mysql cursor to execute
    # DictCursor allows you to select colum  via user['column_name']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    cursor.execute('SELECT * FROM users WHERE username = %s', (username,))

    user = cursor.fetchone()

    # if the user name and pass are not in db, return wrong username and pass
    # case: if user comes as none
    if user is None or not UserUtils.is_password_correct(user, password, bcrypt):
        # or not bcrypt.check_password_hash(user['password'], password)
        return {"msg": "Wrong username or password"}, 401
    # create accesstoken if succsesful
    access_token = create_access_token(identity=username)
    response = {"access_token": access_token}
    return response

# this refreshes the jwt authentication so it does not randomly log you out


@app.after_request
def refresh_expiring_jwts(response):
    ''' If a certain amount time passes, the JWT Auth token is refreshed'''
    try:
        exp_timestamp = get_jwt()["expt"]
        now = datetime.now(timezone.utc)
        target_timestamp = datetime.timestamp(now + timedelta(minutes=30))
        if target_timestamp > exp_timestamp:
            access_token = create_access_token(identity=get_jwt_identity())
            data = response.get_json()
            if isinstance(data) is dict:
                data["access_token"] = access_token
                response.data = json.dumps(data)
            return response
    except (RuntimeError, KeyError):
        # case where there is not a valid JWT. Just return the original response
        return response

# Api route for logging out users


@app.route('/logout', methods=['POST'])
def logout():
    ''' Logs user out of session. Unsets the JWT Auth Token'''
    response = jsonify({"msg": "logout successful"})
    unset_jwt_cookies(response)
    return response


@app.route('/delete_user', methods=['POST'])
def delete_user():
    ''' deletes specified user '''
    username = request.json['username']
    cursor = mysql.connection.cursor()
    cursor.execute('DELETE FROM users WHERE username = %s', [username])
    mysql.connection.commit()
    cursor.close()
    return "Successfully Deleted User"

# Api route to grab user data
# jwt_required() means that you must be logged in (authenticated) to access it
# return type: dict of user data {FirstName: '',
#                                 LastName: '',
#                                 University: ''}


@app.route('/get_profile', methods=['GET', 'POST'])
@jwt_required()
def get_profile():
    '''Grabs current user data from db and sends to front end to display on profile page'''
    # Grabs the identity of jwt auth token
    # current_user = username of user
    current_user = get_jwt_identity()

    # create mysql cursor
    # the DictCursor makes it possible to select the colums like user['firstName']
    cursor = mysql.connection.cursor(MySQLdb.cursors.DictCursor)

    # select user whree the username is equal to current_suer
    cursor.execute('SELECT * FROM users WHERE username = %s', (current_user,))
    user = cursor.fetchone()

    # set profile data
    profile_data = {
        'firstName': user['firstName'],
        'lastName': user['lastName'],
        'university': user['university'],
        # 'confirmed': user['confirmed']
    }
    return profile_data

# route to save addresses to db


@app.route('/save_address', methods=['POST'])
@jwt_required()
def save_address():
    ''' Grabs user address input data from front end
        Stores in current user section of db. 
    '''
    # Grab current user so msql knows where to store it
    current_user = get_jwt_identity()

    # initialize cursor
    cursor = mysql.connection.cursor()

    # request json from front end and store in variables
    address_to_save = request.json['address']

    # insert varables in to columns in mysql db
    cursor.execute('INSERT INTO addresses (username, address) VALUES(%s,%s)',
                   (current_user, address_to_save))
    # commit the changes
    cursor.connection.commit()
    # close the cursor
    cursor.close()

    return "Successfully added Address to DataBase"


@app.route('/remove_address', methods=['POST'])
@jwt_required()
def remove_address():
    current_user = get_jwt_identity()
    cursor = mysql.connection.cursor()
    address_to_remove = request.json['address']
    cursor.execute('DELETE FROM addresses WHERE (username=%s AND address=%s)',
                   (current_user, address_to_remove))
    cursor.connection.commit()
    # close the cursor
    cursor.close()
    return "Address successfully removed"

# route to grab address from db


@app.route('/get_address', methods=['GET', 'POST'])
@jwt_required()
def get_address():
    ''' Grabs saved addresses of current user and sends to front end'''
    current_user = get_jwt_identity()
    cursor = mysql.connection.cursor()
    cursor.execute(
        'SELECT address FROM addresses WHERE username = %s', (current_user,))
    address_result = cursor.fetchall()
    address_list = []
    for address in address_result:
        address_list.append(address[0])
    response = {'address_list': address_list}
    return response

# ROUTING MANAGEMENT

# Api route to grab google routing data


@app.route('/get_route', methods=['GET', 'POST'])
def get_google_route():
    ''' API Route to call google maps api in backend. Currently not in use.'''
    # Will call google routes from a handler file
    # print(get_route().text)
    return get_route()


@app.route('/get_schedule', methods=['GET'])
@jwt_required()
def get_schedule():
    # Grabs current user's schedule for the week
    current_user = get_jwt_identity()
    cursor = mysql.connection.cursor()

    # Pull user's weekly schedule from db by joining scheduledRoutes and scheduledRoutesDayOfWeek
    cursor.execute('SELECT scheduledRoutes.routeID, dayOfWeek, travelMode, departArrive,' +
                   'timeOfDay, origin, destination FROM scheduledRoutes INNER JOIN ' +
                   'scheduledRoutesDayOfWeek ON ' +
                   'scheduledRoutes.routeID=scheduledRoutesDayOfWeek.routeID ' +
                   'WHERE username = %s', (current_user,))

    # Convert query results into a frontend-friendly array of dictionaries
    # First, get the names of all the columns in the query. These will be the keys
    description = cursor.description
    column_names = [column[0] for column in description]

    # Next, zip column_names with each row in the query result to get an array of dictionaries!
    schedule_result = [dict(zip(column_names, row)) for row in cursor]

    # Last step, we need to convert the datetime saved by the db to a string so that it can be
    # converted to JSON and read by the frontend
    for route in schedule_result:
        for key, value in route.items():
            if (key == "timeOfDay"):
                # I shaved off the seconds, fyi
                route[key] = ':'.join(str(value).split(':')[:2])

    return schedule_result

# Api Route to save scheduled direction parameters to user profile


@app.route('/save_scheduled_directions', methods=['POST'])
@jwt_required()
def save_scheduled_directions():
    ''' 
        Grabs schedule user imput data and stores in db.
        Currently not implemented.
    '''
    current_user = get_jwt_identity()
    cursor = mysql.connection.cursor()

    # Retrieve JSON input values
    travelMode = request.json['scheduledTravelMode']
    departArrive = request.json['departArrive']
    timeOfDay = request.json['scheduledTime']
    origin = request.json['scheduledOrigin']
    destination = request.json['scheduledDestination']
    dayOfWeek = request.json['dayOfWeek']

    # Input data into the scheduledRoutes table
    cursor.execute('INSERT INTO scheduledRoutes (username, travelMode, departArrive, timeOfDay,' +
                   'origin, destination) VALUES(%s,%s,%s,%s,%s,%s)',
                   (current_user, travelMode, departArrive, timeOfDay, origin, destination,))

    # Retrieve routeID of the just-saved directions
    routeID = cursor.lastrowid

    # Enter dayOfWeek into scheduledRoutesDayOfWeek for the just-saved directions
    for (dayIndex, dayEnabled) in enumerate(dayOfWeek):
        if (dayEnabled):
            print(str(index) + ": added to table")
            cursor.execute('INSERT INTO scheduledRoutesDayOfWeek (routeID, dayOfWeek)' +
                           'VALUES(%s,%s)', (routeID, dayIndex))

    cursor.connection.commit()
    cursor.close()
    return "Successfully added Scheduled Directions to DataBase"


@app.route('/remove_scheduled_directions', methods=['POST'])
@jwt_required()
def remove_scheduled_directions():
    '''
        Removes a specified scheduled Route.
    '''
    cursor = mysql.connection.cursor()
    routeID = request.json['routeID']

    cursor.execute('DELETE FROM scheduledRoutes ' +
                   'WHERE (routeID=%s)', (routeID,))

    cursor.connection.commit()
    # close the cursor
    cursor.close()
    return "Scheduled directions successfully removed"


@app.route("/edit_profile", methods=["POST"])
@jwt_required()
def edit_profile():
    '''
        Edits the user's information.
    '''
    cursor = mysql.connection.cursor()

    current_user = get_jwt_identity()

    first_name = request.json['firstName']
    last_name = request.json['lastName']
    university = request.json['university']

    cursor.execute('UPDATE users SET firstName = %s, lastName = %s, university = %s WHERE username = %s',
                   (first_name, last_name, university, current_user))

    cursor.connection.commit()
    cursor.close()

    return "Succesfully updated profile information"

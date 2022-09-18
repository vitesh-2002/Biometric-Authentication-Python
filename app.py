# Importing flask module in the project is mandatory
# An object of Flask class is our WSGI application.
from flask import Blueprint, g, render_template, request, jsonify, Flask
import os
from passageidentity import Passage, PassageError
PASSAGE_API_KEY = os.environ.get("PASSAGE_API_KEY")
PASSAGE_APP_ID = os.environ.get("PASSAGE_APP_ID")

# Flask constructor takes the name of
# current module (__name__) as argument.
app = Flask(__name__)
main = Blueprint('main', __name__)
auth = Blueprint('auth', __name__)


try:
    psg = Passage(PASSAGE_APP_ID, PASSAGE_API_KEY)
except PassageError as e:
    print(e)
    exit()

# decorator that will run before every route in the auth blueprint
@auth.before_request
def before_request():
    try:
        g.user = psg.authenticateRequest(request)
    except PassageError as e:
        # this is an issue with the auth check, return 401
        return render_template('unauthorized.html')
# The route() function of the Flask class is a decorator,
# which tells the application which URL should call
# the associated function.
@app.route('/')
# ‘/’ URL is bound with hello_world() function.
def index():
    return render_template('index.html', psg_app_id=PASSAGE_APP_ID)

# want this to have auth
@auth.route('/dashboard', methods=['GET'])
def dashboard():
    # g.user will be set here.
	  # use Passage to get the user information and add it to the dashboard
    psg_user = psg.getUser(g.user)

    return render_template('dashboard.html', email=psg_user.email)# main driver function
if __name__ == '__main__':

	# run() method of Flask class runs the application
	# on the local development server.
	app.run()

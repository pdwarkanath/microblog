## Steps to build a flask app:

1. Install flask
2. Create flask environment and activate it
3. Install extensions - flask-env
4. create the app object of class Flask in the init file for app folder and import routes (not yet created) to it at the end
5. Create routes.py file and import app object from app folder at the top
6. In routes.py file which defines functions when a link is requested by a browser using render_template 
7. Write html files and use Jenja2 to reference variables from routes.py file and run loops
8. create the app_name.py file in the highest level folder and set it as FLASK_APP = app_name.py (replace app_name with actual name of the app)
9. flask run in terminal to start the app
10. Configure the app
11. Install flask-wtf for forms and define child class(es) of the FlaskForm class which can then be used to create form object(s) in routes.py
12. Install flask-sqlalchemy for database
13. Define child classes using database models 


Add password setting and hashing to user class
install flask-login
make login object of class LoginManager
inherit user class from UserMixin from flask_login
add user_loader decorator and load_user function to models.py
login user by querying database for username and checking password
url redirect to page originally requested by logging in user
add @login_required decorator from flask_login to pages that require login
Add to html
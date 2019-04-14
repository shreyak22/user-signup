from flask import Flask, request, redirect 
import cgi
import os
import jinja2

template_dir = os.path.join(os.path.dirname(__file__), 'templates')
jinja_env = jinja2.Environment(loader = jinja2.FileSystemLoader(template_dir), autoescape=True)


app = Flask(__name__)
app.config['DEBUG'] = True


@app.route("/")
def index():
    template = jinja_env.get_template('base.html')
    return template.render(user_error="",pass_error="",confirm_error="",email_error="",user_value="",email_value="")
   

@app.route("/", methods=['POST'])
def verify():
    username = request.form['username']
    password = request.form['password']
    retype_password = request.form['verify']
    email = request.form['email']

    user_verified = verify_username(username)
    password_verified = verify_password(password)
    retype_verified = verify_password_reenter(password, retype_password)
    email_verified = verify_email(email)

    if user_verified == "" and password_verified =="" and retype_verified =="" and email_verified=="":
        return redirect('/valid-form?username={0}'.format(username))

    template = jinja_env.get_template('base.html')
    return template.render(user_error=user_verified,pass_error=password_verified,confirm_error=retype_verified,email_error=email_verified,user_value=username,email_value=email)
   
    
    


def verify_username(username):
    username_str = str(username)
    if len(username_str)== 0 or len(username_str)>20 or len(username_str)<3 or (" " in username_str):
        return "That's not a valid username"
    else: 
        return ""

def verify_password(password):
    if len(password)== 0 or len(password)>20 or len(password)<3 or (" " in password):
        return "That's not a valid password"
    else:
        return ""

def verify_password_reenter(password, retype_password):
    if password != retype_password:
        return "Passwords don't match"
    else:
        return ""

def verify_email(email):
    if len(email)==0:
        return ""
    if (email.count("@")!=1) or (email.count(".")!=1) or len(email)>20 or len(email)<3 or (" " in email):
        return "That's not a valid email"
    else:
        return ""

@app.route('/valid-form')
def valid_form():
    user = request.args.get('username')
    template = jinja_env.get_template('welcome.html')
    return template.render(username=user)


app.run()
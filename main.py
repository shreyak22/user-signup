from flask import Flask, request, redirect 


app = Flask(__name__)
app.config['DEBUG'] = True

form = '''
<html><head>
        <style>
            .error {{
                color: red;
            }}
        </style>
    </head>
    <body>
    <h1>Signup</h1>
        <form method="post">
            <table>
                <tbody><tr>
                    <td><label for="username">Username</label></td>
                    <td>
                        <input name="username" type="text" value="{4}">
                        <span class="error">{0}</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="password">Password</label></td>
                    <td>
                        <input name="password" type="password">
                        <span class="error">{1}</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="verify">Verify Password</label></td>
                    <td>
                        <input name="verify" type="password">
                        <span class="error">{2}</span>
                    </td>
                </tr>
                <tr>
                    <td><label for="email">Email (optional)</label></td>
                    <td>
                        <input name="email" value="{5}">
                        <span class="error">{3}</span>
                    </td>
                </tr>
            </tbody></table>
            <input type="submit">
        </form>
    
</body>
</html>
'''
@app.route("/")
def index():
    return form.format("","","","","","")

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
   
    return form.format(user_verified, password_verified, retype_verified, email_verified, username,email)
    


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
    return '<h1>Welcome! {0}.</h1>'.format(user)


app.run()
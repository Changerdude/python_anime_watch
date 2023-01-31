from flask_app import app,bcrypt
from flask_app.models.model_user import User
from flask import session,redirect,request,flash

@app.route('/register', methods=["POST"])
def register():
    data ={
        **request.form,
    }
    if not User.validate_registration(data):
        return redirect("/")
    data['pw_hash'] = bcrypt.generate_password_hash(data['pw'])
    data["user_icon"] = None
    data["is_private"] = False
    session['uuid'] = User.create(data)
    return redirect('/')

@app.route('/login', methods=['POST'])
def login():
    data ={ 'email' : request.form['email']}
    user_attempt = User.get_user_by_email(data)
    if not user_attempt:
        flash("Invalid email password combination", "err_email_login")
        return redirect("/")
    if not bcrypt.check_password_hash(user_attempt.pw_hash, request.form['pw']):
        flash("Invalid email password combination", "err_email_login")
        return redirect("/")
    session['uuid'] = user_attempt.id
    return redirect('/')

@app.route('/logout')
def logout():
    session.pop('uuid')
    return redirect('/')
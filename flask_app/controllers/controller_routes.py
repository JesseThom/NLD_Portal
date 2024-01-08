from flask import render_template,session,redirect
from flask_app import app,bcrypt

#landing page
@app.route('/')
def landing_page():

    if 'uuid' in session:
        # user_id = session['uuid']
        admin = session['admin']
        if admin == 1:
            return redirect('/admin')
        else:
            return redirect(f'/dashboard')

    return render_template("index.html")

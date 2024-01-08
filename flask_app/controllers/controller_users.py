from flask import render_template, redirect, session, request
from flask_app import app, bcrypt
# from flask_app.config.helpers import encrypt,decrypt
# from cryptography.fernet import Fernet

from flask_app.models.model_users import User
from flask_app.models.model_timecards import Timecard
from flask_app.models.model_jobs import Job
# from flask_app.models.model_paystubs import Paystub


#route to create new user
@app.route('/admin/user/new')
def user_new():
    if 'uuid' not in session:
        return redirect('/')
    elif session['admin'] != 1:
        return redirect('/')

    return render_template('/admin/user_new.html')

#route to submit create user form
@app.route('/user/create',methods=['post'])
def user_create():
    if not User.validate(request.form):
        return redirect('/admin/user/new')
    
    hash_pw = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password': hash_pw
    }

    user_id = User.create(data)    
    if user_id == False:
        print("Failed to create user")
    else:
        print(f"User Created at {user_id} id")

    return redirect('/admin')

#route to edit user page
@app.route('/admin/employee/<employee_id>/edit')
def user_edit(employee_id):
    if 'uuid' not in session:
        return redirect('/')
    elif session['admin'] != 1:
        return redirect('/')

    user = User.get_one_by_employee_id({'employee_id':employee_id})

    return render_template('/admin/user_edit.html',user=user)

#route to update user
@app.route('/user/<employee_id>/update', methods = ["post"])
def user_update(employee_id):
    if not User.validate_update(request.form):
        return redirect(f'/user/{employee_id}/edit')
    
    hash_pw = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password': hash_pw
    }
    print(data)
    User.update_one(data)

    return redirect('/')

#login route
@app.route('/user/login', methods = ['post'])
def user_login():
    data = request.form
    user = User.get_one_by_employee_id({'employee_id':data['employee_id']})

    if not User.validate_login(data,user):
        return redirect('/')

    session['uuid'] = user.id
    session['first_name'] = user.first_name
    session['last_name'] = user.last_name
    session['employee_id'] = user.employee_id
    session['admin'] = user.admin

    if user.admin == 1:
        return redirect('/admin')
    else:
        return redirect(f'/dashboard')

#admin route
@app.route('/admin')
def admin_show():
    if 'uuid' not in session:
        return redirect('/')
    elif session['admin'] != 1:
        return redirect('/')

    users = User.get_all()
    jobs = Job.get_all()

    return render_template("/admin/admin_dashboard.html",users=users,jobs=jobs)

#route to show individual user
@app.route('/dashboard')
# @admin_reqired
# @login required
def dashboard():
    if 'uuid' not in session:
        return redirect('/')
    elif session['admin'] == 1:
        return redirect('/')

    timecards = Timecard.get_all_by_user_id({'user_id': session['uuid']})
    user = User.get_one({'id': session['uuid']})
    # paystubs = Paystub.get_all_by_employee_id({'employee_id':session['employee_id']})

    return render_template("/users/user_dashboard.html",user=user,timecards=timecards)

#route to show all employees under admin
@app.route('/admin/employee/<user_id>')
def user_show(user_id):
    if 'uuid' not in session:
        return redirect('/')
    elif session['admin'] != 1:
        return redirect('/')

    user = User.get_one({'id': user_id})
    timecards = Timecard.get_all_by_user_id({'user_id':user_id})
    # paystubs = Paystub.get_all_by_employee_id({'employee_id':employee_id})

    return render_template("/admin/user_show.html",user=user,timecards=timecards)

#logout
@app.route('/user/logout')
def logout():
    session.clear()
    return redirect('/')

#delete user route
@app.route('/user/<int:id>/delete')
def user_delete(id):
    User.delete_one({'id': id})
    return redirect('/')
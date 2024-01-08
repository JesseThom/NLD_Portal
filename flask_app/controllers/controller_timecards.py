from flask import render_template, redirect, session, request
from flask_app import app

from flask_app.models.model_timecards import Timecard
from flask_app.models.model_jobs import Job

#route to new timecard form page
@app.route('/timecard/<int:id>/new')
def timecard_new(id):
    if 'uuid' not in session:
        return redirect('/')

    user = {'id' : id}
    admin = session['admin']

    jobs = Job.get_all()

    return render_template("/timecards/timecard_new.html",admin=admin,user=user,jobs=jobs)

#route to submit create timecard form
@app.route('/timecard/create',methods=['post'])
def timecard_create():
    print(request.form["user_id"])
    if not Timecard.validate(request.form):
        return redirect(f'/timecard/{request.form["user_id"]}/new')
    
    timecard_id = Timecard.create(request.form)
    
    if timecard_id == False:
        print("Failed to create timecard")
    else:
        print(f"timecard Created at {timecard_id} id")
        
    return redirect(f'/dashboard')

#route to show individual timecard
# @app.route('/employee/<int:employee_id>/timecard/<int:id>')
# def timecard_show(employee_id,id):
#     if 'uuid' not in session:
#         return redirect('/')

#     admin = session['admin']
#     timecard = Timecard.get_one_with_user({'id':id})
    
#     return render_template("/timecards/timecard_show.html",admin=admin,timecard=timecard)

#route to edit timecard form
@app.route('/admin/timecard/<int:id>/edit')
def timecard_edit(id):
    if 'uuid' not in session:
        return redirect('/')

    admin = session['admin']
    timecard = Timecard.get_one_with_user({'id': id})

    return render_template("/timecards/timecard_edit.html", timecard=timecard)

#route to submit edit form
@app.route('/timecard/<int:id>/update',methods=['post'])
def timecard_update(id):
    if not Timecard.validate(request.form):
        return redirect(f'/timecard/{id}/edit')

    data = {
        **request.form,
        'id':id
        }
        
    Timecard.update_one(data)

    return redirect('/dashboard')

# route to process timecard
@app.route('/<int:id>/<int:processed>/unprocess')
def timecard_process(id,processed):
    if processed == 0:
        processed = 1
    else:
        processed = 0
    data = {
        'id': id,
        'processed' : processed,
    }

    Timecard.process(data)
    return redirect('/')

#delete timecard route
@app.route('/timecard/<int:id>/delete')
def timecard_delete(id):
    # user_id = session['uuid']
    Timecard.delete_one({'id': id})
    return redirect('/')

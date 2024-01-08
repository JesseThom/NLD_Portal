from flask import render_template, redirect, session, request
from flask_app import app

from flask_app.models.model_jobs import Job #TODO import model file here
from flask_app.models.model_timecards import Timecard

#route to new job form page
@app.route('/admin/job/new')
def job_new():
    return render_template("/jobs/job_new.html")

#route to submit create job form
@app.route('/job/create',methods=["post"])
def job_create():
    data = request.form

    if not Job.validate(data):
        return redirect('/admin/job/new')

    job_id = Job.create(data)
    if job_id == False:
        print("Failed to create job")
    else:
        print(f"job Created at {job_id} id")
    return redirect('/')

#route to show individual job
@app.route('/admin/job/<int:id>')
def job_show(id):
    data = {'id': id}
    job = Job.get_one(data)
    timecards = Timecard.get_all_with_employee({'jobs_id':id})
    hour_data = Timecard.get_total_hours_by_job({'jobs_id':id})
    total_hours = int(hour_data[0]['total_hours'])
    return render_template("/jobs/job_show.html", job=job,timecards=timecards,total_hours=total_hours)

#route to edit job form
@app.route('/job/<int:id>/edit')
def job_edit(id):
    data = {'id': id}
    job = Job.get_one(data)
    return render_template("job_edit.html", job=job)

#route to submit edit form
@app.route('/job/<int:id>/update',methods=['post'])
def job_update(id):
    data = {
        **request.form,
        'id':id
        }
    Job.update_one(data)
    return redirect('/')

#delete job route
@app.route('/job/<int:id>/delete')
def job_delete(id):
    data = {'id': id}
    Job.delete_one(data)
    return redirect("/")
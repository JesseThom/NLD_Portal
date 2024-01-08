from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import DATABASE

class Job:
    def __init__(self,data:dict):
        #for every column in table from db, must have an attribute
        self.id = data['id']
        self.job_number = data['job_number']
        self.description =  data['description']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.full_name = f"{self.job_number} {self.description}"

#validation
    @staticmethod
    def validate(data):
        is_valid = True

        if not data['job_number']:
            flash("Job number required", "err_job_number")
            is_valid = False

        if not data['description']:
            flash("Description required", "err_description")
            is_valid = False
        elif len(data["description"]) > 45:
            flash("Description must be less that 45 characters long","err_description")
            is_valid = False

        return is_valid

#C
    @classmethod
    def create(cls,data):
        #1 query statement
        query = "INSERT INTO jobs (job_number, description) VALUES (%(job_number)s,%(description)s);"
        #2 contact the data
        job_id = connectToMySQL(DATABASE).query_db(query, data) 
        return job_id
#R
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM jobs WHERE id = %(id)s;"
        #returns list of dictionaries
        results = connectToMySQL(DATABASE).query_db(query,data)
        return cls(results[0])

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM jobs ORDER BY id DESC"
        results = connectToMySQL(DATABASE).query_db(query)
        all_jobs = []
        for dict in results:
            all_jobs.append(cls(dict))
        return all_jobs
#U
    @classmethod
    def update_one(cls,data):
        query = "UPDATE jobs SET job_number = %(job_number)s,description =%(description)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)
#D
    @classmethod
    def delete_one(cls,data):
        query = "DELETE FROM jobs WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)
from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash
from flask_app import DATABASE
from flask_app.models import model_users
from flask_app.models import model_jobs


class Timecard:
    def __init__(self,data:dict):
        #for every column in table from db, must have an attribute
        self.id = data['id']
        self.day = data['day']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']
        self.processed = data['processed']
        self.jobs_id = data['jobs_id']
        self.hours = data['hours']



#validation
    @staticmethod
    def validate(data):
        is_valid = True

        if not data["day"]:
            flash("day required","err_timecards_day")
            is_valid=False

        if int(data["jobs_id"]) == 0:
            flash("job number required","err_job_number")
            is_valid = False
        
        if not data["hours"]:
            flash("hours required","err_hours")
            is_valid = False

        return is_valid

#C
    @classmethod
    def create(cls,data):
        query = "INSERT INTO timecards (day, user_id, jobs_id, hours) VALUES (%(day)s,%(user_id)s,%(jobs_id)s,%(hours)s);"
        user_id = connectToMySQL(DATABASE).query_db(query, data) 

        return user_id
#R
    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM timecards WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        
        if not results:
            return False

        return cls(results[0])

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM timecards"
        results = connectToMySQL(DATABASE).query_db(query)

        all_timecards = []
        for dict in results:
            all_timecards.append(cls(dict))

        return all_timecards

    @classmethod
    def get_all_by_user_id(cls,data):
        query = "SELECT * FROM timecards JOIN jobs ON jobs_id = jobs.id WHERE user_id = %(user_id)s"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if not results:
            return []

        all_timecards = []
        for dict in results:
            timecard_data = {
                'id' : dict['id'],
                'day' : dict['day'],
                'hours' : dict['hours'],
                'jobs_id' : dict['jobs_id'],
                'created_at' : dict['created_at'],
                'updated_at' : dict['updated_at'],
                'user_id' : dict['user_id'],
                'jobs_id' : dict['jobs_id'],
                'processed' : dict['processed']
            }
            job_data = {
                'id' : dict['id'],
                'job_number' : dict['job_number'],
                'description' : dict['description'],
                'created_at' : dict['created_at'],
                'updated_at' : dict['updated_at']
            }

            timecard = cls(timecard_data)
            timecard.job = model_jobs.Job(job_data)
            all_timecards.append(timecard)

        return all_timecards

    @classmethod
    def get_all_by_employee_id(cls,data):
        query = "SELECT * FROM timecards WHERE employee_id = %(employee_id)s"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if not results:
            return []

        all_timecards = []
        for dict in results:
            all_timecards.append(cls(dict))

        return all_timecards
    
    @classmethod
    def get_all_by_job(cls,data):
        query = "SELECT * FROM timecards WHERE jobs_id = %(jobs_id)s"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if not results:
            return []

        all_timecards = []
        for dict in results:
            all_timecards.append(cls(dict))

        return all_timecards

    @classmethod
    def get_all_with_employee(cls, data):
        query = "SELECT * FROM timecards JOIN users ON user_id = users.id WHERE jobs_id = %(jobs_id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if not results:
            return []
        all_timecards = []
        for dict in results:
            timecard_data = {
                'id' : dict['id'],
                'day' : dict['day'],
                'hours' : dict['hours'],
                'jobs_id' : dict['jobs_id'],
                'created_at' : dict['created_at'],
                'updated_at' : dict['updated_at'],
                'user_id' : dict['user_id'],
                'jobs_id' : dict['jobs_id'],
                'processed' : dict['processed']
            }
            
            user_data = {
                'id':dict['users.id'],
                'first_name' : dict['first_name'],
                'last_name' : dict['last_name'],
                'password' : dict['password'],
                'created_at' : dict['created_at'],
                'updated_at' : dict['updated_at'],
                'employee_id' : dict['employee_id'],
                'admin' : dict['admin']
            }

            timecard = cls(timecard_data)
            timecard.user = model_users.User(user_data)
            all_timecards.append(timecard)

        return all_timecards

    @classmethod
    def get_one_with_user(cls, data):
        query = "SELECT * FROM timecards JOIN users ON timecards.user_id = users.id JOIN jobs ON timecards.jobs_id = jobs.id WHERE timecards.id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        if not results:
            return False

        results = results[0]
        
        user_data = {
            'id' : results['users.id'],
            'first_name' : results['first_name'],
            'last_name' : results['last_name'],
            'password' : results['password'],
            'employee_id' : results['employee_id'],
            'created_at' : results['users.created_at'],
            'updated_at' : results['users.updated_at'],
            'admin' : results['admin'],
        }
        timecard_data = {
            'id' :results['id'],
            'day' :results['day'],
            'created_at' :results['created_at'],
            'updated_at' :results['updated_at'],
            'user_id' :results['user_id'],
            'processed' :results['processed'],
            'jobs_id' : results['jobs_id'],
            'hours' : results['hours']
        }
        job_data = {
                'id' : results['id'],
                'job_number' : results['job_number'],
                'description' : results['description'],
                'created_at' : results['created_at'],
                'updated_at' : results['updated_at']
            }

        timecard = Timecard(timecard_data)
        timecard.user = model_users.User(user_data)
        timecard.job = model_jobs.Job(job_data)

        return timecard

    @classmethod
    def get_total_hours_by_job(cls,data):
        query = "SELECT SUM(hours) as total_hours FROM timecards WHERE jobs_id = %(jobs_id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)

        return results

#U
    @classmethod
    def update_one(cls,data):
        query = "UPDATE timecards SET day = %(day)s,hours =%(hours)s,jobs_id = %(jobs_id)s WHERE id = %(id)s;"

        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    def process(cls,data):
        query = "UPDATE timecards SET processed = %(processed)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query,data)

#D
    @classmethod
    def delete_one(cls,data):
        query = "DELETE FROM timecards WHERE id = %(id)s;"

        return connectToMySQL(DATABASE).query_db(query,data)

#D
    @classmethod
    def delete_all_by_user_id(cls,data):
        query = "DELETE FROM timecards WHERE user_id = %(user_id)s;"

        return connectToMySQL(DATABASE).query_db(query,data)



    # @classmethod
    # def get_all_with_liked(cls):
    #     query = "SELECT * FROM timecards LEFT JOIN liked_shows ON timecards.id = timecard_id JOIN users ON users.id = timecards.user_id;"
    #     results = connectToMySQL(DATABASE).query_db(query)

    #     if not results:
    #         return []

    #     all_timecards = []
    #     for dict in results:
    #         timecard_data = {
    #             'id' : dict['id'],
    #             'day' : dict['day'],
    #             'end_day' : dict['end_day'],
    #             'hours_1' : dict['hours_1'],
    #             'job_number_1' : dict['job_number_1'],
    #             'created_at' : dict['created_at'],
    #             'updated_at' : dict['updated_at'],
    #             'user_id' : dict['user_id'],
    #         }
            
    #         user_data = {
    #             'id':dict['users.id'],
    #             'first_name' : dict['first_name'],
    #             'last_name' : dict['last_name'],
    #             'email' : dict['email'],
    #             'password' : dict['password'],
    #             'created_at' : dict['created_at'],
    #             'updated_at' : dict['updated_at'],
    #         }

    #         liked_data = {
    #             'user_id':dict['liked_shows.user_id'],
    #             'timecard_id': dict['timecard_id'],
    #         }

    #         timecard = cls(timecard_data)
    #         timecard.users = model_users.User(user_data)
    #         timecard.liked = model_liked_shows.Liked_show(liked_data)
    #         all_timecards.append(timecard)
            
    #     return all_timecards



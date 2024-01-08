from flask_app.config.mysqlconnection import connectToMySQL
from flask import flash, session
from flask_app import DATABASE, bcrypt
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

class User:
    def __init__(self,data:dict):
        #for every column in table from db, must have an attribute
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        if 'password'in data:
            self.password = data['password']
        else:
            self.password = []
        self.employee_id = data['employee_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.admin = data['admin']
        self.full_name = f"{self.first_name} {self.last_name}"


#create validation
    @staticmethod
    def validate(data):
        is_valid = True
        pwd = data["password"]

        if len(data["first_name"]) < 2:
            flash("First name must be at least 2 characters.","err_users_first_name")
            is_valid=False

        if len(data["last_name"]) < 2:
            flash("Last name must be at least 2 characters.","err_users_last_name")
            is_valid=False

        if len(data['employee_id']) < 6:
            flash("employee id must be at least 6 characters.","err_users_employee_id")
            is_valid=False
        else:
            temp_user = User.get_one_by_employee_id({'employee_id': data['employee_id']})
            # print(temp_user)
            if temp_user:
                flash("employee id already exhist.","err_users_employee_id")
                is_valid=False

        if len(pwd) < 8:
            flash("Password must be at least 8 characters.","err_users_password")
            is_valid=False
        elif not re.search('[0-9]', pwd or not re.search('[A-Z]', pwd)):
            flash("password must contain 1 number and uppercase letter","err_users_password")

        return is_valid

#login validation
    @staticmethod
    def validate_login(data,user):
        is_valid = True

        if not user:
            flash("Employee Id is not recgonized","err_users_login")
            is_valid = False
        else:
            password_check = bcrypt.check_password_hash(user.password, data['password'])
            if not password_check:
                flash ("Incorrect Password","err_users_login_pw")
                is_valid = False

        if len(data["password"]) < 8:
            flash("Password must be at least 8 characters.","err_users_login_pw")
            is_valid=False

        return is_valid

#update validation
    @staticmethod
    def validate_update(data):
        is_valid = True
        pwd = data["password"]
        if len(data["first_name"]) < 2:
            flash("First name must be at least 2 characters.","err_users_first_name")
            is_valid=False

        if len(data["last_name"]) < 2:
            flash("Last name must be at least 2 characters.","err_users_last_name")
            is_valid=False

        if len(pwd) < 8:
            flash("Password must be at least 8 characters.","err_users_password")
            is_valid=False
        elif not re.search('[0-9]', pwd or not re.search('[A-Z]', pwd)):
            flash("password must contain 1 number and uppercase letter","err_users_password")

        return is_valid

#C
    @classmethod
    def create(cls,data):
        query = "INSERT INTO users (first_name, last_name, password, employee_id) VALUES (%(first_name)s, %(last_name)s, %(password)s, %(employee_id)s);"
        user_id = connectToMySQL(DATABASE).query_db(query, data) 

        return user_id
#R
    @classmethod
    def get_one_by_employee_id(cls, data):
        query = "SELECT * FROM users WHERE employee_id = %(employee_id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)

        if not results:
            return False

        return cls(results[0])

    @classmethod
    def get_one(cls, data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query,data)
        
        if not results:
            return False

        return cls(results[0])

    # @classmethod
    # def get_one_with_bank(cls, data):
    #     query = "SELECT * FROM users LEFT JOIN banks ON users.id = banks.user_id WHERE employee_id = %(employee_id)s;"
    #     results = connectToMySQL(DATABASE).query_db(query,data)
    #     if not results:
    #         return []

    #     results = results[0]
    #     user_data = {
    #         'id' : results['id'],
    #         'first_name' : results['first_name'],
    #         'last_name' : results['last_name'],
    #         'password' : results['password'],
    #         'employee_id' : results['employee_id'],
    #         'created_at' : results['created_at'],
    #         'updated_at' : results['updated_at'],
    #         'admin' : results['admin'],
    #     }

    #     bank_data = {
    #         'id' : results['banks.id'],
    #         'bank_name' : decrypt(results['bank_name']),
    #         'routing' : decrypt(results['routing']),
    #         'account' : decrypt(results['account']),
    #         'created_at' : results['banks.created_at'],
    #         'updated_at' : results['banks.updated_at'],
    #         'user_id' : results['user_id'],
    #     }

    #     user = cls(user_data)
    #     user.bank = model_banks.Bank(bank_data)

    #     return user

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM users WHERE admin = 0"
        results = connectToMySQL(DATABASE).query_db(query)

        all_users = []
        for dict in results:
            all_users.append(cls(dict))

        return all_users

#U
    @classmethod
    def update_one(cls,data):
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, password = %(password)s WHERE id = %(id)s;"

        return connectToMySQL(DATABASE).query_db(query,data)
#D
    @classmethod
    def delete_one(cls,data):
        query = "DELETE FROM users WHERE id = %(id)s;"

        return connectToMySQL(DATABASE).query_db(query,data)
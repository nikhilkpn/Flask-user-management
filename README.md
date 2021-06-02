# Flask-user-management
#1 Create a virtual environment
#2 Run 'pip install -r requirements.txt'
#3 Create database by running "python3 create_db.py"
#4 Start the application by running "python3 app.py"

APIs available

1.GET all users       --> http://localhost:5000/users
2.CREATE a user       --> http://localhost:5000/user ; 
                payload = {"first_name":"my name" ,"last_name":"surname" }
3.GET single user     --> http://localhost:5000/user/<user_id>
4.UPDATE single user     --> http://localhost:5000/user/<user_id>
                payload = {"first_name":"updated my name" ,"last_name":"updated surname" }
5.DELETE single user     --> http://localhost:5000/user/<user_id>
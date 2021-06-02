 

# 3rd party moudles
from flask import Blueprint,request,Flask
from users import *
# local modules
from config import app



# bp = Blueprint('users', __name__)
# create a URL route in our application for "/"
@app.route("/users")
def users():
    """
    This function just responds to the browser URL
    localhost:5000/
    :return:        the rendered template "home.html"
    """
    if request.method == "GET":
        data = read_all()
        result = {"statusCode": 200, "data": data}
        return result

@app.route("/user",methods=['POST'])
def createuser():
    """
    This function just responds to the browser URL
    localhost:5000/
    :return:        the rendered template "home.html"
    """
    if request.method == "POST":
        data = request.get_json()
        response = create(data)
        result = {"statusCode": 201, "data": response}
        return result
        

@app.route("/user/<int:user_id>",methods=["GET", "POST",'PUT','DELETE'])
def user(user_id):
    """
    This function just responds to the browser URL
    localhost:5000/
    :return:        the rendered template "home.html"
    """
    if request.method == "GET":
        data = read_one(user_id)
        result = {"statusCode": 200, "data": data}
        return result

    
    if request.method == "PUT":
        data = request.get_json()
        response = update(user_id,data)
        result = {"statusCode": 200, "data": response}
        return result

    if request.method == "DELETE":
        data = delete(user_id)
        result = {"statusCode": 204, "data": data}
        return result


@app.route("/")
def hello():
    result = {"statusCode": 200, "data": "Pong"}
    return result

if __name__ == "__main__":
    app.run(debug=True)
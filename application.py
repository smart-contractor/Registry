import time
import json
import random



from flask import Flask, jsonify, request, render_template
from flask_pymongo import PyMongo
from flask_mail import Mail, Message



application = Flask(__name__)

#AWS
# Remember kids, always 'pip freeze!' before deploying to AWS.
# eb init -p python-2.7 svalbard-registry --region us-east-2
# eb create svalbard-registry-env
# live at http://svalbard-registry-env.bqaqwab2de.us-east-2.elasticbeanstalk.com/

# Mail 
# Attempting to use gmail server.
# In the future, use a dedicated address/password for this.

application.config['DEBUG'] = True
application.config['MAIL_SERVER'] = 'smtp.gmail.com'
application.config['MAIL_PORT'] = 465
application.config['MAIL_USE_TLS'] = False
application.config['MAIL_USE_SSL'] = True
application.config['MAIL_USERNAME'] = 'lagadonian2@gmail.com'
application.config['MAIL_PASSWORD'] = 'sfwctydaxiqstwhd'

mail = Mail(application)


# Database:
# The database is located at https://mlab.com/databases/svalbard_registry.

application.config['MONGO_DBNAME'] = 'svalbard_registry'
application.config['MONGO_URI'] = 'mongodb://lagadonian:lagadonian1@ds217131.mlab.com:17131/svalbard_registry'
mongo = PyMongo(application)




def codemaker():
	# Creates a random four digit code.
	a = random.randint(1, 9)
	b = random.randint(1, 9)
	c = random.randint(1, 9)
	d = random.randint(1, 9)
	code = str(a)+str(b)+str(c)+str(d)
	return code

@application.route("/")
def hello():
	# Returns a generic homepage. 
    return render_template('index.html')

@application.route("/register", methods=['GET', 'POST'])
def register():
    # Registers a payment address and email address.
    # Creates a random verification code and associates it with the payment address.
    if (request.method == 'POST'):

        msg_json = request.get_json()
        address = str(msg_json["address"])
        email = str(msg_json["email"])

        addresses = mongo.db.addresses

        flag = addresses.find_one({"address": address}) or addresses.find_one({"email": email})
        # Indicates that either the payment or email address has already been used. 

        if not flag:
            code = codemaker()
            addresses.insert({'address': address, "email": email, "code": code, "verified": "False"})

            #TODO: Add email verification using https://pythonhosted.org/Flask-Mail/.
            # 'Message' is an imported object class from Flask-Mail
            # 'mail' is the mail server object
            msg = Message("Payment Address Registration", sender="lagadonian2@gmail.com", recipients=[email])
            msg.body = "Your verification code is "+code+"."
            mail.send(msg)

            return jsonify({'message': 'address registered'})
        else: return jsonify({'message': 'error: address or email already registered'})
    # Instructions:
    else: return jsonify({'message': 'send as address:address'})


@application.route("/verify", methods=['GET', 'POST'])
def verify():
	# Checks the verification code.
	# Sets the address as verified.
	if (request.method == 'POST'):

		msg_json = request.get_json()
		address = str(msg_json["address"])
		code = str(msg_json["code"])

		addresses = mongo.db.addresses

		flag = addresses.find_one({"address": address, "code": code}) 
		# Indicates that the address has been registered.
		# Indicates that the code given matches the code associated with the address.

		if flag:
			addresses.update_one({"address": address}, {"$set": {"verified": "True"}})
			return jsonify({'message': 'address verified'})
		else: return jsonify({'message': 'address or code invalid'})
	#Instructions:
	else: return jsonify({'message': 'send as address:address, code:code'})







if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
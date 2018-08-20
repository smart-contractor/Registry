import time
import json
import random



from flask import Flask, jsonify, request, render_template
from flask_pymongo import PyMongo
from flask_mail import Mail, Message


import config

application = Flask(__name__)

#AWS
#EDIT THIS LINE TO TEST GITHUB
# Remember kids, always 'pip freeze!' before deploying to AWS.
# eb init -p python-2.7 svalbard-registry --region us-east-2
# eb create svalbard-registry-env
# To push changes:
# git init
# git add .
# git commit -m "comment" (must do this once to create repository "head")
# eb deploy svalbard-registry-env --staged

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
application.config['MAIL_PASSWORD'] = config.mailpassword

mail = Mail(application)


# Database:
# The database is located at https://mlab.com/databases/svalbard_registry.

application.config['MONGO_DBNAME'] = config.mongoname
application.config['MONGO_URI'] = config.mongouri
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

@application.route("/check", methods=['GET', 'POST'])
def check():
    #gets the status of an address
    if (request.method == 'POST'):

        msg_json = request.get_json()
        address = str(msg_json["address"])

        addresses = mongo.db.addresses

        flag = addresses.find_one({"address": address, "verified": "True"})

        if flag:
            return jsonify({'message': 'verified'})
        else: return jsonify({'message': 'unverified'})
    else: return jsonify({'message': 'send as address:address'})

#returns active bounties
#def getset():

#Adds bounty to the database
#
@application.route("/bounty", methods=['GET', 'POST'])
def bounty():
    if (request.method == 'POST'):

        msg_json = request.get_json()

        address = str(msg_json["address"])
        description = str(msg_json["description"])
        amount = str(msg_json["amount"])
        timeout = int(msg_json["timeout"])
        maxsub = int(msg_json["maxsub"])
        #status = 'closed', 'live', or 'finished'

        #Generate transaction envelope to be signed that creates new wallet with bounty amount
        #Create bounty object in mongodb

        bounties = mongo.db.bounties
        bounties.insert({'address': address,  
            "description": description, 
            "amount": amount,
            "timeout": timeout,
            "maxsub": maxsub,
            "status": 'closed',
            "submissions": [] })
        #^add submission ids to submission
        #^when a submission is added, it must be added to mongo.db.submissions
        #and its id must be added to the bounty record...which must be closed
        #when number of submissions = maxsub, set bounty to "closed"



        #after bounty is added:

        #Redirect user to sign transaction envelope
        #Submit to stellar network
        #Generate new transaction envelope
        # - adds platform as main signer
        # - adds preauth transaction for user to retrieve funds after X days
        #Redirect user to sign this envelope
        #Submit to stellar network

        #When bounty is available, set bounty to "open"
        #Redirect user to the bounty



        return jsonify({'message': 'success'})
    else: return jsonify({'message': 'hi'})


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
        else: return jsonify({'message': 'error'})
    # Instructions:
    else: return jsonify({'message': 'send as address:address, address:address'})


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
		else: return jsonify({'message': 'error'})
	#Instructions:
	else: return jsonify({'message': 'send as address:address, code:code'})









if __name__ == "__main__":
    # Setting debug to True enables debug output. This line should be
    # removed before deploying a production app.
    application.debug = True
    application.run()
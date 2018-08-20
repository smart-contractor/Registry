# Registry
NOTE: 
- need to create a config.py file with:
emailaddress:
emailpassword:
mongouri:
mongoname:



PURPOSE: perform back-end operations
live at: localhost:5000


API:


returns { "message": _ }

/register

send POST format { "address": _STELLAR ADDRESS_ , "email": _EMAIL_ADDRESS_ }

temporarily adds a stellar address and email address pair to the db and generates and emails a verification code to email address

creates mongo db object: 

{
"code": _FOUR_DIGIT_NUMBER_
"email": _EMAIL_ADDRESS_
"address": _STELLAR_ADDRESS_
"verified": "False"
}

/verify

send POST format {"address": _STELLAR_ADDRESS_ , "code": _FOUR_DIGIT_CODE_ }

changes "verified" to "True"

/check

send POST format {"address": _STELLAR_ADDRESS_}

returns "verified" or "unverified"

/bounty

send POST format 
    {
    'address': _STELLAR_ADDRESS_,
		'description': STRING,
		'amount': INTEGER,
		'timeout': INTEGER,
		'maxsub': INTEGER
    }

creates mongodb object 
    {
    'address': address,  
    "description": description, 
    "amount": amount,
    "timeout": timeout,
    "maxsub": maxsub,
    "status": 'closed',
    "submissions": [] 
    }



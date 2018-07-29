# Registry
purpose: tie Stellar addresses to a form of ID (for now: an email address, later: an ID chain)

API:

current address: http://svalbard-registry-env.bqaqwab2de.us-east-2.elasticbeanstalk.com

returns { "message": _ }

/register

POST format { "address": _STELLAR ADDRESS_ , "email": _EMAIL_ADDRESS_ }

temporarily adds a stellar address and email address pair to the db and generates and emails a verification code to email address

creates mongo db object: 

{
"code": _FOUR_DIGIT_NUMBER_
"email": _EMAIL_ADDRESS_
"address": _STELLAR_ADDRESS_
"verified": "True" OR "False"
}

/verify

POST format {"address": _STELLAR_ADDRESS_ , "code": _FOUR_DIGIT_CODE_ }

changes "verified" status to "True"



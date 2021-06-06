import boto3
import botocore.exceptions
import hmac
import hashlib
import base64
import json

USER_POOL_ID = 'us-east-1_LvlGnVvYO'
CLIENT_ID = '48ltihuk0i56199654rugke02g'

def signup(user):
    for field in ["username", "email", "password"]:
        if not user.get(field):
            return {"error": False, "success": False, 'message': f"{field} is not present", "data": None}
    username = user['username']
    email = user["email"]
    password = user['password']

    client = boto3.client('cognito-idp')

    try:
        resp = client.sign_up(
            ClientId=CLIENT_ID,
            Username=username,
            Password=password,
            UserAttributes=[
            {
                'Name': "email",
                'Value': email
            }
            ],
            ValidationData=[
                {
                'Name': "email",
                'Value': email
            },
            {
                'Name': "custom:username",
                'Value': username
            }
        ])


    except client.exceptions.UsernameExistsException as e:
        return {"error": False,
               "success": False,
               "message": "This username already exists",
               "data": None}
    except client.exceptions.InvalidPasswordException as e:

        return {"error": False,
               "success": False,
               "message": "Password should have Caps,\
                          Special chars, Numbers",
               "data": None}
    except client.exceptions.UserLambdaValidationException as e:
        return {"error": False,
               "success": False,
               "message": "Email already exists",
               "data": None}

    except Exception as e:
        return {"error": False,
                "success": False,
                "message": str(e),
               "data": None}

    return {"error": False,
            "success": True,
            "message": "New user: " + username + " signed up successfully.\nPlease check your email at " + email + " for a link to verify your account",
            "data": None}

def login(user):
   client = boto3.client('cognito-idp')

   for field in ["username", "password"]:
     if user.get(field) is None:
       return  {"error": True,
                "success": False,
                "message": f"{field} is required",
                "data": None}

   resp, msg = initiate_auth(client, user.get("username"), user.get("password"))

   if msg != None:
      return {'message': msg,
              "error": True, "success": False, "data": None}

   if resp.get("AuthenticationResult"):
      return {'message': "success",
               "error": False,
               "success": True,
               "data": {
                   "id_token": resp["AuthenticationResult"]["IdToken"],
                   "refresh_token": resp["AuthenticationResult"]["RefreshToken"],
                   "access_token": resp["AuthenticationResult"]["AccessToken"],
                   "expires_in": resp["AuthenticationResult"]["ExpiresIn"],
                   "token_type": resp["AuthenticationResult"]["TokenType"]
       }}

def get_user(access_token):
    client = boto3.client('cognito-idp')

    try:
        resp = client.get_user(
            AccessToken=access_token
        )
    except Exception as e:
        return {"success": False,
                "message": e.__str__(),
                "data": None}
    return {"success": True,
            "message": None,
            "data": resp}

def initiate_auth(client, username, password):
    try:
      resp = client.admin_initiate_auth(
                 UserPoolId=USER_POOL_ID,
                 ClientId=CLIENT_ID,
                 AuthFlow='ADMIN_NO_SRP_AUTH',
                 AuthParameters={
                     'USERNAME': username,
                     'PASSWORD': password,
                  },
                ClientMetadata={
                  'username': username,
                  'password': password,
              })
    except client.exceptions.NotAuthorizedException:
        return None, "The username or password is incorrect"
    except client.exceptions.UserNotConfirmedException:
        return None, "User is not confirmed"
    except Exception as e:
        return None, e.__str__()
    return resp, None

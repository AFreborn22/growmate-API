from app.schemas.user import UserSignupResponse, UserUpdateResponse, HTTPError, Token, UserData

signup = {
    200: {
        "description": "User successfully registered.",
        "model": UserSignupResponse, 
    },
    400: {
        "description": "Bad Request. NIK or Email already registered, or data integrity error.",
        "model": HTTPError,
        "content": {
            "application/json": {
                "examples": {
                    "nik exists": {"value": {"detail": "NIK already registered"}},
                    "email exists": {"value": {"detail": "Email already registered"}},
                    "integrity error": {"value": {"detail": "Data integrity error"}},
                }
            }
        }
    },
    500: {
        "description": "Internal Server Error. An unexpected error occurred.",
        "model": HTTPError,
    }
}

login = {
    200: {
        "description": "User successfully registered.",
        "model": Token,
    },
    400: {
        "description": "Invalid Credetials",
        "model": HTTPError,
        "content": {
            "application/json": {
                "examples": {
                    "invalid credentials": {"value": {"detail": "Incorrect Email or Password"}},
                    "integrity_error": {"value": {"detail": "Data integrity error"}},
                }
            }
        }
    },
    500: {
        "description": "Internal Server Error. An unexpected error occurred.",
        "model": HTTPError,
    }
}

getData = {
    200: {
        "description" : "",
        "model" : UserData,
    },
    404: {
        "description" : "Invalid Credentials",
        "model" : HTTPError,
        "content" : {
            "application/json" : {
                "examples" : {
                    "Invalid Token" : {"value" : {"detail" : "Unauthorized Token"}}
                }
            }
        }
    },
    500: {
        "description" : "Internal Server Error. An unexpected error occurred.",
        "model" : HTTPError,
    }
    
}

updateData = {
    200: {
        "description" : "User Succesfully Updated",
        "model" : UserUpdateResponse,
        "content": {
            "application/json": {
                "examples": {
                    "Update Success": {"value": {"detail": "Updated Succesfully"}},
                    "No Changes": {"value": {"detail": "No Changes Made"}},
                }
            }
        }
    },
    404: {
        "description" : "Invalid Credentials",
        "model" : HTTPError,
        "content" : {
            "application/json" : {
                "examples" : {
                    "Invalid Token" : {"value" : {"detail" : "Unauthorized Token"}}
                }
            }
        }
    },
    500: {
        "description" : "Internal Server Error. An unexpected error occurred.",
        "model" : HTTPError,
    }
}
from app.schemas.user import UserSignUpResponse, UserUpdateResponse, Token, UserData, UnauthorizedError, NotFoundError, BadRequestError, InternalServerError

signup = {
    200: {
        "description": "User successfully registered.",
        "model": UserSignUpResponse,
        "content": {
            "application/json": {
                "examples": {
                    "Success": {
                        "value": {
                            "message": "User successfully registered.",
                            "data": {
                                "nik": "123456789",
                                "nama": "Elizabeth Huang",
                                "tempat_lahir": "Jakarta",
                                "tanggal_lahir": "1990-05-15",
                                "tanggal_kehamilan_pertama": "2025-06-01",
                                "pal": "lightly_active",
                                "usia": 35,
                                "periode_kehamilan": "trisemester2",
                                "alamat": "Jl. Merdeka No.1, Jakarta",
                                "email": "elizabeth@example.com",
                                "berat_badan": 70.5,
                                "tinggi_badan": 170,
                                "lingkar_lengan_atas": 25.5,
                                "password": "$2b$12$bt06VmHJzC1dwjJEwSGWUeUs/HjDkp10Zv4fAtTe3.mcI.RZHYQ0m"          
                            }
                        }
                    }
                }
            }
        }
    },
    400: {
        "description": "Bad Request. NIK or Email already registered, or data integrity error.",
        "model": BadRequestError,
        "content": {
            "application/json": {
                "examples": {
                    "nik exists": {"value": {"detail": "NIK already registered"}},
                    "email exists": {"value": {"detail": "Email already registered"}},
                    "integrity error": {"value": {"detail": "Data integrity error"}}
                }
            }
        }
    },
    500: {
        "description": "Internal Server Error.",
        "model": InternalServerError,
        "content": {
            "application/json": {
                "examples": {
                    "server error": {"value": {"detail": "Internal server error occurred"}}
                }
            }
        }
    }
}

login = {
    200: {
        "description": "User successfully logged in.",
        "model": Token,
        "content": {
            "application/json": {
                "examples": {
                    "Success": {
                        "value": {
                            "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                            "token_type": "bearer"
                        }
                    }
                }
            }
        }
    },
    400: {
        "description": "Invalid credentials.",
        "model": BadRequestError,
        "content": {
            "application/json": {
                "examples": {
                    "invalid credentials": {"value": {"detail": "Incorrect Email or Password"}}
                }
            }
        }
    },
    500: {
        "description": "Internal Server Error.",
        "model": InternalServerError,
        "content": {
            "application/json": {
                "examples": {
                    "server error": {"value": {"detail": "Internal server error occurred"}}
                }
            }
        }
    }
}

getData = {
    200: {
        "description": "User data retrieved successfully.",
        "model": UserData,
    },
    401: {
        "description": "Unauthorized access.",
        "model": UnauthorizedError,
        "content": {
            "application/json": {
                "examples": {
                    "Unauthorized": {"value": {"detail": "Unauthorized access. Token may be invalid or missing"}}
                }
            }
        }
    },
    404: {
        "description": "User not found.",
        "model": NotFoundError,
        "content": {
            "application/json": {
                "examples": {
                    "Not Found": {"value": {"detail": "User not found"}}
                }
            }
        }
    },
    500: {
        "description": "Internal Server Error.",
        "model": InternalServerError,
        "content": {
            "application/json": {
                "examples": {
                    "server error": {"value": {"detail": "Internal server error occurred"}}
                }
            }
        }
    }
}

updateData = {
    200: {
        "description": "User Successfully Updated",
        "model": UserUpdateResponse,
        "content": {
            "application/json": {
                "examples": {
                    "Update Success": {
                        "value": {
                            "message": "Updated Successfully",
                            "data": {
                                "nama": "Elizabeth Huang",
                                "tempat_lahir": "Jakarta",
                                "tanggal_lahir": "1990-05-15",
                                "tanggal_kehamilan_pertama": "2025-06-01",
                                "pal": "lightly_active",
                                "usia": 35,
                                "periode_kehamilan": "trisemester2",
                                "alamat": "Jl. Merdeka No.1, Jakarta",
                                "email": "elizabeth@example.com",
                                "berat_badan": 70.5,
                                "tinggi_badan": 170,
                                "lingkar_lengan_atas": 25.5
                            }
                        }
                    },
                    "No Changes": {
                        "value": {
                            "message": "No Changes Made",
                            "data": { }
                        }
                    },
                }
            }
        }
    },
    404: {
        "description": "User not found.",
        "model": NotFoundError,
        "content": {
            "application/json": {
                "examples": {
                    "Not Found": {"value": {"detail": "User not found"}}
                }
            }
        }
    },
    500: {
        "description": "Internal Server Error.",
        "model": InternalServerError,
        "content": {
            "application/json": {
                "examples": {
                    "server error": {"value": {"detail": "Internal server error occurred"}}
                }
            }
        }
    }
}
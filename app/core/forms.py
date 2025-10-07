from typing import Optional, List
from fastapi import Form

class OAuth2PasswordRequestFormCompat:
    def __init__(
        self,
        username: Optional[str] = Form(None),          
        email: Optional[str] = Form(None),             
        password: str = Form(...),
        scope: str = Form(""),
        client_id: Optional[str] = Form(None),
        client_secret: Optional[str] = Form(None),
    ):
        self.email: str = email or (username or "")
        self.password: str = password
        self.scopes: List[str] = scope.split()
        self.client_id = client_id
        self.client_secret = client_secret
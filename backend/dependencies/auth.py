from fastapi.security import HTTPBasic, HTTPBasicCredentials
from src.settings import env_settings
from typing_extensions import Annotated
from fastapi import Depends, HTTPException, status

security = HTTPBasic()
auth_dependency = Annotated[HTTPBasicCredentials, Depends(security)]


users = {
    f"{env_settings.AUTH_USER}": {
        "password": f"{env_settings.AUTH_PASSWORD}",
        "token": "",
        "priviliged": True,
    }
}


def verification(creds: auth_dependency):
    username = creds.username
    password = creds.password
    if username in users and password == users[username]["password"]:
        print("User Validated")
        return True
    else:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Basic"},
        )


if __name__ == "__main__":
    print(users)

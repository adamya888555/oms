import json
import os

def login(username: str, password: str) -> str | None:
    """
    Authenticate user against users.json and return their role.
    Returns role (str) if authenticated, None otherwise.
    """
    file_path = os.path.join(os.path.dirname(__file__), "..", "data", "users.json")
    try:
        with open(file_path, "r") as f:
            users = json.loads(f.read())  # Read file content as string first
        for user in users:
            if user["username"] == username and user["password"] == password:
                return user["role"]
        return None
    except FileNotFoundError:
        return None
    except json.JSONDecodeError:
        return None
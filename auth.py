users = [
    {"username":"admin","password":"1234"},
    {"username":"test","password":"password"}
]

def login(username,password):
    for u in users:
        if u["username"] == username:
            if u["password"] == password:
                return u
    return None

def register(username,password):
    users.append({
        "username": username,
        "password": password
    })

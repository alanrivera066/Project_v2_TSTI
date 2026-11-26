"""login() oficial de la A3, sin cambios. Se conserva solo para compararlo con las 3 versiones."""


def login(user, password):
    if user == "admin":
        if password == "1234":
            return "access granted"
        else:
            return "wrong password"
    return "user not found "

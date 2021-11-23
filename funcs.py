def checkUserPass(usuario, password, listado):
    for user in listado:
        if usuario == user.username:
            if password == user.password:
                return True
    return False


def getProfile(usuario, listado):
    for user in listado:
        if usuario == user.username:
            return user.perfil


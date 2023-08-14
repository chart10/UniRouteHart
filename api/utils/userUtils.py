def hash_password(password, bcrypt):
    return bcrypt.generate_password_hash(password).decode('utf-8')


def is_password_correct(user, password, bcrypt):
    return bcrypt.check_password_hash(user["password"], password)

from flask_bcrypt import Bcrypt

bcrypt = Bcrypt()

herbert = bcrypt.generate_password_hash('herbert')
print(herbert)

herbert = bcrypt.generate_password_hash('herbert').decode('utf-8')
print(herbert)

print(bcrypt.check_password_hash(herbert, 'herbert'))

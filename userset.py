import sys
from getpass import getpass
from sbcswebsite.models import db, User
from passlib.hash import bcrypt

if len(sys.argv) < 1:
	print "USAGE: python userset.py username"

username = sys.argv[1]


user = User.query.filter_by(username=username).first()
if user is None:
	print "User {0} does not exist. Creating".format(username)
	user = User(username)

user.password = bcrypt.encrypt(getpass("Enter a password for user {0}: ".format(username)))

db.session.add(user)
db.session.commit()

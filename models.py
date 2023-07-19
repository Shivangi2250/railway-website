from market import db, login_manager
from market import bcrypt
from flask_login import UserMixin
import os
import base64
import onetimepass as otp

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


# model relationship
class User(db.Model, UserMixin):
    id = db.Column(db.Integer(), primary_key=True)
    username = db.Column(db.String(length=30), nullable=False, unique=True)
    email_address = db.Column(db.String(length=50), nullable=False, unique=True)
    password_hash = db.Column(db.String(length=60), nullable=False)


    # totp_secret = db.String(length=16)
    #
    # def __init__(self, **kwargs):
    #     super(User, self).__init__(**kwargs)
    #     if self.totp_secret is None:
    #         self.otp_secret = base64.b32encode(os.urandom(10)).decode('utf-8')
    #
    #
    # def get_totp_uri(self):
    #     return f'otpauth://totp/TOTPDemo:{self.username}?secret={self.totp_secret}&issuer=TOTPDemo'
    #
    # def verify_totp(self, token):
    #     return otp.valid_totp(token, self.totp_secret)




    budget = db.Column(db.Integer(), nullable=False, default=1000)
    # items = db.relationship('Item', backref='owned_user', lazy=True)

    @property
    def prettier_budget(self):
        if len(str(self.budget)):
            return f'{str(self.budget)[:-3]}, {str(self.budget)[-3:]} '
        else:
            return f'{self.budget}'

    # user authentication part1 and part2
    @property
    def password(self):
        return self.password

    @password.setter
    def password(self, plain_text_password):
        self.password_hash = bcrypt.generate_password_hash(plain_text_password).decode('utf-8')

       # login user authentication(to check if the password entered is same as before ) Part2:
    def check_password_correction(self, attempted_password):

        # using bcrypt functionalities check_password_hash check is the passwor_hash=attempted_password. if yes then returns true otherwise returns false
        return bcrypt.check_password_hash(self.password_hash,attempted_password)

    # def can_purchase(self,item_obj):
    #     return self.budget >=item_obj.price
    #
    # def can_sell(self, item_obj):
    #     return item_obj in self.items

    # /user authentication
# /model r/p end



# class Item(db.Model):
#     id = db.Column(db.Integer(), primary_key=True)
#     name = db.Column(db.String(length=30), nullable=False, unique=True)
#     price = db.Column(db.Integer(), nullable=False)
#     barcode = db.Column(db.String(length=12), nullable=False, unique=True)
#     description = db.Column(db.String(length=1024), nullable=False, unique=True)
#
#     # to know the owner of this item. here we've "user.id" as an owner
#     owner = db.Column(db.Integer(), db.ForeignKey('user.id'))
#
#     def __repr__(self):
#         return f'Item {self.name}'
#
#
#     def buy(self, user):
#         self.owner = user.id
#         user.budget -= self.price
#         db.session.commit()
# #
#     def sell(self, user):
#         self.owner = None
#         user.budget += self.price
#         db.session.commit()
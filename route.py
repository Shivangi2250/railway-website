from market import app
from flask import render_template, redirect, url_for,flash, request
from market.models import User
from market import db
from market.forms import RegisterForm, LoginForm,PurchaseItemForm, SellItemForm
from flask_login import login_user,logout_user, login_required, current_user


@app.route('/')
@app.route('/home')
def home_page():
    return render_template('home.html')


@app.route('/market', methods=['GET', 'POST'])
@login_required
def market_page():
    # db.create_all()
    # purchase_form = PurchaseItemForm()
    # selling_form = SellItemForm()
    # if request.method=="POST":
    #     # PURCHASE ITEM LOGIC
    #     purchased_item = request.form.get('purchased_item')
    #     p_item_object = Item.query.filter_by(name=purchased_item).first()
    #     if p_item_object:
    #         if current_user.can_purchase(p_item_object):
    #             p_item_object.buy(current_user)
    #             flash(f'Congratulations! Your purchased {p_item_object.name} for {p_item_object.price}₹', category='success')
    #
    #         else:
    #             flash(f"Unfortunately you don't have enough money to purchase {p_item_object.name}!", category='danger')
    #     # SELL ITEM LOGIC
    #     sold_item = request.form.get('sold_item')
    #     s_item_object = Item.query.filter_by(name=sold_item).first()
    #     if s_item_object:
    #         if current_user.can_sell(s_item_object):
    #             s_item_object.sell(current_user)
    #             flash(f'Congratulations! you sold {s_item_object.name} back to market!', category='success')
    #
    #         else:
    #             flash(f"Something wen wrong with selling {s_item_object.name}", category='danger')
    #
    #     return redirect(url_for('market_page'))
    # if request.method == "GET":
    #     items = Item.query.filter_by(owner = None)
    #
    #     # to bring the item that hte current user owns
    #     owned_items = Item.query.filter_by(owner=current_user.id)

    return render_template('market.html')


@app.route('/register', methods=['GET', 'POST'])
def register_page():
    # created instance of RegisterForm class
    form = RegisterForm()

    # form.validate_on_submit() does 2 things. 1=validate if the user has entered correct info,
                                              # 2=check if the submit button is clicked
    if form.validate_on_submit():
        # create instance of the data which we've entered in the form
        user_to_create = User(username=form.username.data,
                              email_address=form.email_address.data,
                              password=form.password1.data)

        # add this data to the database
        db.session.add(user_to_create)

        # save the data
        db.session.commit()





        # if request.method == 'POST':
        #     username = form.username.data
        #     User.set_password(form.password1.data)
        #     db.session.add(User)
        #     db.session.commit()
        #     flash('You are now registered.')
        #     db.session['username'] = username
        #     return redirect(url_for('qr'))
        # return render_template('register.html')





 # Part13:logout and customization
        login_user(user_to_create)
        flash(f'Account created successfully! You are now logged in as {user_to_create.username}',category='success')

        # redirect to the market page after successful registration
        return redirect(url_for('market_page'))

    # to check if the user has followed the conditionals/requirements or not
    if form.errors != {}:  #if there are no errors form the validations
        for err_msg in form.errors.values():
            flash(f'there was an error with creating a user: {err_msg}', category='danger')

    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login_page():
    form = LoginForm()

    if form.validate_on_submit():

        # get the data that is filled in the username
        attempted_user= User.query.filter_by(username=form.username.data).first()

        if attempted_user and attempted_user.check_password_correction(attempted_password=form.password.data):
            login_user(attempted_user)
            flash(f'Success! You are logged in as: {attempted_user.username}', category='success')
            return redirect(url_for('market_page'))

        else:
            flash('Username and password are not matched! Please try again',category='danger')

    #     we'll check 2 things:1= if the username is already there ,
#                              2=if the password for the entered username is correct

    return render_template('login.html',form=form)


@app.route('/logout')
def logout_page():
    logout_user()
    flash("You have been logged out!", category='info')
    return redirect(url_for('home_page'))


@app.route('/about')
def about_page():
    return render_template('about.html')


@app.route('/contact')
def contact_page():
    return render_template('contact.html')

# @app.route('/register', methods=['GET', 'POST'])
# def register_page():
#     form = RegisterForm()
#     if request.method == 'POST':
#         username = form.username.data
#         User.set_password(form.password1.data)
#         db.session.add(User)
#         db.session.commit()
#         flash('You are now registered.')
#         db.session['username'] = username
#         return redirect(url_for('qr'))
#     return render_template('register.html')

# @app.route('/qr')
# def qr():
#     if 'username' not in db.session:
#         return redirect(url_for('register'))
#     username = db.session['username']
#     user = User.query.filter_by(username=username).first()
#     if user is None:
#         return redirect(url_for('register'))
#     return render_template('qr.html'), 200, {
#         'Cache-Control': 'no-cache, no-store, must-revalidate',
#         'Pragma': 'no-cache',
#         'Expires': '0'}




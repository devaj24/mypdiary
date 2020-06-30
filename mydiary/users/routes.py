from flask import Blueprint, render_template, request, redirect, url_for, current_app, flash, session
from mydiary import db
from mydiary.users.forms import RegisterationForm, LoginForm, ChangePasswordForm, ResetPasswordForm, AccountActivationForm
from werkzeug.utils import secure_filename
import os
from mydiary.models import User
from mydiary.login_required import login_required



users = Blueprint('users', __name__)

@users.route('/register/', methods=['GET','POST'])
def register():
	global activation_code
	form = RegisterationForm()
	if form.validate_on_submit():
		global email 
		email = form.email.data
		username = form.username.data
		password = form.password.data
		confirm_password = form.c_password.data

		dp = form.dp.data
		if dp != None:
			dp_filename = secure_filename(dp.filename)
			path_of_dp = os.path.join(current_app.root_path, 'static/dp', dp_filename)
			dp.save(path_of_dp)

		else:
			dp_filename = 'default.jpg'
		
		user = User(email=email,username=username,password=password,dp=dp_filename)
		db.session.add(user)
		db.session.commit()

		'''msg = Message('mydiary Account Activation',
				sender='mydiary24@yandex.com',
				recipients=[email])
			
		char = list('1234567890')
		activation_code = ''
		for i in range(8):
			activation_code += random.choice(char)

		flash('Your Account has been created! Please Check your email for activation','success')'''
		flash('Your Account Has been Created. You can now login', 'success')
		return redirect(url_for('users.login'))

	return render_template('users/register.html', form=form, title='Register')

'''@users.route('/account_created')
def account_created():
	global activation_code, email
	form = AccountActivationForm()
	if form.validate_on_submit():
		code = form.code.data
		if code == activation_code:
			user = User.query.filter_by(email=email)
			user.activated = True
			flash('Your Account has been activated. Please Login', 'success')
			return redirect(url_for('users.login'))

		else:
			flash('Inavlid Code')

	return render_template('users/account_created.html', form=form, title='Account Activation')'''

@users.route('/login/', methods=['GET', 'POST'])
def login():
	form = LoginForm()
	if form.validate_on_submit():
		email = form.email.data
		password = form.password.data

		user = User.query.filter_by(email=email).first()

		if user and user.password==password:
			session['logged_in'] = True
			session['username'] = user.username
			session['email'] = user.email
			return redirect(url_for('main.home'))
			flash('Login Successfull', 'success')
		else:
			flash('Login failed. Please check email and password', 'danger')


	return render_template('users/login.html', form=form, title='Login')

@users.route('/logout/')
@login_required
def logout():
	session.clear()
	flash('You are logged out', 'warning')
	return redirect(url_for('main.home'))


@users.route('/account/', methods=['GET', 'POST'])
@login_required
def account():
	user = User.query.filter_by(username=session['username']).first()
	dp = url_for('static', filename=f'dp/{user.dp}')
	form = ChangePasswordForm()
	if form.validate_on_submit():
		dp = form.change_dp.data
		old_password = form.old_password.data
		new_password = form.new_password.data
		confirm_password = form.confirm_password.data

		if dp != None:
			dp_filename = secure_filename(dp.filename)
			path_to_save = os.path.join(current_app.root_path, 'static/dp', dp_filename)
			dp.save(path_to_save)
			user.dp = dp_filename
		else:
			dp_filename = user.dp

		if old_password != '':
			if new_password != '':
				if old_password == user.password:
					if confirm_password != '':
						if len(new_password) >= 6: 
							if new_password == confirm_password:
									user.password = new_password
							else:
								flash('Confirm Password does not match new password', 'warning')
								return redirect(url_for('users.register'))
						else:
							flash('Password Must be atleast 6 characters long.', 'danger')
							return redirect(url_for('users.account'))
					else:
						flash('Please Confirm Your Password', 'warning')
						return redirect(url_for('users.account'))
				else:
					flash('Old Password does not match', 'warning')
					return redirect(url_for('users.account'))

		db.session.commit()
		flash('Your changes have been saved', 'success')
		return redirect(url_for('users.account'))


	return render_template('users/account.html', user=user, dp=dp, title="Account", form=form)

@users.route('/delete_account/')
@login_required
def delete_account():
	User.query.filter_by(username=session['username']).delete()
	db.session.commit()
	session.clear()
	flash('Your Account has Been deleted', 'danger')
	return redirect(url_for('main.home'))


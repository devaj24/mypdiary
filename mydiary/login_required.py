from functools import wraps
from flask import session, flash, render_template, url_for, redirect

def login_required(f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if 'logged_in' in session:
			return f(*args, **kwargs)
		else:
			flash('You need to login First')
			return redirect(url_for('users.login'))
	return wrap

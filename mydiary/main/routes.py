from flask import Blueprint, render_template, redirect, url_for, request, session, flash, current_app
from mydiary.users.forms import RegisterationForm
from mydiary import db
from mydiary.models import User, Page, Feedback, Support


main = Blueprint('main', __name__)


@main.route('/')
def home():
	if 'logged_in' in session:
		user = User.query.filter_by(username=session['username']).first()
	else:
		user = ''
	return render_template('index.html', user=user, title='Home')
	

@main.route('/about')
def about():
	return render_template('about.html')

@main.route('/support', methods=['GET', 'POST'])
def support():
	if request.method == "POST":
		options = bool(request.form.getlist('options')[0])

		support = Support(answer=options)
		db.session.add(support)
		db.session.commit()

		flash('Thanks for Response', 'success')
		return redirect(url_for('main.home'))

	return render_template('support.html')

@main.route('/feedback', methods=['GET', 'POST'])
def feedback():
	if request.method == "POST":
		rating = request.form['rating']
		feedback = request.form['feedback']

		feedback_db = Feedback(rating=rating, feedback=feedback)

		db.session.add(feedback_db)
		db.session.commit()
		
		return redirect(url_for('main.home'))

	return render_template('feedback.html')
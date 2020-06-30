from flask import Blueprint, render_template, current_app, redirect, url_for, flash, session
from mydiary.pages.forms import New_Page, Edit_Page
from mydiary.login_required import login_required
from mydiary import db
from mydiary.models import Page, User
from werkzeug.utils import secure_filename
import os
from mydiary.users.forms import RegisterationForm


pages = Blueprint('pages', __name__)


@pages.route('/new_page/', methods=['GET', 'POST'])
@login_required
def new_page():
    form = New_Page()

    user = User.query.filter_by(username=session['username']).first()

    if form.validate_on_submit():
        title = form.title.data
        notes = form.notes.data
        image = form.image.data

        if image != None:
            img_name = secure_filename(image.filename)
            img_path = os.path.join(current_app.root_path, 'static/images', img_name)
            image.save(img_path)
        else:
            img_name = None

        page = Page(title=title, notes=notes, image=img_name, user_id=user.id)
        db.session.add(page)
        db.session.commit()

        flash('Your Page has been Created', 'success')
        return redirect(url_for('main.home'))
        
    return render_template('pages/new_page.html', form=form, title="New Page")


@pages.route('/diary_pages/<int:diary_page_no>/')
@login_required
def detailed_view(diary_page_no):
    page = Page.query.get_or_404(diary_page_no)
    image = page.image
    if image != None:
        image = url_for('static', filename=f'images/{image}')

    return render_template('pages/detailed_view.html', page=page, image=image)

@pages.route('/delete_page/<page_no>')
def delete_page(page_no):
    Page.query.filter_by(id=page_no).delete()

    db.session.commit()
    flash(f'Your Page has been deleted.', 'success')
    return redirect(url_for('main.home'))

@pages.route('/edit_page/<page_no>', methods=['GET', 'POST'])
@login_required
def edit_page(page_no):
    form = Edit_Page()
    page = Page.query.get_or_404(page_no)
    form.notes.data = page.notes
    if form.validate_on_submit():
        title = form.title.data
        notes = form.notes.data
        image = form.image.data

        if image != None:
            img_name = secure_filename(image.filename)
            img_path = os.path.join(current_app.root_path, 'static/images', img_name)
            image.save(img_path)
        else:
            img_name = page.image


        page.title = title
        page.notes = notes
        page.image = img_name
        db.session.commit()

        flash(f'Your Page {page.title} has been updated', 'success')
        return redirect(url_for('main.home'))

    return render_template('pages/edit_page.html', form=form, page=page, title="Edit Page")
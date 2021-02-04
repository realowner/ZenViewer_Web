from flask.helpers import flash
from sqlalchemy.orm import query
from app import app, database
from flask import render_template, flash, redirect, url_for
from app.forms import LinkQueueForm, NumberOfViewes
from app.models import LinkQueue

@app.route('/', methods=['GET', 'POST'])
def index():
    queue_links = LinkQueue.query.all()

    queue_form = LinkQueueForm()
    views_num_form = NumberOfViewes()

    if queue_form.validate_on_submit():
        link = LinkQueue(url=queue_form.url.data, views=queue_form.views.data)
        database.session.add(link)
        database.session.commit()
        flash('[INFO] Successfully added!')
        return redirect(url_for('index'))

    if views_num_form.validate_on_submit():
        # alg here
        link = LinkQueue.query.filter_by(url=views_num_form.url.data)
        a = link.views
        point = 'test'
        flash('[INFO] Successfully completed!')
        return redirect(url_for('index'))

    return render_template('index.html', queue_form=queue_form, queue_links=queue_links, views_num_form=views_num_form)
from flask.helpers import flash
from sqlalchemy.orm import query
from app import app, database
from flask import render_template, flash, redirect, url_for
from app.forms import LinkQueueForm, NumberOfViewes
from app.models import LinkQueue

@app.route('/', methods=['GET', 'POST'])
def index():

    return render_template('index2.html')

@app.route('/queue', methods=['GET', 'POST'])
def queue():
    queue_form = LinkQueueForm()
    queue_links = LinkQueue.query.all()

    if queue_form.validate_on_submit():
        link = LinkQueue(url=queue_form.url_for_queue.data, views=queue_form.views.data)
        database.session.add(link)
        database.session.commit()
        flash('[INFO] Successfully added!')
        return redirect(url_for('queue'))

    return render_template('queue.html', queue_form=queue_form, queue_links=queue_links)


@app.route('/queue/<int:id>/delete')
def delete(id):
    # try:
    link = LinkQueue.query.filter_by(id=id)
    for l in link:
        database.session.delete(l)
    database.session.commit()
    flash('[INFO] Successfully deleted!')
    # except:
        # flash('[ERROR] Delete fail!')

    return redirect(url_for('queue'))


@app.route('/views', methods=['GET', 'POST'])
def views():
    views_num_form = NumberOfViewes()
    queue_links = LinkQueue.query.all()

    return render_template('views.html', views_num_form=views_num_form, queue_links=queue_links)


@app.route('/views/<int:id>/start')
def start(id):
    views_num_form = NumberOfViewes()

    if views_num_form.validate_on_submit():
        # alg here
        # link = LinkQueue.query.filter_by(id=id)
        # a = link.views
        # point = 'test'
        flash(f'[INFO] Successfully completed! {id}')
        return redirect(url_for('index'))
    
    return redirect(url_for('index'))

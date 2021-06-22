from flask.globals import request
from flask.helpers import flash
from flask import render_template, flash, redirect, url_for
from threading import Thread, enumerate
from datetime import date

from .log import main_logger, custom_logger
from .daemon_tasks import DaemonTasks as dt
from config import basedir

from app import app, database
from app.forms import LinkQueueForm, NumberOfViewes, FilterForm, AllLinkViewes
from app.models import LinkQueue, BrowsingHistory

mlog = main_logger()

@app.route('/', methods=['GET', 'POST'])
def index():

    return render_template('index.html')

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
    try:
        link = LinkQueue.query.filter_by(id=id)
        for l in link:
            database.session.delete(l)
        database.session.commit()
        flash('[INFO] Successfully deleted!')
    except:
        flash('[ERROR] Delete fail!')

    return redirect(url_for('queue'))


@app.route('/views', methods=['GET', 'POST'])
def views():
    all_links_form = AllLinkViewes()
    views_num_form = NumberOfViewes()
    queue_links = LinkQueue.query.all()

    for thr in enumerate():
        if thr.name == 'daemonViewer':
            daemon_viewer = True
            # id_in_viewer = thr._args[1]
            break
        else:
            daemon_viewer = False
            # id_in_viewer = None

    if all_links_form.validate_on_submit():
        clog = custom_logger(0, 'secondary_alg')

        thread = Thread(target=dt.daemon_func_salg, name=f'daemonViewer', args=(clog,), daemon=True)
        # thread = Thread(target=dt.daemon_task_test, name=f'daemonViewer', args=(clog, id), daemon=True)
        thread.start()

        return redirect(url_for('views'))
    
    return render_template(
        'views.html', 
        all_links_form=all_links_form, 
        views_num_form=views_num_form, 
        queue_links=queue_links, 
        daemon_viewer=daemon_viewer, 
        # id_in_viewer=id_in_viewer
    )


@app.route('/views/<int:id>/start', methods=['POST'])
def start(id):
    views_num_form = NumberOfViewes()
    clog = custom_logger(id, 'primary_alg')

    thread = Thread(target=dt.daemon_func_alg, name=f'daemonViewer', args=(views_num_form.num.data, id, clog), daemon=True)
    thread.start()

    return redirect(url_for('views'))


@app.route('/database', methods=['GET', 'POST'])
def database_page():
    filter_form = FilterForm()
    page = request.args.get('page', 1, type=int)
    history = BrowsingHistory.query.paginate(page, 10, False)
    count = len(BrowsingHistory.query.all())
    curr_object = 'All'

    next_page = url_for('database_page', page=history.next_num) if history.has_next else None
    prev_page = url_for('database_page', page=history.prev_num) if history.has_prev else None

    if filter_form.validate_on_submit():
        if filter_form.data['submit_filter'] == True:
            history = BrowsingHistory.query.filter_by(url=filter_form.curr_url.data.url).all()
            count = len(history)
            curr_object = 'Current'
            return render_template('database.html', filter_form=filter_form, history=history, count=count, curr_object=curr_object)
        if filter_form.data['submit_delete'] == True:
            links_to_delete = BrowsingHistory.query.filter_by(url=filter_form.curr_url.data.url).all()
            for link in links_to_delete:
                database.session.delete(link)
            database.session.commit()
            return redirect(url_for('database_page'))

    return render_template('database.html', filter_form=filter_form, history=history.items, count=count, curr_object=curr_object, next_page=next_page, prev_page=prev_page)


@app.route('/logs')
def logs():

    today = date.today()
    curr_date = today.strftime('%d_%m_%Y')

    glob_log = open(f'{basedir}/logs/app.log', 'r')
    prim_log = open(f'{basedir}/logs/viewer/primary_alg_{curr_date}.log', 'r')
    secn_log = open(f'{basedir}/logs/viewer/secondary_alg_{curr_date}.log', 'r')

    return render_template('logs.html', glob_log=glob_log, prim_log=prim_log, secn_log=secn_log)
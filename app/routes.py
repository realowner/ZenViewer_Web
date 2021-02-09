from flask.helpers import flash
from flask import render_template, flash, redirect, url_for
from threading import Thread
import time

from .zensel.algorithm import Algorithm as alg
from .zensel.secondary.GetProxy import GetProxy as gpr

from app import app, database
from app.forms import LinkQueueForm, NumberOfViewes
from app.models import LinkQueue, BrowsingHistory


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
    views_num_form = NumberOfViewes()
    queue_links = LinkQueue.query.all()

    return render_template('views.html', views_num_form=views_num_form, queue_links=queue_links)


@app.route('/views/<int:id>/start', methods=['GET', 'POST'])
def start(id):
    views_num_form = NumberOfViewes()
    links = LinkQueue.query.filter_by(id=id)

    try:
        before_urls_count = len([item.ip for item in BrowsingHistory.query.filter_by(url=links[0].url)])
    except Exception as count_ex:
        print(count_ex)
        before_urls_count = 0

    print(f'---> BUC: {before_urls_count}')

    proxies = gpr.get_list()
    try:
        ###############################
        thread_list = []
        if proxies == None:
            print('No suitable proxy')
        else:
            for count in range(views_num_form.num.data):
                thread = Thread(target=alg.read_article_withwhile, name=f'THREAD {count+1}', args=(count+1, links))
                thread_list.append(thread)
                thread.start()
                start_time = time.time()
                print(f'> THREAD {count+1} started')

            for thr in thread_list:
                thr.join()
                print(f'> {thr.name} stopped')
                print(f'    - time: {time.time() - start_time}')

        print('\nCOMPLETED')
        print(f'TIME: {time.time() - start_time}')

        after_urls_count = len([item.ip for item in BrowsingHistory.query.filter_by(url=links[0].url)])

        print(f'---> AUC: {after_urls_count}')

        if after_urls_count > before_urls_count:
            flash('[INFO] Successfully completed!')
            return redirect(url_for('views'))
        else:
            flash('[INFO] No suitable proxy, try again!')
            return redirect(url_for('views'))
        ###############################

        # link = LinkQueue.query.filter_by(id=id)
        # for l in link:
        #     l.views = l.views - views_num_form.num.data
        #     if l.views == 0:
        #         database.session.delete(l)
        # database.session.commit()
        # flash('[INFO] Successfully completed!')
        # return redirect(url_for('views'))
    except Exception as ex:
        print(ex)
        flash('[ERROR] Viewer failed!')
        return redirect(url_for('views'))

from flask.globals import request, session
from flask.helpers import flash
from flask import render_template, flash, redirect, url_for
from threading import Thread
import time

from .zensel.algorithm import Algorithm as alg
from .zensel.secondary_algorithm import SecondaryAlgorithm as salg
from .zensel.secondary.GetProxy import GetProxy as gpr
from .zensel.secondary.ThreadNum import ThreadNum as thn
from .log import *

from app import app, database
from app.forms import LinkQueueForm, NumberOfViewes, FilterForm, AllLinkViewes
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
    all_links_form = AllLinkViewes()
    views_num_form = NumberOfViewes()
    queue_links = LinkQueue.query.all()
    url_slices = lambda urls, count: [urls[i:i+count] for i in range(0, len(urls), count)]

    if all_links_form.validate_on_submit():
        thr_num = thn.how_many_threads(len(queue_links))
        links = url_slices(queue_links, int(len(queue_links)/thr_num))
        proxies = gpr.get_list()

        try:
            before_urls_count = len(BrowsingHistory.query.all())
        except Exception as count_ex:
            logging.exception(count_ex)
            before_urls_count = 0

        logging.info(f'---> BUC: {before_urls_count}')

        try:
            thread_list = []
            if proxies == None:
                logging.info('No suitable proxy')
            else:
                for count in range(thr_num):
                    thread = Thread(target=salg.read_article_withwhile, name=f'THREAD {count+1}', args=(count+1, links[count]))
                    thread_list.append(thread)
                    thread.start()
                    start_time = time.time()
                    logging.info(f'> THREAD {count+1} started')
                    time.sleep(5)

                for thr in thread_list:
                    thr.join()
                    logging.info(f'> {thr.name} stopped - time: {time.time() - start_time}')

            logging.info(f'COMPLETED WITH TIME: {time.time() - start_time}')

            after_urls_count = len(BrowsingHistory.query.all())

            logging.info(f'---> AUC: {after_urls_count}')
            difference = after_urls_count - before_urls_count

            if after_urls_count > before_urls_count:
                for link in links:
                    for l in link:
                        l.views = l.views - 1
                        if l.views <= 0:
                            database.session.delete(l)
                    database.session.commit()

                flash(f'[INFO] Successfully completed. {difference} of {len(queue_links)}')
                return redirect(url_for('views'))
            else:
                flash('[INFO] No suitable proxy or bad url, try again!')
                return redirect(url_for('views'))

        except Exception as ex:
            logging.exception(ex)
            flash('[ERROR] Viewer failed!')
            return redirect(url_for('views'))


    return render_template('views.html', all_links_form=all_links_form, views_num_form=views_num_form, queue_links=queue_links)


@app.route('/views/<int:id>/start', methods=['GET', 'POST'])
def start(id):
    views_num_form = NumberOfViewes()
    links = LinkQueue.query.filter_by(id=id)

    try:
        before_urls_count = len([item.ip for item in BrowsingHistory.query.filter_by(url=links[0].url)])
    except Exception as count_ex:
        logging.exception(count_ex)
        before_urls_count = 0

    logging.info(f'---> BUC: {before_urls_count}')

    thr_num = thn.how_many_threads(views_num_form.num.data)
    views_num = int(views_num_form.num.data / thr_num)

    proxies = gpr.get_list()
    try:
        thread_list = []
        if proxies == None:
            logging.info('No suitable proxy')
        else:
            for count in range(thr_num):
                thread = Thread(target=alg.read_article_withwhile, name=f'THREAD {count+1}', args=(count+1, links, views_num))
                thread_list.append(thread)
                thread.start()
                start_time = time.time()
                logging.info(f'> THREAD {count+1} started')
                time.sleep(5)

            for thr in thread_list:
                thr.join()
                logging.info(f'> {thr.name} stopped - time: {time.time() - start_time}')

        logging.info(f'COMPLETED WITH TIME: {time.time() - start_time}')

        after_urls_count = len([item.ip for item in BrowsingHistory.query.filter_by(url=links[0].url)])

        logging.info(f'---> AUC: {after_urls_count}')
        difference = after_urls_count - before_urls_count

        if after_urls_count > before_urls_count:
            for l in links:
                l.views = l.views - difference
                if l.views <= 0:
                    database.session.delete(l)
            database.session.commit()

            flash(f'[INFO] Successfully completed. {difference} of {views_num_form.num.data}')
            return redirect(url_for('views'))
        else:
            flash('[INFO] No suitable proxy or bad url, try again!')
            return redirect(url_for('views'))

    except Exception as ex:
        logging.exception(ex)
        flash('[ERROR] Viewer failed!')
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

    return render_template('logs.html')
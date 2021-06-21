import time
from threading import Thread
from app import database
from app.models import BrowsingHistory
from .zensel.algorithm import Algorithm as alg
from .zensel.secondary_algorithm import SecondaryAlgorithm as salg
from .zensel.secondary.GetProxy import GetProxy as gpr
from .zensel.secondary.ThreadNum import ThreadNum as thn


class DaemonTasks:

    def daemon_func_alg(before_urls_count, views_num_form, links, clog):
        clog.info(f'---> BUC: {before_urls_count}')

        thr_num = thn.how_many_threads(views_num_form)
        views_num = int(views_num_form / thr_num)

        proxies = gpr.get_list()
        try:
            thread_list = []
            if proxies == None:
                clog.info('No suitable proxy')
            else:
                for count in range(thr_num):
                    thread = Thread(target=alg.read_article_withwhile, name=f'THREAD {count+1}', args=(count+1, links, views_num, clog))
                    thread_list.append(thread)
                    thread.start()
                    start_time = time.time()
                    clog.info(f'> THREAD {count+1} started')
                    time.sleep(5)

                for thr in thread_list:
                    thr.join()
                    clog.info(f'> {thr.name} stopped - time: {time.time() - start_time}')

            clog.info(f'COMPLETED WITH TIME: {time.time() - start_time}')

            after_urls_count = len([item.ip for item in BrowsingHistory.query.filter_by(url=links[0].url)])

            clog.info(f'---> AUC: {after_urls_count}')
            difference = after_urls_count - before_urls_count

            if after_urls_count > before_urls_count:
                for l in links:
                    l.views = l.views - difference
                    if l.views <= 0:
                        database.session.delete(l)
                database.session.commit()
                
                clog.info(f'[INFO] Successfully completed. {difference} of {views_num_form}')
            else:
                clog.info('[INFO] No suitable proxy or bad url, try again!')

        except Exception as ex:
            clog.exception(ex)
            clog.info('[ERROR] Viewer failed!')


    def daemon_func_salg(queue_links, before_urls_count, clog):
        url_slices = lambda urls, count: [urls[i:i+count] for i in range(0, len(urls), count)]

        thr_num = thn.how_many_threads(len(queue_links))
        links = url_slices(queue_links, int(len(queue_links)/thr_num))
        proxies = gpr.get_list()
        clog.info(f'---> BUC: {before_urls_count}')

        try:
            thread_list = []
            if proxies == None:
                clog.info('No suitable proxy')
            else:
                for count in range(thr_num):
                    thread = Thread(target=salg.read_article_withwhile, name=f'THREAD {count+1}', args=(count+1, links[count], clog))
                    thread_list.append(thread)
                    thread.start()
                    start_time = time.time()
                    clog.info(f'> THREAD {count+1} started')
                    time.sleep(5)

                for thr in thread_list:
                    thr.join()
                    clog.info(f'> {thr.name} stopped - time: {time.time() - start_time}')

            clog.info(f'COMPLETED WITH TIME: {time.time() - start_time}')

            after_urls_count = len(BrowsingHistory.query.all())

            clog.info(f'---> AUC: {after_urls_count}')
            difference = after_urls_count - before_urls_count

            if after_urls_count > before_urls_count:
                for link in links:
                    for l in link:
                        l.views = l.views - 1
                        if l.views <= 0:
                            database.session.delete(l)
                    database.session.commit()

                clog.info(f'[INFO] Successfully completed. {difference} of {len(queue_links)}')
                # flash(f'[INFO] Successfully completed. {difference} of {len(queue_links)}')
                # return redirect(url_for('views'))
            else:
                clog.info('[INFO] No suitable proxy or bad url, try again!')
                # flash('[INFO] No suitable proxy or bad url, try again!')
                # return redirect(url_for('views'))

        except Exception as ex:
            clog.exception(ex)
            clog.info('[ERROR] Viewer failed!')
            # flash('[ERROR] Viewer failed!')
            # return redirect(url_for('views'))

    def daemon_task_test(clog, id):
        for counter in range (3):
            clog.info(f'---> [DAEMON TEST TASK] Iteration {counter}')
            time.sleep(60)
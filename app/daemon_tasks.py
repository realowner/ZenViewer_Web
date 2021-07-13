import time
from threading import Thread
from app import database
from app.models import BrowsingHistory, LinkQueue
from .zensel.algorithm import Algorithm as alg
from .zensel.secondary.GetProxy import GetProxy as gpr
from .zensel.secondary.ThreadNum import ThreadNum as thn


class DaemonTasks:

    def daemon_func_alg(views_num_form, id, clog):
        links = LinkQueue.query.filter_by(id=id)
        try:
            before_urls_count = len([item.ip for item in BrowsingHistory.query.filter_by(url=links[0].url)])
        except Exception as count_ex:
            clog.exception(count_ex)
            before_urls_count = 0

        clog.info('=========================================================================')
        clog.info(f'---> BUC: {before_urls_count}')

        thr_num = thn.how_many_threads(views_num_form)
        views_num = int(views_num_form / thr_num)

        proxies = gpr.get_list()
        try:
            thread_list = []
            if proxies == None:
                clog.warning('Failed to get proxy!')
            else:
                for count in range(thr_num):
                    thread = Thread(target=alg.read_article_withwhile_primary, name=f'THREAD {count+1}', args=(count+1, links, views_num, proxies, clog))
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
                clog.error('[INFO] No suitable proxy or bad url, try again!')

        except Exception as ex:
            clog.exception(ex)
            clog.error('[ERROR] Viewer failed!')


    def daemon_func_salg(clog):
        queue_links = LinkQueue.query.filter_by(service='Zen').all()
        url_slices = lambda urls, count: [urls[i:i+count] for i in range(0, len(urls), count)]

        thr_num = thn.how_many_threads(len(queue_links))
        links = url_slices(queue_links, int(len(queue_links)/thr_num))
        proxies = gpr.get_list()
        
        try:
            before_urls_count = len(BrowsingHistory.query.all())
        except Exception as count_ex:
            clog.exception(count_ex)
            before_urls_count = 0

        clog.info('=========================================================================')
        clog.info(f'---> BUC: {before_urls_count}')

        try:
            thread_list = []
            if proxies == None:
                clog.warning('Failed to get proxy!')
            else:
                for count in range(thr_num):
                    thread = Thread(target=alg.read_article_withwhile_secondary, name=f'THREAD {count+1}', args=(count+1, links[count], proxies, clog))
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
            else:
                clog.error('[INFO] No suitable proxy or bad url, try again!')

        except Exception as ex:
            clog.exception(ex)
            clog.error('[ERROR] Viewer failed!')


    def daemon_func_behance(views_num_form, id, clog):
        links = LinkQueue.query.filter_by(id=id)
        try:
            before_urls_count = len([item.ip for item in BrowsingHistory.query.filter_by(url=links[0].url)])
        except Exception as count_ex:
            clog.exception(count_ex)
            before_urls_count = 0

        clog.info('=========================================================================')
        clog.info(f'---> BUC: {before_urls_count}')

        thr_num = thn.how_many_threads(views_num_form)
        views_num = int(views_num_form / thr_num)

        proxies = gpr.get_list()
        try:
            thread_list = []
            if proxies == None:
                clog.warning('Failed to get proxy!')
            else:
                for count in range(thr_num):
                    thread = Thread(target=alg.behance_alg, name=f'THREAD {count+1}', args=(count+1, links, views_num, proxies, clog))
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
                    # l.views = l.views - difference
                    if l.views <= 0:
                        database.session.delete(l)
                database.session.commit()
                
                clog.info(f'[INFO] Successfully completed. {difference} of {views_num_form}')
            else:
                clog.error('[INFO] No suitable proxy or bad url, try again!')

        except Exception as ex:
            clog.exception(ex)
            clog.error('[ERROR] Viewer failed!')
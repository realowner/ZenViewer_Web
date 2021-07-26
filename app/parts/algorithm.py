from itertools import cycle

import time

from app.models import BrowsingHistory, CurrentViewer
from app import database
from .browser import Browser as brw
from .secondary.GetProxy import GetProxy as gpr
from .secondary.TimeToRead import TimeToRead as ttr


class Algorithm:

    def zen_alg(number, link, ip, port, clog):
        try:
            history_insert = BrowsingHistory(url=link.url, ip=ip, is_successful=True)
            database.session.add(history_insert)
            database.session.commit()
            clog.info(f'[THREAD {number} - LINK {link.id}]   {ip}:{port} insert DONE')
            browser = brw.my_browser(ip, port)
            winsize = browser.get_window_size()
            window_height = winsize["height"]
            browser.set_page_load_timeout(30)
            try:
                clog.info(f'[THREAD {number} - LINK {link.id}]   browser init DONE')
                browser.get(link.url)
                time.sleep(30)
                div = browser.find_element_by_class_name('article-render')
                try:
                    clog.info(f'[THREAD {number} - LINK {link.id}]   article block detected')
                    read_time = browser.find_element_by_xpath('/html/body/div[3]/div[1]/article/div/div[2]/footer/div/div/div[3]/div[2]/span[2]').text
                    article_info = ttr.determine(read_time, div.size['height'], window_height)
                    time.sleep(article_info['time_to_scroll'])
                    for scr_num in range(0, article_info['scrolls']):
                        browser.execute_script(f"window.scrollBy(0,{article_info['scroll_down']})")
                        time.sleep(article_info['time_to_scroll'])
                    clog.info(f'[THREAD {number} - LINK {link.id}]   scroll DONE')
                    like_button = browser.find_element_by_xpath('/html/body/div[3]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/button')
                    like_button.click()
                    time.sleep(20)
                    clog.info(f'[THREAD {number} - LINK {link.id}]   like DONE')
                    clog.info(f'[THREAD {number} - LINK {link.id}]   ALG DETERMINE')
                    return True
                except:
                    article_info = ttr.determine_except(div_height=div.size['height'], div_text=div.text, win_height=window_height)
                    for scr_num in range(0, article_info['scrolls']):
                        browser.execute_script(f"window.scrollBy(0,{article_info['scroll_down']})")
                        time.sleep(article_info['time_to_scroll'])
                    clog.info(f'[THREAD {number} - LINK {link.id}]   scroll DONE')
                    clog.info(f'[THREAD {number} - LINK {link.id}]   ALG DETERMINE EXCEPT')
                    return True
            except:
                clog.warning(f'[THREAD {number} - LINK {link.id}]   {ip}:{port} bad proxy')
                # database.session.delete(history_insert)
                history_insert.is_successful = False
                database.session.commit()
                clog.warning(f'[THREAD {number} - LINK {link.id}]   history insert saved with FALSE')
                return False
            finally:
                browser.close()
                browser.quit()
        except Exception as insert_ex:
            clog.exception(insert_ex)
            clog.error(f'[THREAD {number} - LINK {link.id}]   {ip}:{port} insert FAIL')
            return False

    
    def zen_alg_secondary(number, links, prxs, clog):
        total_views = 0
        cycle_counter = 0
        ip_list = []
        port_dict = {}
        for prx in prxs:
            ip_list.append(prx['host'])
            port_dict.update({prx["host"]: prx["port"]})
            
        ip_cycler = cycle(ip_list)

        for link in links:
            while True:
                cycle_counter += 1

                if cycle_counter == 11:
                    clog.info(f'[THREAD {number} - LINK {link.id}]   no suitable proxy, 60s sleep')
                    cycle_counter = 0
                    ip_list = []
                    port_dict = {}
                    time.sleep(60)
                    proxies = gpr.get_list()
                    for prx in proxies:
                        ip_list.append(prx['host'])
                        port_dict.update({prx["host"]: prx["port"]})
                    ip_cycler = cycle(ip_list)

                ip = next(ip_cycler)
                port = port_dict.get(ip)

                try:
                    ip_from_db = [item.ip for item in BrowsingHistory.query.filter_by(url=link.url).all()]
                except:
                    ip_from_db = []

                if ip not in ip_from_db:

                    try:
                        history_insert = BrowsingHistory(url=link.url, ip=ip, is_successful=True)
                        database.session.add(history_insert)
                        database.session.commit()
                        clog.info(f'[THREAD {number} - LINK {link.id}]   {ip}:{port} insert DONE')

                        browser = brw.my_browser(ip, port)
                        winsize = browser.get_window_size()
                        window_height = winsize["height"]
                        browser.set_page_load_timeout(30)
                        try:
                            browser.get(link.url)
                            time.sleep(20)
                            div = browser.find_element_by_class_name('article-render')

                            try:
                                read_time = browser.find_element_by_xpath('/html/body/div[3]/div[1]/article/div/div[2]/footer/div/div/div[3]/div[2]/span[2]').text
                                article_info = ttr.determine(read_time, div.size['height'], window_height)
                                time.sleep(article_info['time_to_scroll'])
                                for scr_num in range(0, article_info['scrolls']):
                                    browser.execute_script(f"window.scrollBy(0,{article_info['scroll_down']})")
                                    time.sleep(article_info['time_to_scroll'])

                                like_button = browser.find_element_by_xpath('/html/body/div[3]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/button')
                                like_button.click()
                                time.sleep(20)

                                clog.info(f'[THREAD {number} - LINK {link.id}]   ALG DETERMINE')
                            except:
                                article_info = ttr.determine_except(div_height=div.size['height'], div_text=div.text, win_height=window_height)
                                for scr_num in range(0, article_info['scrolls']):
                                    browser.execute_script(f"window.scrollBy(0,{article_info['scroll_down']})")
                                    time.sleep(article_info['time_to_scroll'])
                                clog.info(f'[THREAD {number} - LINK {link.id}]   ALG DETERMINE EXCEPT')
                            
                            clog.info(f'[THREAD {number} - LINK {link.id}]   proxy {ip}:{port} ...COMPLETED')
                            break

                        except:
                            clog.warning(f'[THREAD {number} - LINK {link.id}]   {ip}:{port} bad proxy')
                            database.session.delete(history_insert)
                            database.session.commit()
                        finally:
                            browser.close()
                            browser.quit()

                    except Exception as insert_ex:
                        clog.exception(insert_ex)
                        clog.error(f'[THREAD {number} - LINK {link.id}]   {ip}:{port} insert FAIL')
 
                else:
                    clog.info(f'[THREAD {number} - LINK {link.id}]   link already viewed with {ip}:{port}')

    
    def behance_alg(number, link, ip, port, clog):  
        try:
            history_insert = BrowsingHistory(url=link.url, ip=ip, is_successful=True)
            database.session.add(history_insert)
            database.session.commit()
            try:
                clog.info(f'[THREAD {number} - LINK {link.id}]   {ip}:{port} insert DONE')
                browser = brw.my_browser(ip, port)
                winsize = browser.get_window_size()
                window_height = winsize["height"]
                browser.set_page_load_timeout(60)
                try:
                    clog.info(f'[THREAD {number} - LINK {link.id}]   browser init DONE')
                    browser.get(link.url)
                    time.sleep(20)
                    try:
                        clog.info(f'[THREAD {number} - LINK {link.id}]      Link loaded')
                        work = browser.find_element_by_id("project-modules")
                        work_height =  work.rect['height']
                        work_info = ttr.for_behance(work_height, window_height)
                        try:
                            clog.info(f'[THREAD {number} - LINK {link.id}]      work block detected')
                            for scr_num in range(0, work_info['scrolls']):
                                browser.execute_script(f"window.scrollBy(0,{work_info['scroll_down']})")
                                time.sleep(15)
                            try:
                                clog.info(f'[THREAD {number} - LINK {link.id}]      scrolling DONE')
                                like = browser.find_element_by_class_name("Appreciate-wrapper-9hi")
                                like.click()
                                clog.info(f'[THREAD {number} - LINK {link.id}]      like DONE')
                                
                                time.sleep(5)
                                return True
                            except:
                                clog.error(f'[THREAD {number} - LINK {link.id}]     like btn error!')
                                return False
                        except:
                            clog.error(f'[THREAD {number} - LINK {link.id}]     scrolls error!')
                            return False
                    except:
                        clog.error(f'[THREAD {number} - LINK {link.id}]     work block not found!')
                        database.session.delete(history_insert)
                        database.session.commit()
                        clog.warning(f'[THREAD {number} - LINK {link.id}]   history insert deleted')
                        return False
                except:
                    clog.warning(f'[THREAD {number} - LINK {link.id}]   {ip}:{port} bad proxy')
                    # database.session.delete(history_insert)
                    history_insert.is_successful = False
                    database.session.commit()
                    clog.warning(f'[THREAD {number} - LINK {link.id}]   history insert saved with FALSE')
                    return False
                finally:
                    browser.close()
                    browser.quit()
            except:
                clog.error(f'[THREAD {number} - LINK {link.id}]   browser init FAIL')
                database.session.delete(history_insert)
                database.session.commit()
                clog.warning(f'[THREAD {number} - LINK {link.id}]   history insert deleted')
                return False
        except:
            clog.error(f'[THREAD {number} - LINK {link.id}]   {ip}:{port} insert FAIL')
            return False


    def youtube_alg(number, link, ip, port, clog):
        try:
            history_insert = BrowsingHistory(url=link.url, ip=ip, is_successful=True)
            database.session.add(history_insert)
            database.session.commit()
            try:
                clog.info(f'[THREAD {number} - LINK {link.id}]   {ip}:{port} insert DONE')
                browser = brw.my_browser(ip, port)
                browser.set_page_load_timeout(60)
                try:
                    clog.info(f'[THREAD {number} - LINK {link.id}]   browser init DONE')
                    browser.get(link.url)
                    time.sleep(15)
                    try:
                        clog.info(f'[THREAD {number} - LINK {link.id}]      Link loaded')
                        ########################################################################
                        try:
                            captcha = browser.find_element_by_id('captcha-form')
                            clog.warning(f'[THREAD {number} - LINK {link.id}]      captcha detected')
                            # database.session.delete(history_insert)
                            history_insert.is_successful = False
                            database.session.commit()
                            clog.warning(f'[THREAD {number} - LINK {link.id}]   history insert saved with FALSE')
                            return False
                        except:
                            clog.info(f'[THREAD {number} - LINK {link.id}]      page without captcha')
                            try:
                                confirm = browser.find_element_by_class_name('productLogoContainer')
                                try:
                                    clog.info(f'[THREAD {number} - LINK {link.id}]      confirm detected')
                                    confirm_btn = browser.find_element_by_xpath('/html/body/div[2]/div[3]/form/input[12]')
                                    confirm_btn.click()
                                    time.sleep(15)
                                    try:
                                        clog.info(f'[THREAD {number} - LINK {link.id}]      confirm DONE')
                                        play_btn = browser.find_element_by_class_name('ytp-play-button')
                                        video_time = browser.find_element_by_class_name('ytp-time-duration')
                                        wait_sec = ttr.for_youtube(video_time.text)
                                        play_btn.click()
                                        time.sleep(wait_sec)
                                        return True
                                    except:
                                        clog.warning(f'[THREAD {number} - LINK {link.id}]      play FAIL')
                                        database.session.delete(history_insert)
                                        database.session.commit()
                                        clog.warning(f'[THREAD {number} - LINK {link.id}]   history insert deleted')
                                        return False
                                except:
                                    clog.warning(f'[THREAD {number} - LINK {link.id}]      confirm FAIL')
                                    database.session.delete(history_insert)
                                    database.session.commit()
                                    clog.warning(f'[THREAD {number} - LINK {link.id}]   history insert deleted')
                                    return False
                            except:
                                clog.info(f'[THREAD {number} - LINK {link.id}]      page without confirm')
                                play_btn = browser.find_element_by_class_name('ytp-play-button')
                                video_time = browser.find_element_by_class_name('ytp-time-duration')
                                wait_sec = ttr.for_youtube(video_time.text)
                                play_btn.click()
                                clog.info(f'[THREAD {number} - LINK {link.id}]      play DONE')
                                clog.info(f'[THREAD {number} - LINK {link.id}]      waiting {wait_sec} sec')
                                time.sleep(wait_sec)
                                clog.info(f'[THREAD {number} - LINK {link.id}]      DONE...')
                                return True
                        ########################################################################
                    except:
                        clog.warning(f'[THREAD {number} - LINK {link.id}]      play FAIL')
                        database.session.delete(history_insert)
                        database.session.commit()
                        clog.warning(f'[THREAD {number} - LINK {link.id}]   history insert deleted')
                        return False
                except:
                    clog.warning(f'[THREAD {number} - LINK {link.id}]   {ip}:{port} bad proxy')
                    # database.session.delete(history_insert)
                    history_insert.is_successful = False
                    database.session.commit()
                    clog.warning(f'[THREAD {number} - LINK {link.id}]   history insert saved with FALSE')
                    return False
                finally:
                    browser.close()
                    browser.quit()
            except:
                clog.error(f'[THREAD {number} - LINK {link.id}]   browser init FAIL')
                database.session.delete(history_insert)
                database.session.commit()
                clog.warning(f'[THREAD {number} - LINK {link.id}]   history insert deleted')
                return False
        except:
            clog.error(f'[THREAD {number} - LINK {link.id}]   {ip}:{port} insert FAIL')
            return False
    

    def main(number, links, views_num, prxs, clog, service):
        db_viewer = CurrentViewer.query.get(1)

        total_views = 0
        cycle_counter = 0
        ip_list = []
        port_dict = {}
        for prx in prxs:
            ip_list.append(prx['host'])
            port_dict.update({prx["host"]: prx["port"]})
            
        ip_cycler = cycle(ip_list)
        
        for link in links:
            while total_views != views_num:
                cycle_counter += 1

                if cycle_counter == 11:
                    clog.info(f'[THREAD {number} - LINK {link.id}]   no suitable proxy, 60s sleep')
                    cycle_counter = 0
                    ip_list = []
                    port_dict = {}
                    time.sleep(60)
                    clog.info(f'[THREAD {number} - LINK {link.id}]   alg awakening...')
                    proxies = gpr.get_list()
                    for prx in proxies:
                        ip_list.append(prx['host'])
                        port_dict.update({prx["host"]: prx["port"]})
                    ip_cycler = cycle(ip_list)

                ip = next(ip_cycler)
                port = port_dict.get(ip)

                try:
                    ip_from_db = [item.ip for item in BrowsingHistory.query.filter_by(url=link.url).all()]
                except:
                    ip_from_db = []

                if ip not in ip_from_db:

                    if service == 'Zen':
                        sequence = Algorithm.zen_alg(number, link, ip, port, clog)
                    elif service == 'Behance':
                        sequence = Algorithm.behance_alg(number, link, ip, port, clog)
                    elif service == 'Youtube':
                        sequence = Algorithm.youtube_alg(number, link, ip, port, clog)

                    if sequence:
                        total_views += 1

                        try:
                            link.views = link.views - 1
                            current_link_session = database.session.object_session(link)
                            current_link_session.commit()

                            db_viewer.curr_views += 1
                            database.session.commit()
                            clog.info(f'[THREAD {number} - LINK {link.id}]      db commit DONE')
                        except:
                            clog.info(f'[THREAD {number} - LINK {link.id}]      db commit FAIL')

                else:
                    clog.info(f'[THREAD {number} - LINK {link.id}]   link already viewed with {ip}:{port}')
from itertools import cycle

import time
import math

from app.models import BrowsingHistory
from app import database
from app.log import *

from .browser import Browser as brw
from .secondary.GetProxy import GetProxy as gpr
from .secondary.TimeToRead import TimeToRead as ttr


class SecondaryAlgorithm:

    def read_article_withwhile(number, links):
        total_views = 0
        cycle_counter = 0
        ip_list = []
        port_dict = {}
        proxies = gpr.get_list()
        for prx in proxies:
            ip_list.append(prx['host'])
            port_dict.update({prx["host"]: prx["port"]})
            
        ip_cycler = cycle(ip_list)

        for link in links:
            while True:
                cycle_counter += 1

                if cycle_counter == 11:
                    logging.info(f'[THREAD {number} - LINK {link.id}]   no suitable proxy, 60s sleep')
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
                        # history_insert = BrowsingHistory(url=link.url, ip=ip)
                        # database.session.add(history_insert)
                        # database.session.commit()
                        logging.info(f'[THREAD {number} - LINK {link.id}]   {ip}:{port} insert DONE')

                        browser = brw.my_browser(ip, port)
                        browser.set_page_load_timeout(30)
                        try:
                            browser.get(link.url)
                            time.sleep(20)
                            div = browser.find_element_by_class_name('article-render')

                            try:
                                read_time = browser.find_element_by_xpath('/html/body/div[3]/div[1]/article/div/div[2]/footer/div/div/div[3]/div[2]/span[2]').text
                                article_info = ttr.determine(read_time, div.size['height'])
                                time.sleep(article_info['time_to_scroll'])
                                for scr_num in range(0, article_info['scrolls']):
                                    browser.execute_script(f"window.scrollBy(0,{article_info['scroll_down']})")
                                    time.sleep(article_info['time_to_scroll'])

                                like_button = browser.find_element_by_xpath('/html/body/div[3]/div[1]/div[1]/div[2]/div[2]/div[1]/div[1]/div[1]/button')
                                like_button.click()
                                time.sleep(20)

                                logging.info(f'[THREAD {number} - LINK {link.id}]   ALG DETERMINE')
                            except:
                                article_info = ttr.determine_except(div_height=div.size['height'], div_text=div.text)
                                for scr_num in range(0, article_info['scrolls']):
                                    browser.execute_script(f"window.scrollBy(0,{article_info['scroll_down']})")
                                    time.sleep(article_info['time_to_scroll'])
                                logging.info(f'[THREAD {number} - LINK {link.id}]   ALG DETERMINE EXCEPT')
                            
                            logging.info(f'[THREAD {number} - LINK {link.id}]   proxy {ip}:{port} ...COMPLETED')
                            break

                        except:
                            logging.info(f'[THREAD {number} - LINK {link.id}]   {ip}:{port} bad proxy')
                            # database.session.delete(history_insert)
                            # database.session.commit()
                        finally:
                            browser.close()
                            browser.quit()

                    except Exception as insert_ex:
                        logging.exception(insert_ex)
                        logging.info(f'[THREAD {number} - LINK {link.id}]   {ip}:{port} insert FAIL')
 
                else:
                    logging.info(f'[THREAD {number} - LINK {link.id}]   link already viewed with {ip}:{port}')
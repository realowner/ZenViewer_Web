from itertools import cycle

import time
import math

from app.models import BrowsingHistory
from app import database
from app.log import *

from .browser import Browser as brw
from .secondary.GetProxy import GetProxy as gpr
from .secondary.ShortUrl import ShortUrl as shu
from .secondary.TimeToRead import TimeToRead as ttr
from .secondary.InfoToPrint import InfoToPrint as itp


class Algorithm:

    def read_article_withwhile(number, links):
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

                # rework
                if cycle_counter == 11:
                    logging.info(f'[THREAD {number} - LINK {link.id}]   no suitable proxy, 30s sleep')
                    cycle_counter = 0
                    time.sleep(30)
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
                        history_insert = BrowsingHistory(url=link.url, ip=ip)
                        database.session.add(history_insert)
                        database.session.commit()
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
                                logging.info(f'[THREAD {number} - LINK {link.id}]   ALG DETERMINE EXCEPT | TT:{article_info["total_time"]}, NM:{article_info["num_to_multiply"]}')
                            
                            itp.simple_info(number, link.id, ip, port)
                            break

                        except:
                            logging.info(f'[THREAD {number} - LINK {link.id}]   {ip}:{port} bad proxy')
                            database.session.delete(history_insert)
                            database.session.commit()
                        finally:
                            browser.close()
                            browser.quit()

                    except Exception as insert_ex:
                        logging.exception(insert_ex)
                        logging.info(f'[THREAD {number} - LINK {link.id}]   {ip}:{port} insert FAIL')
 
                else:
                    logging.info(f'[THREAD {number} - LINK {link.id}]   link already viewed with {ip}:{port}')
from .ShortUrl import ShortUrl as shu
from app.log import *

class InfoToPrint:

    def sys_info(number, ip_info, country_info, os_info, browser_info, useragent_info=None, webdriver_info=None):
        print(f'''> THREAD {number} info
    - IP: {ip_info}
    - Country: {country_info}
    - OS: {os_info}
    - Browser: {browser_info}''')

    def zen_article_info(number, link, window_wh, div, article_info, read_time):
        print(f'''> THREAD {number} LINK {link['id']} ...done
    - DETAILS
        Url: {link['url']}
        Window: {window_wh}
        DivHeight: {str(div.size['height'])}
        ReadArea: {article_info['article_height']}
        ZenTimeRead: {read_time}
        TreadTimeRead: {article_info['thread_num']}
        ScrollDown: {article_info['scroll_down']}
        Scrolls: {article_info['scrolls']}
        ScrollTime: {article_info['time_to_scroll']}''')

    def simple_info(number, link, ip, port):
        logging.info(f'[THREAD {number} - LINK {shu.url_shortener(link)}]   proxy {ip}:{port} ...shutdown')
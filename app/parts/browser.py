from selenium import webdriver
from fake_useragent import UserAgent
from config import basedir

from .secondary.WindowSize import WindowSize


class Browser:

    def my_browser(ip=None, port=None):

        useragent = UserAgent()

        options = webdriver.FirefoxOptions()
        options.set_preference('dom.webdriver.enabled', False)
        options.set_preference('dom.webnotifications.enabled', False)
        options.set_preference('media.volume_scale', '0.0')
        options.set_preference('general.useragent.override', useragent.random)

        if ip and port:
            options.set_preference('network.proxy.type', 1)
            options.set_preference('network.proxy.http', ip)
            options.set_preference('network.proxy.http_port', port)
            options.set_preference('network.proxy.https', ip)
            options.set_preference('network.proxy.https_port', port)
            options.set_preference('network.proxy.ssl', ip)
            options.set_preference('network.proxy.ssl_port', port)

        options.headless = True

        browser = webdriver.Firefox(
            # executable_path="firefoxdriver\geckodriver.exe",
            # executable_path='firefoxdriver/geckodriver',
            executable_path=f'{basedir}/app/parts/firefoxdriver/geckodriver',
            options=options,
            log_path=f'{basedir}/logs/geckodriver.log',
        )

        window_size = WindowSize.get_size()
        browser.set_window_size(window_size['width'], window_size['height'])

        return browser

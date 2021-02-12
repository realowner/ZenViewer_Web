from .zensel.browser import Browser as brw
import time

ip = '194.247.179.164'
port = 80
url = 'https://zen.yandex.ru/media/different_angle/a-vy-znali-chto-neznaika-rodom-iz-kanady-istoriia-poiavleniia-personaja-602291079eeef76a69411c66'

test_browser = brw.my_browser(ip, port)

try:
    test_browser.get(url)
    time.sleep(20)
    
except:
    print('Error')
finally:
    test_browser.close()
    test_browser.quit()
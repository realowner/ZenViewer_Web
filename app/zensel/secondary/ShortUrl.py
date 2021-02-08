import pyshorteners


class ShortUrl:

    def url_shortener(url):

        short_url = pyshorteners.Shortener().clckru.short(url)
        return short_url
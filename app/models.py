from app import database


class LinkQueue(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    url = database.Column(database.Text, nullable=False)
    views = database.Column(database.Integer, nullable=True)

    def __rerp__(self):
        return f'{self.url} > {self.views} views left'


class BrowsingHistory(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    url = database.Column(database.Text, nullable=False)
    ip = database.Column(database.String(30), nullable=False)

    def __repr__(self):
        return f'{self.url} has been viewed with {self.ip}'

from app import database


class LinkQueue(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    url = database.Column(database.Text, nullable=False)
    service = database.Column(database.String(15), nullable=False)
    views = database.Column(database.Integer, nullable=True)

    def __rerp__(self):
        return f'{self.url} > {self.views} views/likes left'


class BrowsingHistory(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    url = database.Column(database.Text, nullable=False)
    ip = database.Column(database.String(30), nullable=False)
    is_successful = database.Column(database.Boolean, nullable=False)

    def __repr__(self):
        return f'{self.url} has been viewed with {self.ip}'


class Settings(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    thr_num = database.Column(database.Integer, nullable=False)
    sec_alg = database.Column(database.Boolean, nullable=False)


class CurrentViewer(database.Model):
    id = database.Column(database.Integer, primary_key=True)
    curr_views = database.Column(database.Integer, nullable=False)
    need_views = database.Column(database.Integer, nullable=False)
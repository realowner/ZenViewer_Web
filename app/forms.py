from flask_wtf import FlaskForm
from wtforms import IntegerField, TextField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from app.models import LinkQueue


class LinkQueueForm(FlaskForm):
    url_for_queue = TextField('Url:', validators=[DataRequired()])
    views = IntegerField('How many views:', validators=[DataRequired()])
    submit_link = SubmitField('Add to queue')

    def validate_url(self, url):
        url_from_db = LinkQueue.query.filter_by(url=url.data).first()
        if url_from_db is not None:
            raise ValidationError('Url already exist!')


class NumberOfViewes(FlaskForm):
    # url_for_viewer = TextField('Url:', validators=[DataRequired()])
    num = IntegerField('Views:', validators=[DataRequired()])
    submit_view = SubmitField('Start')
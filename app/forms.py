from flask_wtf import FlaskForm
from wtforms import IntegerField, TextField, SubmitField
from wtforms.validators import DataRequired, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.models import LinkQueue


class LinkQueueForm(FlaskForm):
    url_for_queue = TextField('Url:', validators=[DataRequired()])
    views = IntegerField('How many views:', validators=[DataRequired()])
    submit_link = SubmitField('Add to queue')

    def validate_url_for_queue(self, url_for_queue):
        url_from_db = LinkQueue.query.filter_by(url=url_for_queue.data).first()
        if url_from_db is not None:
            raise ValidationError('Url already exist.')   
        if 'https://' not in url_for_queue.data:
            raise ValidationError('Url not valid.')

    def validate_views(self, views):
        if type(views.data) is not int:
            raise ValidationError('Not int')
        if views.data <= 0:
            raise ValidationError('Num not valid.')


class NumberOfViewes(FlaskForm):
    # url_for_viewer = TextField('Url:', validators=[DataRequired()])
    num = IntegerField('Views:', validators=[DataRequired()])
    submit_view = SubmitField('Start')


class FilterForm(FlaskForm):
    curr_url = QuerySelectField('Url', query_factory=lambda: LinkQueue.query.all(), get_label='url')
    submit_filter = SubmitField('Search')
    submit_delete = SubmitField('Delete')
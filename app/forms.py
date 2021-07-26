from flask_wtf import FlaskForm
from sqlalchemy.orm import defaultload
from wtforms import IntegerField, TextField, SubmitField, BooleanField
from wtforms.fields.core import SelectField
from wtforms.validators import DataRequired, ValidationError
from wtforms.ext.sqlalchemy.fields import QuerySelectField
from app.models import LinkQueue


class SettingsForm(FlaskForm):
    thr_num = IntegerField('Threads quantity:', validators=[DataRequired()])
    sec_alg = BooleanField('Secondary algorithm')
    submit_all = SubmitField('Save')

    def validate_thr_num(self, thr_num):
        if type(thr_num.data) is not int:
            raise ValidationError('Must be int')
        if thr_num.data <= 0:
            raise ValidationError('Num not valid.')


class LinkQueueForm(FlaskForm):
    url_for_queue = TextField('Url:', validators=[DataRequired()])
    views = IntegerField('Views:', validators=[DataRequired()])
    service = SelectField('Service:', validators=[DataRequired()], choices=[('Zen', 'Zen'), ('Behance', 'Behance'), ('Youtube', 'Youtube')])
    submit_link = SubmitField('Add')

    def validate_url_for_queue(self, url_for_queue):
        url_from_db = LinkQueue.query.filter_by(url=url_for_queue.data).first()
        if url_from_db is not None:
            raise ValidationError('Url already exist.')   
        if 'https://' not in url_for_queue.data:
            raise ValidationError('Url not valid.')

    def validate_views(self, views):
        if type(views.data) is not int:
            raise ValidationError('Must be int')
        if views.data <= 0:
            raise ValidationError('Num not valid.')


class NumberOfViewes(FlaskForm):
    num = IntegerField('Views:', validators=[DataRequired()])
    submit_view = SubmitField('Start')


class AllLinkViewes(FlaskForm):
    submit_all = SubmitField('Start All')


class FilterForm(FlaskForm):
    curr_url = QuerySelectField('Url', query_factory=lambda: LinkQueue.query.all(), get_label='url')
    submit_filter = SubmitField('Search')
    submit_delete = SubmitField('Delete')
from flask_wtf import CSRFProtect, FlaskForm
from wtforms import StringField, TextField, SubmitField,validators,SelectMultipleField,PasswordField,BooleanField \
,IntegerField,HiddenField
from wtforms.validators import (DataRequired,
                                Email,
                                EqualTo,
                                Length,
                                URL)
from wtforms_sqlalchemy.fields import QuerySelectField,QuerySelectMultipleField

"""
 fix Flask WTForms and WTForms-SQLAlchemy QuerySelectField produce too many values to unpack 
"""
from ..models.fix_wtf_sql import fix_wtfsql
fix_wtfsql()

class UpdateUser(FlaskForm):
    from ..models.user import User
    """Contact form."""
    name = StringField('Name', [
        DataRequired()])
    email = StringField('Email', [
        Email(message=('Not a valid email address.')),
        DataRequired()]) 
    source = TextField('source', [
        DataRequired(),
        Length(min=4, message=('Your message is too short.'))], 
        render_kw={'class':'myclass','style':'font-size:150%'})
    active = BooleanField('Active')        

    submit = SubmitField('Submit')    

class UserRolesForm(FlaskForm):
    from ..models.user import Roles,getRoles
    id = HiddenField('id')
    name = StringField('Name')
    roles = QuerySelectMultipleField('Roles', 
            query_factory=getRoles)
    submit = SubmitField('Submit') 
    # Custom validate
    def validate(self):
        # ... custom validation
        return True        
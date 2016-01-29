"""
forms.py: Application forms

__author__ = "Fernando P. Lopes"
__email__ = "fpedrosa@gmail.com"

"""

from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField
from wtforms.validators import InputRequired, Length, Email


# noinspection PyAbstractClass
class ContactForm(Form):
    name = StringField("Nome", validators=[
        InputRequired("Por favor, informe o seu nome")
        , Length(min=2, message="O seu nome deve ter pelo menos 2 caracteres")
        , Length(max=128, message="O seu nome deve ter no máximo 128 caracteres")
    ])

    email = StringField("Email", validators=[
        InputRequired("Por favor, informe seu email")
        , Length(min=6, message="O seu email deve ter pelo menos 6 caracteres")
        , Email(message="Por favor, informe um email válido")
    ])

    message = TextAreaField("Mensagem", validators=[
        InputRequired("Por favor, escreva sua mensagem")
        , Length(min=3, max=512, message="A sua mensagem deve ter no mínimo 3 caracteres e no máximo 512")
    ])

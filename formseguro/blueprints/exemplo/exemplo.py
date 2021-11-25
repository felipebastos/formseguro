from flask import Blueprint, request, render_template

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, FileField, EmailField
from wtforms.validators import DataRequired, Email, EqualTo

from formseguro.ext.database import db
from formseguro.models import Usuario

#Formulário
class CadastroForm(FlaskForm):
    nome = StringField(label='Nome:', name="nome", validators=[DataRequired(message="Você tem nome, não?")])
    senha = PasswordField(label='Senha:', name="senha", validators=[EqualTo('confirm', message="A senha deveria ser igual"), DataRequired(message="Tu num quer senha não?")])
    confirm = PasswordField('Repita a senha')
    email = EmailField(label='Email:', name="email", validators=[Email()])
    fotoperfil = FileField(label='Foto de perfil:', name="fotoperfil")


bp = Blueprint('exemplo', __name__, url_prefix='/exemplo', template_folder='templates')


@bp.route('/', methods=['GET', 'POST'])
def root():
    form = CadastroForm()

    if request.method == 'POST':
        if form.validate_on_submit():
            novo = Usuario()
            novo.nome = form.nome.data
            novo.senha = form.senha.data

            db.session.add(novo)
            db.session.commit()

            return "Validou"

    return render_template('exemplo/index.html', form=form)


def init_app(app):
    app.register_blueprint(bp)
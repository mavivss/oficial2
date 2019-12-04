from flask import Flask, render_template, request, flash, redirect, url_for
from flask_sqlalchemy import SQLAlchemy
from forms import CadastroUsuario, LoginUsuario
from flask_login import LoginManager, login_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///MeuSite.db'
app.config['SECRET_KEY'] = 'ajlkecbgajlkecbg' 

db = SQLAlchemy(app)
login_manager = LoginManager(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    usuario = db.Column(db.String(80), unique=True, nullable=True)
    email = db.Column(db.String(12), unique=True, nullable=False)
    senha = db.Column(db.String(120), nullable=False)

    @property
    def is_authenticated(self):
        return True

    @property
    def is_active(self):
        return True

    @property
    def is_anonymou(self):
        return False
      
    def get_id(self):
        return str(self.id)

    def __repr__(self):
        return '<User %r>' % self.usuario

@login_manager.user_loader
def load_user(id):
    return User.query.filter_by(id=id).first()

@app.route('/')
@app.route('/index')
def index():
    users=User.query.all()
    return render_template('index.html', users=users)


@app.route('/doacoes')
def doacoes():
    return render_template('/doacoes.html')


@app.route('/cadastre', methods = ['GET', 'POST'])
def cadastre():
    form = CadastroUsuario()
    if form.validate_on_submit():
        usuario = form.usuario.data
        email = form.email.data
        senha = form.senha.data
        repita_senha = form.repita_senha.data
        user = User.query.filter_by(email=email).first()
        if user:
            flash("Dados inválidos")
            return redirect(url_for('cadastre'))

        if senha != repita_senha:
            flash("Dados inválidos")
            return redirect(url_for('cadastre'))

        new_user = User(usuario=usuario, email=email, senha=generate_password_hash(senha))
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for("login"))
    return render_template('cadastre.html', form = form)

@app.route('/login', methods = ['GET', 'POST'])
def login():
    form = LoginUsuario()
    if form.validate_on_submit():
        print("entrei aqui")
        user = User.query.filter_by(usuario=form.usuario.data).first()
        print(user)
        if user and user.senha == form.senha.data:
            print(user)
            login_user(user)
            flash("Acesso permitido")
            return redirect(url_for("index"))
        else:
            flash("Acesso negado")
            return redirect(url_for("login"))
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for("index"))

if __name__ == "__main__":
   app.run(debug=True)

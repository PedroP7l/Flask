from flask import Flask, render_template, request, redirect, session, flash, url_for
from dao import TreinamentoDao, UsuarioDao
from flask_mysqldb import MySQL
from models import Treinamento, Usuario
import os

app = Flask(__name__)
app.secret_key = 'alura'

app.config['MYSQL_HOST'] = "localhost"
app.config['MYSQL_USER'] = "root"
app.config['MYSQL_PASSWORD'] = "admin"
app.config['MYSQL_DB'] = "treinamentoteca"
app.config['MYSQL_PORT'] = 3306
app.config['UPLOAD_PATH'] = os.path.dirname(os.path.abspath(__file__)) + '/uploads'


db = MySQL(app)
treinamento_dao = TreinamentoDao(db)
usuario_dao = UsuarioDao(db)


@app.route('/')
def index():
    lista = treinamento_dao.listar()
    return render_template('lista.html', titulo='Treinamentos', treinamentos=lista)


@app.route('/novo')
def novo():
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('novo')))
    return render_template('novo.html', titulo='Novo Treinamento')


@app.route('/criar', methods=['POST', ])
def criar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    treinamento = Treinamento(nome, categoria, console)
    treinamento = treinamento_dao.salvar(treinamento)

    arquivo = request.files['arquivo']
    upload_path = app.config['UPLOAD_PATH']
    arquivo.save(f'{upload_path}/capa{treinamento.id}.jpg')
    return redirect(url_for('index'))


@app.route('/editar/<int:id>')
def editar(id):
    if 'usuario_logado' not in session or session['usuario_logado'] == None:
        return redirect(url_for('login', proxima=url_for('editar')))
    treinamento = treinamento_dao.busca_por_id(id)
    return render_template('editar.html', titulo='Editando Treinamento', treinamento=treinamento)


@app.route('/atualizar', methods=['POST', ])
def atualizar():
    nome = request.form['nome']
    categoria = request.form['categoria']
    console = request.form['console']
    treinamento = Treinamento(nome, categoria, console, id=request.form['id'])
    treinamento_dao.salvar(treinamento)
    return redirect(url_for('index'))


@app.route('/deletar/<int:id>')
def deletar(id):
    treinamento = treinamento_dao.busca_por_id(id)
    treinamento_dao.deletar(id)
    flash('O treinamento ' + treinamento.nome + ' foi removido com sucesso!')
    return redirect(url_for('index'))


@app.route('/login')
def login():
    proxima = request.args.get('proxima')
    return render_template('login.html', proxima=proxima)


@app.route('/autenticar', methods=['POST', ])
def autenticar():
    usuario = usuario_dao.buscar_por_id(request.form['usuario'])
    if usuario:
        if usuario.senha == request.form['senha']:
            session['usuario_logado'] = usuario.id
            flash(usuario.nome + ' logou com sucesso!')
            proxima_pagina = request.form['proxima']
            return redirect(proxima_pagina)
    else:
        flash('Não logado, tente denovo!')
        return redirect(url_for('login'))


@app.route('/logout')
def logout():
    session['usuario_logado'] = None
    flash('Nenhum usuário logado!')
    return redirect(url_for('index'))


app.run(debug=True)

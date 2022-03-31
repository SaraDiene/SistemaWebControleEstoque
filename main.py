
from flask import Flask, redirect, render_template, request,session,url_for
from banco_dados_estoque import Categoria, Produto, Usuario,Venda
from datetime import datetime




app = Flask(__name__)
app.secret_key = 'senac'
grupo_logado = None



@app.route('/')
def abre_index():
    if 'username' in session:
        return render_template('index.html', grupo_user = grupo_logado)
    return redirect(url_for('abre_login'))


@app.route('/cadastro_produto')
def abre_pagina_cadastro_itens():
    if 'username' in session:
        categoria_objeto = Categoria(None,None)
        lista_categorias = categoria_objeto.select_todas_categorias()
        produto_objeto = Produto(None,None,None,None,None,None,None)
        return render_template('cadastro.html', lista = lista_categorias, lista_produto = produto_objeto.select_todos_produtos())
    return redirect(url_for('abre_login'))

@app.route('/cadastro_produto', methods = ['POST'])
def salva_produto():
    id_categoria = request.form['id_categoria']
    nome_produto = request.form['nome_produto']
    valor_produto = request.form['valor_produto']
    validade_produto = request.form['validade_produto']
    quantidade_produto = request.form['quantidade_produto']
    descricao_produto = request.form['descricao_produto']
    objeto_produto = Produto(id = None, nome = nome_produto, valor = valor_produto, quantidade = quantidade_produto, validade = validade_produto,descricao = descricao_produto, categoria = id_categoria ) #Dessa forma podemos passar os parametros na ordem que quisermos.
    objeto_produto.insere_produtos()
    return render_template('cadastro.html')
    

@app.route('/categoria')
def abre_pagina_cadastro_categoria():
    if 'username' in session:
        lista_categoria = Categoria(None,None)
        return render_template('cadastro_categoria.html',lista = lista_categoria.select_todas_categorias())
    return redirect(url_for('abre_login'))


@app.route('/categoria', methods = ['POST'])
def salva_cadastro_categoria():
    valor = request.form['nome_categoria']
    categoria_objeto = Categoria(None,valor) #Dessa forma os parametros precisam estar exatamente da forma que está pedindo
    mensagem = categoria_objeto.insert_categoria()  
    return render_template('cadastro_categoria.html', resultado = mensagem, lista = categoria_objeto.select_todas_categorias())

@app.route('/pesquisar_categorias', methods = ['POST'])
def busca_categoria():
    id = request.form['id_categoria']
    nome_produto = request.form['nome_produto']
    produto_objeto = Produto()
    categoria_objeto = Categoria(None,None)
    lista_produto = produto_objeto.select_produto_categoria(id,nome_produto)
    lista_categoria = categoria_objeto.select_todas_categorias()
    return render_template('cadastro.html', lista_produto = lista_produto, lista_categoria = lista_categoria)

@app.route('/vendas')
def abre_venda():
    objeto_produto = Produto()
    return render_template('vendas.html', produto = objeto_produto)

@app.route('/realiza_venda', methods = ['POST'])
def realiza_venda():
    Id = request.form['id']
    quantidade_estoque = int(request.form['quantidade_estoque'])
    quantidade_comprada = int(request.form['quantidade_produto'])
    valor_produto =float(request.form['valor_produto'])
    valor_venda = valor_produto * quantidade_comprada
    objeto_produto = Produto()

    if quantidade_comprada <= quantidade_estoque:
        quantidade = quantidade_estoque - quantidade_comprada
        objeto_produto.atualiza_quantidade(quantidade,Id)
        objeto_venda = Venda(produto_id = Id, data = datetime.now(), valor = valor_venda, quantidade = quantidade_comprada)
        objeto_venda.insere_venda()

    else:
        return render_template('vendas.html', alerta = "Estoque insuficiente")

    return redirect(url_for('abre_venda'))
    

@app.route('/pesquisa_produtos', methods = ['POST'])
def pesquisa_produto():
    codigo = request.form['codigo_produto']
    nome = request.form['nome_produto']
    produto_carregado = Produto()
    return render_template('vendas.html', produto = produto_carregado.pesquisa_produto_id(codigo))

@app.route('/administrador')
def abre_administrador():
    if 'username' in session and grupo_logado == 1: 
        usuario = Usuario()     
        return render_template('administrador.html', lista_usuario = usuario.exibe_usuarios())
    else:
        return redirect(url_for('abre_login'))
     

@app.route('/cadastro_usuario', methods = ['POST'])
def cadastro_usuario():
    usuario = request.form['nome']
    cpf = request.form['cpf']
    depto = request.form['depto']
    email = request.form['email']
    grupo = request.form['grupo']
    senha = request.form['password']
    novo_usuario = Usuario(usuario,cpf,depto,email,senha,grupo)
    resposta = novo_usuario.insere_usuario()
    return render_template('administrador.html', mensagem = resposta, lista_usuario = novo_usuario.exibe_usuarios())

@app.route('/login')
def abre_login():
    return render_template('login.html')

@app.route('/login', methods = ['POST'])
def login():
    login = request.form['user']
    senha = request.form['senha']
    usuario_logado = Usuario(login,None,None,None,senha)
    resultado = usuario_logado.realiza_login()
    if resultado == True:
        session ["username"] = usuario_logado.usuario_nome
        global grupo_logado
        grupo_logado = usuario_logado.grupo
        return redirect(url_for('abre_index'))
    else:
        return render_template('login.html', mensagem = 'Usuário ou senha inválido')


@app.route('/logout')
def logout():
    session.pop('username', None)
    return redirect (url_for('abre_login'))

@app.route('/delete', methods = ['POST'])
def deleta_usuario():
    usuario_objeto = Usuario()
    usuario_nome2 = request.form['usuario_excluido']
    usuario_objeto.exclui_usuario(usuario_nome2)
    return redirect(url_for("abre_administrador"))


app.run(debug=True)



'''Fazer uma cópia do projeto Estoque e criar grupos de usuários, administrador e usuário comum.
Somente administrador pode acessar a página administrador.
Mostrar os usuários no painel administrador.
Permitir a exclusão dos usuários na tela Administrador. '''
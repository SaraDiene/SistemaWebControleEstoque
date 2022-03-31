import mysql.connector as bd
import cripto


class BancoDados:
    def __init__(self):
        self.conexao = None
    
    def get_conexao(self):
        self.conexao = bd.connect(host = 'localhost',
                                user = 'root',
                                password = '########',
                                database = 'db_estoque')
        return self.conexao
        

class Categoria:
    
    def __init__(self, id, nome_categoria):
        self.id = id
        self.nome_categoria = nome_categoria

    def get_id(self):
        return self.id
    
    def get_nome_categoria(self):
        return self.nome_categoria

    def insert_categoria(self):
        banco = BancoDados()
        conexao = banco.get_conexao()
                                

        COMANDO_INSERT = 'insert into categoria (nome_categoria) values (%s)'
        valor = (self.nome_categoria,)
        manipulador_sql = conexao.cursor()
        manipulador_sql.execute(COMANDO_INSERT, valor)
        conexao.commit()
        return 'Inserido com sucesso!'

    def select_todas_categorias(self):
        banco = BancoDados()
        conexao = banco.get_conexao()
        
        COMANDO_SELECT = 'select id, nome_categoria from categoria order by nome_categoria'

        manipulador_sql = conexao.cursor()
        manipulador_sql.execute(COMANDO_SELECT)
        lista_categoria = []
        for x in manipulador_sql.fetchall():
            categoria = Categoria(id=x[0],nome_categoria=x[1])
            lista_categoria.append(categoria)

        return lista_categoria

class Produto:
    def __init__(self,id = None,nome = None,valor = None,quantidade = None,validade = None,descricao = None, categoria = None):
        self.id_produto = id
        self.nome_produto = nome
        self.valor_produto = valor
        self.quantidade_produto = quantidade
        self.validade_produto = validade
        self.descricao_produto = descricao
        self.categoria = categoria

    def insere_produtos(self):
        banco = BancoDados()
        conexao = banco.get_conexao()
        COMANDO_INSERT = 'insert into produto (nome_produto,quantidade,valor,validade,descricao,id_categoria) values(%s,%s,%s,%s,%s,%s)'
        valores = (self.nome_produto, self.quantidade_produto, self.valor_produto, self.validade_produto, self.descricao_produto,self.categoria)
        manipulador_sql = conexao.cursor()
        manipulador_sql.execute(COMANDO_INSERT,valores)
        conexao.commit()
        return 'Inserido com sucesso!'

    def select_todos_produtos(self):
        banco = BancoDados()
        conexao = banco.get_conexao()

        COMANDO_SELECT = 'select p.id,nome_produto, quantidade,valor, validade, descricao, id_categoria, nome_categoria from produto p, categoria c where p.id_categoria = c.id'
        manipulador_sql = conexao.cursor()
        manipulador_sql.execute(COMANDO_SELECT)
        lista_produto = []
        for produto in manipulador_sql.fetchall():
            categoria = Categoria(produto[6], produto[7])
            objeto_produto = Produto(id = produto [0],nome = produto[1], quantidade = produto[2], valor = produto[3], validade = produto[4], descricao = produto[5],categoria = categoria)
            lista_produto.append(objeto_produto)
        return lista_produto



    def select_produto_categoria(self, id_categoria,nome_prod):
        banco = BancoDados()
        conexao = banco.get_conexao()
        COMANDO_SELECT = None
        valor = ()
        if id_categoria != "-1":
            COMANDO_SELECT = 'select p.id,nome_produto, quantidade,valor, validade, descricao, id_categoria, nome_categoria from produto p, categoria c where p.id_categoria = c.id and c.id = %s'
            valor = (id_categoria,)
            
        else:
            COMANDO_SELECT = 'select p.id,nome_produto, quantidade,valor, validade, descricao, id_categoria, nome_categoria from produto p, categoria c where p.id_categoria = c.id and p.nome_produto like %s'
            valor = (nome_prod,)
            
        manipulador_sql = conexao.cursor()
        manipulador_sql.execute(COMANDO_SELECT, valor)
        lista_produto = []
        for produto in manipulador_sql.fetchall():
            categoria = Categoria(produto[6], produto[7])
            objeto_produto = Produto(id = produto [0],nome = produto[1], quantidade = produto[2], valor = produto[3], validade = produto[4], descricao = produto[5],categoria = categoria)
            lista_produto.append(objeto_produto)
        return lista_produto

    def pesquisa_produto_id(self,id):
        banco = BancoDados()
        conexao = banco.get_conexao()
        COMANDO_SELECT = 'select id, nome_produto, quantidade, valor, validade, descricao from produto where id = %s'
        valor = (id,)
        manipulador_sql = conexao.cursor()
        manipulador_sql.execute(COMANDO_SELECT,valor)
        produto_buscado = manipulador_sql.fetchone()
        produto_objeto = Produto(id = produto_buscado[0], nome = produto_buscado [1], valor = produto_buscado[3],quantidade = produto_buscado[2], validade = produto_buscado[4], descricao = produto_buscado[5])
        return produto_objeto

    def atualiza_quantidade(self,quantidade,id):
        banco = BancoDados()
        conexao = banco.get_conexao()
        COMANDO_UPDATE = 'update produto set quantidade = %s where id = %s'
        valor = (quantidade,id)
        manipulador_sql = conexao.cursor()
        manipulador_sql.execute(COMANDO_UPDATE,valor)
        conexao.commit()

class Venda:
    def __init__(self, id = None, produto_id = None,data = None, valor = None,quantidade= None):
        self.id = id
        self.produto_id = produto_id
        self.valor = valor
        self.quantidade = quantidade
        self.data = data
        
    def insere_venda(self):
        banco = BancoDados()
        conexao = banco.get_conexao()
        COMANDO_INSERT = 'insert into venda (Produto_vendido, Dt_venda, Valor_venda, Quantidade_vendida) values (%s,%s,%s,%s,)'
        valores = (self.produto_id,self.data,self.valor,self.quantidade)
        manipulador_sql = conexao.cursor()
        manipulador_sql.execute(COMANDO_INSERT,valores)
        conexao.commit()

class Usuario:
    def __init__(self,usuario = None,cpf = None, depto = None, email = None, senha = None, grupo = 0):
        self.usuario_nome = usuario
        self.cpf = cpf
        self.depto = depto
        self.email = email
        self.grupo = grupo
        self.usuario_senha = senha

    def insere_usuario(self):
        obj_banco = BancoDados()
        conexao = obj_banco.get_conexao()
        try:
            COMANDO_INSERT = 'insert into usuarios (Nome,CPF,Depto,Email,senha,grupo) values (%s,%s,%s,%s,%s,%s)'
            hash_senha = cripto.criptografa_senha(self.usuario_senha)
            valor = (self.usuario_nome,self.cpf,self.depto,self.email, hash_senha, self.grupo)
            manipulador_sql = conexao.cursor()
            manipulador_sql.execute(COMANDO_INSERT,valor)
            conexao.commit()
            return "Usuário cadastrado"
        except:
            return 'Usuário já possui cadastro'

    def realiza_login(self):
        obj_banco = BancoDados()
        conexao = obj_banco.get_conexao()

        COMANDO_SELECT = 'select senha,grupo from usuarios where Nome like binary %s'
        valor = (self.usuario_nome,)
        manipulador_sql = conexao.cursor()
        manipulador_sql.execute(COMANDO_SELECT,valor)
        senha_banco_dados = manipulador_sql.fetchone()
        
        if senha_banco_dados != None:

            resultado = cripto.valida_senha(self.usuario_senha,senha_banco_dados [0])
            self.grupo = senha_banco_dados [1]
            return resultado
        return ('Deu erro aqui')

    def exibe_usuarios(self):
        obj_banco = BancoDados()
        conexao = obj_banco.get_conexao()
        COMANDO_SELECT = 'select Nome,CPF,Depto,Email from usuarios order by Nome'
        manipulador_sql = conexao.cursor()
        manipulador_sql.execute(COMANDO_SELECT)
        resultado = manipulador_sql.fetchall()
        lista = []
        for usu in resultado:
            usuario = Usuario(usuario = usu[0], cpf = usu [1], depto = usu [2], email = usu [3])
            lista.append(usuario)
        return lista

    def exclui_usuario(self, nome_usuario):
        obj_banco = BancoDados()
        conexao = obj_banco.get_conexao()
        COMANDO_DELETE = 'delete from usuarios where Nome like %s'
        valor = (nome_usuario,)
        manipulador_sql = conexao.cursor()
        manipulador_sql.execute(COMANDO_DELETE, valor)
        conexao.commit()
        return "Registro deletado"








        



create database if not exists db_estoque;
use db_estoque;

create table if not exists categoria(
										id integer primary key auto_increment,
										nome_categoria varchar (255)
);
create table if not exists produto(
									id integer primary key auto_increment,
                                    nome_produto varchar (255),
                                    quantidade integer,
                                    valor double,
                                    validade date,
                                    descricao varchar(255),
                                    id_categoria integer,
                                    foreign key(id_categoria) references categoria(id)
                                    );
                                    
select p.id,nome_produto, quantidade,valor, validade, descricao, id_categoria, nome_categoria from produto p, categoria c where p.id_categoria = c.id;
drop table produto;

create table if not exists usuarios(
									Id integer primary key auto_increment,
                                    Nome varchar (255) not null unique,	
                                    CPF varchar(18) not null,
                                    Depto varchar(255) not null,
                                    Email varchar(255) not null,
                                    senha varchar (255) not null
                                    );
                                    
create table if not exists venda(
									Id integer primary key auto_increment,
                                    Produto_vendido integer not null,
                                    Dt_venda datetime not null,
                                    Valor_venda double not null,
                                    foreign key (Produto_vendido) references produto(id)
);
                                    

alter table usuarios add column grupo int not null;
update usuarios set grupo = 1 where Depto = "Administrativo";
drop table usuarios;
select * from categoria;
select  * from produto;
select * from usuarios;

/*JOIN = Conceito de juntar informações de duas ou mais tabelas;
Através da chave estrangeira (id_categoria) ligamos ela a chave primária de outra tabela*/
/*
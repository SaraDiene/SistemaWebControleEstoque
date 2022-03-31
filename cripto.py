import bcrypt


def criptografa_senha(senha):
    senha = senha.encode('utf-8')

    senha_cript = bcrypt.hashpw(senha, bcrypt.gensalt())

    return (senha_cript)

def valida_senha(senha, hash_senha):
    senha = senha.encode('utf-8')
    hash_senha = hash_senha.encode('utf-8')
    resultado = bcrypt.checkpw(senha,hash_senha)
    return(resultado)


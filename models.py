class Treinamento:
    def __init__(self, id, nome, categoria, prazo, instrutor, aluno):
        self.id = id
        self.nome = nome
        self.categoria = categoria
        self.prazo = prazo
        self.instrutor = instrutor
        self.aluno = aluno


class Usuario:
    def __init__(self, id, nome, senha, categoria):
        self.id = id
        self.nome = nome
        self.senha = senha
        self.cateogria = categoria


from models import Treinamento, Usuario

SQL_DELETA_JOGO = 'delete from treinamento where id = %s'
SQL_JOGO_POR_ID = 'SELECT id, nome, categoria, console from treinamento where id = %s'
SQL_USUARIO_POR_ID = 'SELECT id, nome, senha from usuario where id = %s'
SQL_ATUALIZA_JOGO = 'UPDATE treinamento SET nome=%s, categoria=%s, console=%s where id = %s'
SQL_BUSCA_JOGOS = 'SELECT id, nome, categoria, console from treinamento'
SQL_CRIA_JOGO = 'INSERT into treinamento (nome, categoria, console) values (%s, %s, %s)'


class TreinamentoDao:
    def __init__(self, db):
        self.__db = db

    def salvar(self, treinamento):
        cursor = self.__db.connection.cursor()

        if (treinamento.id):
            cursor.execute(SQL_ATUALIZA_JOGO, (treinamento.nome, treinamento.categoria, treinamento.console, treinamento.id))
        else:
            cursor.execute(SQL_CRIA_JOGO, (treinamento.nome, treinamento.categoria, treinamento.console))
            treinamento.id = cursor.lastrowid
        self.__db.connection.commit()
        return treinamento

    def listar(self):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_BUSCA_JOGOS)
        treinamentos = traduz_treinamentos(cursor.fetchall())
        return treinamentos

    def busca_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_JOGO_POR_ID, (id,))
        tupla = cursor.fetchone()
        return Treinamento(tupla[1], tupla[2], tupla[3], id=tupla[0])

    def deletar(self, id):
        self.__db.connection.cursor().execute(SQL_DELETA_JOGO, (id, ))
        self.__db.connection.commit()


class UsuarioDao:
    def __init__(self, db):
        self.__db = db

    def buscar_por_id(self, id):
        cursor = self.__db.connection.cursor()
        cursor.execute(SQL_USUARIO_POR_ID, (id,))
        dados = cursor.fetchone()
        usuario = traduz_usuario(dados) if dados else None
        return usuario


def traduz_treinamentos(treinamentos):
    def cria_treinamento_com_tupla(tupla):
        return Treinamento(tupla[1], tupla[2], tupla[3], id=tupla[0])
    return list(map(cria_treinamento_com_tupla, treinamentos))


def traduz_usuario(tupla):
    return Usuario(tupla[0], tupla[1], tupla[2])

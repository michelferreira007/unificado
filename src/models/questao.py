from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

# Usar a mesma instância de db do modelo user
from src.models.user import db

class Questao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ano = db.Column(db.Integer)
    vestibular = db.Column(db.String(100))
    numero = db.Column(db.Integer)
    materia = db.Column(db.String(100))
    assunto = db.Column(db.String(200))
    enunciado = db.Column(db.Text, nullable=False)
    alternativas = db.Column(db.Text)  # JSON string
    resposta_correta = db.Column(db.String(10))
    explicacao = db.Column(db.Text)
    dificuldade = db.Column(db.String(20))  # 'Fácil', 'Médio', 'Difícil'
    dia = db.Column(db.String(50))  # Para PAS-UEM
    caderno = db.Column(db.String(50))  # Para PAS-UEM
    idioma = db.Column(db.String(20), default='Português')  # 'Português', 'Inglês', 'Espanhol'
    conteudo_materia = db.Column(db.String(200))  # Novo filtro
    imagem_url = db.Column(db.String(500))  # URL para imagens
    texto_base = db.Column(db.Text)  # Texto base para múltiplas questões
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Questao {self.id} - {self.vestibular} {self.ano}>'

    def to_dict(self):
        return {
            'id': self.id,
            'ano': self.ano,
            'vestibular': self.vestibular,
            'numero': self.numero,
            'materia': self.materia,
            'assunto': self.assunto,
            'enunciado': self.enunciado,
            'alternativas': json.loads(self.alternativas) if self.alternativas else [],
            'resposta_correta': self.resposta_correta,
            'explicacao': self.explicacao,
            'dificuldade': self.dificuldade,
            'dia': self.dia,
            'caderno': self.caderno,
            'idioma': self.idioma,
            'conteudo_materia': self.conteudo_materia,
            'imagem_url': self.imagem_url,
            'texto_base': self.texto_base,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class ProgressoQuestao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    questao_id = db.Column(db.Integer, db.ForeignKey('questao.id'), nullable=False)
    respondida = db.Column(db.Boolean, default=False)
    acertou = db.Column(db.Boolean)
    resposta_usuario = db.Column(db.String(10))
    data_resposta = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ProgressoQuestao User:{self.user_id} Questao:{self.questao_id}>'

    def to_dict(self):
        return {
            'id': self.id,
            'user_id': self.user_id,
            'questao_id': self.questao_id,
            'respondida': self.respondida,
            'acertou': self.acertou,
            'resposta_usuario': self.resposta_usuario,
            'data_resposta': self.data_resposta.isoformat() if self.data_resposta else None
        }

class ComentarioQuestao(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    questao_id = db.Column(db.Integer, db.ForeignKey('questao.id'), nullable=False)
    comentario = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ComentarioQuestao User:{self.user_id} Questao:{self.questao_id}>'

    def to_dict(self):
        from src.models.user import User
        user = User.query.get(self.user_id)
        return {
            'id': self.id,
            'user_id': self.user_id,
            'questao_id': self.questao_id,
            'comentario': self.comentario,
            'username': user.username if user else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class Simulado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(200), nullable=False)
    questoes_ids = db.Column(db.Text)  # JSON string de IDs de questões
    descricao = db.Column(db.Text)
    tempo_limite = db.Column(db.Integer)  # Em minutos
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<Simulado {self.nome}>'

    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'questoes_ids': json.loads(self.questoes_ids) if self.questoes_ids else [],
            'descricao': self.descricao,
            'tempo_limite': self.tempo_limite,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }

class ResultadoSimulado(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    simulado_id = db.Column(db.Integer, db.ForeignKey('simulado.id'), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    respostas = db.Column(db.Text)  # JSON string de respostas do usuário
    pontuacao = db.Column(db.Integer)
    total_questoes = db.Column(db.Integer)
    tempo_gasto = db.Column(db.Integer)  # Em minutos
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<ResultadoSimulado User:{self.user_id} Simulado:{self.simulado_id}>'

    def to_dict(self):
        from src.models.user import User
        user = User.query.get(self.user_id)
        simulado = Simulado.query.get(self.simulado_id)
        return {
            'id': self.id,
            'simulado_id': self.simulado_id,
            'user_id': self.user_id,
            'respostas': json.loads(self.respostas) if self.respostas else {},
            'pontuacao': self.pontuacao,
            'total_questoes': self.total_questoes,
            'tempo_gasto': self.tempo_gasto,
            'username': user.username if user else None,
            'simulado_nome': simulado.nome if simulado else None,
            'created_at': self.created_at.isoformat() if self.created_at else None
        }


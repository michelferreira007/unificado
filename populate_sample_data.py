#!/usr/bin/env python3
"""
Script para popular o banco de dados com dados de exemplo
"""
import os
import sys
import json
from datetime import datetime

# Adicionar o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from src.models.user import db, User
from src.models.questao import Questao, ProgressoQuestao, ComentarioQuestao, Simulado, ResultadoSimulado
from src.main import app

def create_sample_data():
    """Criar dados de exemplo para teste"""
    
    with app.app_context():
        # Limpar dados existentes
        db.drop_all()
        db.create_all()
        
        # Criar usuário de exemplo
        user = User(username='admin', email='admin@exemplo.com')
        user.set_password('123456')
        db.session.add(user)
        
        user2 = User(username='estudante', email='estudante@exemplo.com')
        user2.set_password('123456')
        db.session.add(user2)
        
        # Criar questões de exemplo
        questoes_exemplo = [
            {
                'ano': 2024,
                'vestibular': 'PAS-UEM',
                'numero': 1,
                'materia': 'Matemática',
                'assunto': 'Álgebra',
                'enunciado': 'Resolva a equação x² - 5x + 6 = 0.',
                'alternativas': json.dumps(['x = 2 e x = 3', 'x = 1 e x = 6', 'x = -2 e x = -3', 'x = 0 e x = 5', 'x = 1 e x = 5']),
                'resposta_correta': 'x = 2 e x = 3',
                'explicacao': 'Usando a fórmula de Bhaskara ou fatoração: (x-2)(x-3) = 0, logo x = 2 ou x = 3.',
                'dificuldade': 'Médio',
                'dia': 'Etapa 1',
                'caderno': 'A',
                'idioma': 'Português',
                'conteudo_materia': 'Equações do 2º grau'
            },
            {
                'ano': 2024,
                'vestibular': 'PAS-UEM',
                'numero': 2,
                'materia': 'Português',
                'assunto': 'Literatura',
                'enunciado': 'Sobre o Romantismo brasileiro, assinale a alternativa correta.',
                'alternativas': json.dumps([
                    'Teve início no século XVIII',
                    'José de Alencar foi um dos principais representantes',
                    'Caracterizou-se pelo objetivismo',
                    'Não teve influência europeia',
                    'Focou apenas na poesia'
                ]),
                'resposta_correta': 'José de Alencar foi um dos principais representantes',
                'explicacao': 'José de Alencar foi um dos principais escritores do Romantismo brasileiro, autor de obras como "O Guarani" e "Iracema".',
                'dificuldade': 'Fácil',
                'dia': 'Etapa 1',
                'caderno': 'A',
                'idioma': 'Português',
                'conteudo_materia': 'Movimentos literários'
            },
            {
                'ano': 2023,
                'vestibular': 'ENEM',
                'numero': 1,
                'materia': 'Física',
                'assunto': 'Mecânica',
                'enunciado': 'Um corpo em movimento retilíneo uniforme percorre 100m em 10s. Qual sua velocidade?',
                'alternativas': json.dumps(['5 m/s', '10 m/s', '15 m/s', '20 m/s', '25 m/s']),
                'resposta_correta': '10 m/s',
                'explicacao': 'Velocidade = distância / tempo = 100m / 10s = 10 m/s',
                'dificuldade': 'Fácil',
                'idioma': 'Português',
                'conteudo_materia': 'Cinemática'
            },
            {
                'ano': 2023,
                'vestibular': 'ENEM',
                'numero': 2,
                'materia': 'Química',
                'assunto': 'Química Orgânica',
                'enunciado': 'Qual é a fórmula molecular do metano?',
                'alternativas': json.dumps(['CH₄', 'C₂H₆', 'C₃H₈', 'C₄H₁₀', 'C₅H₁₂']),
                'resposta_correta': 'CH₄',
                'explicacao': 'O metano é o hidrocarboneto mais simples, com fórmula molecular CH₄.',
                'dificuldade': 'Fácil',
                'idioma': 'Português',
                'conteudo_materia': 'Hidrocarbonetos'
            },
            {
                'ano': 2024,
                'vestibular': 'VESTIBULAR UEM',
                'numero': 1,
                'materia': 'Biologia',
                'assunto': 'Citologia',
                'enunciado': 'Sobre as organelas celulares, é correto afirmar que:',
                'alternativas': json.dumps([
                    'As mitocôndrias são responsáveis pela fotossíntese',
                    'O retículo endoplasmático rugoso possui ribossomos',
                    'O núcleo está presente apenas em células vegetais',
                    'Os cloroplastos estão presentes em todas as células',
                    'O complexo de Golgi não existe em células animais'
                ]),
                'resposta_correta': 'O retículo endoplasmático rugoso possui ribossomos',
                'explicacao': 'O retículo endoplasmático rugoso é caracterizado pela presença de ribossomos aderidos à sua superfície.',
                'dificuldade': 'Médio',
                'idioma': 'Português',
                'conteudo_materia': 'Estrutura celular'
            },
            {
                'ano': 2024,
                'vestibular': 'PAS-UEM',
                'numero': 3,
                'materia': 'Inglês',
                'assunto': 'Reading Comprehension',
                'enunciado': 'Read the text and choose the correct alternative.\n\n"The importance of education cannot be overstated. It is the foundation of personal growth and societal development."',
                'alternativas': json.dumps([
                    'Education is not important',
                    'Education is very important',
                    'Education is only for children',
                    'Education is expensive',
                    'Education is optional'
                ]),
                'resposta_correta': 'Education is very important',
                'explicacao': 'The text states that "The importance of education cannot be overstated", meaning it is very important.',
                'dificuldade': 'Médio',
                'dia': 'Etapa 2',
                'caderno': 'B',
                'idioma': 'Inglês',
                'conteudo_materia': 'Interpretação de texto'
            }
        ]
        
        for questao_data in questoes_exemplo:
            questao = Questao(**questao_data)
            db.session.add(questao)
        
        # Commit das questões primeiro para obter os IDs
        db.session.commit()
        
        # Criar progresso de exemplo
        questoes = Questao.query.all()
        if len(questoes) >= 2:
            progresso1 = ProgressoQuestao(
                user_id=user2.id,
                questao_id=questoes[0].id,
                respondida=True,
                acertou=True,
                resposta_usuario=questoes[0].resposta_correta
            )
            db.session.add(progresso1)
            
            progresso2 = ProgressoQuestao(
                user_id=user2.id,
                questao_id=questoes[1].id,
                respondida=True,
                acertou=False,
                resposta_usuario='Resposta incorreta'
            )
            db.session.add(progresso2)
        
        # Criar comentários de exemplo
        if len(questoes) >= 1:
            comentario = ComentarioQuestao(
                user_id=user2.id,
                questao_id=questoes[0].id,
                comentario='Excelente questão! A explicação ficou muito clara.'
            )
            db.session.add(comentario)
        
        # Criar simulado de exemplo
        if len(questoes) >= 3:
            simulado = Simulado(
                nome='Simulado de Matemática e Português',
                questoes_ids=json.dumps([questoes[0].id, questoes[1].id]),
                descricao='Simulado básico com questões de matemática e português',
                tempo_limite=60
            )
            db.session.add(simulado)
            
            # Commit do simulado para obter o ID
            db.session.commit()
            
            # Criar resultado de simulado
            resultado = ResultadoSimulado(
                simulado_id=simulado.id,
                user_id=user2.id,
                respostas=json.dumps({
                    str(questoes[0].id): questoes[0].resposta_correta,
                    str(questoes[1].id): 'Resposta incorreta'
                }),
                pontuacao=1,
                total_questoes=2,
                tempo_gasto=30
            )
            db.session.add(resultado)
        
        # Commit final
        db.session.commit()
        
        print("✅ Dados de exemplo criados com sucesso!")
        print(f"👤 Usuários criados: {User.query.count()}")
        print(f"📝 Questões criadas: {Questao.query.count()}")
        print(f"📊 Progressos criados: {ProgressoQuestao.query.count()}")
        print(f"💬 Comentários criados: {ComentarioQuestao.query.count()}")
        print(f"🎯 Simulados criados: {Simulado.query.count()}")
        print(f"📈 Resultados criados: {ResultadoSimulado.query.count()}")
        print("\n🔑 Credenciais de teste:")
        print("Admin: admin@exemplo.com / 123456")
        print("Estudante: estudante@exemplo.com / 123456")

if __name__ == '__main__':
    create_sample_data()


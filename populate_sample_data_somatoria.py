#!/usr/bin/env python3
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.main import app
from src.models.questao import db, Questao
import json

def create_sample_data():
    with app.app_context():
        # Limpar dados existentes
        Questao.query.delete()
        
        # Questões somatórias de exemplo baseadas na plataforma de referência
        questoes_somatorias = [
            {
                'ano': 2024,
                'vestibular': 'PAS-UEM',
                'numero': 1,
                'materia': 'História',
                'assunto': 'Arte na Pré-História',
                'enunciado': 'Sobre a arte na Pré-História, assinale o que for correto.',
                'tipo_questao': 'somatoria',
                'alternativas_somatorias': [
                    {'valor': 1, 'texto': 'As expressões artísticas conhecidas como arte rupestre (pinturas, gravuras, desenhos) foram utilizadas pelos homens, entre outras coisas, para enfrentar seus medos, e se relacionavam a rituais como forma de proteção, por exemplo, contra ameaças de animais e manifestações climáticas.'},
                    {'valor': 2, 'texto': 'De acordo com os agrupamentos e a catalogação dos sítios arqueológicos já sistematizados, as figuras representadas na arte rupestre expressam a ideia de movimento e ação.'},
                    {'valor': 4, 'texto': 'As mais antigas figuras feitas pelo ser humano foram desenhadas em paredes, em tetos de cavernas e em grutas. O desenvolvimento do registro artístico era feito com os dedos e com a técnica da pintura da mão em negativo.'},
                    {'valor': 8, 'texto': 'Os escultores do período produziram peças em mármore e granito, utilizando-se, majoritariamente, de dois métodos: o do entalhe geométrico, exigindo ferramental específico, e o método da justaposição de elementos. Em ambos eram dispensadas as construções e o preparo de formas.'},
                    {'valor': 16, 'texto': 'No amensalismo, uma espécie inibidora impede o crescimento de outra, chamada amensal. Um exemplo são os antibióticos, produzidos pelo fungo Penicillium notatum, que impede a multiplicação das bactérias (amensais) e é usado na medicina, como é o caso da penicilina, produzida pelo fungo Penicillium notatum, que impede a multiplicação das bactérias (amensais).'}
                ],
                'resposta_somatoria': 7,  # 1 + 2 + 4
                'explicacao': 'As alternativas 01, 02 e 04 estão corretas sobre a arte na Pré-História. A alternativa 08 está incorreta pois não havia mármore e granito trabalhados no período. A alternativa 16 está completamente fora do contexto, falando sobre biologia.',
                'dificuldade': 'Médio',
                'dia': 'Etapa 1',
                'caderno': 'A',
                'idioma': 'Português',
                'conteudo_materia': 'Arte Rupestre'
            },
            {
                'ano': 2024,
                'vestibular': 'PAS-UEM',
                'numero': 11,
                'materia': 'Matemática',
                'assunto': 'Função Quadrática e Dinâmica Populacional',
                'enunciado': 'Suponha que a população de uma colônia de bactérias, t dias após ser iniciado um experimento, possa ser modelada por uma função quadrática P(t) = -2t² + 5t + 2 em milhões de bactérias. Com base nos dados, e em conhecimentos sobre dinâmica de populações, assinale o que for correto.',
                'tipo_questao': 'somatoria',
                'alternativas_somatorias': [
                    {'valor': 1, 'texto': 'No início do experimento a população da colônia de bactérias era de 2 milhões.'},
                    {'valor': 2, 'texto': 'Segundo esse modelo matemático, essa colônia de bactérias nunca se extinguirá.'},
                    {'valor': 4, 'texto': 'A população dessa colônia de bactérias dobra antes do término do primeiro dia.'},
                    {'valor': 8, 'texto': 'De acordo com esse modelo matemático, a população dessa colônia terá quantidade máxima de 14,5 milhões de bactérias.'},
                    {'valor': 16, 'texto': 'No amensalismo, uma espécie inibidora impede o crescimento de outra, chamada amensal. Um exemplo são os antibióticos, produzidos pelo fungo Penicillium notatum, que impede a multiplicação das bactérias (amensais) e é usado na medicina, como é o caso da penicilina.'}
                ],
                'resposta_somatoria': 13,  # 1 + 4 + 8
                'explicacao': 'Alternativa 01: P(0) = -2(0)² + 5(0) + 2 = 2 milhões. CORRETA. Alternativa 02: Como a função é quadrática com coeficiente negativo, ela terá raízes e a população se extinguirá. INCORRETA. Alternativa 04: P(1) = -2(1)² + 5(1) + 2 = 5 milhões, que é mais que o dobro de 2 milhões. CORRETA. Alternativa 08: O máximo ocorre em t = -b/2a = -5/(-4) = 1,25. P(1,25) = 5,125 milhões. INCORRETA (valor incorreto). Alternativa 16: Fora do contexto. INCORRETA.',
                'dificuldade': 'Difícil',
                'dia': 'Etapa 2',
                'caderno': 'B',
                'idioma': 'Português',
                'conteudo_materia': 'Funções Quadráticas'
            },
            {
                'ano': 2024,
                'vestibular': 'PAS-UEM',
                'numero': 5,
                'materia': 'Língua Portuguesa',
                'assunto': 'Análise Textual e Crítica Social',
                'enunciado': 'Com base no texto sobre o homem que morreu de fome, assinale o que for correto.',
                'tipo_questao': 'somatoria',
                'alternativas_somatorias': [
                    {'valor': 1, 'texto': 'A descrição detalhada do homem e de suas condições de vida indica um profundo conhecimento sobre sua identidade por parte do autor.'},
                    {'valor': 2, 'texto': 'A ausência de socorro ao homem pelas autoridades e pela sociedade revela uma crítica à desumanização e à indiferença presentes na sociedade.'},
                    {'valor': 4, 'texto': 'O texto retrata a morte do homem como um evento inevitável e natural, sem responsabilidade social ou institucional envolvida.'},
                    {'valor': 8, 'texto': 'A descrição do homem como de "trinta anos presumíveis" demonstra a incerteza sobre sua identidade.'},
                    {'valor': 16, 'texto': 'A repetição da frase "morreu de fome" enfatiza a causa da morte e a inação das pessoas e instituições.'}
                ],
                'resposta_somatoria': 26,  # 2 + 8 + 16
                'explicacao': 'Alternativa 01: INCORRETA - O texto não demonstra conhecimento profundo sobre a identidade do homem. Alternativa 02: CORRETA - O texto critica a indiferença social. Alternativa 04: INCORRETA - O texto critica justamente a responsabilidade social. Alternativa 08: CORRETA - "Presumíveis" indica incerteza. Alternativa 16: CORRETA - A repetição enfatiza a crítica social.',
                'dificuldade': 'Médio',
                'dia': 'Etapa 1',
                'caderno': 'A',
                'idioma': 'Português',
                'conteudo_materia': 'Interpretação de Texto'
            },
            {
                'ano': 2023,
                'vestibular': 'PAS-UEM',
                'numero': 8,
                'materia': 'Biologia',
                'assunto': 'Relações Ecológicas',
                'enunciado': 'Sobre as relações ecológicas entre os seres vivos, assinale o que for correto.',
                'tipo_questao': 'somatoria',
                'alternativas_somatorias': [
                    {'valor': 1, 'texto': 'O mutualismo é uma relação em que ambas as espécies se beneficiam, sendo obrigatória para a sobrevivência de pelo menos uma delas.'},
                    {'valor': 2, 'texto': 'Na competição interespecífica, indivíduos de espécies diferentes disputam pelos mesmos recursos do ambiente.'},
                    {'valor': 4, 'texto': 'O parasitismo é uma relação em que uma espécie se beneficia causando prejuízo à outra, sem necessariamente causar a morte do hospedeiro.'},
                    {'valor': 8, 'texto': 'Na predação, o predador mata e consome total ou parcialmente a presa para obter energia e nutrientes.'},
                    {'valor': 16, 'texto': 'O comensalismo é uma relação em que uma espécie se beneficia enquanto a outra não é afetada, nem positiva nem negativamente.'}
                ],
                'resposta_somatoria': 31,  # 1 + 2 + 4 + 8 + 16 (todas corretas)
                'explicacao': 'Todas as alternativas estão corretas sobre relações ecológicas: mutualismo (01), competição interespecífica (02), parasitismo (04), predação (08) e comensalismo (16).',
                'dificuldade': 'Fácil',
                'dia': 'Etapa 2',
                'caderno': 'C',
                'idioma': 'Português',
                'conteudo_materia': 'Ecologia'
            },
            {
                'ano': 2024,
                'vestibular': 'PAS-UEM',
                'numero': 15,
                'materia': 'Física',
                'assunto': 'Cinemática e Movimento Uniforme',
                'enunciado': 'Um móvel percorre uma trajetória retilínea com velocidade constante de 20 m/s. Sobre este movimento, assinale o que for correto.',
                'tipo_questao': 'somatoria',
                'alternativas_somatorias': [
                    {'valor': 1, 'texto': 'A aceleração do móvel é nula durante todo o movimento.'},
                    {'valor': 2, 'texto': 'O móvel percorre 20 metros a cada segundo.'},
                    {'valor': 4, 'texto': 'Em 5 segundos, o móvel percorre uma distância de 100 metros.'},
                    {'valor': 8, 'texto': 'A velocidade média do móvel em qualquer intervalo de tempo é 20 m/s.'},
                    {'valor': 16, 'texto': 'O gráfico da posição em função do tempo é uma parábola.'}
                ],
                'resposta_somatoria': 15,  # 1 + 2 + 4 + 8
                'explicacao': 'Alternativas 01, 02, 04 e 08 estão corretas para movimento uniforme. A alternativa 16 está incorreta pois o gráfico s×t no movimento uniforme é uma reta, não uma parábola.',
                'dificuldade': 'Fácil',
                'dia': 'Etapa 1',
                'caderno': 'B',
                'idioma': 'Português',
                'conteudo_materia': 'Cinemática'
            },
            {
                'ano': 2023,
                'vestibular': 'PAS-UEM',
                'numero': 20,
                'materia': 'Química',
                'assunto': 'Ligações Químicas',
                'enunciado': 'Sobre as ligações químicas e propriedades dos compostos, assinale o que for correto.',
                'tipo_questao': 'somatoria',
                'alternativas_somatorias': [
                    {'valor': 1, 'texto': 'Na ligação iônica, há transferência de elétrons entre átomos de diferentes eletronegatividades.'},
                    {'valor': 2, 'texto': 'Compostos iônicos geralmente apresentam altos pontos de fusão e ebulição.'},
                    {'valor': 4, 'texto': 'Na ligação covalente, os átomos compartilham pares de elétrons.'},
                    {'valor': 8, 'texto': 'Compostos moleculares são sempre solúveis em água.'},
                    {'valor': 16, 'texto': 'A ligação metálica é caracterizada pela mobilidade dos elétrons de valência.'}
                ],
                'resposta_somatoria': 23,  # 1 + 2 + 4 + 16
                'explicacao': 'Alternativas 01, 02, 04 e 16 estão corretas. A alternativa 08 está incorreta pois nem todos os compostos moleculares são solúveis em água (exemplo: óleo).',
                'dificuldade': 'Médio',
                'dia': 'Etapa 3',
                'caderno': 'A',
                'idioma': 'Português',
                'conteudo_materia': 'Ligações Químicas'
            }
        ]
        
        # Adicionar questões ao banco
        for questao_data in questoes_somatorias:
            questao = Questao(
                ano=questao_data['ano'],
                vestibular=questao_data['vestibular'],
                numero=questao_data['numero'],
                materia=questao_data['materia'],
                assunto=questao_data['assunto'],
                enunciado=questao_data['enunciado'],
                tipo_questao=questao_data['tipo_questao'],
                alternativas_somatorias=json.dumps(questao_data['alternativas_somatorias']),
                resposta_somatoria=questao_data['resposta_somatoria'],
                explicacao=questao_data['explicacao'],
                dificuldade=questao_data['dificuldade'],
                dia=questao_data['dia'],
                caderno=questao_data['caderno'],
                idioma=questao_data['idioma'],
                conteudo_materia=questao_data['conteudo_materia']
            )
            db.session.add(questao)
        
        db.session.commit()
        print(f"✅ {len(questoes_somatorias)} questões somatórias adicionadas com sucesso!")

if __name__ == '__main__':
    create_sample_data()


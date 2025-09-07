from flask import Blueprint, request, jsonify, session
from src.models.questao import db, Questao, ProgressoQuestao, ComentarioQuestao, Simulado, ResultadoSimulado
from src.routes.user import login_required
from sqlalchemy import and_, or_, func
import json

questoes_bp = Blueprint('questoes', __name__)

@questoes_bp.route('/api/questoes', methods=['GET'])
def get_questoes():
    """Buscar questões com filtros opcionais"""
    try:
        # Parâmetros de filtro
        ano = request.args.get('ano', type=int)
        vestibular = request.args.get('vestibular')
        materia = request.args.get('materia')
        assunto = request.args.get('assunto')
        dificuldade = request.args.get('dificuldade')
        idioma = request.args.get('idioma')
        conteudo_materia = request.args.get('conteudo_materia')
        busca = request.args.get('busca')
        
        # Parâmetros de paginação
        page = request.args.get('page', 1, type=int)
        per_page = request.args.get('per_page', 10, type=int)
        
        # Construir query
        query = Questao.query
        
        # Aplicar filtros apenas se não forem "Todas" ou vazios
        if ano and ano != 0:
            query = query.filter(Questao.ano == ano)
        if vestibular and vestibular.lower() not in ['todas', 'todos os vestibulares', '']:
            query = query.filter(Questao.vestibular.ilike(f'%{vestibular}%'))
        if materia and materia.lower() not in ['todas', 'todas as matérias', '']:
            query = query.filter(Questao.materia.ilike(f'%{materia}%'))
        if assunto and assunto.lower() not in ['todos', 'todos os assuntos', '']:
            query = query.filter(Questao.assunto.ilike(f'%{assunto}%'))
        if dificuldade and dificuldade.lower() not in ['todas', 'todas as dificuldades', '']:
            query = query.filter(Questao.dificuldade == dificuldade)
        if idioma and idioma.lower() not in ['todos', 'todos os idiomas', '']:
            query = query.filter(Questao.idioma == idioma)
        if conteudo_materia and conteudo_materia.lower() not in ['todos', 'todos os conteúdos', '']:
            query = query.filter(Questao.conteudo_materia.ilike(f'%{conteudo_materia}%'))
        if busca:
            query = query.filter(or_(
                Questao.enunciado.ilike(f'%{busca}%'),
                Questao.assunto.ilike(f'%{busca}%'),
                Questao.texto_base.ilike(f'%{busca}%')
            ))
        
        # Executar query com paginação
        questoes_paginadas = query.paginate(
            page=page, 
            per_page=per_page, 
            error_out=False
        )
        
        # Se o usuário estiver logado, incluir progresso
        questoes_com_progresso = []
        for questao in questoes_paginadas.items:
            questao_dict = questao.to_dict()
            if 'user_id' in session:
                progresso = ProgressoQuestao.query.filter_by(
                    user_id=session['user_id'],
                    questao_id=questao.id
                ).first()
                questao_dict['progresso'] = progresso.to_dict() if progresso else None
            questoes_com_progresso.append(questao_dict)
        
        return jsonify({
            'questoes': questoes_com_progresso,
            'total': questoes_paginadas.total,
            'pages': questoes_paginadas.pages,
            'current_page': page,
            'per_page': per_page
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@questoes_bp.route('/api/questoes/<int:questao_id>', methods=['GET'])
def get_questao(questao_id):
    """Buscar uma questão específica"""
    try:
        questao = Questao.query.get_or_404(questao_id)
        questao_dict = questao.to_dict()
        
        # Se o usuário estiver logado, incluir progresso
        if 'user_id' in session:
            progresso = ProgressoQuestao.query.filter_by(
                user_id=session['user_id'],
                questao_id=questao.id
            ).first()
            questao_dict['progresso'] = progresso.to_dict() if progresso else None
        
        return jsonify(questao_dict)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@questoes_bp.route('/api/questoes', methods=['POST'])
@login_required
def create_questao():
    """Criar uma nova questão"""
    try:
        data = request.get_json()
        
        questao = Questao(
            ano=data.get('ano'),
            vestibular=data.get('vestibular'),
            numero=data.get('numero'),
            materia=data.get('materia'),
            enunciado=data['enunciado'],
            alternativas=json.dumps(data.get('alternativas', [])),
            resposta_correta=data.get('resposta_correta'),
            assunto=data.get('assunto'),
            explicacao=data.get('explicacao'),
            dificuldade=data.get('dificuldade'),
            dia=data.get('dia'),
            caderno=data.get('caderno'),
            idioma=data.get('idioma', 'Português'),
            conteudo_materia=data.get('conteudo_materia'),
            imagem_url=data.get('imagem_url'),
            texto_base=data.get('texto_base'),
            tipo_questao=data.get('tipo_questao', 'multipla_escolha'),
            alternativas_somatorias=json.dumps(data.get('alternativas_somatorias', [])),
            resposta_somatoria=data.get('resposta_somatoria')
        )
        
        db.session.add(questao)
        db.session.commit()
        
        return jsonify(questao.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@questoes_bp.route('/api/questoes/filtros', methods=['GET'])
def get_filtros():
    """Obter opções disponíveis para filtros"""
    try:
        # Parâmetros para filtragem dinâmica
        materia = request.args.get('materia')
        ano = request.args.get('ano', type=int)
        vestibular = request.args.get('vestibular')
        
        # Query base
        query = Questao.query
        
        # Aplicar filtros se fornecidos para filtragem dinâmica
        if materia and materia.lower() not in ['todas', 'todas as matérias', '']:
            query = query.filter(Questao.materia.ilike(f'%{materia}%'))
        if ano and ano != 0:
            query = query.filter(Questao.ano == ano)
        if vestibular and vestibular.lower() not in ['todos', 'todos os vestibulares', '']:
            query = query.filter(Questao.vestibular.ilike(f'%{vestibular}%'))
        
        # Obter valores únicos
        anos = db.session.query(Questao.ano.distinct()).filter(Questao.ano.isnot(None)).all()
        vestibulares = db.session.query(Questao.vestibular.distinct()).filter(Questao.vestibular.isnot(None)).all()
        materias = db.session.query(Questao.materia.distinct()).filter(Questao.materia.isnot(None)).all()
        
        # Assuntos filtrados dinamicamente baseados nos filtros aplicados
        assuntos = query.with_entities(Questao.assunto.distinct()).filter(Questao.assunto.isnot(None)).all()
        
        dificuldades = db.session.query(Questao.dificuldade.distinct()).filter(Questao.dificuldade.isnot(None)).all()
        idiomas = db.session.query(Questao.idioma.distinct()).filter(Questao.idioma.isnot(None)).all()
        conteudos_materia = db.session.query(Questao.conteudo_materia.distinct()).filter(Questao.conteudo_materia.isnot(None)).all()
        
        return jsonify({
            'anos': sorted([a[0] for a in anos], reverse=True),
            'vestibulares': sorted([v[0] for v in vestibulares]),
            'materias': sorted([m[0] for m in materias]),
            'assuntos': sorted([a[0] for a in assuntos]),
            'dificuldades': sorted([d[0] for d in dificuldades]),
            'idiomas': sorted([i[0] for i in idiomas]),
            'conteudos_materia': sorted([c[0] for c in conteudos_materia])
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@questoes_bp.route('/api/progresso/questao', methods=['POST'])
@login_required
def salvar_progresso_questao():
    """Registrar progresso de uma questão"""
    try:
        data = request.get_json()
        user_id = session['user_id']
        questao_id = data['questao_id']
        
        # Buscar a questão para verificar o tipo
        questao = Questao.query.get(questao_id)
        if not questao:
            return jsonify({'error': 'Questão não encontrada'}), 404
        
        # Buscar progresso existente ou criar novo
        progresso = ProgressoQuestao.query.filter_by(
            user_id=user_id,
            questao_id=questao_id
        ).first()
        
        if not progresso:
            progresso = ProgressoQuestao(
                user_id=user_id,
                questao_id=questao_id
            )
            db.session.add(progresso)
        
        # Atualizar dados baseado no tipo de questão
        progresso.respondida = data.get('respondida', True)
        
        if questao.tipo_questao == 'somatoria':
            # Para questões somatórias
            alternativas_selecionadas = data.get('alternativas_selecionadas', [])
            soma_usuario = sum(alternativas_selecionadas)
            
            progresso.alternativas_selecionadas = json.dumps(alternativas_selecionadas)
            progresso.resposta_usuario = str(soma_usuario)
            progresso.acertou = (soma_usuario == questao.resposta_somatoria)
        else:
            # Para questões múltipla escolha
            resposta_usuario = data.get('resposta_usuario')
            progresso.resposta_usuario = resposta_usuario
            progresso.acertou = (resposta_usuario == questao.resposta_correta)
        
        db.session.commit()
        
        return jsonify(progresso.to_dict()), 200
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@questoes_bp.route('/api/progresso/user/<int:user_id>', methods=['GET'])
@login_required
def get_progresso_usuario(user_id):
    """Obter progresso de questões de um usuário"""
    try:
        # Verificar se o usuário pode acessar esses dados
        if session['user_id'] != user_id:
            return jsonify({'error': 'Acesso negado'}), 403
        
        progressos = ProgressoQuestao.query.filter_by(user_id=user_id).all()
        return jsonify([p.to_dict() for p in progressos])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@questoes_bp.route('/api/comentarios/questao/<int:questao_id>', methods=['POST'])
@login_required
def adicionar_comentario(questao_id):
    """Adicionar comentário a uma questão"""
    try:
        data = request.get_json()
        
        comentario = ComentarioQuestao(
            user_id=session['user_id'],
            questao_id=questao_id,
            comentario=data['comentario']
        )
        
        db.session.add(comentario)
        db.session.commit()
        
        return jsonify(comentario.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@questoes_bp.route('/api/comentarios/questao/<int:questao_id>', methods=['GET'])
def get_comentarios_questao(questao_id):
    """Obter comentários de uma questão"""
    try:
        comentarios = ComentarioQuestao.query.filter_by(questao_id=questao_id).order_by(ComentarioQuestao.created_at.desc()).all()
        return jsonify([c.to_dict() for c in comentarios])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@questoes_bp.route('/api/simulados', methods=['GET'])
def get_simulados():
    """Listar todos os simulados"""
    try:
        simulados = Simulado.query.order_by(Simulado.created_at.desc()).all()
        return jsonify([s.to_dict() for s in simulados])
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@questoes_bp.route('/api/simulados', methods=['POST'])
@login_required
def create_simulado():
    """Criar um novo simulado"""
    try:
        data = request.get_json()
        
        simulado = Simulado(
            nome=data['nome'],
            questoes_ids=json.dumps(data['questoes_ids']),
            descricao=data.get('descricao'),
            tempo_limite=data.get('tempo_limite')
        )
        
        db.session.add(simulado)
        db.session.commit()
        
        return jsonify(simulado.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@questoes_bp.route('/api/simulados/<int:simulado_id>', methods=['GET'])
def get_simulado(simulado_id):
    """Buscar um simulado específico com suas questões"""
    try:
        simulado = Simulado.query.get_or_404(simulado_id)
        questoes_ids = json.loads(simulado.questoes_ids)
        questoes = Questao.query.filter(Questao.id.in_(questoes_ids)).all()
        
        simulado_dict = simulado.to_dict()
        simulado_dict['questoes'] = [q.to_dict() for q in questoes]
        
        return jsonify(simulado_dict)
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@questoes_bp.route('/api/simulados/<int:simulado_id>/resultado', methods=['POST'])
@login_required
def salvar_resultado_simulado(simulado_id):
    """Salvar resultado de um simulado"""
    try:
        data = request.get_json()
        
        resultado = ResultadoSimulado(
            simulado_id=simulado_id,
            user_id=session['user_id'],
            respostas=json.dumps(data['respostas']),
            pontuacao=data['pontuacao'],
            total_questoes=data['total_questoes'],
            tempo_gasto=data.get('tempo_gasto')
        )
        
        db.session.add(resultado)
        db.session.commit()
        
        return jsonify(resultado.to_dict()), 201
        
    except Exception as e:
        db.session.rollback()
        return jsonify({'error': str(e)}), 500

@questoes_bp.route('/api/simulados/resultados/user/<int:user_id>', methods=['GET'])
@login_required
def get_resultados_usuario(user_id):
    """Buscar resultados de simulados de um usuário"""
    try:
        # Verificar se o usuário pode acessar esses dados
        if session['user_id'] != user_id:
            return jsonify({'error': 'Acesso negado'}), 403
        
        resultados = ResultadoSimulado.query.filter_by(user_id=user_id).order_by(ResultadoSimulado.created_at.desc()).all()
        return jsonify([r.to_dict() for r in resultados])
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@questoes_bp.route('/api/estatisticas', methods=['GET'])
def get_estatisticas():
    """Obter estatísticas gerais do banco de questões"""
    try:
        total_questoes = Questao.query.count()
        total_simulados = Simulado.query.count()
        total_resultados = ResultadoSimulado.query.count()
        
        questoes_por_vestibular = db.session.query(
            Questao.vestibular, 
            func.count(Questao.id)
        ).group_by(Questao.vestibular).all()
        
        questoes_por_materia = db.session.query(
            Questao.materia, 
            func.count(Questao.id)
        ).group_by(Questao.materia).all()
        
        questoes_por_dificuldade = db.session.query(
            Questao.dificuldade, 
            func.count(Questao.id)
        ).group_by(Questao.dificuldade).all()
        
        return jsonify({
            'total_questoes': total_questoes,
            'total_simulados': total_simulados,
            'total_resultados': total_resultados,
            'questoes_por_vestibular': dict(questoes_por_vestibular),
            'questoes_por_materia': dict(questoes_por_materia),
            'questoes_por_dificuldade': dict(questoes_por_dificuldade)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500


from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from datetime import datetime, timedelta
import json
import os

app = Flask(__name__)
CORS(app)

# Configuração do banco de dados
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///ordem_servicos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SECRET_KEY'] = 'sua-chave-secreta-aqui'

db = SQLAlchemy(app)

# Modelos do banco de dados
class Setor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    descricao = db.Column(db.Text)
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'descricao': self.descricao
        }

class Trabalhador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    setor_id = db.Column(db.Integer, db.ForeignKey('setor.id'), nullable=False)
    cargo = db.Column(db.String(100))
    
    setor = db.relationship('Setor', backref=db.backref('trabalhadores', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'setor_id': self.setor_id,
            'setor_nome': self.setor.nome if self.setor else None,
            'cargo': self.cargo
        }

class Maquina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    codigo = db.Column(db.String(50), unique=True)
    setor_id = db.Column(db.Integer, db.ForeignKey('setor.id'), nullable=False)
    status = db.Column(db.String(20), default='Operacional')  # Operacional, Parada, Manutenção
    
    setor = db.relationship('Setor', backref=db.backref('maquinas', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'nome': self.nome,
            'codigo': self.codigo,
            'setor_id': self.setor_id,
            'setor_nome': self.setor.nome if self.setor else None,
            'status': self.status
        }

class OrdemServico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero_os = db.Column(db.String(20), unique=True, nullable=False)
    titulo = db.Column(db.String(200), nullable=False)
    descricao = db.Column(db.Text)
    requisitante = db.Column(db.String(100), nullable=False)
    setor_requisitante = db.Column(db.String(100))
    prioridade = db.Column(db.String(20), default='Normal')  # Baixa, Normal, Alta, Urgente
    status = db.Column(db.String(20), default='Aberta')  # Aberta, Em Andamento, Concluída, Cancelada
    data_abertura = db.Column(db.DateTime, default=datetime.utcnow)
    data_inicio = db.Column(db.DateTime)
    data_conclusao = db.Column(db.DateTime)
    maquina_id = db.Column(db.Integer, db.ForeignKey('maquina.id'))
    tempo_parada_horas = db.Column(db.Float, default=0)
    
    maquina = db.relationship('Maquina', backref=db.backref('ordens_servico', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'numero_os': self.numero_os,
            'titulo': self.titulo,
            'descricao': self.descricao,
            'requisitante': self.requisitante,
            'setor_requisitante': self.setor_requisitante,
            'prioridade': self.prioridade,
            'status': self.status,
            'data_abertura': self.data_abertura.isoformat() if self.data_abertura else None,
            'data_inicio': self.data_inicio.isoformat() if self.data_inicio else None,
            'data_conclusao': self.data_conclusao.isoformat() if self.data_conclusao else None,
            'maquina_id': self.maquina_id,
            'maquina_nome': self.maquina.nome if self.maquina else None,
            'tempo_parada_horas': self.tempo_parada_horas
        }

class AtividadeTrabalhador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ordem_servico_id = db.Column(db.Integer, db.ForeignKey('ordem_servico.id'), nullable=False)
    trabalhador_id = db.Column(db.Integer, db.ForeignKey('trabalhador.id'), nullable=False)
    data_inicio = db.Column(db.DateTime, nullable=False)
    data_fim = db.Column(db.DateTime)
    horas_trabalhadas = db.Column(db.Float, default=0)
    descricao_atividade = db.Column(db.Text)
    status = db.Column(db.String(20), default='Em Andamento')  # Em Andamento, Concluída, Pausada
    
    ordem_servico = db.relationship('OrdemServico', backref=db.backref('atividades', lazy=True))
    trabalhador = db.relationship('Trabalhador', backref=db.backref('atividades', lazy=True))
    
    def to_dict(self):
        return {
            'id': self.id,
            'ordem_servico_id': self.ordem_servico_id,
            'trabalhador_id': self.trabalhador_id,
            'trabalhador_nome': self.trabalhador.nome if self.trabalhador else None,
            'setor_nome': self.trabalhador.setor.nome if self.trabalhador and self.trabalhador.setor else None,
            'data_inicio': self.data_inicio.isoformat() if self.data_inicio else None,
            'data_fim': self.data_fim.isoformat() if self.data_fim else None,
            'horas_trabalhadas': self.horas_trabalhadas,
            'descricao_atividade': self.descricao_atividade,
            'status': self.status
        }

# Rotas da API

@app.route('/')
def dashboard():
    return render_template('dashboard.html')

# CRUD Setores
@app.route('/api/setores', methods=['GET'])
def get_setores():
    setores = Setor.query.all()
    return jsonify([setor.to_dict() for setor in setores])

@app.route('/api/setores', methods=['POST'])
def create_setor():
    data = request.json
    setor = Setor(nome=data['nome'], descricao=data.get('descricao'))
    db.session.add(setor)
    db.session.commit()
    return jsonify(setor.to_dict()), 201

# CRUD Trabalhadores
@app.route('/api/trabalhadores', methods=['GET'])
def get_trabalhadores():
    trabalhadores = Trabalhador.query.all()
    return jsonify([trabalhador.to_dict() for trabalhador in trabalhadores])

@app.route('/api/trabalhadores', methods=['POST'])
def create_trabalhador():
    data = request.json
    trabalhador = Trabalhador(
        nome=data['nome'],
        setor_id=data['setor_id'],
        cargo=data.get('cargo')
    )
    db.session.add(trabalhador)
    db.session.commit()
    return jsonify(trabalhador.to_dict()), 201

# CRUD Máquinas
@app.route('/api/maquinas', methods=['GET'])
def get_maquinas():
    maquinas = Maquina.query.all()
    return jsonify([maquina.to_dict() for maquina in maquinas])

@app.route('/api/maquinas', methods=['POST'])
def create_maquina():
    data = request.json
    maquina = Maquina(
        nome=data['nome'],
        codigo=data['codigo'],
        setor_id=data['setor_id'],
        status=data.get('status', 'Operacional')
    )
    db.session.add(maquina)
    db.session.commit()
    return jsonify(maquina.to_dict()), 201

# CRUD Ordens de Serviço
@app.route('/api/ordens-servico', methods=['GET'])
def get_ordens_servico():
    ordens = OrdemServico.query.all()
    return jsonify([ordem.to_dict() for ordem in ordens])

@app.route('/api/ordens-servico', methods=['POST'])
def create_ordem_servico():
    data = request.json
    
    # Gerar número da OS automaticamente
    ultimo_numero = db.session.query(db.func.max(OrdemServico.id)).scalar() or 0
    numero_os = f"OS{str(ultimo_numero + 1).zfill(6)}"
    
    ordem = OrdemServico(
        numero_os=numero_os,
        titulo=data['titulo'],
        descricao=data.get('descricao'),
        requisitante=data['requisitante'],
        setor_requisitante=data.get('setor_requisitante'),
        prioridade=data.get('prioridade', 'Normal'),
        maquina_id=data.get('maquina_id'),
        tempo_parada_horas=data.get('tempo_parada_horas', 0)
    )
    db.session.add(ordem)
    db.session.commit()
    return jsonify(ordem.to_dict()), 201

@app.route('/api/ordens-servico/<int:os_id>/iniciar', methods=['PUT'])
def iniciar_ordem_servico(os_id):
    ordem = OrdemServico.query.get_or_404(os_id)
    ordem.status = 'Em Andamento'
    ordem.data_inicio = datetime.utcnow()
    db.session.commit()
    return jsonify(ordem.to_dict())

@app.route('/api/ordens-servico/<int:os_id>/concluir', methods=['PUT'])
def concluir_ordem_servico(os_id):
    ordem = OrdemServico.query.get_or_404(os_id)
    ordem.status = 'Concluída'
    ordem.data_conclusao = datetime.utcnow()
    
    # Finalizar todas as atividades em andamento
    atividades_abertas = AtividadeTrabalhador.query.filter_by(
        ordem_servico_id=os_id,
        status='Em Andamento'
    ).all()
    
    for atividade in atividades_abertas:
        atividade.data_fim = datetime.utcnow()
        atividade.status = 'Concluída'
        if atividade.data_inicio:
            delta = atividade.data_fim - atividade.data_inicio
            atividade.horas_trabalhadas = delta.total_seconds() / 3600
    
    db.session.commit()
    return jsonify(ordem.to_dict())

# CRUD Atividades dos Trabalhadores
@app.route('/api/atividades', methods=['GET'])
def get_atividades():
    ordem_id = request.args.get('ordem_id')
    if ordem_id:
        atividades = AtividadeTrabalhador.query.filter_by(ordem_servico_id=ordem_id).all()
    else:
        atividades = AtividadeTrabalhador.query.all()
    return jsonify([atividade.to_dict() for atividade in atividades])

@app.route('/api/atividades', methods=['POST'])
def create_atividade():
    data = request.json
    atividade = AtividadeTrabalhador(
        ordem_servico_id=data['ordem_servico_id'],
        trabalhador_id=data['trabalhador_id'],
        data_inicio=datetime.fromisoformat(data['data_inicio'].replace('Z', '+00:00')),
        descricao_atividade=data.get('descricao_atividade')
    )
    db.session.add(atividade)
    db.session.commit()
    return jsonify(atividade.to_dict()), 201

@app.route('/api/atividades/<int:atividade_id>/finalizar', methods=['PUT'])
def finalizar_atividade(atividade_id):
    atividade = AtividadeTrabalhador.query.get_or_404(atividade_id)
    atividade.data_fim = datetime.utcnow()
    atividade.status = 'Concluída'
    
    if atividade.data_inicio:
        delta = atividade.data_fim - atividade.data_inicio
        atividade.horas_trabalhadas = delta.total_seconds() / 3600
    
    db.session.commit()
    return jsonify(atividade.to_dict())

# Relatórios e Dashboard
@app.route('/api/relatorio/tempo-trabalhadores')
def relatorio_tempo_trabalhadores():
    # Relatório de tempo gasto por trabalhador
    resultado = db.session.query(
        Trabalhador.nome,
        Setor.nome.label('setor'),
        db.func.sum(AtividadeTrabalhador.horas_trabalhadas).label('total_horas'),
        db.func.count(AtividadeTrabalhador.id).label('total_atividades')
    ).join(
        AtividadeTrabalhador, Trabalhador.id == AtividadeTrabalhador.trabalhador_id
    ).join(
        Setor, Trabalhador.setor_id == Setor.id
    ).group_by(
        Trabalhador.id, Trabalhador.nome, Setor.nome
    ).all()
    
    dados = []
    for row in resultado:
        dados.append({
            'trabalhador': row.nome,
            'setor': row.setor,
            'total_horas': float(row.total_horas or 0),
            'total_atividades': row.total_atividades
        })
    
    return jsonify(dados)

@app.route('/api/relatorio/tempo-setores')
def relatorio_tempo_setores():
    # Relatório de tempo gasto por setor
    resultado = db.session.query(
        Setor.nome,
        db.func.sum(AtividadeTrabalhador.horas_trabalhadas).label('total_horas'),
        db.func.count(db.distinct(AtividadeTrabalhador.trabalhador_id)).label('total_trabalhadores'),
        db.func.count(AtividadeTrabalhador.id).label('total_atividades')
    ).join(
        Trabalhador, Setor.id == Trabalhador.setor_id
    ).join(
        AtividadeTrabalhador, Trabalhador.id == AtividadeTrabalhador.trabalhador_id
    ).group_by(
        Setor.id, Setor.nome
    ).all()
    
    dados = []
    for row in resultado:
        dados.append({
            'setor': row.nome,
            'total_horas': float(row.total_horas or 0),
            'total_trabalhadores': row.total_trabalhadores,
            'total_atividades': row.total_atividades
        })
    
    return jsonify(dados)

@app.route('/api/relatorio/paradas-maquinas')
def relatorio_paradas_maquinas():
    # Relatório de tempo de parada por máquina
    resultado = db.session.query(
        Maquina.nome,
        Maquina.codigo,
        Setor.nome.label('setor'),
        db.func.sum(OrdemServico.tempo_parada_horas).label('total_parada'),
        db.func.count(OrdemServico.id).label('total_ordens')
    ).join(
        OrdemServico, Maquina.id == OrdemServico.maquina_id
    ).join(
        Setor, Maquina.setor_id == Setor.id
    ).group_by(
        Maquina.id, Maquina.nome, Maquina.codigo, Setor.nome
    ).all()
    
    dados = []
    for row in resultado:
        dados.append({
            'maquina': row.nome,
            'codigo': row.codigo,
            'setor': row.setor,
            'total_parada_horas': float(row.total_parada or 0),
            'total_ordens': row.total_ordens
        })
    
    return jsonify(dados)

@app.route('/api/dashboard/resumo')
def dashboard_resumo():
    # Estatísticas gerais para o dashboard
    total_ordens = OrdemServico.query.count()
    ordens_abertas = OrdemServico.query.filter_by(status='Aberta').count()
    ordens_andamento = OrdemServico.query.filter_by(status='Em Andamento').count()
    ordens_concluidas = OrdemServico.query.filter_by(status='Concluída').count()
    
    total_trabalhadores = Trabalhador.query.count()
    total_maquinas = Maquina.query.count()
    maquinas_paradas = Maquina.query.filter_by(status='Parada').count()
    
    # Tempo total de trabalho nas últimas 30 dias
    data_limite = datetime.utcnow() - timedelta(days=30)
    tempo_trabalho_mes = db.session.query(
        db.func.sum(AtividadeTrabalhador.horas_trabalhadas)
    ).filter(
        AtividadeTrabalhador.data_inicio >= data_limite
    ).scalar() or 0
    
    # Tempo total de parada nas últimas 30 dias
    tempo_parada_mes = db.session.query(
        db.func.sum(OrdemServico.tempo_parada_horas)
    ).filter(
        OrdemServico.data_abertura >= data_limite
    ).scalar() or 0
    
    return jsonify({
        'total_ordens': total_ordens,
        'ordens_abertas': ordens_abertas,
        'ordens_andamento': ordens_andamento,
        'ordens_concluidas': ordens_concluidas,
        'total_trabalhadores': total_trabalhadores,
        'total_maquinas': total_maquinas,
        'maquinas_paradas': maquinas_paradas,
        'tempo_trabalho_mes': float(tempo_trabalho_mes),
        'tempo_parada_mes': float(tempo_parada_mes)
    })

def init_db():
    """Inicializa o banco de dados com dados de exemplo"""
    db.create_all()
    
    # Verificar se já existem dados
    if Setor.query.first() is not None:
        return
    
    # Criar setores de exemplo
    setores = [
        Setor(nome='Produção', descricao='Setor de produção industrial'),
        Setor(nome='Manutenção', descricao='Setor de manutenção preventiva e corretiva'),
        Setor(nome='Qualidade', descricao='Controle de qualidade'),
        Setor(nome='Logística', descricao='Armazenagem e distribuição')
    ]
    
    for setor in setores:
        db.session.add(setor)
    
    db.session.commit()
    
    # Criar trabalhadores de exemplo
    trabalhadores = [
        Trabalhador(nome='João Silva', setor_id=1, cargo='Operador de Máquina'),
        Trabalhador(nome='Maria Santos', setor_id=2, cargo='Técnica de Manutenção'),
        Trabalhador(nome='Pedro Costa', setor_id=1, cargo='Supervisor'),
        Trabalhador(nome='Ana Oliveira', setor_id=3, cargo='Inspetora de Qualidade'),
        Trabalhador(nome='Carlos Souza', setor_id=2, cargo='Mecânico'),
        Trabalhador(nome='Lucia Ferreira', setor_id=4, cargo='Operadora de Empilhadeira')
    ]
    
    for trabalhador in trabalhadores:
        db.session.add(trabalhador)
    
    db.session.commit()
    
    # Criar máquinas de exemplo
    maquinas = [
        Maquina(nome='Torno CNC 01', codigo='TNC001', setor_id=1, status='Operacional'),
        Maquina(nome='Fresadora 02', codigo='FRS002', setor_id=1, status='Operacional'),
        Maquina(nome='Prensa Hidráulica', codigo='PRH003', setor_id=1, status='Parada'),
        Maquina(nome='Empilhadeira 01', codigo='EMP001', setor_id=4, status='Operacional'),
        Maquina(nome='Esteira Transportadora', codigo='EST001', setor_id=4, status='Operacional')
    ]
    
    for maquina in maquinas:
        db.session.add(maquina)
    
    db.session.commit()

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
from flask import Flask, render_template, request, redirect, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, timedelta
import json
import plotly
import plotly.graph_objs as go

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///controle_servicos.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelos do Banco de Dados
class Setor(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False, unique=True)
    descricao = db.Column(db.Text)
    
    def __repr__(self):
        return f'<Setor {self.nome}>'

class Trabalhador(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    setor_id = db.Column(db.Integer, db.ForeignKey('setor.id'), nullable=False)
    cargo = db.Column(db.String(100))
    
    setor = db.relationship('Setor', backref=db.backref('trabalhadores', lazy=True))
    
    def __repr__(self):
        return f'<Trabalhador {self.nome}>'

class Maquina(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(100), nullable=False)
    codigo = db.Column(db.String(50), unique=True)
    setor_id = db.Column(db.Integer, db.ForeignKey('setor.id'), nullable=False)
    status = db.Column(db.String(20), default='Ativa')  # Ativa, Parada, Manutenção
    
    setor = db.relationship('Setor', backref=db.backref('maquinas', lazy=True))
    
    def __repr__(self):
        return f'<Maquina {self.nome}>'

class OrdemServico(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    numero = db.Column(db.String(20), unique=True, nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    requisitante = db.Column(db.String(100), nullable=False)
    setor_requisitante_id = db.Column(db.Integer, db.ForeignKey('setor.id'), nullable=False)
    maquina_id = db.Column(db.Integer, db.ForeignKey('maquina.id'))
    prioridade = db.Column(db.String(20), default='Normal')  # Baixa, Normal, Alta, Urgente
    status = db.Column(db.String(20), default='Aberta')  # Aberta, Em Andamento, Concluída, Cancelada
    data_abertura = db.Column(db.DateTime, default=datetime.utcnow)
    data_inicio = db.Column(db.DateTime)
    data_conclusao = db.Column(db.DateTime)
    tempo_parada = db.Column(db.Integer, default=0)  # em minutos
    
    setor_requisitante = db.relationship('Setor', backref=db.backref('ordens_requisitadas', lazy=True))
    maquina = db.relationship('Maquina', backref=db.backref('ordens_servico', lazy=True))
    
    def __repr__(self):
        return f'<OrdemServico {self.numero}>'

class AtividadeOS(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ordem_servico_id = db.Column(db.Integer, db.ForeignKey('ordem_servico.id'), nullable=False)
    trabalhador_id = db.Column(db.Integer, db.ForeignKey('trabalhador.id'), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    data_inicio = db.Column(db.DateTime, nullable=False)
    data_fim = db.Column(db.DateTime)
    tempo_gasto = db.Column(db.Integer, default=0)  # em minutos
    status = db.Column(db.String(20), default='Em Andamento')  # Em Andamento, Concluída, Pausada
    
    ordem_servico = db.relationship('OrdemServico', backref=db.backref('atividades', lazy=True))
    trabalhador = db.relationship('Trabalhador', backref=db.backref('atividades', lazy=True))
    
    def __repr__(self):
        return f'<AtividadeOS {self.id}>'

# Rotas
@app.route('/')
def dashboard():
    # Estatísticas gerais
    total_ordens = OrdemServico.query.count()
    ordens_abertas = OrdemServico.query.filter_by(status='Aberta').count()
    ordens_andamento = OrdemServico.query.filter_by(status='Em Andamento').count()
    ordens_concluidas = OrdemServico.query.filter_by(status='Concluída').count()
    
    # Tempo total de parada
    tempo_total_parada = db.session.query(db.func.sum(OrdemServico.tempo_parada)).scalar() or 0
    
    # Gráfico de ordens por status
    status_data = [ordens_abertas, ordens_andamento, ordens_concluidas]
    status_labels = ['Abertas', 'Em Andamento', 'Concluídas']
    
    fig_status = go.Figure(data=[go.Pie(labels=status_labels, values=status_data, hole=.3)])
    fig_status.update_layout(title_text="Distribuição de Ordens por Status")
    graphJSON_status = json.dumps(fig_status, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Tempo gasto por trabalhador
    trabalhadores_tempo = db.session.query(
        Trabalhador.nome,
        db.func.sum(AtividadeOS.tempo_gasto).label('tempo_total')
    ).join(AtividadeOS).group_by(Trabalhador.id).all()
    
    if trabalhadores_tempo:
        nomes = [t[0] for t in trabalhadores_tempo]
        tempos = [t[1] or 0 for t in trabalhadores_tempo]
        
        fig_tempo = go.Figure(data=[go.Bar(x=nomes, y=tempos)])
        fig_tempo.update_layout(title_text="Tempo Gasto por Trabalhador (minutos)", xaxis_title="Trabalhador", yaxis_title="Tempo (minutos)")
        graphJSON_tempo = json.dumps(fig_tempo, cls=plotly.utils.PlotlyJSONEncoder)
    else:
        graphJSON_tempo = json.dumps({}, cls=plotly.utils.PlotlyJSONEncoder)
    
    return render_template('dashboard.html', 
                         total_ordens=total_ordens,
                         ordens_abertas=ordens_abertas,
                         ordens_andamento=ordens_andamento,
                         ordens_concluidas=ordens_concluidas,
                         tempo_total_parada=tempo_total_parada,
                         graphJSON_status=graphJSON_status,
                         graphJSON_tempo=graphJSON_tempo)

@app.route('/ordens')
def listar_ordens():
    ordens = OrdemServico.query.order_by(OrdemServico.data_abertura.desc()).all()
    return render_template('ordens.html', ordens=ordens)

@app.route('/ordem/<int:id>')
def detalhes_ordem(id):
    ordem = OrdemServico.query.get_or_404(id)
    return render_template('detalhes_ordem.html', ordem=ordem)

@app.route('/nova_ordem', methods=['GET', 'POST'])
def nova_ordem():
    if request.method == 'POST':
        numero = request.form['numero']
        descricao = request.form['descricao']
        requisitante = request.form['requisitante']
        setor_requisitante_id = request.form['setor_requisitante_id']
        maquina_id = request.form.get('maquina_id') or None
        prioridade = request.form['prioridade']
        tempo_parada = int(request.form.get('tempo_parada', 0))
        
        ordem = OrdemServico(
            numero=numero,
            descricao=descricao,
            requisitante=requisitante,
            setor_requisitante_id=setor_requisitante_id,
            maquina_id=maquina_id,
            prioridade=prioridade,
            tempo_parada=tempo_parada
        )
        
        db.session.add(ordem)
        db.session.commit()
        
        return redirect(url_for('listar_ordens'))
    
    setores = Setor.query.all()
    maquinas = Maquina.query.all()
    return render_template('nova_ordem.html', setores=setores, maquinas=maquinas)

@app.route('/iniciar_atividade/<int:ordem_id>', methods=['GET', 'POST'])
def iniciar_atividade(ordem_id):
    if request.method == 'POST':
        trabalhador_id = request.form['trabalhador_id']
        descricao = request.form['descricao']
        
        atividade = AtividadeOS(
            ordem_servico_id=ordem_id,
            trabalhador_id=trabalhador_id,
            descricao=descricao,
            data_inicio=datetime.utcnow()
        )
        
        db.session.add(atividade)
        
        # Atualizar status da ordem para "Em Andamento"
        ordem = OrdemServico.query.get(ordem_id)
        if ordem.status == 'Aberta':
            ordem.status = 'Em Andamento'
            ordem.data_inicio = datetime.utcnow()
        
        db.session.commit()
        
        return redirect(url_for('detalhes_ordem', id=ordem_id))
    
    ordem = OrdemServico.query.get_or_404(ordem_id)
    trabalhadores = Trabalhador.query.all()
    return render_template('iniciar_atividade.html', ordem=ordem, trabalhadores=trabalhadores)

@app.route('/finalizar_atividade/<int:atividade_id>')
def finalizar_atividade(atividade_id):
    atividade = AtividadeOS.query.get_or_404(atividade_id)
    atividade.data_fim = datetime.utcnow()
    atividade.status = 'Concluída'
    
    # Calcular tempo gasto
    if atividade.data_inicio and atividade.data_fim:
        delta = atividade.data_fim - atividade.data_inicio
        atividade.tempo_gasto = int(delta.total_seconds() / 60)  # em minutos
    
    db.session.commit()
    
    return redirect(url_for('detalhes_ordem', id=atividade.ordem_servico_id))

@app.route('/relatorios')
def relatorios():
    # Relatório de produtividade por trabalhador
    trabalhadores_stats = db.session.query(
        Trabalhador.nome,
        Setor.nome.label('setor_nome'),
        db.func.count(AtividadeOS.id).label('total_atividades'),
        db.func.sum(AtividadeOS.tempo_gasto).label('tempo_total'),
        db.func.avg(AtividadeOS.tempo_gasto).label('tempo_medio')
    ).join(Setor).join(AtividadeOS).group_by(Trabalhador.id).all()
    
    # Relatório de tempo de parada por máquina
    maquinas_parada = db.session.query(
        Maquina.nome,
        Maquina.codigo,
        Setor.nome.label('setor_nome'),
        db.func.sum(OrdemServico.tempo_parada).label('tempo_total_parada'),
        db.func.count(OrdemServico.id).label('total_ordens')
    ).join(Setor).join(OrdemServico).group_by(Maquina.id).all()
    
    return render_template('relatorios.html', 
                         trabalhadores_stats=trabalhadores_stats,
                         maquinas_parada=maquinas_parada)

@app.route('/configuracoes')
def configuracoes():
    setores = Setor.query.all()
    trabalhadores = Trabalhador.query.all()
    maquinas = Maquina.query.all()
    return render_template('configuracoes.html', 
                         setores=setores, 
                         trabalhadores=trabalhadores,
                         maquinas=maquinas)

# API endpoints
@app.route('/api/tempo_trabalhador/<int:trabalhador_id>')
def api_tempo_trabalhador(trabalhador_id):
    atividades = AtividadeOS.query.filter_by(trabalhador_id=trabalhador_id).all()
    tempo_total = sum(a.tempo_gasto for a in atividades if a.tempo_gasto)
    return jsonify({'tempo_total': tempo_total, 'total_atividades': len(atividades)})

def init_db():
    """Inicializar banco de dados com dados de exemplo"""
    db.create_all()
    
    # Verificar se já existem dados
    if Setor.query.count() == 0:
        # Criar setores
        setores = [
            Setor(nome='Manutenção', descricao='Setor de manutenção industrial'),
            Setor(nome='Produção', descricao='Setor de produção'),
            Setor(nome='Qualidade', descricao='Controle de qualidade'),
            Setor(nome='Elétrica', descricao='Manutenção elétrica'),
            Setor(nome='Mecânica', descricao='Manutenção mecânica')
        ]
        
        for setor in setores:
            db.session.add(setor)
        
        db.session.commit()
        
        # Criar trabalhadores
        trabalhadores = [
            Trabalhador(nome='João Silva', setor_id=1, cargo='Técnico em Manutenção'),
            Trabalhador(nome='Maria Santos', setor_id=1, cargo='Engenheira de Manutenção'),
            Trabalhador(nome='Pedro Oliveira', setor_id=4, cargo='Eletricista'),
            Trabalhador(nome='Ana Costa', setor_id=5, cargo='Mecânica'),
            Trabalhador(nome='Carlos Lima', setor_id=2, cargo='Operador de Produção')
        ]
        
        for trabalhador in trabalhadores:
            db.session.add(trabalhador)
        
        db.session.commit()
        
        # Criar máquinas
        maquinas = [
            Maquina(nome='Torno CNC 01', codigo='TRN001', setor_id=2),
            Maquina(nome='Fresadora 02', codigo='FRS002', setor_id=2),
            Maquina(nome='Compressor 01', codigo='CMP001', setor_id=1),
            Maquina(nome='Esteira Transportadora', codigo='EST001', setor_id=2),
            Maquina(nome='Prensa Hidráulica', codigo='PRH001', setor_id=2)
        ]
        
        for maquina in maquinas:
            db.session.add(maquina)
        
        db.session.commit()
        
        print("Banco de dados inicializado com dados de exemplo!")

if __name__ == '__main__':
    with app.app_context():
        init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
from flask import Flask, render_template, request, redirect, url_for, jsonify
import sqlite3
from datetime import datetime
import json
import plotly
import plotly.graph_objs as go

app = Flask(__name__)
app.config['SECRET_KEY'] = 'sua_chave_secreta_aqui'

DATABASE = 'controle_servicos.db'

def init_db():
    """Inicializar banco de dados"""
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    
    # Criar tabelas
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS setor (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT UNIQUE NOT NULL,
        descricao TEXT
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS trabalhador (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        setor_id INTEGER NOT NULL,
        cargo TEXT,
        FOREIGN KEY (setor_id) REFERENCES setor (id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS maquina (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        nome TEXT NOT NULL,
        codigo TEXT UNIQUE,
        setor_id INTEGER NOT NULL,
        status TEXT DEFAULT 'Ativa',
        FOREIGN KEY (setor_id) REFERENCES setor (id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS ordem_servico (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        numero TEXT UNIQUE NOT NULL,
        descricao TEXT NOT NULL,
        requisitante TEXT NOT NULL,
        setor_requisitante_id INTEGER NOT NULL,
        maquina_id INTEGER,
        prioridade TEXT DEFAULT 'Normal',
        status TEXT DEFAULT 'Aberta',
        data_abertura DATETIME DEFAULT CURRENT_TIMESTAMP,
        data_inicio DATETIME,
        data_conclusao DATETIME,
        tempo_parada INTEGER DEFAULT 0,
        FOREIGN KEY (setor_requisitante_id) REFERENCES setor (id),
        FOREIGN KEY (maquina_id) REFERENCES maquina (id)
    )
    ''')
    
    cursor.execute('''
    CREATE TABLE IF NOT EXISTS atividade_os (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        ordem_servico_id INTEGER NOT NULL,
        trabalhador_id INTEGER NOT NULL,
        descricao TEXT NOT NULL,
        data_inicio DATETIME NOT NULL,
        data_fim DATETIME,
        tempo_gasto INTEGER DEFAULT 0,
        status TEXT DEFAULT 'Em Andamento',
        FOREIGN KEY (ordem_servico_id) REFERENCES ordem_servico (id),
        FOREIGN KEY (trabalhador_id) REFERENCES trabalhador (id)
    )
    ''')
    
    # Inserir dados de exemplo se não existirem
    cursor.execute('SELECT COUNT(*) FROM setor')
    if cursor.fetchone()[0] == 0:
        setores = [
            ('Manutenção', 'Setor de manutenção industrial'),
            ('Produção', 'Setor de produção'),
            ('Qualidade', 'Controle de qualidade'),
            ('Elétrica', 'Manutenção elétrica'),
            ('Mecânica', 'Manutenção mecânica')
        ]
        cursor.executemany('INSERT INTO setor (nome, descricao) VALUES (?, ?)', setores)
        
        trabalhadores = [
            ('João Silva', 1, 'Técnico em Manutenção'),
            ('Maria Santos', 1, 'Engenheira de Manutenção'),
            ('Pedro Oliveira', 4, 'Eletricista'),
            ('Ana Costa', 5, 'Mecânica'),
            ('Carlos Lima', 2, 'Operador de Produção')
        ]
        cursor.executemany('INSERT INTO trabalhador (nome, setor_id, cargo) VALUES (?, ?, ?)', trabalhadores)
        
        maquinas = [
            ('Torno CNC 01', 'TRN001', 2),
            ('Fresadora 02', 'FRS002', 2),
            ('Compressor 01', 'CMP001', 1),
            ('Esteira Transportadora', 'EST001', 2),
            ('Prensa Hidráulica', 'PRH001', 2)
        ]
        cursor.executemany('INSERT INTO maquina (nome, codigo, setor_id) VALUES (?, ?, ?)', maquinas)
    
    conn.commit()
    conn.close()
    print("Banco de dados inicializado com sucesso!")

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def dashboard():
    conn = get_db_connection()
    
    # Estatísticas gerais
    total_ordens = conn.execute('SELECT COUNT(*) FROM ordem_servico').fetchone()[0]
    ordens_abertas = conn.execute('SELECT COUNT(*) FROM ordem_servico WHERE status = "Aberta"').fetchone()[0]
    ordens_andamento = conn.execute('SELECT COUNT(*) FROM ordem_servico WHERE status = "Em Andamento"').fetchone()[0]
    ordens_concluidas = conn.execute('SELECT COUNT(*) FROM ordem_servico WHERE status = "Concluída"').fetchone()[0]
    
    # Tempo total de parada
    tempo_total_parada = conn.execute('SELECT SUM(tempo_parada) FROM ordem_servico').fetchone()[0] or 0
    
    # Gráfico de ordens por status
    status_data = [ordens_abertas, ordens_andamento, ordens_concluidas]
    status_labels = ['Abertas', 'Em Andamento', 'Concluídas']
    
    fig_status = go.Figure(data=[go.Pie(labels=status_labels, values=status_data, hole=.3)])
    fig_status.update_layout(title_text="Distribuição de Ordens por Status")
    graphJSON_status = json.dumps(fig_status, cls=plotly.utils.PlotlyJSONEncoder)
    
    # Tempo gasto por trabalhador
    trabalhadores_tempo = conn.execute('''
        SELECT t.nome, SUM(a.tempo_gasto) as tempo_total
        FROM trabalhador t
        LEFT JOIN atividade_os a ON t.id = a.trabalhador_id
        GROUP BY t.id, t.nome
        HAVING tempo_total > 0
    ''').fetchall()
    
    if trabalhadores_tempo:
        nomes = [t['nome'] for t in trabalhadores_tempo]
        tempos = [t['tempo_total'] or 0 for t in trabalhadores_tempo]
        
        fig_tempo = go.Figure(data=[go.Bar(x=nomes, y=tempos)])
        fig_tempo.update_layout(title_text="Tempo Gasto por Trabalhador (minutos)", 
                               xaxis_title="Trabalhador", yaxis_title="Tempo (minutos)")
        graphJSON_tempo = json.dumps(fig_tempo, cls=plotly.utils.PlotlyJSONEncoder)
    else:
        graphJSON_tempo = json.dumps({}, cls=plotly.utils.PlotlyJSONEncoder)
    
    conn.close()
    
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
    conn = get_db_connection()
    ordens = conn.execute('''
        SELECT os.*, s.nome as setor_nome, m.nome as maquina_nome
        FROM ordem_servico os
        JOIN setor s ON os.setor_requisitante_id = s.id
        LEFT JOIN maquina m ON os.maquina_id = m.id
        ORDER BY os.data_abertura DESC
    ''').fetchall()
    conn.close()
    return render_template('ordens_simple.html', ordens=ordens)

@app.route('/ordem/<int:id>')
def detalhes_ordem(id):
    conn = get_db_connection()
    ordem = conn.execute('''
        SELECT os.*, s.nome as setor_nome, m.nome as maquina_nome, m.codigo as maquina_codigo
        FROM ordem_servico os
        JOIN setor s ON os.setor_requisitante_id = s.id
        LEFT JOIN maquina m ON os.maquina_id = m.id
        WHERE os.id = ?
    ''', (id,)).fetchone()
    
    atividades = conn.execute('''
        SELECT a.*, t.nome as trabalhador_nome, s.nome as setor_nome
        FROM atividade_os a
        JOIN trabalhador t ON a.trabalhador_id = t.id
        JOIN setor s ON t.setor_id = s.id
        WHERE a.ordem_servico_id = ?
        ORDER BY a.data_inicio DESC
    ''', (id,)).fetchall()
    
    conn.close()
    return render_template('detalhes_ordem_simple.html', ordem=ordem, atividades=atividades)

@app.route('/nova_ordem', methods=['GET', 'POST'])
def nova_ordem():
    if request.method == 'POST':
        conn = get_db_connection()
        
        numero = request.form['numero']
        descricao = request.form['descricao']
        requisitante = request.form['requisitante']
        setor_requisitante_id = request.form['setor_requisitante_id']
        maquina_id = request.form.get('maquina_id') or None
        prioridade = request.form['prioridade']
        tempo_parada = int(request.form.get('tempo_parada', 0))
        
        conn.execute('''
            INSERT INTO ordem_servico 
            (numero, descricao, requisitante, setor_requisitante_id, maquina_id, prioridade, tempo_parada)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (numero, descricao, requisitante, setor_requisitante_id, maquina_id, prioridade, tempo_parada))
        
        conn.commit()
        conn.close()
        
        return redirect(url_for('listar_ordens'))
    
    conn = get_db_connection()
    setores = conn.execute('SELECT * FROM setor').fetchall()
    maquinas = conn.execute('SELECT * FROM maquina').fetchall()
    conn.close()
    
    return render_template('nova_ordem_simple.html', setores=setores, maquinas=maquinas)

@app.route('/iniciar_atividade/<int:ordem_id>', methods=['GET', 'POST'])
def iniciar_atividade(ordem_id):
    if request.method == 'POST':
        conn = get_db_connection()
        
        trabalhador_id = request.form['trabalhador_id']
        descricao = request.form['descricao']
        
        # Inserir atividade
        conn.execute('''
            INSERT INTO atividade_os (ordem_servico_id, trabalhador_id, descricao, data_inicio)
            VALUES (?, ?, ?, ?)
        ''', (ordem_id, trabalhador_id, descricao, datetime.now()))
        
        # Atualizar status da ordem
        conn.execute('''
            UPDATE ordem_servico 
            SET status = 'Em Andamento', data_inicio = ?
            WHERE id = ? AND status = 'Aberta'
        ''', (datetime.now(), ordem_id))
        
        conn.commit()
        conn.close()
        
        return redirect(url_for('detalhes_ordem', id=ordem_id))
    
    conn = get_db_connection()
    ordem = conn.execute('SELECT * FROM ordem_servico WHERE id = ?', (ordem_id,)).fetchone()
    trabalhadores = conn.execute('''
        SELECT t.*, s.nome as setor_nome
        FROM trabalhador t
        JOIN setor s ON t.setor_id = s.id
    ''').fetchall()
    conn.close()
    
    return render_template('iniciar_atividade_simple.html', ordem=ordem, trabalhadores=trabalhadores)

@app.route('/finalizar_atividade/<int:atividade_id>')
def finalizar_atividade(atividade_id):
    conn = get_db_connection()
    
    # Buscar atividade
    atividade = conn.execute('SELECT * FROM atividade_os WHERE id = ?', (atividade_id,)).fetchone()
    
    if atividade:
        data_fim = datetime.now()
        data_inicio = datetime.fromisoformat(atividade['data_inicio'])
        tempo_gasto = int((data_fim - data_inicio).total_seconds() / 60)
        
        # Atualizar atividade
        conn.execute('''
            UPDATE atividade_os 
            SET data_fim = ?, tempo_gasto = ?, status = 'Concluída'
            WHERE id = ?
        ''', (data_fim, tempo_gasto, atividade_id))
        
        conn.commit()
        ordem_id = atividade['ordem_servico_id']
    
    conn.close()
    return redirect(url_for('detalhes_ordem', id=ordem_id))

@app.route('/relatorios')
def relatorios():
    conn = get_db_connection()
    
    # Relatório de produtividade por trabalhador
    trabalhadores_stats = conn.execute('''
        SELECT 
            t.nome,
            s.nome as setor_nome,
            COUNT(a.id) as total_atividades,
            SUM(a.tempo_gasto) as tempo_total,
            AVG(a.tempo_gasto) as tempo_medio
        FROM trabalhador t
        JOIN setor s ON t.setor_id = s.id
        LEFT JOIN atividade_os a ON t.id = a.trabalhador_id
        GROUP BY t.id
        HAVING total_atividades > 0
    ''').fetchall()
    
    # Relatório de tempo de parada por máquina
    maquinas_parada = conn.execute('''
        SELECT 
            m.nome,
            m.codigo,
            s.nome as setor_nome,
            SUM(os.tempo_parada) as tempo_total_parada,
            COUNT(os.id) as total_ordens
        FROM maquina m
        JOIN setor s ON m.setor_id = s.id
        LEFT JOIN ordem_servico os ON m.id = os.maquina_id
        GROUP BY m.id
        HAVING tempo_total_parada > 0
    ''').fetchall()
    
    conn.close()
    
    return render_template('relatorios_simple.html', 
                         trabalhadores_stats=trabalhadores_stats,
                         maquinas_parada=maquinas_parada)

@app.route('/configuracoes')
def configuracoes():
    conn = get_db_connection()
    setores = conn.execute('SELECT * FROM setor').fetchall()
    trabalhadores = conn.execute('''
        SELECT t.*, s.nome as setor_nome
        FROM trabalhador t
        JOIN setor s ON t.setor_id = s.id
    ''').fetchall()
    maquinas = conn.execute('''
        SELECT m.*, s.nome as setor_nome
        FROM maquina m
        JOIN setor s ON m.setor_id = s.id
    ''').fetchall()
    conn.close()
    
    return render_template('configuracoes_simple.html', 
                         setores=setores, 
                         trabalhadores=trabalhadores,
                         maquinas=maquinas)

if __name__ == '__main__':
    init_db()
    app.run(debug=True, host='0.0.0.0', port=5000)
// Variáveis globais
let dadosGlobais = {
    setores: [],
    trabalhadores: [],
    maquinas: [],
    ordens: [],
    atividades: []
};

// Inicialização
document.addEventListener('DOMContentLoaded', function() {
    carregarDadosIniciais();
    atualizarDashboard();
});

// Funções de carregamento de dados
async function carregarDadosIniciais() {
    try {
        mostrarLoading(true);
        
        // Carregar todos os dados em paralelo
        const [setores, trabalhadores, maquinas, ordens] = await Promise.all([
            fetch('/api/setores').then(r => r.json()),
            fetch('/api/trabalhadores').then(r => r.json()),
            fetch('/api/maquinas').then(r => r.json()),
            fetch('/api/ordens-servico').then(r => r.json())
        ]);
        
        dadosGlobais.setores = setores;
        dadosGlobais.trabalhadores = trabalhadores;
        dadosGlobais.maquinas = maquinas;
        dadosGlobais.ordens = ordens;
        
        // Preencher selects
        preencherSelectMaquinas();
        
        mostrarLoading(false);
    } catch (error) {
        console.error('Erro ao carregar dados iniciais:', error);
        mostrarAlerta('Erro ao carregar dados iniciais', 'danger');
        mostrarLoading(false);
    }
}

async function atualizarDashboard() {
    try {
        mostrarLoading(true);
        
        // Carregar dados do resumo e relatórios
        const [resumo, tempoTrabalhadores, tempoSetores, paradasMaquinas] = await Promise.all([
            fetch('/api/dashboard/resumo').then(r => r.json()),
            fetch('/api/relatorio/tempo-trabalhadores').then(r => r.json()),
            fetch('/api/relatorio/tempo-setores').then(r => r.json()),
            fetch('/api/relatorio/paradas-maquinas').then(r => r.json())
        ]);
        
        // Atualizar cards de estatísticas
        atualizarCardsEstatisticas(resumo);
        
        // Atualizar gráficos
        criarGraficoTempoTrabalhadores(tempoTrabalhadores);
        criarGraficoTempoSetores(tempoSetores);
        criarGraficoParadasMaquinas(paradasMaquinas);
        criarGraficoStatusOrdens(resumo);
        
        mostrarLoading(false);
    } catch (error) {
        console.error('Erro ao atualizar dashboard:', error);
        mostrarAlerta('Erro ao atualizar dashboard', 'danger');
        mostrarLoading(false);
    }
}

// Funções de interface
function mostrarSecao(secao) {
    // Esconder todas as seções
    document.querySelectorAll('.secao').forEach(el => {
        el.style.display = 'none';
    });
    
    // Remover classe active dos links
    document.querySelectorAll('.sidebar .nav-link').forEach(el => {
        el.classList.remove('active');
    });
    
    // Mostrar seção selecionada
    document.getElementById(`secao-${secao}`).style.display = 'block';
    
    // Adicionar classe active ao link
    event.target.classList.add('active');
    
    // Carregar dados específicos da seção
    switch(secao) {
        case 'ordens':
            carregarTabelaOrdens();
            break;
        case 'trabalhadores':
            carregarTabelaTrabalhadores();
            break;
        case 'maquinas':
            carregarTabelaMaquinas();
            break;
        case 'relatorios':
            carregarRelatoriosDetalhados();
            break;
    }
}

function mostrarLoading(mostrar) {
    const loading = document.getElementById('loading');
    loading.style.display = mostrar ? 'block' : 'none';
}

function mostrarAlerta(mensagem, tipo = 'info') {
    // Criar elemento de alerta
    const alerta = document.createElement('div');
    alerta.className = `alert alert-${tipo} alert-dismissible fade show position-fixed`;
    alerta.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
    alerta.innerHTML = `
        ${mensagem}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(alerta);
    
    // Remover após 5 segundos
    setTimeout(() => {
        if (alerta.parentNode) {
            alerta.parentNode.removeChild(alerta);
        }
    }, 5000);
}

// Funções de atualização de interface
function atualizarCardsEstatisticas(dados) {
    const container = document.getElementById('cards-estatisticas');
    container.innerHTML = `
        <div class="col-lg-3 col-md-6 mb-3">
            <div class="card stat-card">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <h6 class="card-subtitle mb-1 text-muted">Total de Ordens</h6>
                            <h3 class="card-title mb-0">${dados.total_ordens}</h3>
                        </div>
                        <div class="text-primary">
                            <i class="fas fa-clipboard-list fa-2x"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-lg-3 col-md-6 mb-3">
            <div class="card stat-card success">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <h6 class="card-subtitle mb-1 text-muted">Em Andamento</h6>
                            <h3 class="card-title mb-0">${dados.ordens_andamento}</h3>
                        </div>
                        <div class="text-success">
                            <i class="fas fa-cog fa-2x"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-lg-3 col-md-6 mb-3">
            <div class="card stat-card warning">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <h6 class="card-subtitle mb-1 text-muted">Máquinas Paradas</h6>
                            <h3 class="card-title mb-0">${dados.maquinas_paradas}</h3>
                        </div>
                        <div class="text-warning">
                            <i class="fas fa-exclamation-triangle fa-2x"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
        <div class="col-lg-3 col-md-6 mb-3">
            <div class="card stat-card danger">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-center">
                        <div>
                            <h6 class="card-subtitle mb-1 text-muted">Horas de Parada (mês)</h6>
                            <h3 class="card-title mb-0">${dados.tempo_parada_mes.toFixed(1)}h</h3>
                        </div>
                        <div class="text-danger">
                            <i class="fas fa-clock fa-2x"></i>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    `;
}

// Funções de gráficos
function criarGraficoTempoTrabalhadores(dados) {
    if (dados.length === 0) {
        document.getElementById('grafico-tempo-trabalhadores').innerHTML = '<p class="text-center text-muted">Nenhum dado disponível</p>';
        return;
    }
    
    const trace = {
        x: dados.map(d => d.trabalhador),
        y: dados.map(d => d.total_horas),
        type: 'bar',
        marker: {
            color: dados.map(d => getCorPorSetor(d.setor)),
            opacity: 0.8
        },
        text: dados.map(d => `${d.total_horas.toFixed(1)}h`),
        textposition: 'auto',
        hovertemplate: '<b>%{x}</b><br>' +
                      'Setor: %{customdata}<br>' +
                      'Horas: %{y:.1f}h<br>' +
                      '<extra></extra>',
        customdata: dados.map(d => d.setor)
    };
    
    const layout = {
        title: false,
        xaxis: { title: 'Trabalhadores' },
        yaxis: { title: 'Horas Trabalhadas' },
        margin: { t: 20, b: 80, l: 60, r: 20 },
        font: { family: 'Segoe UI, sans-serif' }
    };
    
    const config = { responsive: true, displayModeBar: false };
    
    Plotly.newPlot('grafico-tempo-trabalhadores', [trace], layout, config);
}

function criarGraficoTempoSetores(dados) {
    if (dados.length === 0) {
        document.getElementById('grafico-tempo-setores').innerHTML = '<p class="text-center text-muted">Nenhum dado disponível</p>';
        return;
    }
    
    const trace = {
        labels: dados.map(d => d.setor),
        values: dados.map(d => d.total_horas),
        type: 'pie',
        hole: 0.4,
        marker: {
            colors: ['#2563eb', '#059669', '#d97706', '#dc2626', '#7c3aed']
        },
        textinfo: 'label+percent+value',
        texttemplate: '%{label}<br>%{value:.1f}h (%{percent})',
        hovertemplate: '<b>%{label}</b><br>' +
                      'Horas: %{value:.1f}h<br>' +
                      'Trabalhadores: %{customdata}<br>' +
                      '<extra></extra>',
        customdata: dados.map(d => d.total_trabalhadores)
    };
    
    const layout = {
        title: false,
        margin: { t: 20, b: 20, l: 20, r: 20 },
        font: { family: 'Segoe UI, sans-serif' }
    };
    
    const config = { responsive: true, displayModeBar: false };
    
    Plotly.newPlot('grafico-tempo-setores', [trace], layout, config);
}

function criarGraficoParadasMaquinas(dados) {
    if (dados.length === 0) {
        document.getElementById('grafico-paradas-maquinas').innerHTML = '<p class="text-center text-muted">Nenhum dado disponível</p>';
        return;
    }
    
    const trace = {
        x: dados.map(d => d.maquina),
        y: dados.map(d => d.total_parada_horas),
        type: 'bar',
        marker: {
            color: '#dc2626',
            opacity: 0.8
        },
        text: dados.map(d => `${d.total_parada_horas.toFixed(1)}h`),
        textposition: 'auto',
        hovertemplate: '<b>%{x}</b><br>' +
                      'Código: %{customdata.codigo}<br>' +
                      'Setor: %{customdata.setor}<br>' +
                      'Horas parada: %{y:.1f}h<br>' +
                      'Ordens: %{customdata.ordens}<br>' +
                      '<extra></extra>',
        customdata: dados.map(d => ({
            codigo: d.codigo,
            setor: d.setor,
            ordens: d.total_ordens
        }))
    };
    
    const layout = {
        title: false,
        xaxis: { title: 'Máquinas' },
        yaxis: { title: 'Horas de Parada' },
        margin: { t: 20, b: 80, l: 60, r: 20 },
        font: { family: 'Segoe UI, sans-serif' }
    };
    
    const config = { responsive: true, displayModeBar: false };
    
    Plotly.newPlot('grafico-paradas-maquinas', [trace], layout, config);
}

function criarGraficoStatusOrdens(dados) {
    const statusData = [
        { status: 'Abertas', valor: dados.ordens_abertas, cor: '#d97706' },
        { status: 'Em Andamento', valor: dados.ordens_andamento, cor: '#2563eb' },
        { status: 'Concluídas', valor: dados.ordens_concluidas, cor: '#059669' }
    ];
    
    const trace = {
        labels: statusData.map(d => d.status),
        values: statusData.map(d => d.valor),
        type: 'pie',
        hole: 0.4,
        marker: {
            colors: statusData.map(d => d.cor)
        },
        textinfo: 'label+percent+value',
        texttemplate: '%{label}<br>%{value} (%{percent})'
    };
    
    const layout = {
        title: false,
        margin: { t: 20, b: 20, l: 20, r: 20 },
        font: { family: 'Segoe UI, sans-serif' }
    };
    
    const config = { responsive: true, displayModeBar: false };
    
    Plotly.newPlot('grafico-status-ordens', [trace], layout, config);
}

// Funções de tabelas
function carregarTabelaOrdens() {
    const tbody = document.querySelector('#tabela-ordens tbody');
    tbody.innerHTML = '';
    
    dadosGlobais.ordens.forEach(ordem => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><strong>${ordem.numero_os}</strong></td>
            <td>${ordem.titulo}</td>
            <td>${ordem.requisitante}</td>
            <td>${ordem.maquina_nome || 'N/A'}</td>
            <td><span class="badge ${getBadgeClassStatus(ordem.status)}">${ordem.status}</span></td>
            <td><span class="badge ${getBadgeClassPrioridade(ordem.prioridade)}">${ordem.prioridade}</span></td>
            <td>
                <div class="btn-group btn-group-sm">
                    <button class="btn btn-outline-primary" onclick="verDetalhesOS(${ordem.id})" title="Ver Detalhes">
                        <i class="fas fa-eye"></i>
                    </button>
                    ${ordem.status === 'Aberta' ? `
                        <button class="btn btn-outline-success" onclick="iniciarOS(${ordem.id})" title="Iniciar">
                            <i class="fas fa-play"></i>
                        </button>
                    ` : ''}
                    ${ordem.status === 'Em Andamento' ? `
                        <button class="btn btn-outline-warning" onclick="concluirOS(${ordem.id})" title="Concluir">
                            <i class="fas fa-check"></i>
                        </button>
                    ` : ''}
                </div>
            </td>
        `;
        tbody.appendChild(row);
    });
}

function carregarTabelaTrabalhadores() {
    const tbody = document.querySelector('#tabela-trabalhadores tbody');
    tbody.innerHTML = '';
    
    dadosGlobais.trabalhadores.forEach(trabalhador => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><strong>${trabalhador.nome}</strong></td>
            <td>${trabalhador.setor_nome}</td>
            <td>${trabalhador.cargo || 'N/A'}</td>
            <td>
                <button class="btn btn-outline-primary btn-sm" onclick="verAtividadesTrabalhador(${trabalhador.id})" title="Ver Atividades">
                    <i class="fas fa-tasks"></i>
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

function carregarTabelaMaquinas() {
    const tbody = document.querySelector('#tabela-maquinas tbody');
    tbody.innerHTML = '';
    
    dadosGlobais.maquinas.forEach(maquina => {
        const row = document.createElement('tr');
        row.innerHTML = `
            <td><strong>${maquina.nome}</strong></td>
            <td>${maquina.codigo}</td>
            <td>${maquina.setor_nome}</td>
            <td><span class="badge ${getBadgeClassStatusMaquina(maquina.status)}">${maquina.status}</span></td>
            <td>
                <button class="btn btn-outline-primary btn-sm" onclick="verHistoricoMaquina(${maquina.id})" title="Ver Histórico">
                    <i class="fas fa-history"></i>
                </button>
            </td>
        `;
        tbody.appendChild(row);
    });
}

// Funções de modal
function abrirModalNovaOS() {
    const modal = new bootstrap.Modal(document.getElementById('modalNovaOS'));
    document.getElementById('formNovaOS').reset();
    modal.show();
}

async function salvarNovaOS() {
    const form = document.getElementById('formNovaOS');
    const formData = new FormData(form);
    
    const dados = {
        titulo: formData.get('titulo'),
        requisitante: formData.get('requisitante'),
        setor_requisitante: formData.get('setor_requisitante'),
        prioridade: formData.get('prioridade'),
        maquina_id: formData.get('maquina_id') || null,
        tempo_parada_horas: parseFloat(formData.get('tempo_parada_horas')) || 0,
        descricao: formData.get('descricao')
    };
    
    try {
        const response = await fetch('/api/ordens-servico', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify(dados)
        });
        
        if (response.ok) {
            const novaOrdem = await response.json();
            dadosGlobais.ordens.push(novaOrdem);
            
            bootstrap.Modal.getInstance(document.getElementById('modalNovaOS')).hide();
            mostrarAlerta('Ordem de serviço criada com sucesso!', 'success');
            
            // Atualizar interface se estiver na seção de ordens
            const secaoOrdens = document.getElementById('secao-ordens');
            if (secaoOrdens.style.display !== 'none') {
                carregarTabelaOrdens();
            }
            
            atualizarDashboard();
        } else {
            throw new Error('Erro ao criar ordem de serviço');
        }
    } catch (error) {
        console.error('Erro ao salvar OS:', error);
        mostrarAlerta('Erro ao criar ordem de serviço', 'danger');
    }
}

async function iniciarOS(osId) {
    try {
        const response = await fetch(`/api/ordens-servico/${osId}/iniciar`, {
            method: 'PUT'
        });
        
        if (response.ok) {
            const ordemAtualizada = await response.json();
            
            // Atualizar dados locais
            const index = dadosGlobais.ordens.findIndex(o => o.id === osId);
            if (index !== -1) {
                dadosGlobais.ordens[index] = ordemAtualizada;
            }
            
            mostrarAlerta('Ordem de serviço iniciada!', 'success');
            carregarTabelaOrdens();
            atualizarDashboard();
        } else {
            throw new Error('Erro ao iniciar ordem de serviço');
        }
    } catch (error) {
        console.error('Erro ao iniciar OS:', error);
        mostrarAlerta('Erro ao iniciar ordem de serviço', 'danger');
    }
}

async function concluirOS(osId) {
    if (!confirm('Tem certeza que deseja concluir esta ordem de serviço?')) {
        return;
    }
    
    try {
        const response = await fetch(`/api/ordens-servico/${osId}/concluir`, {
            method: 'PUT'
        });
        
        if (response.ok) {
            const ordemAtualizada = await response.json();
            
            // Atualizar dados locais
            const index = dadosGlobais.ordens.findIndex(o => o.id === osId);
            if (index !== -1) {
                dadosGlobais.ordens[index] = ordemAtualizada;
            }
            
            mostrarAlerta('Ordem de serviço concluída!', 'success');
            carregarTabelaOrdens();
            atualizarDashboard();
        } else {
            throw new Error('Erro ao concluir ordem de serviço');
        }
    } catch (error) {
        console.error('Erro ao concluir OS:', error);
        mostrarAlerta('Erro ao concluir ordem de serviço', 'danger');
    }
}

// Funções auxiliares
function preencherSelectMaquinas() {
    const select = document.getElementById('select-maquinas');
    select.innerHTML = '<option value="">Selecione uma máquina</option>';
    
    dadosGlobais.maquinas.forEach(maquina => {
        const option = document.createElement('option');
        option.value = maquina.id;
        option.textContent = `${maquina.nome} (${maquina.codigo}) - ${maquina.setor_nome}`;
        select.appendChild(option);
    });
}

function getBadgeClassStatus(status) {
    const classes = {
        'Aberta': 'bg-warning text-dark',
        'Em Andamento': 'bg-primary',
        'Concluída': 'bg-success',
        'Cancelada': 'bg-secondary'
    };
    return classes[status] || 'bg-secondary';
}

function getBadgeClassPrioridade(prioridade) {
    const classes = {
        'Baixa': 'bg-info',
        'Normal': 'bg-secondary',
        'Alta': 'bg-warning text-dark',
        'Urgente': 'bg-danger'
    };
    return classes[prioridade] || 'bg-secondary';
}

function getBadgeClassStatusMaquina(status) {
    const classes = {
        'Operacional': 'bg-success',
        'Parada': 'bg-danger',
        'Manutenção': 'bg-warning text-dark'
    };
    return classes[status] || 'bg-secondary';
}

function getCorPorSetor(setor) {
    const cores = {
        'Produção': '#2563eb',
        'Manutenção': '#059669',
        'Qualidade': '#d97706',
        'Logística': '#dc2626'
    };
    return cores[setor] || '#64748b';
}

// Funções de relatórios detalhados
async function carregarRelatoriosDetalhados() {
    try {
        const [tempoTrabalhadores, tempoSetores] = await Promise.all([
            fetch('/api/relatorio/tempo-trabalhadores').then(r => r.json()),
            fetch('/api/relatorio/tempo-setores').then(r => r.json())
        ]);
        
        criarRelatorioProdutividade(tempoTrabalhadores);
        criarRelatorioEficienciaSetor(tempoSetores);
        criarRelatorioTempoResolucao();
    } catch (error) {
        console.error('Erro ao carregar relatórios detalhados:', error);
    }
}

function criarRelatorioProdutividade(dados) {
    if (dados.length === 0) {
        document.getElementById('relatorio-produtividade').innerHTML = '<p class="text-center text-muted">Nenhum dado disponível</p>';
        return;
    }
    
    const trace1 = {
        x: dados.map(d => d.trabalhador),
        y: dados.map(d => d.total_horas),
        name: 'Horas Trabalhadas',
        type: 'bar',
        marker: { color: '#2563eb', opacity: 0.8 }
    };
    
    const trace2 = {
        x: dados.map(d => d.trabalhador),
        y: dados.map(d => d.total_atividades),
        name: 'Atividades',
        type: 'bar',
        yaxis: 'y2',
        marker: { color: '#059669', opacity: 0.8 }
    };
    
    const layout = {
        title: false,
        xaxis: { title: 'Trabalhadores' },
        yaxis: { title: 'Horas Trabalhadas', side: 'left' },
        yaxis2: { title: 'Número de Atividades', side: 'right', overlaying: 'y' },
        margin: { t: 20, b: 100, l: 60, r: 60 },
        font: { family: 'Segoe UI, sans-serif' },
        showlegend: true
    };
    
    const config = { responsive: true, displayModeBar: false };
    
    Plotly.newPlot('relatorio-produtividade', [trace1, trace2], layout, config);
}

function criarRelatorioEficienciaSetor(dados) {
    if (dados.length === 0) {
        document.getElementById('relatorio-eficiencia-setor').innerHTML = '<p class="text-center text-muted">Nenhum dado disponível</p>';
        return;
    }
    
    // Calcular eficiência (horas por atividade)
    const dadosEficiencia = dados.map(d => ({
        setor: d.setor,
        eficiencia: d.total_atividades > 0 ? d.total_horas / d.total_atividades : 0
    }));
    
    const trace = {
        x: dadosEficiencia.map(d => d.setor),
        y: dadosEficiencia.map(d => d.eficiencia),
        type: 'bar',
        marker: {
            color: dadosEficiencia.map(d => getCorPorSetor(d.setor)),
            opacity: 0.8
        },
        text: dadosEficiencia.map(d => `${d.eficiencia.toFixed(1)}h/ativ`),
        textposition: 'auto'
    };
    
    const layout = {
        title: false,
        xaxis: { title: 'Setores' },
        yaxis: { title: 'Horas por Atividade' },
        margin: { t: 20, b: 60, l: 60, r: 20 },
        font: { family: 'Segoe UI, sans-serif' }
    };
    
    const config = { responsive: true, displayModeBar: false };
    
    Plotly.newPlot('relatorio-eficiencia-setor', [trace], layout, config);
}

function criarRelatorioTempoResolucao() {
    // Filtrar ordens concluídas com datas válidas
    const ordensCompletas = dadosGlobais.ordens.filter(ordem => 
        ordem.status === 'Concluída' && 
        ordem.data_abertura && 
        ordem.data_conclusao
    );
    
    if (ordensCompletas.length === 0) {
        document.getElementById('relatorio-tempo-resolucao').innerHTML = '<p class="text-center text-muted">Nenhum dado disponível</p>';
        return;
    }
    
    // Calcular tempo de resolução em horas
    const temposResolucao = ordensCompletas.map(ordem => {
        const abertura = new Date(ordem.data_abertura);
        const conclusao = new Date(ordem.data_conclusao);
        const tempoHoras = (conclusao - abertura) / (1000 * 60 * 60);
        return {
            numero: ordem.numero_os,
            tempo: tempoHoras,
            prioridade: ordem.prioridade
        };
    });
    
    // Agrupar por prioridade
    const prioridades = ['Baixa', 'Normal', 'Alta', 'Urgente'];
    const traces = prioridades.map(prioridade => {
        const dados = temposResolucao.filter(t => t.prioridade === prioridade);
        return {
            y: dados.map(d => d.tempo),
            name: prioridade,
            type: 'box',
            boxpoints: 'all',
            jitter: 0.3,
            pointpos: -1.8
        };
    });
    
    const layout = {
        title: false,
        yaxis: { title: 'Tempo de Resolução (horas)' },
        margin: { t: 20, b: 60, l: 60, r: 20 },
        font: { family: 'Segoe UI, sans-serif' },
        showlegend: true
    };
    
    const config = { responsive: true, displayModeBar: false };
    
    Plotly.newPlot('relatorio-tempo-resolucao', traces, layout, config);
}
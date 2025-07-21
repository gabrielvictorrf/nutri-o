# Sistema de Controle de Ordens de Serviço

## 📋 Descrição

Sistema completo para controle e gerenciamento de ordens de serviço com dashboard interativo que demonstra:

- **Tempo gasto por trabalhador ou equipes** em cada atividade
- **Setores que trabalharam** em cada ordem de serviço
- **Requisitante do serviço** e informações detalhadas
- **Tempo de parada das máquinas** e impacto na produção
- **Relatórios de produtividade** e indicadores de performance (KPIs)

## 🚀 Funcionalidades Principais

### Dashboard Interativo
- Estatísticas em tempo real das ordens de serviço
- Gráficos de distribuição por status
- Tempo gasto por trabalhador (gráfico de barras)
- Indicadores de tempo total de parada
- Atualização automática a cada 30 segundos

### Gestão de Ordens de Serviço
- **Criação** de novas ordens com todas as informações necessárias
- **Acompanhamento** do status: Aberta → Em Andamento → Concluída
- **Priorização** por níveis: Baixa, Normal, Alta, Urgente
- **Vinculação** com máquinas específicas e setores
- **Controle de tempo de parada** para cada máquina

### Controle de Atividades
- **Registro detalhado** de cada atividade realizada
- **Cronometragem automática** do tempo gasto
- **Atribuição** de trabalhadores específicos
- **Timeline** completa de cada ordem de serviço

### Relatórios Avançados
- **Produtividade por trabalhador**: tempo total, atividades realizadas, eficiência
- **Tempo de parada por máquina**: impacto na produção, MTTR
- **Indicadores de Performance (KPIs)**: eficiência operacional, tempo médio de reparo
- **Resumos executivos** com métricas importantes

### Configurações
- **Gestão de setores**: cadastro e organização por departamentos
- **Cadastro de trabalhadores**: vinculação com setores e cargos
- **Registro de máquinas**: códigos, status e localização
- **Configurações do sistema**: notificações e parâmetros

## 🛠️ Tecnologias Utilizadas

- **Backend**: Python 3.8+ com Flask
- **Banco de Dados**: SQLite com SQLAlchemy ORM
- **Frontend**: HTML5, CSS3, Bootstrap 5, JavaScript
- **Gráficos**: Plotly.js para visualizações interativas
- **Icons**: Font Awesome 6

## 📦 Instalação e Configuração

### Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)

### Passos para Instalação

1. **Clone ou baixe o projeto**
```bash
# Se usando git
git clone <url-do-repositorio>
cd sistema-os

# Ou extraia os arquivos em uma pasta
```

2. **Instale as dependências**
```bash
pip install -r requirements.txt
```

3. **Execute a aplicação**
```bash
python app.py
```

4. **Acesse o sistema**
```
http://localhost:5000
```

## 🎯 Como Usar

### 1. Primeiro Acesso
- O sistema será inicializado com dados de exemplo
- Setores, trabalhadores e máquinas já estarão cadastrados
- Você pode começar criando sua primeira ordem de serviço

### 2. Criando uma Ordem de Serviço
1. Acesse **"Nova Ordem"** no menu lateral
2. Preencha os campos obrigatórios:
   - Número da OS (auto-gerado)
   - Descrição detalhada do serviço
   - Requisitante e setor
   - Prioridade
   - Máquina (se aplicável)
   - Tempo de parada (se houver)

### 3. Iniciando Atividades
1. Na lista de ordens, clique em "Ver Detalhes"
2. Clique em "Iniciar Atividade"
3. Selecione o trabalhador responsável
4. Descreva a atividade a ser realizada
5. A cronometragem iniciará automaticamente

### 4. Finalizando Atividades
1. Na tela de detalhes da ordem
2. Clique em "Finalizar" na atividade em andamento
3. O tempo será calculado automaticamente

### 5. Acompanhando Relatórios
- Acesse **"Relatórios"** para ver:
  - Produtividade por trabalhador
  - Tempo de parada por máquina
  - KPIs e indicadores de performance

## 📊 Estrutura do Banco de Dados

### Tabelas Principais

- **Setor**: Departamentos da empresa
- **Trabalhador**: Funcionários vinculados aos setores
- **Maquina**: Equipamentos com códigos e status
- **OrdemServico**: Ordens de serviço com todas as informações
- **AtividadeOS**: Atividades realizadas em cada ordem

### Relacionamentos
- Trabalhador → Setor (muitos para um)
- Máquina → Setor (muitos para um)
- OrdemServico → Setor + Máquina (muitos para um)
- AtividadeOS → OrdemServico + Trabalhador (muitos para um)

## 🔧 Configurações Avançadas

### Personalização
- Modifique os setores em **Configurações → Setores**
- Adicione trabalhadores em **Configurações → Trabalhadores**
- Cadastre máquinas em **Configurações → Máquinas**

### Backup
- O banco SQLite fica em `controle_servicos.db`
- Faça backup regular deste arquivo
- Para restaurar, substitua o arquivo e reinicie o sistema

## 📈 Indicadores e Métricas

### KPIs Disponíveis
- **Eficiência Operacional**: % de tempo produtivo vs. tempo de parada
- **MTTR**: Tempo Médio de Reparo por máquina
- **Produtividade**: Atividades por trabalhador
- **Tempo de Resposta**: Tempo médio para conclusão de ordens

### Filtros e Análises
- Por período de tempo
- Por setor ou trabalhador
- Por prioridade das ordens
- Por tipo de máquina

## 🔐 Segurança

### Dados
- Banco SQLite local (sem exposição externa)
- Dados sensíveis apenas localmente
- Backup manual recomendado

### Acesso
- Sistema single-user (um usuário por instância)
- Acesso via localhost por padrão
- Para acesso remoto, configure adequadamente

## 🆘 Solução de Problemas

### Problemas Comuns

**Erro ao instalar dependências:**
```bash
# Tente atualizar o pip
pip install --upgrade pip
pip install -r requirements.txt
```

**Porta 5000 já em uso:**
- Modifique a linha final do `app.py`:
```python
app.run(debug=True, host='0.0.0.0', port=5001)  # Mude para outra porta
```

**Banco de dados corrompido:**
- Delete o arquivo `controle_servicos.db`
- Reinicie a aplicação para recriar com dados de exemplo

## 🤝 Contribuição

Para contribuir com melhorias:
1. Faça um fork do projeto
2. Crie uma branch para sua feature
3. Commit suas mudanças
4. Push para a branch
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo LICENSE para mais detalhes.

## 📞 Suporte

Para dúvidas ou problemas:
- Abra uma issue no repositório
- Consulte a documentação técnica
- Verifique os logs da aplicação

## 🔄 Atualizações

### Versão 1.0.0
- Sistema completo de controle de OS
- Dashboard interativo
- Relatórios de produtividade
- Gestão de tempo de parada
- Interface responsiva

### Próximas Funcionalidades
- [ ] Exportação de relatórios (PDF/Excel)
- [ ] Sistema de notificações por email
- [ ] API REST para integração
- [ ] Módulo de estoque de peças
- [ ] Calendário de manutenções preventivas
- [ ] App mobile

---

**Desenvolvido com ❤️ para otimizar a gestão de manutenção industrial**
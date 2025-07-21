# Sistema de Controle de Ordem de Serviços

Um sistema completo para gerenciamento de ordens de serviço com dashboard interativo que demonstra o tempo gasto por trabalhadores em atividades, setores envolvidos, requisitantes, tempo de parada de máquinas e muito mais.

## 🚀 Funcionalidades

### Dashboard Principal
- **Cards de estatísticas** com resumo geral do sistema
- **Gráficos interativos** com Plotly.js mostrando:
  - Tempo trabalhado por funcionário
  - Distribuição de tempo por setor
  - Tempo de parada por máquina
  - Status das ordens de serviço

### Gestão de Ordens de Serviço
- Criação, edição e acompanhamento de ordens
- Controle de status (Aberta, Em Andamento, Concluída)
- Definição de prioridades (Baixa, Normal, Alta, Urgente)
- Associação com máquinas e tempo de parada
- Histórico completo de atividades

### Controle de Atividades
- Registro de tempo por trabalhador em cada ordem
- Descrição detalhada das atividades realizadas
- Controle de início e fim de atividades
- Cálculo automático de horas trabalhadas

### Relatórios Detalhados
- Produtividade por trabalhador
- Eficiência por setor
- Tempo médio de resolução por prioridade
- Análise de paradas de máquinas

### Gestão de Recursos
- Cadastro de trabalhadores por setor
- Controle de máquinas e equipamentos
- Organização por setores da empresa

## 🛠 Tecnologias Utilizadas

### Backend
- **Python 3.8+**
- **Flask** - Framework web
- **SQLAlchemy** - ORM para banco de dados
- **SQLite** - Banco de dados (pode ser alterado facilmente)

### Frontend
- **HTML5/CSS3** com design responsivo
- **Bootstrap 5** - Framework CSS
- **JavaScript ES6+**
- **Plotly.js** - Gráficos interativos
- **Font Awesome** - Ícones

## 📦 Instalação

### 1. Clonar o repositório
```bash
git clone <url-do-repositorio>
cd sistema-ordem-servicos
```

### 2. Criar ambiente virtual (recomendado)
```bash
python -m venv venv

# Linux/Mac
source venv/bin/activate

# Windows
venv\Scripts\activate
```

### 3. Instalar dependências
```bash
pip install -r requirements.txt
```

### 4. Configurar o banco de dados
```bash
# Criar banco com dados de exemplo
python popular_dados.py
```

### 5. Executar a aplicação
```bash
python app.py
```

A aplicação estará disponível em: `http://localhost:5000`

## 🎯 Como Usar

### Primeira Execução
1. Execute o script `popular_dados.py` para criar dados de exemplo
2. Acesse `http://localhost:5000` no navegador
3. Explore o dashboard e as diferentes seções

### Criando uma Nova Ordem de Serviço
1. Clique em "Nova OS" no dashboard ou na seção "Ordens de Serviço"
2. Preencha os campos obrigatórios:
   - Título da ordem
   - Requisitante
   - Prioridade
   - Máquina (opcional)
   - Tempo de parada estimado
3. Salve a ordem

### Gerenciando Atividades
1. Vá para a seção "Ordens de Serviço"
2. Clique no ícone de "Ver Detalhes" de uma ordem
3. Adicione atividades com trabalhadores específicos
4. Registre o tempo gasto em cada atividade

### Visualizando Relatórios
1. Acesse a seção "Relatórios" no menu lateral
2. Explore os gráficos interativos
3. Use o hover para ver detalhes específicos
4. Os dados são atualizados automaticamente

## 📊 Estrutura do Banco de Dados

### Principais Tabelas
- **Setor**: Departamentos da empresa
- **Trabalhador**: Funcionários por setor
- **Maquina**: Equipamentos e máquinas
- **OrdemServico**: Ordens de serviço principais
- **AtividadeTrabalhador**: Atividades detalhadas por funcionário

### Relacionamentos
- Trabalhadores pertencem a Setores
- Máquinas pertencem a Setores
- Ordens podem estar associadas a Máquinas
- Atividades conectam Trabalhadores com Ordens

## 🔧 Personalização

### Adicionando Novos Setores
```python
# Via interface web ou diretamente no banco
setor = Setor(nome='Novo Setor', descricao='Descrição do setor')
```

### Configurando Cores dos Gráficos
Edite o arquivo `static/js/dashboard.js` na função `getCorPorSetor()`:

```javascript
function getCorPorSetor(setor) {
    const cores = {
        'Produção': '#2563eb',
        'Manutenção': '#059669',
        'Qualidade': '#d97706',
        'Logística': '#dc2626',
        'Seu Setor': '#sua-cor'
    };
    return cores[setor] || '#64748b';
}
```

### Alterando Banco de Dados
Para usar PostgreSQL ou MySQL, altere a configuração em `app.py`:

```python
# PostgreSQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://user:password@localhost/dbname'

# MySQL
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://user:password@localhost/dbname'
```

## 📈 Métricas Disponíveis

### Dashboard Principal
- Total de ordens de serviço
- Ordens em andamento
- Máquinas paradas
- Horas de parada no mês

### Relatórios de Tempo
- Horas trabalhadas por funcionário
- Distribuição de tempo por setor
- Tempo médio por atividade
- Eficiência por setor

### Análise de Máquinas
- Tempo de parada por equipamento
- Frequência de manutenções
- Status operacional

## 🔒 Segurança

### Configurações Recomendadas para Produção
1. Altere a `SECRET_KEY` no arquivo `app.py`
2. Use variáveis de ambiente para configurações sensíveis
3. Configure HTTPS
4. Implemente autenticação de usuários
5. Use um banco de dados robusto (PostgreSQL/MySQL)

### Exemplo de Configuração com Variáveis de Ambiente
```python
import os
from dotenv import load_dotenv

load_dotenv()

app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'sua-chave-super-secreta')
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///ordem_servicos.db')
```

## 🚀 Deploy

### Opções de Deploy
1. **Heroku**: Ideal para testes e pequenas aplicações
2. **AWS/Google Cloud**: Para aplicações empresariais
3. **VPS**: Controle total sobre o ambiente

### Exemplo para Heroku
1. Crie um `Procfile`:
```
web: python app.py
```

2. Configure as variáveis de ambiente
3. Faça o push para o Heroku

## 🤝 Contribuição

1. Faça um fork do projeto
2. Crie uma branch para sua feature (`git checkout -b feature/AmazingFeature`)
3. Commit suas mudanças (`git commit -m 'Add some AmazingFeature'`)
4. Push para a branch (`git push origin feature/AmazingFeature`)
5. Abra um Pull Request

## 📝 Licença

Este projeto está sob a licença MIT. Veja o arquivo `LICENSE` para mais detalhes.

## 🆘 Suporte

Se encontrar problemas ou tiver dúvidas:

1. Verifique se todas as dependências estão instaladas
2. Confirme que o banco de dados foi criado corretamente
3. Verifique os logs do console para erros
4. Abra uma issue no repositório

## 🎉 Agradecimentos

- Bootstrap pela interface responsiva
- Plotly.js pelos gráficos interativos
- Flask pela simplicidade e poder
- Font Awesome pelos ícones

---

**Desenvolvido com ❤️ para facilitar o controle de ordens de serviço**
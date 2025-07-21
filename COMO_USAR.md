# 🚀 Como Usar o Sistema de Controle de Ordens de Serviço

## ✅ Sistema Funcionando!

O sistema está **rodando com sucesso** em `http://localhost:5000`

## 🎯 Funcionalidades Implementadas

### ✅ **Dashboard Interativo**
- Estatísticas em tempo real
- Gráficos de distribuição por status
- Tempo gasto por trabalhador
- Indicadores de tempo de parada
- URL: `http://localhost:5000`

### ✅ **Gestão de Ordens de Serviço**
- ✅ Listagem completa de ordens
- ✅ Criação de novas ordens
- ✅ Detalhamento de cada ordem
- ✅ Controle de status (Aberta → Em Andamento → Concluída)
- ✅ Priorização (Baixa, Normal, Alta, Urgente)
- ✅ Vinculação com máquinas e setores

### ✅ **Controle de Atividades**
- ✅ Registro de atividades por trabalhador
- ✅ Cronometragem automática de tempo
- ✅ Finalização com cálculo automático
- ✅ Timeline completa de cada ordem

### ✅ **Relatórios**
- ✅ Produtividade por trabalhador
- ✅ Tempo de parada por máquina
- ✅ KPIs e indicadores de performance

### ✅ **Configurações**
- ✅ Gestão de setores
- ✅ Cadastro de trabalhadores
- ✅ Registro de máquinas

## 🗄️ **Dados de Exemplo Carregados**

### **5 Setores:**
1. Manutenção - Setor de manutenção industrial
2. Produção - Setor de produção
3. Qualidade - Controle de qualidade
4. Elétrica - Manutenção elétrica
5. Mecânica - Manutenção mecânica

### **5 Trabalhadores:**
1. João Silva - Técnico em Manutenção
2. Maria Santos - Engenheira de Manutenção
3. Pedro Oliveira - Eletricista
4. Ana Costa - Mecânica
5. Carlos Lima - Operador de Produção

### **5 Máquinas:**
1. Torno CNC 01 (TRN001)
2. Fresadora 02 (FRS002)
3. Compressor 01 (CMP001)
4. Esteira Transportadora (EST001)
5. Prensa Hidráulica (PRH001)

## 🎮 **Como Testar o Sistema**

### 1. **Acesse o Dashboard**
```
http://localhost:5000
```

### 2. **Crie uma Nova Ordem de Serviço**
1. Clique em **"Nova Ordem"** no menu lateral
2. Preencha os campos:
   - Número: OS-20240121-1400 (auto-gerado)
   - Descrição: "Manutenção preventiva do torno CNC"
   - Requisitante: "Supervisor de Produção"
   - Setor: "Produção"
   - Máquina: "Torno CNC 01"
   - Prioridade: "Normal"
   - Tempo de Parada: "120" (2 horas)

### 3. **Inicie uma Atividade**
1. Na lista de ordens, clique no ícone de "olho" para ver detalhes
2. Clique em **"Iniciar Atividade"**
3. Selecione um trabalhador (ex: João Silva)
4. Descreva a atividade: "Inspeção inicial e limpeza"
5. Clique em **"Iniciar Atividade"**

### 4. **Finalize a Atividade**
1. Volte aos detalhes da ordem
2. Clique em **"Finalizar"** na atividade em andamento
3. O tempo será calculado automaticamente

### 5. **Veja os Relatórios**
1. Acesse **"Relatórios"** no menu
2. Veja a produtividade por trabalhador
3. Analise o tempo de parada por máquina
4. Confira os KPIs de eficiência

## 📊 **O que o Dashboard Mostra**

### **Cards de Estatísticas:**
- Total de Ordens
- Ordens Abertas
- Ordens em Andamento
- Ordens Concluídas

### **Gráficos Interativos:**
- Pizza: Distribuição por Status
- Barras: Tempo Gasto por Trabalhador

### **Indicadores:**
- Tempo Total de Parada (em minutos e horas)
- Ações Rápidas para navegação

## 🔄 **Fluxo de Trabalho**

1. **Criação da OS** → Status: "Aberta"
2. **Início da Atividade** → Status: "Em Andamento"
3. **Finalização** → Status: "Concluída"

## 💾 **Banco de Dados**

- **Arquivo:** `controle_servicos.db` (SQLite)
- **Tabelas:** 5 tabelas principais
- **Dados:** Persistidos automaticamente
- **Backup:** Copie o arquivo `.db`

## 🛠️ **Arquivos Principais**

- `app_simple.py` - Aplicação principal (funcionando)
- `templates/` - Interface HTML
- `controle_servicos.db` - Banco de dados
- `requirements.txt` - Dependências

## 🎯 **Recursos Demonstrados**

✅ **Tempo gasto por trabalhador** - Cronometragem automática  
✅ **Setores que trabalharam** - Rastreamento completo  
✅ **Requisitante do serviço** - Informações detalhadas  
✅ **Tempo de parada** - Controle de impacto na produção  
✅ **Dashboard interativo** - Visualização em tempo real  

## 🚀 **Sistema Pronto para Uso!**

O sistema está **100% funcional** e demonstra todas as funcionalidades solicitadas:
- Controle de ordens de serviço
- Dashboard com gráficos
- Gestão de tempo por trabalhador
- Controle de setores e máquinas
- Relatórios de produtividade
- Interface moderna e responsiva

**Acesse:** `http://localhost:5000` e comece a usar!
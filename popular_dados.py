#!/usr/bin/env python3
"""
Script para popular o banco de dados com dados de exemplo realistas
"""

from app import app, db, Setor, Trabalhador, Maquina, OrdemServico, AtividadeTrabalhador
from datetime import datetime, timedelta, timezone
import random

def criar_dados_exemplo():
    with app.app_context():
        print("Criando dados de exemplo...")
        
        # Limpar dados existentes
        db.drop_all()
        db.create_all()
        
        # Criar setores
        setores = [
            Setor(nome='Produção', descricao='Setor de produção industrial - fabricação de peças'),
            Setor(nome='Manutenção', descricao='Setor de manutenção preventiva e corretiva'),
            Setor(nome='Qualidade', descricao='Controle de qualidade e inspeção'),
            Setor(nome='Logística', descricao='Armazenagem, transporte e distribuição')
        ]
        
        for setor in setores:
            db.session.add(setor)
        db.session.commit()
        
        print(f"✓ Criados {len(setores)} setores")
        
        # Criar trabalhadores
        trabalhadores = [
            # Produção
            Trabalhador(nome='João Silva', setor_id=1, cargo='Operador de Máquina'),
            Trabalhador(nome='Pedro Costa', setor_id=1, cargo='Supervisor de Produção'),
            Trabalhador(nome='Ana Ferreira', setor_id=1, cargo='Operadora de Torno'),
            Trabalhador(nome='Carlos Mendes', setor_id=1, cargo='Operador de Fresadora'),
            
            # Manutenção
            Trabalhador(nome='Maria Santos', setor_id=2, cargo='Técnica de Manutenção'),
            Trabalhador(nome='Carlos Souza', setor_id=2, cargo='Mecânico Industrial'),
            Trabalhador(nome='Roberto Lima', setor_id=2, cargo='Eletricista'),
            Trabalhador(nome='José Oliveira', setor_id=2, cargo='Supervisor de Manutenção'),
            
            # Qualidade
            Trabalhador(nome='Ana Oliveira', setor_id=3, cargo='Inspetora de Qualidade'),
            Trabalhador(nome='Lucia Pereira', setor_id=3, cargo='Técnica de Controle'),
            
            # Logística
            Trabalhador(nome='Lucia Ferreira', setor_id=4, cargo='Operadora de Empilhadeira'),
            Trabalhador(nome='Marcos Alves', setor_id=4, cargo='Conferente'),
            Trabalhador(nome='Sandra Rosa', setor_id=4, cargo='Supervisora de Logística')
        ]
        
        for trabalhador in trabalhadores:
            db.session.add(trabalhador)
        db.session.commit()
        
        print(f"✓ Criados {len(trabalhadores)} trabalhadores")
        
        # Criar máquinas
        maquinas = [
            # Produção
            Maquina(nome='Torno CNC HAAS ST-10', codigo='TNC001', setor_id=1, status='Operacional'),
            Maquina(nome='Fresadora Universal Romi', codigo='FRS002', setor_id=1, status='Operacional'),
            Maquina(nome='Prensa Hidráulica 200T', codigo='PRH003', setor_id=1, status='Parada'),
            Maquina(nome='Centro de Usinagem VMC', codigo='CUV004', setor_id=1, status='Operacional'),
            Maquina(nome='Torno Convencional Nardini', codigo='TCN005', setor_id=1, status='Manutenção'),
            
            # Logística
            Maquina(nome='Empilhadeira Toyota 2.5T', codigo='EMP001', setor_id=4, status='Operacional'),
            Maquina(nome='Esteira Transportadora A1', codigo='EST001', setor_id=4, status='Operacional'),
            Maquina(nome='Empilhadeira Hyster 3T', codigo='EMP002', setor_id=4, status='Operacional'),
            Maquina(nome='Ponte Rolante 10T', codigo='PRO001', setor_id=4, status='Parada'),
            
            # Qualidade
            Maquina(nome='Máquina de Medição 3D', codigo='MM3D01', setor_id=3, status='Operacional')
        ]
        
        for maquina in maquinas:
            db.session.add(maquina)
        db.session.commit()
        
        print(f"✓ Criadas {len(maquinas)} máquinas")
        
        # Criar ordens de serviço com dados realistas
        ordens_dados = [
            {
                'titulo': 'Manutenção preventiva do torno CNC',
                'descricao': 'Troca de óleo hidráulico, verificação de guias lineares e calibração dos eixos',
                'requisitante': 'Pedro Costa',
                'setor_requisitante': 'Produção',
                'prioridade': 'Normal',
                'maquina_id': 1,
                'tempo_parada_horas': 4.0,
                'status': 'Concluída',
                'dias_atras': 15
            },
            {
                'titulo': 'Reparo no sistema hidráulico da prensa',
                'descricao': 'Vazamento na bomba hidráulica principal, necessário substituir vedações',
                'requisitante': 'João Silva',
                'setor_requisitante': 'Produção',
                'prioridade': 'Alta',
                'maquina_id': 3,
                'tempo_parada_horas': 12.0,
                'status': 'Em Andamento',
                'dias_atras': 2
            },
            {
                'titulo': 'Substituição de rolamentos do fuso',
                'descricao': 'Ruído excessivo e vibração no fuso principal da fresadora',
                'requisitante': 'Carlos Mendes',
                'setor_requisitante': 'Produção',
                'prioridade': 'Urgente',
                'maquina_id': 2,
                'tempo_parada_horas': 8.0,
                'status': 'Concluída',
                'dias_atras': 7
            },
            {
                'titulo': 'Calibração da máquina de medição 3D',
                'descricao': 'Calibração mensal conforme procedimento ISO 9001',
                'requisitante': 'Ana Oliveira',
                'setor_requisitante': 'Qualidade',
                'prioridade': 'Normal',
                'maquina_id': 10,
                'tempo_parada_horas': 2.0,
                'status': 'Aberta',
                'dias_atras': 1
            },
            {
                'titulo': 'Reparo no sistema elétrico da empilhadeira',
                'descricao': 'Problema no carregador de bateria, não está carregando completamente',
                'requisitante': 'Lucia Ferreira',
                'setor_requisitante': 'Logística',
                'prioridade': 'Alta',
                'maquina_id': 6,
                'tempo_parada_horas': 6.0,
                'status': 'Em Andamento',
                'dias_atras': 3
            },
            {
                'titulo': 'Manutenção da esteira transportadora',
                'descricao': 'Substituição de correia e ajuste de tensionamento',
                'requisitante': 'Marcos Alves',
                'setor_requisitante': 'Logística',
                'prioridade': 'Normal',
                'maquina_id': 7,
                'tempo_parada_horas': 3.0,
                'status': 'Concluída',
                'dias_atras': 10
            },
            {
                'titulo': 'Reparo emergencial na ponte rolante',
                'descricao': 'Cabo de aço rompido, necessário substituição imediata',
                'requisitante': 'Sandra Rosa',
                'setor_requisitante': 'Logística',
                'prioridade': 'Urgente',
                'maquina_id': 9,
                'tempo_parada_horas': 24.0,
                'status': 'Aberta',
                'dias_atras': 0
            },
            {
                'titulo': 'Troca de ferramentas do centro de usinagem',
                'descricao': 'Substituição do magazine de ferramentas e verificação do ATC',
                'requisitante': 'Pedro Costa',
                'setor_requisitante': 'Produção',
                'prioridade': 'Normal',
                'maquina_id': 4,
                'tempo_parada_horas': 2.5,
                'status': 'Concluída',
                'dias_atras': 5
            }
        ]
        
        ordens_criadas = []
        for i, dados in enumerate(ordens_dados):
            data_abertura = datetime.now(timezone.utc) - timedelta(days=dados['dias_atras'])
            
            ordem = OrdemServico(
                numero_os=f"OS{str(i+1).zfill(6)}",
                titulo=dados['titulo'],
                descricao=dados['descricao'],
                requisitante=dados['requisitante'],
                setor_requisitante=dados['setor_requisitante'],
                prioridade=dados['prioridade'],
                maquina_id=dados['maquina_id'],
                tempo_parada_horas=dados['tempo_parada_horas'],
                status=dados['status'],
                data_abertura=data_abertura
            )
            
            if dados['status'] in ['Em Andamento', 'Concluída']:
                ordem.data_inicio = data_abertura + timedelta(hours=random.randint(1, 8))
            
            if dados['status'] == 'Concluída':
                ordem.data_conclusao = ordem.data_inicio + timedelta(hours=random.randint(2, 16))
            
            db.session.add(ordem)
            ordens_criadas.append(ordem)
        
        db.session.commit()
        print(f"✓ Criadas {len(ordens_criadas)} ordens de serviço")
        
        # Criar atividades dos trabalhadores para ordens concluídas e em andamento
        atividades_criadas = []
        
        for ordem in ordens_criadas:
            if ordem.status in ['Concluída', 'Em Andamento']:
                # Definir trabalhadores baseado no tipo de serviço
                trabalhadores_disponiveis = []
                
                if ordem.maquina and ordem.maquina.setor_id == 1:  # Produção
                    trabalhadores_disponiveis = [6, 7, 8]  # Manutenção
                elif ordem.maquina and ordem.maquina.setor_id == 4:  # Logística
                    trabalhadores_disponiveis = [6, 7, 8]  # Manutenção
                elif ordem.maquina and ordem.maquina.setor_id == 3:  # Qualidade
                    trabalhadores_disponiveis = [9, 10]  # Qualidade
                else:
                    trabalhadores_disponiveis = [6, 7, 8]  # Manutenção por padrão
                
                # Criar 1-3 atividades por ordem
                num_atividades = random.randint(1, 3)
                
                for i in range(num_atividades):
                    trabalhador_id = random.choice(trabalhadores_disponiveis)
                    
                    # Calcular tempos das atividades
                    if i == 0:
                        data_inicio = ordem.data_inicio
                    else:
                        # Verificar se a última atividade tem data_fim válida
                        ultima_atividade = atividades_criadas[-1]
                        if ultima_atividade.data_fim:
                            data_inicio = ultima_atividade.data_fim + timedelta(minutes=random.randint(30, 180))
                        else:
                            data_inicio = ordem.data_inicio + timedelta(hours=i * random.uniform(1, 4))
                    
                    # Duração da atividade (30min a 8h)
                    duracao_horas = random.uniform(0.5, 8.0)
                    data_fim = data_inicio + timedelta(hours=duracao_horas)
                    
                    # Se a ordem está concluída, todas as atividades devem estar concluídas
                    status_atividade = 'Concluída' if ordem.status == 'Concluída' else random.choice(['Concluída', 'Em Andamento'])
                    
                    if status_atividade == 'Em Andamento':
                        data_fim = None
                        duracao_horas = 0
                    
                    # Descrições de atividades baseadas no tipo de trabalho
                    descricoes = [
                        'Diagnóstico inicial do problema',
                        'Desmontagem e inspeção dos componentes',
                        'Substituição de peças defeituosas',
                        'Montagem e ajustes finais',
                        'Teste de funcionamento e validação',
                        'Limpeza e lubrificação',
                        'Calibração e configuração',
                        'Documentação do serviço realizado'
                    ]
                    
                    atividade = AtividadeTrabalhador(
                        ordem_servico_id=ordem.id,
                        trabalhador_id=trabalhador_id,
                        data_inicio=data_inicio,
                        data_fim=data_fim,
                        horas_trabalhadas=duracao_horas,
                        descricao_atividade=random.choice(descricoes),
                        status=status_atividade
                    )
                    
                    db.session.add(atividade)
                    atividades_criadas.append(atividade)
        
        db.session.commit()
        print(f"✓ Criadas {len(atividades_criadas)} atividades de trabalhadores")
        
        print("\n🎉 Dados de exemplo criados com sucesso!")
        print("\nResumo:")
        print(f"  - {len(setores)} setores")
        print(f"  - {len(trabalhadores)} trabalhadores")
        print(f"  - {len(maquinas)} máquinas")
        print(f"  - {len(ordens_criadas)} ordens de serviço")
        print(f"  - {len(atividades_criadas)} atividades")
        
        # Estatísticas
        ordens_abertas = len([o for o in ordens_criadas if o.status == 'Aberta'])
        ordens_andamento = len([o for o in ordens_criadas if o.status == 'Em Andamento'])
        ordens_concluidas = len([o for o in ordens_criadas if o.status == 'Concluída'])
        
        print(f"\nStatus das Ordens:")
        print(f"  - Abertas: {ordens_abertas}")
        print(f"  - Em Andamento: {ordens_andamento}")
        print(f"  - Concluídas: {ordens_concluidas}")
        
        total_horas_trabalho = sum([a.horas_trabalhadas for a in atividades_criadas])
        total_horas_parada = sum([o.tempo_parada_horas for o in ordens_criadas])
        
        print(f"\nTempo:")
        print(f"  - Total horas trabalho: {total_horas_trabalho:.1f}h")
        print(f"  - Total horas parada: {total_horas_parada:.1f}h")

if __name__ == '__main__':
    criar_dados_exemplo()
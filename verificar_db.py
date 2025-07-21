import sqlite3

conn = sqlite3.connect('controle_servicos.db')
cursor = conn.cursor()

# Verificar tabelas
print("=== TABELAS ===")
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tabelas = cursor.fetchall()
for tabela in tabelas:
    print(f"- {tabela[0]}")

print("\n=== SETORES ===")
cursor.execute("SELECT * FROM setor")
setores = cursor.fetchall()
for setor in setores:
    print(f"ID: {setor[0]}, Nome: {setor[1]}, Descrição: {setor[2]}")

print("\n=== TRABALHADORES ===")
cursor.execute("SELECT t.*, s.nome FROM trabalhador t JOIN setor s ON t.setor_id = s.id")
trabalhadores = cursor.fetchall()
for trab in trabalhadores:
    print(f"ID: {trab[0]}, Nome: {trab[1]}, Cargo: {trab[3]}, Setor: {trab[4]}")

print("\n=== MÁQUINAS ===")
cursor.execute("SELECT m.*, s.nome FROM maquina m JOIN setor s ON m.setor_id = s.id")
maquinas = cursor.fetchall()
for maq in maquinas:
    print(f"ID: {maq[0]}, Nome: {maq[1]}, Código: {maq[2]}, Status: {maq[4]}, Setor: {maq[5]}")

print("\n=== ORDENS DE SERVIÇO ===")
cursor.execute("SELECT COUNT(*) FROM ordem_servico")
total_ordens = cursor.fetchone()[0]
print(f"Total de ordens: {total_ordens}")

conn.close()
print("\nBanco de dados verificado com sucesso!")
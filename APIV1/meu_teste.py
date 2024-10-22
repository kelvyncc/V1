from flask import Flask, jsonify
import cx_Oracle

app = Flask(__name__)

# Definir as credenciais de conexão
username = "tasy"
password = "Hma_T4sy"
dsn = "172.20.10.39/tasy"  # exemplo: "localhost/XE"

# Função para conectar ao banco
def get_db_connection():
    try:
        connection = cx_Oracle.connect(user=username, password=password, dsn=dsn)
        return connection
    except cx_Oracle.DatabaseError as e:
        print(f"Erro ao conectar ao banco de dados: {e}")
        return None

# Rota para buscar dados
@app.route('/ordem/<int:nr_sequencia>', methods=['GET'])
def get_ordem(nr_sequencia):
    connection = get_db_connection()
    if connection is None:
        return jsonify({"error": "Erro ao conectar ao banco de dados"}), 500

    try:
        cursor = connection.cursor()
        query = "SELECT * FROM man_ordem_servico_v WHERE nr_sequencia = :seq"
        cursor.execute(query, [nr_sequencia])
        result = cursor.fetchall()

        # Fechar cursor
        cursor.close()

        if result:
            return jsonify({"data": result})
        else:
            return jsonify({"message": "Ordem não encontrada"}), 404

    except cx_Oracle.DatabaseError as e:
        print(f"Erro na consulta ao banco de dados: {e}")
        return jsonify({"error": "Erro ao consultar o banco de dados"}), 500

    finally:
        if connection:
            connection.close()

# Rota para testar se a API está ativa
@app.route('/')
def home():
    return "API está rodando!"

# Iniciar a aplicação Flask
if __name__ == '__main__':
    app.run(debug=True)

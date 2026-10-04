from flask import Flask, render_template, jsonify, request
import json
import os

app = Flask(__name__)
DATA_FILE = 'dados.json'

DADOS_INICIAIS = {
    "equipamentos": ["Prensa 01", "Prensa 02", "Forno 01", "Forno 02", "Linha de Esmaltação", "Secador 01", "Qualidade/Escolha", "Geral"],
    "bancoParadas": [],
    "historicoFechamentos": [],
    "kpis": {
        "prodAL2": 0,
        "prodTotalL2": 0,
        "prodAL3": 0,
        "prodTotalL3": 0,
        "cacoAcumulado": 0
    }
}

# Cria o ficheiro de dados inicial caso não exista[cite: 1, 2]
if not os.path.exists(DATA_FILE):
    with open(DATA_FILE, 'w', encoding='utf-8') as f:
        json.dump(DADOS_INICIAIS, f, ensure_ascii=False, indent=2)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/api/dados', methods=['GET'])
def get_dados():
    try:
        with open(DATA_FILE, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return jsonify(data)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/dados', methods=['POST'])
def save_dados():
    try:
        data = request.json
        with open(DATA_FILE, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=2)
        return jsonify({"status": "sucesso"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Configuração da porta dinâmica exigida pelo Render (ou porta 8000 por defeito localmente)[cite: 2]
    port = int(os.environ.get("PORT", 8000))
    app.run(host='0.0.0.0', port=port, debug=False)
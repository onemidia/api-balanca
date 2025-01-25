from flask import Flask, request, jsonify
import os
import json

app = Flask(__name__)

UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_file():
    if "file" not in request.files:
        return jsonify({"error": "Nenhum arquivo enviado."}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "Arquivo inválido."}), 400

    # Salva o arquivo TXT no servidor
    filepath = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(filepath)

    # Processa o arquivo TXT para JSON
    json_data = convert_txt_to_json(filepath)

    # Salva o JSON
    json_path = filepath.replace(".txt", ".json")
    with open(json_path, "w", encoding="utf-8") as json_file:
        json.dump(json_data, json_file, indent=4, ensure_ascii=False)

    # Retorna o link para acessar o JSON
    return jsonify({"message": "Arquivo processado com sucesso.", "json_url": f"/json/{file.filename.replace('.txt', '.json')}"})

@app.route("/json/<filename>", methods=["GET"])
def get_json(filename):
    json_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(json_path):
        return jsonify({"error": "JSON não encontrado."}), 404

    with open(json_path, "r", encoding="utf-8") as json_file:
        return jsonify(json.load(json_file))

def convert_txt_to_json(filepath):
    data = []
    with open(filepath, "r", encoding="utf-8") as file:
        for line in file:
            parts = line.strip().split(";")  # Supondo que o delimitador seja ";"
            if len(parts) == 4:
                data.append({
                    "codigo": parts[0],
                    "descricao": parts[1],
                    "preco": float(parts[2]),
                    "unidade": parts[3]
                })
    return data

if __name__ == "__main__":
    app.run(debug=True)

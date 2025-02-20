from flask import Flask, request, jsonify
import pickle
import numpy as np
from flask_cors import CORS
from dotenv import load_dotenv
import os
app = Flask(__name__)

load_dotenv()

CORS(app)

MODEL_PATH = './Model/CropRecomandation_stacking_model(99,77%).pkl'

# Load model
try:
    with open(MODEL_PATH, 'rb') as file:
        model = pickle.load(file)
    print("Model berhasil dimuat dari format .pkl!")
except Exception as e:
    model = None
    print(f"Error saat memuat model: {e}")

# Middleware token
MIDDLEWARE_TOKEN = os.getenv('MIDDLEWARE_TOKEN')

@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "Model tidak berhasil dimuat"}), 500

    try:
        data = request.form.to_dict()
        if "middleware" not in data or data.get("middleware") != MIDDLEWARE_TOKEN:
            return jsonify({"error": "Anda tidak bisa menggunakan API ini"}), 403

        required_keys = ["nitrogen", "fosfor", "kalium", "suhu", "pH", "kelembapan", "curahHujan"]
        if not all(key in data for key in required_keys):
            return jsonify({"error": f"Input harus mengandung {', '.join(required_keys)}"}), 400

        input_array = np.array([
            float(data.get("nitrogen")),
            float(data.get("fosfor")),
            float(data.get("kalium")),
            float(data.get("suhu")),
            float(data.get("kelembapan")),
            float(data.get("pH")),
            float(data.get("curahHujan"))
        ]).reshape(1, -1)

        prediction = model.predict(input_array).tolist()
        probas = model.predict_proba(input_array).tolist()  # Probabilitas untuk masing-masing kelas
        classes = model.classes_  # Daftar kelas yang sesuai dengan urutan probas

        # Gabungkan kelas dan probabilitas menjadi dictionary
        class_probas = {classes[i]: probas[0][i] for i in range(len(classes))}

        highest_prob_index = np.argmax(probas[0])
        highest_prob_value = probas[0][highest_prob_index]

        return jsonify({
            "prediction": prediction[0],
            "probabilitasHigh": highest_prob_value,
            "probabilitasAll": probas,
            "classProbas": class_probas,
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

from flask import Flask, request, jsonify
import pickle
import numpy as np

app = Flask(__name__)

MODEL_PATH = './Model/CropRecomandation_stacking_model(99,77%).pkl'
try:
    with open(MODEL_PATH, 'rb') as file:
        model = pickle.load(file)
    print("Model berhasil dimuat dari format .pkl!")
except Exception as e:
    model = None
    print(f"Error saat memuat model: {e}")

@app.route("/predict", methods=["POST"])
def predict():
    if model is None:
        return jsonify({"error": "Model tidak berhasil dimuat"}), 500

    try:
        data = request.form.to_dict()

        if "input" not in data:
            return jsonify({"error": "Format input tidak valid. Berikan kunci 'input' dengan array."}), 400

        input_array = np.array(eval(data["input"]), dtype=np.float32)

        if input_array.ndim == 1:
            input_array = input_array.reshape(1, -1)

        prediction = model.predict(input_array).tolist()

        return jsonify({
            "prediction": prediction,
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)

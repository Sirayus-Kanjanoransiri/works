from flask import Flask, request, jsonify
import joblib
import numpy as np
import warnings

# Suppress warnings
warnings.filterwarnings("ignore")

app = Flask(__name__)

# Load the model
model = joblib.load("heart.pkl")

@app.route('/api/heart', methods=['POST'])
def house():
    age = request.form.get('age')
    sex = request.form.get('sex')
    blood_pressure = request.form.get('blood_pressure')
    cholestoral = request.form.get('cholestoral')
    blood_sugar_120 = request.form.get('blood_sugar_120')

        # Convert inputs to integers
    age = int(age)
    sex = int(sex)
    blood_pressure = int(blood_pressure)
    cholestoral = int(cholestoral)
    blood_sugar_120 = int(blood_sugar_120)

    # Prepare the input for the model
    x = np.array([[age, sex, blood_pressure, cholestoral, blood_sugar_120]])

    # Predict using the model
    prediction = model.predict(x)
    if(prediction[0] == 0):
        result = "ไม่เป็น"
    elif(prediction[0] == 1):
        result = "เป็น"

    # Return the result
    return jsonify({'result': result}), 200

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=3000)

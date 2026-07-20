import os
import pickle
import numpy as np
from flask import Flask, request, render_template_string

app = Flask(__name__)

# The model file must be in the same directory as app.py
MODEL_PATH = 'SVC_model.pkl'

# Load the model once when the app starts
model = None
if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)

# Cyberpunk UI Template embedded directly in app.py
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SYS.TERMINAL // SVM PREDICTOR</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Share+Tech+Mono&display=swap');
        
        :root {
            --neon-pink: #ff00ff;
            --neon-cyan: #00ffff;
            --dark-bg: #050510;
            --grid-color: rgba(0, 255, 255, 0.1);
        }

        body {
            background-color: var(--dark-bg);
            color: var(--neon-cyan);
            font-family: 'Share Tech Mono', monospace;
            margin: 0;
            padding: 20px;
            background-image: 
                linear-gradient(var(--grid-color) 1px, transparent 1px),
                linear-gradient(90deg, var(--grid-color) 1px, transparent 1px);
            background-size: 30px 30px;
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
        }

        .container {
            background: rgba(5, 5, 16, 0.85);
            border: 2px solid var(--neon-cyan);
            box-shadow: 0 0 15px var(--neon-cyan), inset 0 0 15px var(--neon-cyan);
            padding: 40px;
            max-width: 600px;
            width: 100%;
            position: relative;
            overflow: hidden;
        }

        /* Scanline effect */
        .container::after {
            content: " ";
            display: block;
            position: absolute;
            top: 0;
            left: 0;
            bottom: 0;
            right: 0;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
            z-index: 2;
            background-size: 100% 2px, 3px 100%;
            pointer-events: none;
        }

        h1 {
            text-align: center;
            color: var(--neon-pink);
            text-shadow: 0 0 10px var(--neon-pink);
            margin-bottom: 30px;
            text-transform: uppercase;
            letter-spacing: 2px;
        }

        .form-group {
            margin-bottom: 20px;
            display: flex;
            flex-direction: column;
        }

        label {
            margin-bottom: 5px;
            font-size: 1.1em;
            letter-spacing: 1px;
        }

        input {
            background: transparent;
            border: 1px solid var(--neon-cyan);
            color: var(--neon-pink);
            padding: 10px;
            font-family: 'Share Tech Mono', monospace;
            font-size: 1.2em;
            outline: none;
            transition: all 0.3s ease;
        }

        input:focus {
            box-shadow: 0 0 10px var(--neon-pink);
            border-color: var(--neon-pink);
        }

        button {
            width: 100%;
            background: transparent;
            color: var(--neon-cyan);
            border: 2px solid var(--neon-cyan);
            padding: 15px;
            font-size: 1.5em;
            font-family: 'Share Tech Mono', monospace;
            cursor: pointer;
            text-transform: uppercase;
            transition: all 0.3s ease;
            margin-top: 20px;
        }

        button:hover {
            background: var(--neon-cyan);
            color: var(--dark-bg);
            box-shadow: 0 0 20px var(--neon-cyan);
        }

        .result {
            margin-top: 30px;
            padding: 20px;
            border: 1px dashed var(--neon-pink);
            text-align: center;
            font-size: 1.5em;
            color: var(--neon-pink);
            text-shadow: 0 0 5px var(--neon-pink);
        }
        
        .error {
            color: red;
            text-shadow: 0 0 5px red;
            text-align: center;
            margin-bottom: 20px;
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>SYS.TERMINAL // SVM PREDICTOR</h1>
        
        {% if error %}
            <div class="error">>> ERROR: {{ error }}</div>
        {% endif %}

        <form method="POST" action="/">
            <div class="form-group">
                <label>> GENDER (Numeric)</label>
                <input type="number" step="any" name="gender" required value="{{ request.form['gender'] if request.form else '' }}">
            </div>
            <div class="form-group">
                <label>> AGE</label>
                <input type="number" step="any" name="age" required value="{{ request.form['age'] if request.form else '' }}">
            </div>
            <div class="form-group">
                <label>> STUDY HOURS PER WEEK</label>
                <input type="number" step="any" name="study_hours_per_week" required value="{{ request.form['study_hours_per_week'] if request.form else '' }}">
            </div>
            <div class="form-group">
                <label>> ATTENDANCE RATE</label>
                <input type="number" step="any" name="attendance_rate" required value="{{ request.form['attendance_rate'] if request.form else '' }}">
            </div>
            <div class="form-group">
                <label>> PARENT EDUCATION (Numeric)</label>
                <input type="number" step="any" name="parent_education" required value="{{ request.form['parent_education'] if request.form else '' }}">
            </div>
            <div class="form-group">
                <label>> INTERNET ACCESS (0 or 1)</label>
                <input type="number" step="any" name="internet_access" required value="{{ request.form['internet_access'] if request.form else '' }}">
            </div>
            <div class="form-group">
                <label>> EXTRACURRICULAR (0 or 1)</label>
                <input type="number" step="any" name="extracurricular" required value="{{ request.form['extracurricular'] if request.form else '' }}">
            </div>
            <div class="form-group">
                <label>> PREVIOUS SCORE</label>
                <input type="number" step="any" name="previous_score" required value="{{ request.form['previous_score'] if request.form else '' }}">
            </div>
            <div class="form-group">
                <label>> FINAL SCORE</label>
                <input type="number" step="any" name="final_score" required value="{{ request.form['final_score'] if request.form else '' }}">
            </div>

            <button type="submit">EXECUTE INFERENCE</button>
        </form>

        {% if prediction is not none %}
            <div class="result">
                >> PREDICTION OUTPUT: [ {{ prediction }} ]
            </div>
        {% endif %}
    </div>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    error = None

    if request.method == 'POST':
        if model is None:
            error = "MODEL_NOT_FOUND: Please ensure 'SVC_model.pkl' is uploaded to the server."
        else:
            try:
                # Extracting all 9 features explicitly mapping to the model's structure
                features = [
                    float(request.form['gender']),
                    float(request.form['age']),
                    float(request.form['study_hours_per_week']),
                    float(request.form['attendance_rate']),
                    float(request.form['parent_education']),
                    float(request.form['internet_access']),
                    float(request.form['extracurricular']),
                    float(request.form['previous_score']),
                    float(request.form['final_score'])
                ]
                
                # Convert to numpy array and reshape for a single prediction
                input_data = np.array(features).reshape(1, -1)
                
                # Predict
                result = model.predict(input_data)
                prediction = result[0]
                
            except Exception as e:
                error = f"COMPUTATION_ERROR: {str(e)}"

    return render_template_string(HTML_TEMPLATE, prediction=prediction, error=error)

if __name__ == '__main__':
    # Render requires binding to 0.0.0.0
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

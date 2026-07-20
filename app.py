import os
import pickle
import numpy as np
from flask import Flask, request, render_template_string

app = Flask(__name__)

# The model file must be in the same directory as app.py
MODEL_PATH = 'SVC_model.PKL'

model = None
if os.path.exists(MODEL_PATH):
    with open(MODEL_PATH, 'rb') as f:
        model = pickle.load(f)

# Massive UI Upgrade: Matrix Rain, CRT Flicker, Terminal Logs, Advanced CSS Animations
HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>SYS.NEXUS // ML.PREDICTOR</title>
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Fira+Code:wght@300;400;700&display=swap');
        
        :root {
            --neon-pink: #f900ff;
            --neon-cyan: #00f3ff;
            --neon-green: #00ff66;
            --dark-bg: #030305;
            --panel-bg: rgba(10, 10, 20, 0.85);
        }

        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: var(--dark-bg);
            color: var(--neon-cyan);
            font-family: 'Fira Code', monospace;
            overflow-x: hidden;
            min-height: 100vh;
            display: flex;
            justify-content: center;
            align-items: center;
        }

        /* Matrix Rain Canvas */
        #matrix-bg {
            position: fixed;
            top: 0;
            left: 0;
            width: 100vw;
            height: 100vh;
            z-index: -1;
            opacity: 0.15;
        }

        /* CRT Screen Effects */
        .scanlines {
            position: fixed;
            top: 0; left: 0; width: 100vw; height: 100vh;
            background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), linear-gradient(90deg, rgba(255, 0, 0, 0.06), rgba(0, 255, 0, 0.02), rgba(0, 0, 255, 0.06));
            background-size: 100% 3px, 3px 100%;
            z-index: 999;
            pointer-events: none;
        }

        .flicker {
            animation: crt-flicker 0.15s infinite;
            pointer-events: none;
            position: fixed;
            top: 0; left: 0; width: 100%; height: 100%;
            background: rgba(255,255,255,0.01);
            z-index: 998;
        }

        @keyframes crt-flicker {
            0% { opacity: 0.95; }
            50% { opacity: 0.85; }
            100% { opacity: 1; }
        }

        /* Main UI Container */
        .dashboard {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            width: 95%;
            max-width: 1200px;
            margin: 40px auto;
            position: relative;
            z-index: 10;
        }

        .panel {
            background: var(--panel-bg);
            border: 1px solid var(--neon-cyan);
            box-shadow: 0 0 15px rgba(0, 243, 255, 0.2), inset 0 0 20px rgba(0, 243, 255, 0.1);
            padding: 30px;
            position: relative;
            backdrop-filter: blur(5px);
        }

        .panel::before {
            content: '';
            position: absolute;
            top: -2px; left: -2px;
            width: 20px; height: 20px;
            border-top: 2px solid var(--neon-pink);
            border-left: 2px solid var(--neon-pink);
        }
        
        .panel::after {
            content: '';
            position: absolute;
            bottom: -2px; right: -2px;
            width: 20px; height: 20px;
            border-bottom: 2px solid var(--neon-pink);
            border-right: 2px solid var(--neon-pink);
        }

        h2 {
            color: var(--neon-pink);
            text-shadow: 0 0 10px var(--neon-pink);
            border-bottom: 1px dashed var(--neon-pink);
            padding-bottom: 10px;
            margin-bottom: 20px;
            text-transform: uppercase;
            font-size: 1.5rem;
            display: flex;
            justify-content: space-between;
        }

        h2 span { font-size: 0.5em; color: var(--neon-cyan); align-self: flex-end; }

        /* Form Styling */
        .form-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 15px;
        }

        .input-group {
            display: flex;
            flex-direction: column;
        }

        label {
            font-size: 0.8rem;
            color: #aaa;
            margin-bottom: 5px;
            text-transform: uppercase;
        }

        input {
            background: rgba(0, 243, 255, 0.05);
            border: 1px solid rgba(0, 243, 255, 0.3);
            color: #fff;
            padding: 10px;
            font-family: 'Fira Code', monospace;
            transition: all 0.3s;
        }

        input:focus {
            outline: none;
            border-color: var(--neon-cyan);
            box-shadow: 0 0 10px rgba(0, 243, 255, 0.5);
            background: rgba(0, 243, 255, 0.1);
        }

        /* Glitch Button */
        .btn {
            grid-column: span 2;
            background: transparent;
            color: var(--neon-pink);
            border: 2px solid var(--neon-pink);
            padding: 15px;
            font-size: 1.2rem;
            font-family: inherit;
            font-weight: bold;
            cursor: pointer;
            text-transform: uppercase;
            margin-top: 15px;
            position: relative;
            overflow: hidden;
            transition: 0.2s;
        }

        .btn:hover {
            background: var(--neon-pink);
            color: var(--dark-bg);
            box-shadow: 0 0 20px var(--neon-pink);
        }

        /* Terminal Sidebar */
        .terminal-log {
            font-size: 0.85rem;
            color: var(--neon-green);
            line-height: 1.5;
            height: 100%;
            display: flex;
            flex-direction: column;
        }

        .log-entry { margin-bottom: 10px; opacity: 0; animation: fadeIn 0.5s forwards; }
        .log-entry::before { content: '>'; margin-right: 10px; color: var(--neon-pink); }
        
        @keyframes fadeIn { to { opacity: 1; } }

        .result-box {
            margin-top: auto;
            border: 2px solid var(--neon-cyan);
            padding: 20px;
            text-align: center;
            font-size: 1.5rem;
            background: rgba(0, 243, 255, 0.1);
            animation: pulse 2s infinite;
        }

        @keyframes pulse {
            0% { box-shadow: 0 0 5px rgba(0,243,255,0.2); }
            50% { box-shadow: 0 0 20px rgba(0,243,255,0.6); }
            100% { box-shadow: 0 0 5px rgba(0,243,255,0.2); }
        }

        .error-text { color: #ff003c; font-weight: bold; text-shadow: 0 0 5px #ff003c; }
        
        /* Mobile Responsiveness */
        @media (max-width: 800px) {
            .dashboard { grid-template-columns: 1fr; }
            .form-grid { grid-template-columns: 1fr; }
            .btn { grid-column: span 1; }
        }
    </style>
</head>
<body>
    <div class="scanlines"></div>
    <div class="flicker"></div>
    <canvas id="matrix-bg"></canvas>

    <div class="dashboard">
        <!-- Input Panel -->
        <div class="panel">
            <h2>DATA_INPUT <span>[v1.6.1]</span></h2>
            <form method="POST" action="/" id="svm-form">
                <div class="form-grid">
                    <div class="input-group">
                        <label>Gender_ID</label>
                        <input type="number" step="any" name="gender" required value="{{ request.form.get('gender', '') }}">
                    </div>
                    <div class="input-group">
                        <label>Age_Cycle</label>
                        <input type="number" step="any" name="age" required value="{{ request.form.get('age', '') }}">
                    </div>
                    <div class="input-group">
                        <label>Study_Hours/Wk</label>
                        <input type="number" step="any" name="study_hours_per_week" required value="{{ request.form.get('study_hours_per_week', '') }}">
                    </div>
                    <div class="input-group">
                        <label>Attendance_Rate</label>
                        <input type="number" step="any" name="attendance_rate" required value="{{ request.form.get('attendance_rate', '') }}">
                    </div>
                    <div class="input-group">
                        <label>Guardian_Edu_Level</label>
                        <input type="number" step="any" name="parent_education" required value="{{ request.form.get('parent_education', '') }}">
                    </div>
                    <div class="input-group">
                        <label>Net_Access (0/1)</label>
                        <input type="number" step="any" name="internet_access" required value="{{ request.form.get('internet_access', '') }}">
                    </div>
                    <div class="input-group">
                        <label>Extracurricular (0/1)</label>
                        <input type="number" step="any" name="extracurricular" required value="{{ request.form.get('extracurricular', '') }}">
                    </div>
                    <div class="input-group">
                        <label>Prev_Score_Matrix</label>
                        <input type="number" step="any" name="previous_score" required value="{{ request.form.get('previous_score', '') }}">
                    </div>
                    <div class="input-group">
                        <label>Final_Score_Target</label>
                        <input type="number" step="any" name="final_score" required value="{{ request.form.get('final_score', '') }}">
                    </div>
                    <button type="submit" class="btn" onclick="initiateSequence()">INITIALIZE INFERENCE</button>
                </div>
            </form>
        </div>

        <!-- System Output Panel -->
        <div class="panel">
            <h2>SYS_TERMINAL <span>[LOGS]</span></h2>
            <div class="terminal-log" id="terminal">
                <div class="log-entry" style="animation-delay: 0.1s">Establishing secure connection...</div>
                <div class="log-entry" style="animation-delay: 0.4s">Model 'SVC_model.pkl' recognized.</div>
                <div class="log-entry" style="animation-delay: 0.7s">Awaiting parameter input for kernel=RBF.</div>
                
                {% if error %}
                    <div class="log-entry error-text" style="animation-delay: 1.0s">CRITICAL ERROR: {{ error }}</div>
                {% endif %}

                {% if prediction is not none %}
                    <div class="log-entry" style="animation-delay: 1.0s">Parsing vector array... [9/9] features loaded.</div>
                    <div class="log-entry" style="animation-delay: 1.5s">Executing Support Vector Classification...</div>
                    <div class="log-entry" style="animation-delay: 2.0s">Hyperplane mapped. Target acquired.</div>
                    
                    <div class="result-box" style="animation-delay: 2.5s; opacity: 0; animation: fadeIn 0.5s forwards, pulse 2s infinite 3s;">
                        CLASS PREDICTION: <span style="color: var(--neon-pink);">{{ prediction }}</span>
                    </div>
                {% endif %}
            </div>
        </div>
    </div>

    <script>
        // Matrix Rain Effect Logic
        const canvas = document.getElementById('matrix-bg');
        const ctx = canvas.getContext('2d');
        
        canvas.width = window.innerWidth;
        canvas.height = window.innerHeight;
        
        const chars = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789@#$%^&*';
        const fontSize = 14;
        const columns = canvas.width / fontSize;
        const drops = Array.from({length: columns}).fill(1);
        
        function drawMatrix() {
            ctx.fillStyle = 'rgba(3, 3, 5, 0.05)';
            ctx.fillRect(0, 0, canvas.width, canvas.height);
            ctx.fillStyle = '#00f3ff';
            ctx.font = fontSize + 'px monospace';
            
            for (let i = 0; i < drops.length; i++) {
                const text = chars[Math.floor(Math.random() * chars.length)];
                ctx.fillText(text, i * fontSize, drops[i] * fontSize);
                
                if (drops[i] * fontSize > canvas.height && Math.random() > 0.975) {
                    drops[i] = 0;
                }
                drops[i]++;
            }
        }
        setInterval(drawMatrix, 50);

        // Resize Canvas on Window Resize
        window.addEventListener('resize', () => {
            canvas.width = window.innerWidth;
            canvas.height = window.innerHeight;
        });

        // Form Submission UX enhancement
        function initiateSequence() {
            const btn = document.querySelector('.btn');
            btn.innerHTML = "COMPUTING... PLEASE WAIT";
            btn.style.pointerEvents = "none";
            btn.style.opacity = "0.7";
        }
    </script>
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    prediction = None
    error = None

    if request.method == 'POST':
        if model is None:
            error = "MODEL_NOT_FOUND: Ensure 'SVC_model.pkl' is deployed on the server."
        else:
            try:
                # Capture exactly 9 features
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
                
                input_data = np.array(features).reshape(1, -1)
                result = model.predict(input_data)
                prediction = result[0]
                
            except Exception as e:
                error = f"SYS_FAULT: {str(e)}"

    return render_template_string(HTML_TEMPLATE, prediction=prediction, error=error)

if __name__ == '__main__':
    port = int(os.environ.get("PORT", 10000))
    app.run(host='0.0.0.0', port=port)

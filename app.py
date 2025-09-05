import os
from flask import Flask, request, render_template_string
from recomendador import recomendar

app = Flask(__name__)

HTML_TEMPLATE = """
<!doctype html>
<html>
<head>
    <title>Evaluador de Historia de Usuario</title>
</head>
<body>
    <h2>Ingresa la historia de usuario</h2>
    <form method="post">
        <textarea name="historia" rows="6" cols="60" placeholder="Como [rol] quiero [funcionalidad] para [beneficio]"></textarea><br>
        <input type="submit" value="Evaluar">
    </form>
    {% if recomendaciones %}
        <h3>Recomendaciones:</h3>
        <ul>
        {% for r in recomendaciones %}
            <li>{{ r }}</li>
        {% endfor %}
        </ul>
    {% endif %}
</body>
</html>
"""

@app.route('/', methods=['GET', 'POST'])
def index():
    recomendaciones = []
    if request.method == 'POST':
        historia = request.form['historia']
        recomendaciones = recomendar(historia)
    return render_template_string(HTML_TEMPLATE, recomendaciones=recomendaciones)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)

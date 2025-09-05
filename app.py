from flask import Flask, render_template, request, redirect
import sqlite3

app = Flask(__name__)
DB_NAME = 'hu_evaluations.db'

FIBONACCI = [0, 1, 2, 3, 5, 8, 13, 21]

def redondear_fibonacci(valor):
    return min(FIBONACCI, key=lambda x: abs(x - valor))

def obtener_recomendacion(fib_valor):
    if fib_valor <= 8:
        return "✅ Historia aceptable."
    elif fib_valor < 13 and fib_valor > 8:
        return "⚠️ Considera dividir o refinar la historia."
    else:
        return "❌ División recomendada."

def init_db():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        "CREATE TABLE IF NOT EXISTS evaluations ("
        "id INTEGER PRIMARY KEY AUTOINCREMENT,"
        "description TEXT,"
        "tecnica INTEGER,"
        "desarrollo INTEGER,"
        "dependencias INTEGER,"
        "claridad INTEGER,"
        "riesgos INTEGER,"
        "total INTEGER,"
        "fibonacci INTEGER,"
        "recomendacion TEXT,"
        "fecha TIMESTAMP DEFAULT CURRENT_TIMESTAMP)"
    )
    conn.commit()
    conn.close()

init_db()

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        tecnica = int(request.form['tecnica'])
        desarrollo = int(request.form['desarrollo'])
        dependencias = int(request.form['dependencias'])
        claridad = int(request.form['claridad'])
        riesgos = int(request.form['riesgos'])

        total = tecnica + desarrollo + dependencias + claridad + riesgos
        fib_valor = redondear_fibonacci(total)
        recomendacion = obtener_recomendacion(fib_valor)

        conn = sqlite3.connect(DB_NAME)
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO evaluations (description, tecnica, desarrollo, dependencias, claridad, riesgos, total, fibonacci, recomendacion) "
            "VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)",
            (descripcion, tecnica, desarrollo, dependencias, claridad, riesgos, total, fib_valor, recomendacion)
        )
        conn.commit()
        conn.close()

        return redirect('/')

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM evaluations ORDER BY fecha DESC')
    historial = cursor.fetchall()
    conn.close()
    return render_template('index.html', historial=historial)

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)


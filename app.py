from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime
import os
from recomendador 
import generar_recomendacion

app = Flask(__name__)
DB_PATH = "hu_evaluations.db"

# Crear base de datos si no existe
if not os.path.exists(DB_PATH):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE evaluations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            description TEXT,
            tecnica INTEGER,
            desarrollo INTEGER,
            dependencias INTEGER,
            claridad INTEGER,
            riesgos INTEGER,
            total INTEGER,
            fibonacci INTEGER,
            recomendacion TEXT,
            fecha TEXT
        )
    ''')
    conn.commit()
    conn.close()

# Escala Fibonacci
fibonacci_scale = [0, 1, 2, 3, 5, 8, 13, 21]

def obtener_historia_pivote():
    import sqlite3
    conn = sqlite3.connect('tu_base_de_datos.db')  # Ajusta el nombre si es diferente
    cursor = conn.cursor()
    
    cursor.execute("SELECT texto, complejidad_tecnica, esfuerzo_desarrollo, dependencias_externas, claridad_requisitos, riesgos_incertidumbre FROM historia_pivote LIMIT 1")
    fila = cursor.fetchone()
    conn.close()

    if fila:
        return {
            'texto': fila[0],
            'criterios': {
                'complejidad_tecnica': fila[1],
                'esfuerzo_desarrollo': fila[2],
                'dependencias_externas': fila[3],
                'claridad_requisitos': fila[4],
                'riesgos_incertidumbre': fila[5]
            }
        }
    else:
        return None


def redondear_fibonacci(valor):
    return min(fibonacci_scale, key=lambda x: abs(x - valor))

def obtener_recomendacion(fib_valor):
    if fib_valor <= 8:
        return "✅ Historia aceptable."
    elif fib_valor > 8 and < 13:
        return "⚠️ Considera dividir o refinar la historia."
    else:
        return "❌ División recomendada."

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        descripcion = request.form['descripcion']
        tecnica = int(request.form['tecnica'])
        desarrollo = int(request.form['desarrollo'])
        dependencias = int(request.form['dependencias'])
        claridad = int(request.form['claridad'])
        riesgos = int(request.form['riesgos'])

        
        claridad_transformada = (claridad - 3) * -1
        total = tecnica + desarrollo + dependencias + claridad_transformada + riesgos

        fib_valor = redondear_fibonacci(total)
        recomendacion = obtener_recomendacion(fib_valor)
        fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''
            INSERT INTO evaluations (description, tecnica, desarrollo, dependencias, claridad, riesgos, total, fibonacci, recomendacion, fecha)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        ''', (descripcion, tecnica, desarrollo, dependencias, claridad, riesgos, total, fib_valor, recomendacion, fecha))
        conn.commit()
        conn.close()

        return redirect(url_for('index'))

    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM evaluations ORDER BY fecha DESC')
    historial = cursor.fetchall()
    conn.close()
    return render_template('index.html', historial=historial)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)



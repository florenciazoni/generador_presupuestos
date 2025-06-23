from flask import Flask, render_template, request, send_file
from utils.generar_pdf import crear_presupuesto
import os
import uuid

app = Flask(__name__)

@app.route('/')
def formulario():
    return render_template('formulario.html')

@app.route('/generar', methods=['POST'])
def generar():
    datos = request.form.to_dict(flat=True)
    nombre_archivo = f"{uuid.uuid4().hex}.pdf"
    ruta_pdf = os.path.join("presupuestos", nombre_archivo)

    crear_presupuesto(datos, ruta_pdf)
    return send_file(ruta_pdf, as_attachment=True)

if __name__ == '__main__':
    os.makedirs('presupuestos', exist_ok=True)
    app.run(debug=True)

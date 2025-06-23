from flask import Flask, render_template, request, send_file
from utils.generar_pdf import crear_presupuesto
import os
import uuid
import tempfile
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route('/')
def formulario():
    return render_template('formulario.html')

@app.route('/generar', methods=['POST'])
def generar():
    try:
        # Obtener datos del formulario
        datos = request.form.to_dict(flat=True)
        logo = request.files.get('logo')
        
        logger.info(f"Datos recibidos: {datos}")
        
        # Crear archivos temporales
        with tempfile.NamedTemporaryFile(suffix='.pdf', delete=False) as tmp_pdf:
            ruta_pdf = tmp_pdf.name
        
        ruta_logo = None
        if logo and logo.filename != "":
            # Crear extensión segura
            ext = os.path.splitext(logo.filename)[1]
            if not ext:
                ext = '.png'  # Extensión predeterminada
            
            with tempfile.NamedTemporaryFile(suffix=ext, delete=False) as tmp_logo:
                logo.save(tmp_logo.name)
                ruta_logo = tmp_logo.name
                logger.info(f"Logo guardado temporalmente en: {ruta_logo}")

        # Generar el PDF
        success = crear_presupuesto(datos, ruta_pdf, ruta_logo)
        
        if not success:
            logger.error("Error durante la generación del PDF, se usó respaldo")
        
        # Enviar el archivo
        return send_file(
            ruta_pdf,
            as_attachment=True,
            download_name='presupuesto.pdf',
            mimetype='application/pdf'
        )
    except Exception as e:
        logger.exception("Error grave en el servidor:")
        return f"Error grave en el servidor: {str(e)}", 500
    finally:
        # Limpiar archivos temporales
        if ruta_pdf and os.path.exists(ruta_pdf):
            try:
                os.unlink(ruta_pdf)
            except Exception as e:
                logger.error(f"Error al eliminar PDF temporal: {str(e)}")
        
        if ruta_logo and os.path.exists(ruta_logo):
            try:
                os.unlink(ruta_logo)
            except Exception as e:
                logger.error(f"Error al eliminar logo temporal: {str(e)}")

if __name__ == '__main__':
    os.makedirs('presupuestos', exist_ok=True)
    app.run(debug=True, port=5001)  # Usar puerto diferente para evitar conflictos
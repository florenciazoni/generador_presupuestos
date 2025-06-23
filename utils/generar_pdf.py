from fpdf import FPDF

def crear_presupuesto(datos, ruta_pdf):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    pdf.cell(200, 10, txt="Presupuesto", ln=True, align='C')
    pdf.ln(10)

    pdf.cell(200, 10, txt=f"Proveedor: {datos['nombre']}", ln=True)
    pdf.cell(200, 10, txt=f"Cliente: {datos['cliente']}", ln=True)
    pdf.cell(200, 10, txt=f"Servicios: {datos['servicios']}", ln=True)
    pdf.cell(200, 10, txt=f"Precio total: ${datos['precio']}", ln=True)
    pdf.cell(200, 10, txt=f"Forma de pago: {datos['forma_pago']}", ln=True)
    pdf.cell(200, 10, txt=f"Validez: {datos['validez']} días", ln=True)

    pdf.output(ruta_pdf)

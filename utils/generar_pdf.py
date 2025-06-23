from fpdf import FPDF
import os
from datetime import datetime, timedelta

class ProfessionalPDF(FPDF):
    def header(self):
        # Configuración de márgenes
        self.set_margins(20, 20, 20)
        
        # Logo si está disponible
        if hasattr(self, 'logo_path') and os.path.exists(self.logo_path):
            try:
                self.image(self.logo_path, x=20, y=15, w=40)
                self.set_y(40)  # Posición después del logo
            except RuntimeError as e:
                print(f"Error al cargar el logo: {str(e)}")
        else:
            self.set_y(30)
        
        # Título
        self.set_font('Helvetica', 'B', 18)
        self.set_text_color(44, 62, 80)  # Azul oscuro (#2c3e50)
        self.cell(0, 10, 'PRESUPUESTO', 0, 1, 'C')
        
        # Número de presupuesto
        self.set_font('Helvetica', '', 10)
        self.set_text_color(127, 140, 141)  # Gris (#7f8c8d)
        self.cell(0, 6, f'Nº: {self.presupuesto_numero}', 0, 1, 'C')
        self.ln(8)
    
    def footer(self):
        self.set_y(-25)
        self.set_font('Helvetica', 'I', 9)
        self.set_text_color(127, 140, 141)  # Gris (#7f8c8d)
        self.cell(0, 5, f'{self.empresa_nombre} - NIF: A12345678 - Tel: +34 91 123 4567', 0, 0, 'C')
        self.ln(5)
        self.cell(0, 5, f'www.{self.empresa_nombre.replace(" ", "").lower()}.com', 0, 0, 'C')
    
    def add_company_info(self, empresa, cliente):
        # Información de la empresa
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(44, 62, 80)  # Azul oscuro
        self.cell(95, 7, 'EMPRESA', 0, 0, 'L')
        self.cell(0, 7, 'CLIENTE', 0, 1, 'R')
        
        # Línea decorativa
        self.set_draw_color(52, 152, 219)  # Azul (#3498db)
        self.set_line_width(0.5)
        self.cell(95, 3, '', 'B', 0, 'L')
        self.cell(0, 3, '', 'B', 1, 'R')
        self.ln(5)
        
        # Detalles de la empresa
        self.set_font('Helvetica', '', 10)
        self.set_text_color(0, 0, 0)  # Negro
        self.cell(95, 5, empresa, 0, 0, 'L')
        self.cell(0, 5, cliente, 0, 1, 'R')
        self.cell(95, 5, 'Calle Principal, 123', 0, 0, 'L')
        self.cell(0, 5, 'Cliente Corporativo S.L.', 0, 1, 'R')
        self.cell(95, 5, '28001 Madrid, España', 0, 0, 'L')
        self.cell(0, 5, 'Calle Cliente, 456', 0, 1, 'R')
        self.cell(95, 5, f'info@{empresa.replace(" ", "").lower()}.com', 0, 0, 'L')
        self.cell(0, 5, f'{cliente.replace(" ", ".").lower()}@empresa.com', 0, 1, 'R')
        self.cell(95, 5, '+34 91 123 4567', 0, 0, 'L')
        self.ln(10)
        
        # Información del presupuesto
        try:
            fecha_actual = datetime.now().strftime('%d de %B de %Y')
            fecha_validez = (datetime.now() + timedelta(days=self.validez)).strftime('%d de %B de %Y')
        except Exception:
            fecha_actual = datetime.now().strftime('%d/%m/%Y')
            fecha_validez = (datetime.now() + timedelta(days=30)).strftime('%d/%m/%Y')
        
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(44, 62, 80)  # Azul oscuro
        self.cell(0, 7, 'DETALLES DEL PRESUPUESTO', 0, 1, 'L')
        self.set_draw_color(52, 152, 219)  # Azul
        self.cell(0, 3, '', 'B', 1, 'L')
        self.ln(3)
        
        self.set_font('Helvetica', '', 10)
        self.set_text_color(0, 0, 0)  # Negro
        self.cell(50, 6, 'Fecha:', 0, 0, 'L')
        self.cell(0, 6, fecha_actual, 0, 1, 'L')
        self.cell(50, 6, 'Válido hasta:', 0, 0, 'L')
        self.cell(0, 6, fecha_validez, 0, 1, 'L')
        self.ln(10)
    
    def add_services_section(self, servicios):
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(44, 62, 80)  # Azul oscuro
        self.cell(0, 7, 'SERVICIOS', 0, 1, 'L')
        self.set_draw_color(52, 152, 219)  # Azul
        self.cell(0, 3, '', 'B', 1, 'L')
        self.ln(5)
        
        self.set_font('Helvetica', '', 10)
        self.set_text_color(0, 0, 0)  # Negro
        self.multi_cell(0, 5, servicios)
        self.ln(10)
    
    def add_pricing_table(self, precio, iva):
        # Calcular valores con manejo de errores
        try:
            iva = float(iva)
            precio = float(precio)
            iva_monto = precio * (iva / 100)
            subtotal = precio - iva_monto
        except (ValueError, TypeError):
            iva_monto = 0
            subtotal = precio
        
        # Crear tabla
        self.set_fill_color(241, 241, 241)  # Fondo gris claro (#f1f1f1)
        self.set_font('Helvetica', 'B', 10)
        self.set_text_color(0, 0, 0)  # Negro
        
        # Encabezados de tabla
        self.cell(140, 8, 'Descripción', 1, 0, 'L', 1)
        self.cell(0, 8, 'Importe', 1, 1, 'R', 1)
        
        # Contenido de la tabla
        self.set_font('Helvetica', '', 10)
        self.cell(140, 8, 'Servicios descritos', 1, 0, 'L')
        self.cell(0, 8, self.format_currency(subtotal), 1, 1, 'R')
        
        self.cell(140, 8, f'IVA ({iva}%)', 1, 0, 'L')
        self.cell(0, 8, self.format_currency(iva_monto), 1, 1, 'R')
        
        # Total
        self.set_font('Helvetica', 'B', 10)
        self.set_fill_color(249, 249, 249)  # Fondo gris muy claro (#f9f9f9)
        self.cell(140, 8, 'TOTAL', 1, 0, 'L', 1)
        self.cell(0, 8, self.format_currency(precio), 1, 1, 'R', 1)
        self.ln(10)
    
    def add_payment_conditions(self, forma_pago, notas):
        self.set_font('Helvetica', 'B', 11)
        self.set_text_color(44, 62, 80)  # Azul oscuro
        self.cell(0, 7, 'CONDICIONES DE PAGO', 0, 1, 'L')
        self.set_draw_color(52, 152, 219)  # Azul
        self.cell(0, 3, '', 'B', 1, 'L')
        self.ln(5)
        
        self.set_font('Helvetica', '', 10)
        self.set_text_color(0, 0, 0)  # Negro
        self.multi_cell(0, 5, forma_pago or 'No especificado')
        self.ln(5)
        
        if notas:
            self.set_font('Helvetica', 'B', 10)
            self.cell(0, 7, 'Notas:', 0, 1, 'L')
            self.set_font('Helvetica', '', 10)
            self.multi_cell(0, 5, notas)
    
    def format_currency(self, value):
        try:
            # Formatear como moneda: $1,234.56
            return f"${float(value):,.2f}"
        except (ValueError, TypeError):
            return f"${0:,.2f}"

def crear_presupuesto(datos, ruta_pdf, ruta_logo=None):
    try:
        # Crear instancia del PDF personalizado
        pdf = ProfessionalPDF()
        
        # Asignar propiedades con valores predeterminados seguros
        pdf.presupuesto_numero = f"PR-{datetime.now().strftime('%Y%m%d')}-{os.getpid() % 1000:03d}"
        pdf.empresa_nombre = datos.get('nombre', 'Tu Empresa')
        
        # Manejar validez con valor predeterminado
        try:
            pdf.validez = int(datos.get('validez', '30'))
        except (ValueError, TypeError):
            pdf.validez = 30
        
        # Logo
        if ruta_logo and os.path.exists(ruta_logo):
            pdf.logo_path = ruta_logo
        
        # Configuración general
        pdf.add_page()
        pdf.set_auto_page_break(auto=True, margin=25)
        
        # Añadir secciones con manejo de campos faltantes
        pdf.add_company_info(
            datos.get('nombre', 'Tu Empresa'), 
            datos.get('cliente', 'Cliente')
        )
        
        pdf.add_services_section(datos.get('servicios', 'Servicios no especificados'))
        
        # Obtener precio e IVA con valores predeterminados
        precio = datos.get('precio', '0')
        iva = datos.get('iva', '21')
        
        pdf.add_pricing_table(precio, iva)
        pdf.add_payment_conditions(
            datos.get('forma_pago'), 
            datos.get('notas')
        )
        
        # Generar PDF
        pdf.output(ruta_pdf)
        return True
    except Exception as e:
        print(f"Error grave al generar PDF: {str(e)}")
        # Generar un PDF básico como respaldo
        try:
            pdf_fallback = FPDF()
            pdf_fallback.add_page()
            pdf_fallback.set_font("Arial", size=12)
            pdf_fallback.cell(200, 10, txt="Error al generar presupuesto", ln=True, align='C')
            pdf_fallback.cell(200, 10, txt=f"Contacta al soporte técnico: {str(e)}", ln=True)
            pdf_fallback.output(ruta_pdf)
            return False
        except:
            return False

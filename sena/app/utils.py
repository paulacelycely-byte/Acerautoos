"""
UTILIDADES PARA EXPORTACION DE REPORTES
"""
import os
from weasyprint import HTML
from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from django.http import HttpResponse
from django.template.loader import render_to_string
from django.conf import settings

# Ruta absoluta al logo — WeasyPrint necesita file:/// para cargar imágenes locales
LOGO_PATH = 'file:///' + os.path.join(
    settings.BASE_DIR, 'app', 'static', 'imagenes', 'logo empresa.jpeg'
).replace('\\', '/')


def exportar_pdf(titulo, columnas, datos, nombre_archivo):
    contexto = {
        'titulo': titulo,
        'columnas': columnas,
        'datos': datos,
        'logo_url': LOGO_PATH,
    }
    html_string = render_to_string('reportes/reporte_pdf.html', contexto)
    html_object = HTML(string=html_string, base_url='.')
    pdf_bytes = html_object.write_pdf()
    response = HttpResponse(pdf_bytes, content_type='application/pdf')
    response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}.pdf"'
    return response


def exportar_excel(titulo, columnas, datos, nombre_archivo):
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Reporte"

    title_font = Font(name='Arial', size=14, bold=True, color='FFFFFF')
    title_fill = PatternFill(start_color='366092', end_color='366092', fill_type='solid')
    title_alignment = Alignment(horizontal='center', vertical='center')

    worksheet.merge_cells('A1:' + chr(64 + len(columnas)) + '1')
    titulo_cell = worksheet['A1']
    titulo_cell.value = titulo
    titulo_cell.font = title_font
    titulo_cell.fill = title_fill
    titulo_cell.alignment = title_alignment
    worksheet.row_dimensions[1].height = 25

    header_font = Font(name='Arial', size=11, bold=True, color='FFFFFF')
    header_fill = PatternFill(start_color='4472C4', end_color='4472C4', fill_type='solid')
    header_alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)

    for col_num, columna in enumerate(columnas, 1):
        cell = worksheet.cell(row=3, column=col_num)
        cell.value = columna
        cell.font = header_font
        cell.fill = header_fill
        cell.alignment = header_alignment
    worksheet.row_dimensions[3].height = 20

    data_alignment = Alignment(horizontal='left', vertical='center')
    data_border = Border(
        left=Side(style='thin'), right=Side(style='thin'),
        top=Side(style='thin'), bottom=Side(style='thin')
    )
    data_fill_alternated = PatternFill(start_color='D9E1F2', end_color='D9E1F2', fill_type='solid')

    for row_num, fila in enumerate(datos, 4):
        if isinstance(fila, dict):
            valores = [fila.get(col.lower().replace(' ', '_'), '') for col in columnas]
        else:
            valores = fila
        for col_num, valor in enumerate(valores, 1):
            cell = worksheet.cell(row=row_num, column=col_num)
            cell.value = valor
            cell.alignment = data_alignment
            cell.border = data_border
            if (row_num - 4) % 2 == 0:
                cell.fill = data_fill_alternated

    for col_num, columna in enumerate(columnas, 1):
        max_length = len(str(columna))
        column_letter = chr(64 + col_num)
        for row in worksheet.iter_rows(min_col=col_num, max_col=col_num):
            for cell in row:
                try:
                    if cell.value:
                        max_length = max(max_length, len(str(cell.value)))
                except:
                    pass
        worksheet.column_dimensions[column_letter].width = max_length + 2

    response = HttpResponse(
        content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
    response['Content-Disposition'] = f'attachment; filename="{nombre_archivo}.xlsx"'
    workbook.save(response)
    return response
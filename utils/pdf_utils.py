"""
DriveBD - PDF generation helpers (ReportLab)
"""
import io
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.units import mm
from reportlab.platypus import SimpleDocTemplate, Table, TableStyle, Paragraph, Spacer
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle


def generate_receipt_pdf(title: str, fields: dict) -> bytes:
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=30 * mm, bottomMargin=20 * mm)
    styles = getSampleStyleSheet()
    header_style = ParagraphStyle("Header", parent=styles["Title"], textColor=colors.HexColor("#0B5FFF"))

    elements = [
        Paragraph("DriveBD", header_style),
        Paragraph("Smart Driver & Vehicle Owner Portal", styles["Normal"]),
        Spacer(1, 12),
        Paragraph(title, styles["Heading2"]),
        Spacer(1, 12),
    ]

    data = [[k, str(v)] for k, v in fields.items()]
    table = Table(data, colWidths=[160, 300])
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (0, -1), colors.HexColor("#F0F5FF")),
        ("GRID", (0, 0), (-1, -1), 0.5, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 10),
        ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
        ("PADDING", (0, 0), (-1, -1), 8),
    ]))
    elements.append(table)
    elements.append(Spacer(1, 24))
    elements.append(Paragraph("This is a system-generated document from DriveBD. No signature required.",
                               styles["Italic"]))

    doc.build(elements)
    buffer.seek(0)
    return buffer.read()


def generate_report_pdf(title: str, subtitle: str, df) -> bytes:
    """Generate a tabular report PDF from a pandas DataFrame."""
    buffer = io.BytesIO()
    doc = SimpleDocTemplate(buffer, pagesize=A4, topMargin=20 * mm)
    styles = getSampleStyleSheet()
    header_style = ParagraphStyle("Header", parent=styles["Title"], textColor=colors.HexColor("#0B5FFF"), fontSize=18)

    elements = [
        Paragraph("DriveBD", header_style),
        Paragraph(title, styles["Heading2"]),
        Paragraph(subtitle, styles["Normal"]),
        Spacer(1, 12),
    ]

    data = [list(df.columns)] + df.astype(str).values.tolist()
    table = Table(data, repeatRows=1)
    table.setStyle(TableStyle([
        ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#0B5FFF")),
        ("TEXTCOLOR", (0, 0), (-1, 0), colors.white),
        ("GRID", (0, 0), (-1, -1), 0.4, colors.grey),
        ("FONTSIZE", (0, 0), (-1, -1), 7),
        ("PADDING", (0, 0), (-1, -1), 4),
        ("ROWBACKGROUNDS", (0, 1), (-1, -1), [colors.white, colors.HexColor("#F5F8FF")]),
    ]))
    elements.append(table)

    doc.build(elements)
    buffer.seek(0)
    return buffer.read()

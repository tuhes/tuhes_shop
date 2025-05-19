import os
from io import BytesIO
from django.conf import settings
from reportlab.pdfgen import canvas
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.lib import colors
from reportlab.platypus import Table, TableStyle


def generate_order_pdf(order):
    font_path = os.path.join(settings.BASE_DIR, settings.PDF_ORDER_FONT)
    pdfmetrics.registerFont(TTFont('Artika', font_path))
    buffer = BytesIO()
    pdf = canvas.Canvas(buffer)

    pdf.setFont('Artika', 24)
    pdf.drawString(100, 750, "Детали заказа:")

    y_pos = 700
    pdf.setFont('Artika', 12)
    y_pos -= 20
    pdf.drawString(100, y_pos, f"Номер заказа: {order.id}")
    y_pos -= 20
    pdf.drawString(100, y_pos, f"Email: {order.email}")
    y_pos -= 20
    pdf.drawString(100, y_pos, f"Телефон: {order.phone}")
    y_pos -= 20
    pdf.drawString(100, y_pos, f"Дата создания: {order.created_at.strftime('%d.%m.%Y %H:%M')}")  # Format
    y_pos -= 20
    pdf.drawString(100, y_pos, f"Статус заказа: {order.status}")

    if order.coupon:
        y_pos -= 20
        pdf.drawString(100, y_pos, f"Цена до скидки: {order.get_total_cost()}")
        y_pos -= 20
        pdf.drawString(100, y_pos, f"Промокод: {order.coupon}")
        y_pos -= 20
        pdf.drawString(100, y_pos, f"Скидка: {order.get_discount()} ({order.discount}%)")

    y_pos -= 40

    data = [["Товар", "Цена", "Количество", "Сумма, руб."]]

    order_items = order.orderitem_set.all()
    for item in order_items:
        data.append([item.item.name, str(item.price), str(item.quantity), str(item.total_price())])

    data.append(["", "", "", f'{order.get_total_cost_with_discount()}'])

    table = Table(data, colWidths=[200, 80, 80, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0, 0), (-1, 0), colors.grey),
        ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),
        ('ALIGN', (0, 0), (-1, -1), 'CENTER'),
        ('FONTNAME', (0, 0), (-1, 0), 'Artika'),
        ('BOTTOMPADDING', (0, 0), (-1, 0), 12),
        ('BACKGROUND', (0, 1), (-1, -2), colors.beige),
        ('GRID', (0, 0), (-1, -1), 1, colors.black)
    ]))

    table_height = table.wrapOn(pdf, 0, 0)[1]
    y_pos -= table_height
    table.drawOn(pdf, 100, y_pos)

    y_pos -= 40

    pdf.setFont('Artika', 24)
    pdf.drawString(100, y_pos, "Tuhes SHOP")

    pdf.save()
    buffer.seek(0)
    return buffer
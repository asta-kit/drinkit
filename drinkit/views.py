from django.http import HttpResponse

from datetime import date

from reportlab.lib.pagesizes import A3, landscape
from reportlab.platypus import SimpleDocTemplate
from reportlab.platypus.paragraph import Paragraph
from reportlab.platypus.tables import Table, TableStyle
from reportlab.lib import colors
from reportlab.lib.enums import TA_JUSTIFY, TA_CENTER
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import inch

from .models import Drink, Drinker

# Set the right locale
import locale
locale.setlocale(locale.LC_ALL, 'de_DE.utf8')

# Styles
_normal_style = ParagraphStyle(name='Normal',
                               fontName='Helvetica',
                               fontSize=10,
                               leading=12)
_body_style = ParagraphStyle(name='BodyText',
                             parent=_normal_style,
                             spaceBefore=6,
                             alignment=TA_JUSTIFY,
                             language='DE',
                             hyphenation=True)
_h1_style = ParagraphStyle(name='Heading1',
                           parent=_normal_style,
                           fontName='Helvetica-Bold',
                           alignment=TA_CENTER,
                           fontSize=18,
                           leading=22,
                           spaceBefore=12,
                           spaceAfter=6)
_h2_style = ParagraphStyle(name='Heading2',
                           parent=_normal_style,
                           fontName='Helvetica-Bold',
                           fontSize=14,
                           leading=18,
                           spaceBefore=12,
                           spaceAfter=3)
_h3_style = ParagraphStyle(name='Heading3',
                           parent=_normal_style,
                           fontName='Helvetica-Oblique',
                           fontSize=12,
                           leading=14,
                           spaceBefore=12,
                           spaceAfter=6)
_table_header_style = ParagraphStyle(name='TableHeading',
                           parent=_normal_style,
                           fontName='Helvetica-Bold',
                           alignment=TA_CENTER,
                           fontSize=12,
                           leading=18,
                           spaceBefore=12,
                           spaceAfter=3)

def tally_sheet(request):
    # Create the HttpResponse object with the appropriate PDF headers.
    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="strichliste_{}.pdf"'.format(date.today())

    # Create the document object, using the response object as its "file."
    doc = SimpleDocTemplate(response,
        title='Getränkeliste vom {}'.format(date.today().strftime('%x')),
        pagesize=landscape(A3),
        leftMargin=inch/4,
        rightMargin=inch/4,
        topMargin=inch/4,
        bottomMargin=inch/4,
    )

    f = []

    f.append(Paragraph('Getränke-und-Schokolade-Kühlschrank', _h1_style))
    f.append(Paragraph('So funktioniert\'s: Getränk aus dem Kühlschrank nehmen und Geld in die Kasse auf dem Kühlschrank schmeißen. Wenn du öfter da bist, kannst du stattdessen auch deinen Namen <b>und E-Mail-Adresse</b> unten auf der Liste eintragen und dann einen Strich bei dem Getränk machen. Du bekommst dann bei der Abrechnung eine E-Mail und zahlst dann per Überweisung. Fragen oder Anregungen kannst du gerne an getraenke@asta-kit.de schicken.', _body_style))
    f.append(Paragraph('Liste aufgehängt am {}, und abgehängt am:'.format(date.today().strftime('%x')), _body_style))
    f.append(Paragraph('Bei 4 oder weniger Flaschen von einer Sorte, bitte den Kühlschrank auffüllen. Pro-Tipp: Namen auf die Flasche schreiben', _h2_style))

    header = [Paragraph('Name', _table_header_style)]
    name_col_width = 2*inch
    col_widths = [name_col_width]
    drinks = Drink.objects.filter(active=True)
    for drink in drinks:
        header.append(Paragraph('{}: {}'.format(drink.name, locale.currency(drink.price)), _table_header_style))
        col_widths.append((doc.width-name_col_width)/len(drinks))

    data = [header]
    drinkers = Drinker.objects.filter(active=True)
    for drinker in drinkers:
        data.append((Paragraph(str(drinker), _body_style),))

    row_heights = [None]
    row_heights.extend(len(drinkers)*[inch/3])

    table_style = TableStyle((
        ('GRID', (0,0), (-1,-1), 0.5, colors.black),
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), (colors.lightgrey, colors.white))
    ))
    f.append(Table(data, colWidths=col_widths, rowHeights=row_heights, style=table_style))


    f.append(Paragraph('Platz für neue Menschen (E-Mail-Adresse bitte nicht vergessen)', _h1_style))

    header = [
        Paragraph('Name', _table_header_style),
        Paragraph('E-Mail-Adresse (bitte lesbar schreiben)', _table_header_style),
    ]
    name_col_width = 2.5*inch
    email_col_width = 4*inch
    col_widths = [name_col_width, email_col_width]
    for drink in drinks:
        header.append(Paragraph('{}: {}'.format(drink.name, locale.currency(drink.price)), _table_header_style))
        col_widths.append((doc.width-name_col_width-email_col_width)/len(drinks))

    new_drinkers_len = 30

    data = [header]
    data.extend(new_drinkers_len*[tuple()])

    row_heights = [None]
    row_heights.extend(new_drinkers_len*[inch/3])

    f.append(Table(data, colWidths=col_widths, rowHeights=row_heights, style=table_style))

    doc.build(f)
    return response

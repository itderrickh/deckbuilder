from PyPDF2 import PdfFileWriter, PdfFileReader
import io
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from Models.CardSet import CardSet
import datetime
import os
from AppState.Session import ses

pdf_file_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'pdfgen')
def write_to_pdf(cards, user, outputPDF):
    bd = user.dateofbirth
    pokemon = [x for x in cards if x.type == 'Pok\u00e9mon']
    trainers = [x for x in cards if x.type == 'Trainer Cards']
    energy = [x for x in cards if x.type == 'Energy']
    pksum = sum(c.count for c in pokemon)
    tcsum = sum(c.count for c in trainers)
    ensum = sum(c.count for c in energy)
    cardSets = [x.setName for x in cards]
    setLists = ses.query(CardSet).filter(CardSet.setName in cardSets)
    standard_legal = all(x.standard for x in setLists)

    if standard_legal:
        print("THIS DECK IS DEFINITELY STANDARD LEGAL")
    else:
        print("MAYBE NOT STANDARD LEGAL")
    packet = io.BytesIO()
    # create a new PDF with Reportlab
    can = canvas.Canvas(packet, pagesize=letter)

    # Name and ID
    can.drawString(93, 687, user.name)
    can.drawString(281, 687, user.playerid)

    # Bday
    can.drawString(495, 687, str(bd.month))
    can.drawString(522, 687, str(bd.day))
    can.drawString(547, 687, str(bd.year))

    if bd.year <= 2002:
        # Masters
        can.drawString(375, 640, "x")
    elif bd.year >= 2003 and bd.year <= 2006:
        # Seniors
        can.drawString(375, 654, "x")
    else:
        # Juniors
        can.drawString(375, 667, "x")

    # Pokemon
    for i in list(range(0, len(pokemon))):
        # Count
        can.drawString(286, 586 - (i * 13.2), str(pokemon[i].count))
        # Name
        can.drawString(320, 586 - (i * 13.2), pokemon[i].name)
        # Set
        can.drawString(486, 586 - (i * 13.2), pokemon[i].setName)
        # Number
        can.drawString(534, 586 - (i * 13.2), pokemon[i].number)

    # Trainers
    for i in list(range(0, len(trainers))):
        can.drawString(286, 410 - (i * 13.2), str(trainers[i].count))
        can.drawString(320, 410 - (i * 13.2), trainers[i].name)

    # Energy
    for i in list(range(0, len(energy))):
        can.drawString(286, 128 - (i * 13.2), str(energy[i].count))
        can.drawString(320, 128 - (i * 13.2), energy[i].name)

    can.save()

    #move to the beginning of the StringIO buffer
    packet.seek(0)
    new_pdf = PdfFileReader(packet)
    # read your existing PDF
    existing_pdf = PdfFileReader(open("pokemon_list.pdf", "rb"))
    output = PdfFileWriter()
    # add the "watermark" (which is the new pdf) on the existing page
    page = existing_pdf.getPage(0)
    page.mergePage(new_pdf.getPage(0))
    output.addPage(page)
    # finally, write "output" to a real file
    outputStream = open(os.path.join(pdf_file_dir, outputPDF), "wb")
    output.write(outputStream)
    outputStream.close()
    return outputPDF
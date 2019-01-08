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
    warnings = list()
    bd = user.dateofbirth
    pokemon = [x for x in cards if x.type == 'Pok\u00e9mon']
    trainers = [x for x in cards if x.type == 'Trainer']
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
    can.drawString(98, 697, user.name)
    can.drawString(291, 697, user.playerid)

    # Bday
    can.drawString(505, 697, str(bd.month))
    can.drawString(532, 697, str(bd.day))
    can.drawString(557, 697, str(bd.year))

    if bd.year <= 2002:
        # Masters
        can.drawString(385, 650, "x")
    elif bd.year >= 2003 and bd.year <= 2006:
        # Seniors
        can.drawString(385, 664, "x")
    else:
        # Juniors
        can.drawString(385, 677, "x")

    # Pokemon
    if(len(pokemon) > 10):
        warnings.append("Not all the pokemon could fit. Please review and add cards accordingly.")

    maxPokemon = min(len(pokemon), 10)
    for i in list(range(0, maxPokemon)):
        # Count
        can.drawString(291, 595 - (i * 13.2), str(pokemon[i].count))
        # Name
        can.drawString(325, 595 - (i * 13.2), pokemon[i].name)
        # Set
        can.drawString(491, 595 - (i * 13.2), pokemon[i].setName)
        # Number
        can.drawString(539, 595 - (i * 13.2), pokemon[i].number)

    # Trainers
    if(len(trainers) > 18):
        warnings.append("Not all the trainers could fit. Please review and add cards accordingly.")

    maxtrainers = min(len(trainers), 18)
    for i in list(range(0, maxtrainers)):
        can.drawString(291, 419 - (i * 13.2), str(trainers[i].count))
        can.drawString(325, 419 - (i * 13.2), trainers[i].name)

    # Energy
    if(len(energy) > 18):
        warnings.append("Not all the energy could fit. Please review and add cards accordingly.")

    maxenergy = min(len(energy), 4)
    for i in list(range(0, maxenergy)):
        can.drawString(286, 137 - (i * 13.2), str(energy[i].count))
        can.drawString(320, 137 - (i * 13.2), energy[i].name)

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
    return outputPDF, warnings
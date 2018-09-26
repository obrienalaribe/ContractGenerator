from docx import Document
import datetime
import subprocess

def replace_token(name, quote, date, venue):
    doc = Document('Wedding_Contract_Template.docx')
    for p in doc.paragraphs:
        inline = p.runs
        for i in range(len(inline)):
            text = inline[i].text.replace('<<CLIENT>>', name)
            inline[i].text = text

            text = inline[i].text.replace('<<QUOTE>>', quote)
            inline[i].text = text

            text = inline[i].text.replace('<<DATE>>', date)
            inline[i].text = text

            text = inline[i].text.replace('<<DEPOSIT>>', "100")
            inline[i].text = text

            text = inline[i].text.replace('<<FINAL>>', str(int(quote) - 100))
            inline[i].text = text

            text = inline[i].text.replace('<<VENUE>>', venue)
            inline[i].text = text

            text = inline[i].text.replace('<<NOW>>', str(datetime.datetime.now())[:10])
            inline[i].text = text

    doc.save('Wedding_Contract(' + name + ').docx')
    # subprocess.call(['soffice', '--headless', '--convert-to', 'txt:Text', 'document_to_convert.doc'])

    return 1

replace_token('Kelly Lebaga', "450", "Sunday 12th November 2018", "Syon Park")



# wdFormatPDF = 17


#
# doc.SaveAs(out_file, FileFormat=wdFormatPDF)
# doc.Close()
# word.Quit()
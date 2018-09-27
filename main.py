from docx import Document
import datetime
import boto3
import os
import logging
import uuid
import json
import quote

def lambda_handler(event, context):
    name    =   event['name']
    quote   =   int(os.environ['QUOTE'])
    deposit =   int(os.environ['DEPOSIT'])
    date    =   event['date']
    venue   =   event['venue']
    postcode =  event['postcode']
    email   =   event['email']

    test = calculate()

    logging.info('Received ' + json.dumps(event) )
    filename = generate_contract(name, quote, deposit, date, venue)
    # upload_to_s3(filename)
    # save_to_db(name, email, quote, deposit, date, venue, postcode)
    return

def upload_to_s3(filename):
    s3 = boto3.client('s3')
    bucket_name = os.environ['BUCKET_NAME']
    s3.upload_file(filename, bucket_name, filename)
    logging.info("Uploaded Contract to S3 ...")
    return

def save_to_db(name, email, quote, deposit, date, venue, postcode):
    recordId = str(uuid.uuid4())
    dynamodb = boto3.resource('dynamodb', region_name='eu-west-1')
    table = dynamodb.Table(os.environ['DB_TABLE_NAME'])
    table.put_item(
        Item={
            'id' : recordId,
            'name' : name,
            'email' : email,
            'quote': quote,
            'deposit': deposit,
            'venue' : venue,
            'postcode': postcode,
            'status' : 'REQUEST',
            'date': date
        }
    )
    logging.info("Saved to DB ...")
    return

def generate_contract(name, quote, deposit, date, venue):
    doc = Document('Wedding_Contract_Template.docx')
    for p in doc.paragraphs:
        inline = p.runs
        for i in range(len(inline)):
            text = inline[i].text.replace('<<CLIENT>>', name)
            inline[i].text = text

            text = inline[i].text.replace('<<QUOTE>>', str(quote))
            inline[i].text = text

            text = inline[i].text.replace('<<DATE>>', date)
            inline[i].text = text

            text = inline[i].text.replace('<<DEPOSIT>>', str(deposit))
            inline[i].text = text

            text = inline[i].text.replace('<<FINAL>>', str(quote - deposit))
            inline[i].text = text

            text = inline[i].text.replace('<<VENUE>>', venue)
            inline[i].text = text

            text = inline[i].text.replace('<<NOW>>', str(datetime.datetime.now())[:10])
            inline[i].text = text

    doc_name = 'Wedding_Contract(' + name + ').docx'
    doc.save(doc_name)
    logging.info("Contracted Generated ...")
    # subprocess.call(['soffice', '--headless', '--convert-to', 'txt:Text', 'document_to_convert.doc'])

    return doc_name

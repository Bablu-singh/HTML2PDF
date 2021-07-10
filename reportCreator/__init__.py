import logging
import os
from xhtml2pdf import pisa
import azure.functions as func
import time;
from pathlib import Path
from calendar import timegm
from azure.storage.blob import BlobServiceClient, __version__

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Python HTTP trigger function processed a request.')
    
    timeS = time.strftime("%Y-%m-%d %H:%M:%S",time.gmtime(time.time()))
    epoc_time = timegm(time.strptime(timeS, "%Y-%m-%d %H:%M:%S"))
    fileName = "report"+str(epoc_time)+".pdf"
    
    connection_string = os.environ["STORAGE_CONNECTION"]
    data= str(Path.home()) + "/data"
    
    body = req.get_json()
    source = body['report']
    
    output = data+"report.pdf"

    result = open(output,"w+b")
    
    pisa.CreatePDF(source.encode('utf-8'), dest=result, encoding='utf-8')
    
    result.close()
    
    

    blob_service_client = BlobServiceClient.from_connection_string(connection_string)
    blob_client = blob_service_client.get_blob_client(container="files", blob=fileName)
    
    if result:
        logging.info("Successfully created PDF")
    else:
        logging.error("Error: unable to create the PDF")    
    
    with open(output, "r+b") as pdf_file:
        encoded_string = pdf_file.read()
        # blob_client.upload_blob(encoded_string)
    
    # response_headers = {"Content-Disposition": 'attachment;filename="report.pdf"'}
    return func.HttpResponse(fileName,status_code=200, headers=None, mimetype=None, charset=None)

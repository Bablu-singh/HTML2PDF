const pdf = require('html-pdf');
const base64 = require('base64topdf');
const path = require('path');

const { BlobServiceClient } = require('@azure/storage-blob');
const { v1: uuidv1} = require('uuid');


module.exports = async function (context, req) {
    /** insert your connction string here    
    
    const AZURE_STORAGE_CONNECTION_STRING =CONNECTION_STRING;
    
    */
    const blobServiceClient = BlobServiceClient.fromConnectionString(AZURE_STORAGE_CONNECTION_STRING);
    const containerClient = blobServiceClient.getContainerClient('files');


    
    
    const html = req.body?.report;
    var data = await reeturnHtmlAsPdf(html);
    const timeStamp =Date.now();
    const fileName  = "report"+timeStamp+".pdf";
   
    const blockBlobClient = containerClient.getBlockBlobClient(fileName);
   
    await blockBlobClient.upload(data, data.length);
    
    context.res={
        body: fileName,
        status:200,
        'Content-Type':'text/plain-text'
    }
    context.done();
}
const reeturnHtmlAsPdf =  async (html) =>{
    
    return new Promise((resolve,reject) => {
        pdf.create(html,{  type: 'pdf', timeout: '100000' }).toBuffer((err, buffer) =>{
            if(err){
                reject(err);
            }
            resolve(buffer);
        })
    });
}
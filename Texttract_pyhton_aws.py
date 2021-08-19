def def11(text):
  import boto3
  import time
  # Amazon Comprehend client
  comprehend = boto3.client('comprehend')
  sentiment =  comprehend.detect_sentiment(LanguageCode="en", Text=text)
  print ("\nSentiment\n========\n{}".format(sentiment.get('Sentiment')))

def def22(text):
  import boto3
  import time
  comprehend = boto3.client('comprehend')
  entities =  comprehend.detect_entities(LanguageCode="en", Text=text)
  print("\nEntities\n========")
  for entity in entities["Entities"]:
   print ("{}\t=>\t{}".format(entity["Type"], entity["Text"]))

def def33(text):
  import boto3
  import time
  comprehend = boto3.client('comprehend')
  entities =  comprehend.detect_pii_entities(LanguageCode="en", Text=text)
  print("\nEntities\n========")
  for entity in entities["Entities"]:
    print (entity)
   #print ("{}\t=>\t{}".format(entity["Type"], entity["Text"]))

def def44(text):
  import boto3
  import time
  comprehend = boto3.client('comprehend')
  response=comprehend.classify_document(Text=text,EndpointArn='arn:aws:comprehend:us-east-1:749669622883:document-classifier-endpoint/CCP2')
  print("\n response\n========" , response)
 # for entity in entities["Entities"]:
  #  print (entity)
   #print ("{}\t=>\t{}".format(entity["Type"], entity["Text"]))

def def1(): 
 import boto3
 import time
 def startJob(s3BucketName, objectName):
  response = None
  client = boto3.client('textract')
  response = client.start_document_text_detection(
  DocumentLocation={
  'S3Object': {
  'Bucket': s3BucketName,
  'Name': objectName
  }
  })
  return response["JobId"]
 def isJobComplete(jobId):
  # For production use cases, use SNS based notification 
  # Details at: https://docs.aws.amazon.com/textract/latest/dg/api-async.html
  time.sleep(5)
  client = boto3.client('textract')
  response = client.get_document_text_detection(JobId=jobId)
  status = response["JobStatus"]
  print("Job status: {}".format(status))
  while(status == "IN_PROGRESS"):
   time.sleep(5)
   response = client.get_document_text_detection(JobId=jobId)
   status = response["JobStatus"]
   print("Job status: {}".format(status))
  return status
 def getJobResults(jobId):
  pages = []
  client = boto3.client('textract')
  response = client.get_document_text_detection(JobId=jobId)
  pages.append(response)
  print("Resultset page recieved: {}".format(len(pages)))
  nextToken = None
  if('NextToken' in response):
   nextToken = response['NextToken']
  while(nextToken):
   response = client.get_document_text_detection(JobId=jobId, NextToken=nextToken)
   pages.append(response)
   print("Resultset page recieved: {}".format(len(pages)))
   nextToken = None
   if('NextToken' in response):
    nextToken = response['NextToken']
  return pages
 # Document
 s3= boto3.resource('s3')
 cont=1
 filename1=""
 bucket= s3.Bucket('ocr-12345')
 for obj in bucket.objects.all():
  filename1="outputt.txt"
  filename="".join((filename1,str(cont)))
  print( filename )
  cont=cont+1
  s3BucketName = "ocr-12345"
  key= obj.key
  #documentName = "employmentapp.png"
  jobId = startJob(s3BucketName, key)
  print("Started job with id: {}".format(jobId))
  if(isJobComplete(jobId)):
   response = getJobResults(jobId)
  #print(response)
  # Print detected text
  text = ""
  for resultPage in response:
    for item in resultPage["Blocks"]:
     if item["BlockType"] == "LINE":
      print ('\033[94m' + item["Text"] + '\033[0m')
      text = text + " " + item["Text"]
    print (text)
    with open(f'{filename}','w') as f:
     f.write(text)
     f.close()
  i=input("Enter the options for Text Detection   - \n 1. Type 1 for Sentiment analysis \n 2. Type 2 for Entities detection in text  \n 3. Type 3 for Getting Pearson Identification Values \n 4. To classify document using custom classifier \n :")
  print ( "input recived  " ,i)
  def pattern(i):
        switcher={
                '1': 'def11',
                '2': 'def22',
                '3': 'def33',
                '4': 'def44'
             }
        return switcher.get(i)
  TOcall=pattern(i)
  print ( "calling function " ,TOcall)
  globals()[TOcall](text)

def def2():
 #from subprocess import call
 #call(["python", "Texract_Keyvalue.py"])
 import boto3
 from trp import Document
 # Document
 s3BucketName = "ocr-12345"
 s3= boto3.resource('s3')
 bucket= s3.Bucket('ocr-12345')
 for obj in bucket.objects.all():
  s3BucketName = "ocr-12345"
  key= obj.key
  #documentName = "BankStatementChequing.png"
  # Amazon Textract client
  textract = boto3.client('textract')
  # Call Amazon Textract
  response = textract.analyze_document(
   Document={
   'S3Object': {
   'Bucket': s3BucketName,
   'Name': key
   }
   },
   FeatureTypes=["FORMS"])
  #print(response)
  doc = Document(response)
  for page in doc.pages:
   # Print fields
   print("Fields:")
   for field in page.form.fields:
    print("Key: {}, Value: {}".format(field.key, field.value))
  # Get field by key
   print("\nGet Field by Key:")
   key = "Phone Number:"
   field = page.form.getFieldByKey(key)
   if(field):
    print("Key: {}, Value: {}".format(field.key, field.value))
  # Search fields by key
   print("\nSearch Fields:")
   key = "address"
   fields = page.form.searchFieldsByKey(key)
   for field in fields:
    print("Key: {}, Value: {}".format(field.key, field.value))

def def3():
 import boto3
 from trp import Document
 # Document
 s3BucketName = "ocr-12345"
 #documentName = "employmentapp.png"
 # Amazon Textract client
 s3= boto3.resource('s3')
 bucket= s3.Bucket('ocr-12345')
 for obj in bucket.objects.all():
  s3BucketName = "ocr-12345"
  key= obj.key
  textract = boto3.client('textract')
  # Call Amazon Textract
  response = textract.analyze_document(
   Document={
   'S3Object': {
   'Bucket': s3BucketName,
   'Name': key
   }
   },
   FeatureTypes=["TABLES"])
  #print(response)
  doc = Document(response)
  def isFloat(input):
   try:
    float(input)
   except ValueError:
    return False
    return True
  warning = ""
  for page in doc.pages:
   # Print tables
   for table in page.tables:
    for r, row in enumerate(table.rows):
     itemName = ""
     for c, cell in enumerate(row.cells):
      print("Table[{}][{}] = {}".format(r, c, cell.text))
      if(c == 0):
       itemName = cell.text
      elif(c == 4 and isFloat(cell.text)):
       value = float(cell.text)
       if(value > 1000):
        warning += "{} is greater than $1000.".format(itemName)
        if(warning):
         print("\nReview needed:\n====================\n" + warning)

### Main Processing Start Here ####
 
i=input("Enter the options for OCR - \n 1. Type 1 for text analysis \n 2. Type 2 for Found key and Pair value in document metadata \n 3. Type 3 for OCR to find table in metadata\n :")
print ( "input recived  " ,i) 
def pattern(i):
        switcher={
                '1': 'def1',
                '2': 'def2',
                '3': 'def3'
             }
        return switcher.get(i) 
tocall=pattern(i)
print ( "calling function " ,tocall)
globals()[tocall]()

# Libreries

import os
#from flask import Flask, render_template, request
#from werkzeug.utils import secure_filename
import cups
from flask import Flask, flash, request, redirect, url_for, render_template
from werkzeug.utils import secure_filename
import PyPDF2
import glob

#Variables
UPLOAD_FOLDER = 'static/uploads/'



# Initialing API
app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# # Calling principal html index
# @app.route("/")
# def hello():
#    now = datetime.datetime.now()
#    timeString = now.strftime("%Y-%m-%d %H:%M")
#    templateData = {
#       'title' : 'HELLO!',
#       'time': timeString
#       }
#    return render_template('index.html', **templateData)

# @app.route('/upload')
# def upload_file():
#    return render_template('index.html')

# # Printing after uploading the file	
# @app.route('/Send', methods = ['GET', 'POST'])
# def send_file():
#    print("Send")
#    if request.method == 'POST':
#       f = request.files['file']
#       f.save(secure_filename(f.filename))
#       # conn = cups.Connection ()
#       # printers = conn.getPrinters ()
#       # for printer in printers:
#       #    print (printer, printers[printer]["device-uri"])
#       #    printer_name=printer
#       # print(f.filename)
#       # file =f.filename
#       # conn.printFile (printer_name, file, "Project Report", {})  
#       return render_template('send.html')

#Formats of files allowed to print
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', 'pdf'])

def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

#Display the main page
@app.route('/')
def upload_form():
	return render_template('upload.html')

#Display and do a Post in the API for choosing the file
@app.route('/', methods=['POST'])
def upload_image():
	if 'file' not in request.files:
		flash('No file part')
		return redirect(request.url)
	file = request.files['file']
	if file.filename == '':
		flash('No ha seleccionado archivo')
		return redirect(request.url)
	if file and allowed_file(file.filename):
		filename = secure_filename(file.filename)
		file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

		if filename.rsplit('.', 1)[1].lower() == 'pdf':
			filepdf='static/uploads/'+filename
			file2 = open(filepdf, 'rb')
			readpdf = PyPDF2.PdfFileReader(file2)
			totalpages = readpdf.numPages
			sizeFileV = readpdf.getPage(0).mediaBox
			if sizeFileV[2]>612:
			   sizeFile="Oficio"
			else:
			   sizeFile="Carta"	
		else:
			totalpages = 1
			sizeFile="Carta"	
		print("total pages",totalpages)
		flash('Imagen cargada exitosamente')

		return render_template('pay.html', filename=filename,totalpages=totalpages, sizeFile=sizeFile)
	else:
		flash('Formato del documento no admitido')
		return redirect(request.url)
	
	
#Function to display file
@app.route('/display/<filename>')
def display_image(filename):
	#print('display_image filename: ' + filename)
	return redirect(url_for('static', filename='uploads/' + filename), code=301)

# # Printing after uploading the file	
@app.route('/payProcess/<filename>', methods=['GET','POST'])
def pay(filename):
   color=request.form.get('color')
   numCopies=str(request.form.get('numCopies'))
   pages=request.form.get('pages')
	
   print(color)
   print(numCopies)
   print(pages)
   if request.method == 'POST':
	   #f = request.files['file']
	   #f.save(secure_filename(f.filename))
	   conn = cups.Connection ()
	   printers = conn.getPrinters ()
	   for printer in printers:
		   #print (printer, printers[printer]["device-uri"])
		   #print(printer)
		   printer_name=printer
	   #print("printer:"+printer_name)
	   #file =f.filename
	   file="static/uploads/"+filename
	   print(file)
	   #if pages=="":

	 	   #conn.printFile (printer_name, filename, "Project Report", {})    
	 	   #conn.printFile (printer_name, filename, "Project Report", {"print-color-mode":"monochrome","copies":"1","sides":"two-sided-long-edge"})  
	 	   #conn.printFile (printer_name, file, "Project Report", {"print-color-mode":color,"copies":numCopies,"sides":"one-sided"}) 
	   #else:
	 	   #conn.printFile (printer_name, file, "Project Report", {"print-color-mode":color,"copies":numCopies,"sides":"one-sided","page-ranges":pages}) 
   
   #Removing files after print
   filesRemove=glob.glob('static/uploads/*')
   for f in filesRemove:
	   os.remove(f)

   
   return render_template('payProcess.html')

# Connecting to the localhost
if __name__ == '__main__':
   
   app.run(debug=True, port=3002, host='192.168.1.15')
   #app.run(debug=True, port=3003, host='127.0.0.2')
   
   #app.config['SERVER_NAME']= "printexp.dev:3003"
   #app.url_map.host_matching=True
   #app.run(debug=True, host='printexp.dev:3003')
   
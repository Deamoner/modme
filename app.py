from flask import Flask, request, render_template, send_from_directory, redirect
from privyfilter.privyfilter import Privyfilter as pf
import cv2
import tempfile
import uuid

app = Flask(__name__)

ALLOWED_EXTENSIONS = { 'jpg', 'jpeg'}
def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


######################## Routes ############################################
#server index template
@app.route('/')
def index():
    return render_template('index.html')


#serve static files
@app.route('/public/<path:path>')
def send_pulic(path):
    return send_from_directory('public', path)


@app.route('/uploader', methods = ['POST'])
def upload_file():
   #print(request.files)
   print(request.values)
   if request.files:
       print("got to files existing")
   if request.method == 'GET':
       print("we are making get requests")
   if request.method == 'POST':
      if request.files:
         f = request.files['fileToUpload']
         if f and allowed_file(f.filename):
             id = uuid.uuid1()
             filefullname = f.filename
             handle, filename = tempfile.mkstemp()
             f.save(filename + filefullname)
             print(filename + filefullname)
             swapimg = pf.swapFaces(filename + filefullname, "./assets/trump1.jpg")
             here = cv2.imwrite("./public/results/" + id.hex + ".jpg", swapimg)
             return redirect("../public/results/" + id.hex + ".jpg")
   return "Uploaded file successfully."

if __name__ == '__main__': app.run(debug=True)

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
   if request.method == 'POST':
      if request.files:
         f = request.files['fileToUpload']
         if f and allowed_file(f.filename):
             id = uuid.uuid1()
             filefullname = f.filename
             handle, filename = tempfile.mkstemp()
             try:
                 f.save(filename + filefullname)
                 print(filename + filefullname)
             except:
                print(filename + filefullname)
                print("Error occured saving file to tmp")
                return "Bad upload Save"
             try:
                 swapimg = pf.swapFaces(filename + filefullname, "./assets/china1.jpg")
                 here = cv2.imwrite("./public/results/" + id.hex + ".jpg", swapimg)
                 return redirect("../public/results/" + id.hex + ".jpg")
             except:
                 print("Bad face swapping. ")
                 return "Bad Face Swap"
   return "Uploaded file successfully."

if __name__ == '__main__': app.run(debug=True)

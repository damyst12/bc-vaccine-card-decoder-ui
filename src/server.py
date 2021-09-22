import os
from PIL import Image
import zbarlight
from decode_utils import extract_payload, to_yaml_str
from flask import Flask, request, Response, redirect, url_for, abort

def decode(file_path):
  with open(file_path, 'rb') as image_file:
    image = Image.open(image_file)
    image.load()

  codes = zbarlight.scan_codes(['qrcode'], image)
  if not codes:
    return 'Could not detect a QR code in this image'
  payload = extract_payload(codes[0].decode('utf-8'))
  return to_yaml_str(payload)

app = Flask(__name__)
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024
app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png']

HTML_TEMPLATE = """
<!doctype html>
<html>
  <head>
    <meta name="viewport" content="width=device-width, initial-scale=1">
    <title>B.C. vaccine card decoder</title>
  </head>
  <body style="background-color: #222244; color: #eeeeee; font-family: Arial,sans-serif; font-size: 16px">
    <div style="padding: 10px">
      <h1>B.C. vaccine card decoder</h1>
      <p>
        Upload an image of your vaccine card QR code to see the information contained within.
        <br/>
        <br/>
        The "vaccineCode" field specifies which type of vaccine was administered.
        See <a style="color: #ffffff" target="_blank" rel="noreferrer"
        href="https://www.cdc.gov/vaccines/programs/iis/COVID-19-related-codes.html">this page</a> for a table
        of vaccine products and their codes.
        <br/>
        <br/>
        The image and data are removed from our server immediately, and are not stored or sent anywhere else.
        <br/>
        <br/>
        Disclaimer: this page is not affiliated with the Province of British Columbia. We make no guarantees as to the
        correctness of the data displayed. Use at your own risk.
      </p>
      <form method="POST" action="" enctype="multipart/form-data" id="form" style="margin-top: 2rem; margin-bottom: 2rem">
        <label for="fileinput" style="background-color: #ffffff; color: #222244; border-radius: 6px; padding: 0.7rem">
          Choose File
        </label>
        <input id="fileinput" type="file" name="file" style="display: none" onchange="form.submit()">
      </form>
      <pre style="font-size: 0.8rem">{data}</pre>
    </div>
  </body>
</html>
"""

@app.route('/')
def index():
  return HTML_TEMPLATE.format(data='')

@app.route('/', methods=['POST'])
def upload_file():
    extensions = app.config['UPLOAD_EXTENSIONS']
    uploaded_file = request.files['file']
    filename = uploaded_file.filename
    if filename == '':
      return redirect(url_for('index'))

    file_ext = os.path.splitext(filename)[1]
    if file_ext not in extensions:
      abort(Response(f'Invalid input file - extension must be one of {", ".join(extensions)}'))

    save_path = f'./image.{file_ext}'
    uploaded_file.save(save_path)
    decoded_data = decode(save_path)
    os.remove(save_path)
    return HTML_TEMPLATE.format(data=decoded_data)

def main():
  app.run(host='0.0.0.0', port=8080)

main()

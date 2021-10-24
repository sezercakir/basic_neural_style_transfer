# Flask related libraries
import imghdr
import os

from flask import Flask, render_template, request, redirect, url_for, abort, send_from_directory

from torchvision.transforms.functional import normalize

from werkzeug.utils import secure_filename
import io
import base64
from style import *

# Create Flask app
app = Flask(__name__, static_folder = "static")

# Flask file configurations

app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif','.jpeg']

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0) 
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

def image_preprocessing(uploaded_file):
    style_img = Image.open(uploaded_file[0].stream)
    content_img = Image.open(uploaded_file[1].stream)
    image_style = style_img.resize((imsize,imsize),Image.ANTIALIAS)
    pil_to_tensor_Style = transforms.ToTensor()(image_style).unsqueeze_(0)
    image = content_img.resize((imsize,imsize),Image.ANTIALIAS)
    pil_to_tensor = transforms.ToTensor()(image).unsqueeze_(0)
    content_img = pil_to_tensor
    style_img = pil_to_tensor_Style
    input_img = content_img.clone()
    print(content_img.size(),style_img.size())
    return input_img, content_img, style_img

# to keep names of uploaded files
files = []
print()
@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_files():
    try:
        # get uploaded files
        uploaded_file = request.files['file'],request.files['file2']

        #preprocessing images and runnig model
        input_img, content_img, style_img = image_preprocessing(uploaded_file)
        assert style_img.size() == content_img.size(), \
            "we need to import style and content images of the same size"
        output = run_style_transfer(model_imported, cnn_normalization_mean, cnn_normalization_std,
                                content_img, style_img, input_img)

        # pytorch tensor image convert to PIL image and prepare for html input
        output_pil_Image = transforms.ToPILImage()(output.squeeze())
        image_file = io.BytesIO()
        output_pil_Image.save(image_file,'JPEG')
        encoded_img_data = base64.b64encode(image_file.getvalue()) 
        files.append(encoded_img_data.decode('utf-8'))

        return render_template('index.html',  files=files[0])
    except:
      return render_template('error.html')
    
# Run app
if __name__ == "__main__":
    app.run(debug=True)
    
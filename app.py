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
app = Flask(__name__)

# Flask file configurations

app.config['UPLOAD_EXTENSIONS'] = ['.jpg', '.png', '.gif']
app.config['UPLOAD_PATH'] = 'uploads'

# to keep names of uploaded files
files = []

def validate_image(stream):
    header = stream.read(512)
    stream.seek(0) 
    format = imghdr.what(None, header)
    if not format:
        return None
    return '.' + (format if format != 'jpeg' else 'jpg')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/', methods=['POST'])
def upload_files():
    # get uploaded file
    uploaded_file = request.files['file'],request.files['file2']

    # rename securely
    filename = secure_filename(uploaded_file[0].filename),secure_filename(uploaded_file[1].filename)

    if filename[0] != '' or filename[1]!='':
        file_ext = os.path.splitext(filename[0])[1],os.path.splitext(filename[1])[1]

        if file_ext[0] not in app.config['UPLOAD_EXTENSIONS'] or \
                file_ext[1] not in app.config['UPLOAD_EXTENSIONS'] or \
                file_ext[0] != validate_image(uploaded_file[0].stream) or \
                file_ext[1] != validate_image(uploaded_file[1].stream):
            abort(400)
        
    
    # Read uploaded image as numpy array
    #image = np.array(Image.open(uploaded_file[0].stream)),np.array(Image.open(uploaded_file[1].stream))
    style_img = Image.open(uploaded_file[0].stream)
    content_img = Image.open(uploaded_file[1].stream)
    image_style = style_img.resize((imsize,imsize),Image.ANTIALIAS)
    pil_to_tensor_Style = transforms.ToTensor()(image_style).unsqueeze_(0)
    image = content_img.resize((imsize,imsize),Image.ANTIALIAS)
    pil_to_tensor = transforms.ToTensor()(image).unsqueeze_(0)
    content_img = pil_to_tensor
    style_img = pil_to_tensor_Style
    input_img = content_img.clone()
    output = run_style_transfer(cnn, cnn_normalization_mean, cnn_normalization_std,
                            content_img, style_img, input_img)
    #output_filename = "output.jpg"
    
    
    
    output_pil_Image = transforms.ToPILImage()(output.squeeze())
    assert style_img.size() == content_img.size(), \
        "we need to import style and content images of the same size"
    image_file = io.BytesIO()
    output_pil_Image.save(image_file,'JPEG')
    encoded_img_data = base64.b64encode(image_file.getvalue()) 
    #files.append(output)'%s/real_samples.png' % image_dir,
    # add uploaded filename
    files.append(encoded_img_data.decode('utf-8'))
    
    return render_template('index.html',  files=files[0])

@app.route('/uploads/<filename>')
def upload(filename):
    return send_from_directory(app.config['UPLOAD_PATH'], filename)


# Run app
if __name__ == "__main__":
    app.run(debug=True)
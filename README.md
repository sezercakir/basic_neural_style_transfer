# Basic Nural Style Transfer Image Generator

This repo is a simple style transfer naive project with pytorch framework. 

## Description

In field of style transfer input style image and content image are given to model as inputs. The images are sent ot model after image preprocesing where size and format of images are controlled.
Some tensor to PIL image and PIL image to tensor image conversions are applied on images and lastly output image data send to main html document via flask backend. 
Unfortunately, I have noticed that heroku timeout config are set as 30 second and it couldnt change at the end of the story :/ 

## Model

The vgg19 model, whose architecture is specified in the picture below, is used.
<br>
### Architecture
<img alt="vgg19" src="https://github.com/sezercakir/basic_neural_style_transfer/blob/master/images/vgg.png?raw=true" width="500px">
<br>

## Results
App avaliable at [here](https://style-transfer-with-pytorch.herokuapp.com/) with many outputs. 

### Some Fantastic Outputs

<img alt="output" src="https://github.com/sezercakir/basic_neural_style_transfer/blob/master/images/dicaprio.jpg?raw=true" width="500px">
<br>

<img alt="output" src="https://github.com/sezercakir/basic_neural_style_transfer/blob/master/images/london_eye.jpg?raw=true" width="500px">
<br>





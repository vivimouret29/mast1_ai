# Running the convert script  

First we convert the .weights into the corresponding TensorFlow model which will be saved to a checkpoints folder.  

# Convert darknet weights to tensorflow model

```bash
export PYTHONPATH="${PYTHONPATH}:the_project_location"
python convert_weights/tools/save_model.py --model yolov4 
```
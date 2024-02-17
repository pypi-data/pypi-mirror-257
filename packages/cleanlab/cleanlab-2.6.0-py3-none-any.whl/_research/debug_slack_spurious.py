import pandas as pd 
import numpy as np 
from datasets import Dataset 
import random 
from PIL import Image
from cleanlab import Datalab

dark_images = [Image.new("RGB", (32, 32),(random.randint(0,127), random.randint(0,127), random.randint(0,127)))] * 10 
light_images = [Image.new("RGB", (32, 32),(random.randint(127,255), random.randint(127,255), random.randint(127,255)))] * 10
rand_images = (np.random.rand(100, 32, 32, 3) * 255).astype(np.uint8)
images = dark_images + light_images + [Image.fromarray(img) for img in rand_images]
labels = np.array([0] * 10 + [1] * 10 + [2] * 100)
data = {
    "image" : images, 
    "label" : labels
}
dataset = Dataset.from_dict(data)
lab = Datalab(data=dataset, label_name="label", image_key="image")
lab.find_issues()
lab.issue_summary     ## dark = 10, all the other image properties = 0 
lab._spurious_correlations()
from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from azure.cognitiveservices.vision.computervision.models import VisualFeatureTypes
from msrest.authentication import CognitiveServicesCredentials

from array import array
import os
from PIL import Image
import sys
import time

'''
Authenticate
Authenticates your credentials and creates a client.
'''
subscription_key = os.environ["VISION_KEY"]
endpoint = os.environ["VISION_ENDPOINT"]

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))
'''
END - Authenticate
'''

'''
Quickstart variables
These variables are shared by several examples
'''
# Images used for the examples: Describe an image, Tag an image, Tag an image, 
# Detect faces, Detect adult or racy content, Detect the color scheme, 
# Detect domain-specific content, Detect image types, Detect objects
images_folder = os.path.join (os.path.dirname(os.path.abspath(__file__)), "images")

local_image_path = r"C:\Users\池田　光\OneDrive\Pictures\IMG_8043.JPG"
local_image = open(local_image_path, "rb")

print("===== detect_objects an image - local =====")
detect_objects_result = computervision_client.detect_objects_in_stream(local_image)

# Print results with confidence score
print("Tags in the remote image: ")
if (len(detect_objects_result.objects) == 0):
    print("No objects detected.")
else:
    for object in detect_objects_result.objects:
        print("'{}' with confidence {:.2f}%".format(object.object, object.confidence * 100))
print()
'''
END - Tag an Image - remote
'''
print("End of Computer Vision quickstart.")
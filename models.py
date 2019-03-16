from imageai.Detection import ObjectDetection
import os

'''tinyyolo() for object prediction in image
'''
class tinyyolo:
    def __init__(self):                                  # initializing model
        execution_path = os.getcwd()
        self.detector = ObjectDetection()
        self.detector.setModelTypeAsTinyYOLOv3()
        self.detector.setModelPath( os.path.join(execution_path , "models/yolo-tiny.h5"))
        self.detector.loadModel()
        
    def prediction(self,img_execution_path,pred_img_execution_path,img,pred_img):     # predicting from model
        detections = self.detector.detectObjectsFromImage(input_image=os.path.join(img_execution_path , img), output_image_path=os.path.join(pred_img_execution_path , pred_img))
        return detections


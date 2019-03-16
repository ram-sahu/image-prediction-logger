import os
from models import tinyyolo
from imagedatabase import imagedata

'''logger for managing data , prediction and load result to database
'''
class logger:
    def __init__(self,data_folder,pred_folder):  # initialaizing logger
        self.dir=os.getcwd()
        self.data_dir=self.dir + '\\' + data_folder
        self.pred_dir=self.dir + '\\' + pred_folder
        self.db=imagedata("a")
        
    def db_init(self): # logger database initialaizing
        self.db.create_tables()
        
        
    def model_logger(self):         # model logging 
        model=tinyyolo()
        for img in os.listdir(self.data_dir):
            i=self.next_index()
            extension= img.split(".")[-1]
            pred_img=str(i) + '.' + extension 
            result=model.prediction(self.data_dir,self.pred_dir,img,pred_img)
            self.save_to_db(i,img,pred_img,extension,result)
            
    def next_index(self):               # for generating max index(image id ) for next index 
        index=self.db.custom_query('SELECT max(image_id) FROM image')
        index=index[0][0]
        if(index==None):
            return 1
        else:
            return index+1
    
    def save_to_db(self,index,img,pred_img,extension,result): # save to database
        self.db.insert_image(index,img,pred_img,extension)
        for i in result:
            self.db.insert_prediction(index,i['name'],int(i['percentage_probability']))
            
    def show(self):                    # show save logging 
        print(self.db.show_table())
        print(self.db.show_table('prediction'))
        
    def commit_logger(self):       # for commit logging
        self.db.commit()
            
    def close(self):              # for close logging 
        del self.db
    
    
if __name__ == "__main__":
    a=logger('images_data','prediction')
    print(a.next_index(),"\n")
    print(a.show(),"\n")
    a.close()       
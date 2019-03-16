import sqlite3 as sql


'''database(db_name='') for providing basic funtionality of database
'''
class database:   

    def __init__(self,db_name):              # for initializing database connection
        try:
            self.connection=sql.connect(db_name)
            self.cursor=self.connection.cursor()
        except sql.Error as e:
            print("Database error: %s" % e)
            
            
    def _query(self,query):               # for quering to database (private)
        try:
            if(query):
                self.cursor.execute(query)
            else:
                print("no query is pass")
        except sql.Error as e:
            print("database error:%s"%e)
            
            
    def commit(self):                       # for commit on database
        self.connection.commit()

    def rollback(self):                       # for rollback to last commit on database
        self.connection.rollback()

            
    def truncate(self,table):      # for truncate  given table
        self._query('DELETE FROM '+table)
             

    def __del__(self):                      # for closing connection
        self.connection.close() 
        print("connection close")
        

'''imagedata(db_name='') for providing custom funtionality for image prediction data logging
'''                
class imagedata(database): 
    
    
    def __init__(self,db_name):              # for initializing database 
        database.__init__(self,db_name)
            
            
       

    def create_tables(self):            #for creating "image" & "prediction" tables
        self._query('''CREATE TABLE image(
                                   image_id SMALLINT UNSIGNED,
                                   image_name VARCHAR(20) NOT NULL,
                                   predict_image VARCHAR(20) NOT NULL,
                                   extension VARCHAR(10) NOT NULL,
                                   CONSTRAINT pk_image PRIMARY KEY (image_id)
                                   );''')
        self._query('''CREATE TABLE prediction(
                                   image_id SMALLINT UNSIGNED,
                                   object VARCHAR(20) NOT NULL,
                                   predict_percent REAL NOT NULL,
                                   CONSTRAINT pk_predict_id PRIMARY KEY (image_id),
                                   CONSTRAINT pk_image_id FOREIGN KEY (image_id) REFERENCES image(image_id)
                                   );''')
        

    def insert_image(self,image_id =None ,image_name=None,predict_image=None,extension=None): # for insert metadata of image
        
        if(image_id and image_name and predict_image and extension):
            try:
                 self.cursor.execute("INSERT INTO image VALUES (?,?,?,?)",(image_id,image_name,predict_image,extension))
            except sql.Error as e:
                print("database error :",e)
        else:
            print("database error: none of the field can null ")
            
            
       
    def insert_prediction(self,image_id =None,obj=None,predict_percent=None):      #for insert about prediction 
        if(image_id and obj and predict_percent):
            try:
                 self.cursor.execute("INSERT INTO prediction VALUES (?,?,?)",(image_id,obj,predict_percent))
            except sql.Error as e:
                print("database error :",e)
        else:
                print("database error: none of the field can null ")
                

            
    def search_image(self,image_id=None):   #for searching image metadata
        if(image_id):
                self._query('SELECT * FROM image where image_id='+image_id)
                result= self.cursor.fetchall()
                return result
        else:
                print("database error: please give valid id ")

            
    def search_prediction(self,image_id=None):      #for seraching result of prediction
        if(image_id):
                self._query('SELECT * FROM prediction where image_id='+image_id)
                result= self.cursor.fetchall()
                return result
        else:
                print("database error: please give valid id ")

            
    def show_table(self,table='image'):      # for retriving tables
        self._query('SELECT * FROM '+table)
        result= self.cursor.fetchall()
        return result

    def truncate(self):      # for truncate tables
        self._query('DELETE FROM image')
        self._query('DELETE FROM prediction')

    
    def custom_query(self,query):                     #for custom readonly query (i.e must start with 'select') 
        if( query.startswith('SELECT') or query.startswith('select') ):
                self._query(query)
                result= self.cursor.fetchall()
                return result
        else:
                print("database error: only readable via custom query (start query only via 'SELECT') ")
        
            
from cassandra.cluster import Cluster
from cassandra.auth import PlainTextAuthProvider
import pandas as pd
import numpy as np
import threading

class Cql:
    def __init__(self,HOST:list,PORT:int,KEYSPACE_TABLE_NAME:str,USERNAME:str,PASSWORD:str,INPUT_FILE_NAME:str) -> None:
        auth = PlainTextAuthProvider(username=USERNAME,password=PASSWORD)
        self.cluster = Cluster(HOST,port=PORT,auth_provider=auth)
        if len(KEYSPACE_TABLE_NAME.split("."))!=2: raise Exception("Invalid keyspace.tablename!")
        self.TABLE_NAME = KEYSPACE_TABLE_NAME.split(".")[1]
        self.KEYSPACE_NAME = KEYSPACE_TABLE_NAME.split(".")[0]
        self.session = self.cluster.connect(self.KEYSPACE_NAME)
        self.INPUT_FILE_NAME=INPUT_FILE_NAME
        self.TABLE_SCHEMA = self.session.execute("SELECT column_name,type FROM system_schema.columns WHERE keyspace_name='%s' AND table_name='%s'"%(self.KEYSPACE_NAME,self.TABLE_NAME))
        self.set_conf()

    def set_conf(self):
        self.cql_to_python_type = { 
            'NULL': None,
            'boolean': bool,
            'float': float,
            'double': float,
            'int':int,
            'smallint':int, 
            'tinyint':int,
            'counter':int,
            'varint':int,
            'bigint': int,
            'decimal': float,
            'ascii':str,
            'varchar':str,
            'text': str,
            'blob': str,
            'date': str,
            'timestamp': str,
            'time': str,
            'list': list,
            'set': set,
            'map': dict,
            'timeuuid,': None,
            'uuid': None 
        }
        self.cql_types = {}
        self.cql_columns=[]
        for row in self.TABLE_SCHEMA:
            self.cql_types[row.column_name] = self.cql_to_python_type[row.type]
            self.cql_columns.append(row.column_name)
       
        param_keys = ",".join(self.cql_columns) 
        param_values = ",".join([ '%('+k+')s' for k in self.cql_columns])
        self.insert__statement = "INSERT INTO "+self.TABLE_NAME+" ("+param_keys+") VALUES ("+param_values+")"
    
    def insert_cql(self,stmt,df,session):
        df[df.select_dtypes(include=np.number).columns] = df.select_dtypes(include=np.number).fillna(0) # null value handle for numbers
        df[df.select_dtypes(exclude=np.number).columns] = df.select_dtypes(exclude=np.number).fillna('') # null value handle for string
        for row in df.to_dict(orient='records'):
            session.execute(stmt,row)

    def insert(self,chunck_size=10000):
        df_chunks = pd.read_csv(self.INPUT_FILE_NAME,chunksize=chunck_size)

        for df in df_chunks:
            thread =threading.Thread(target=self.insert_cql,args=(self.insert__statement,df,self.session))    
            thread.start()
            thread.join()

obj = Cql(['192.168.249.198'],9042,"test.student","cassandra","cassandra","dbo_student.csv")
obj.insert()



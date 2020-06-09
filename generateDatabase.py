#!/usr/bin/env python
# coding: utf-8

# In[1]:


import psycopg2
import pandas as pd 
import argparse
import sys
# In[2]:


def ConnectDatabase( database, user, password,ip = "localhost", port = 5432):
    conn = psycopg2.connect(host=ip ,database=database, user=user, password=str(password),port = port)
    conn.autocommit = True
    print("Connect Success")
    cursor = conn.cursor()
    return cursor


# In[3]:


def Drop(database,table):
    database.execute("DROP table if exists {} CASCADE;".format(table))


# In[4]:


def CreateUniversity(database):
    print("Create Table university.")
          
    query = '''Create Table university(
                    id CHAR(3) PRIMARY KEY, 
                    name VARCHAR NOT NULL,
                    position VARCHAR NOT NULL 
                    );'''

    database.execute(query)
    


# In[5]:


def InsertUniversity(database):
    print("Insert Data into university.\n")
    
    nameID = pd.read_csv("datas/name2ID.csv")
    namePos = pd.read_csv("datas/alluniversity.csv")
    #merge two data
    data = list()
    for (i,j) in zip(list(nameID['name']),list(nameID['ID'])):
        for (name,pos)   in zip(list(namePos['學校名稱']),list(namePos['學校地址'])):
            if(i in name):
                data.append((j,i,pos))
    #create query 
    query = '''INSERT INTO university \n Values '''
   
    for (ID,name,pos) in data:
        query+= "('"+str(ID).zfill(3) +"','"+name +"','"+pos+"')"+",\n"
    query = query[:-2]
    query += ';'
   
    database.execute(query)


# In[6]:


def CreateAcademy(database):
    print("Create Table academy.")
    
    query = '''Create Table academy(
                    name VARCHAR PRIMARY KEY 
                   
                    );'''

    database.execute(query)
    
    


# In[7]:


def InsertAcademy(database):
    print("Insert Data into academy.\n")
    
    aca = pd.read_csv("datas/Group.csv")
    query = '''INSERT INTO academy \n Values '''
    
    for i in aca['Group']:
        query+= "('"+i+"'),\n"
    query = query[:-2]
    
    
    database.execute(query)


# In[159]:


def CreateMainDepartment(database):
    print("Create Table mainDepartment.")
    
    query = '''Create Table mainDepartment(
                    academy VARCHAR NOT NULL,
                    department VARCHAR NOT NULL,
                    subject VARCHAR NOT NULL,
                    
                    FOREIGN KEY (academy) REFERENCES academy(name),
                    PRIMARY KEY (academy, department) 
                   
                    );'''

    database.execute(query)
    


# In[160]:


def InsertMainDepartment(database):
    print("Insert Data into mainDepartment.\n")
    
    md =  pd.read_csv("datas/Group_Department_Subject.csv")
    query = '''INSERT INTO MainDepartment \n Values '''
    
    for (i,j,k) in zip(md['Group'],md['Department'],md['Subjects']):
        query+= "('"+i+"','"+j+"','"+k+"'),\n"
    query = query[:-2]
    
    
    database.execute(query)


# In[161]:


def CreateDepartment(database):
    print("Create Table department.")
 
    query = '''Create Table department(
                    id VARCHAR NOT NULL,
                    name VARCHAR NOT NULL,
                    
                    university_id CHAR(3) NOT NULL,
                    academy VARCHAR NOT NULL,
                    
                    PRIMARY KEY (id), 
                    FOREIGN KEY (academy) REFERENCES academy(name),
                    FOREIGN KEY (university_id) REFERENCES university(id)
                   
                    );'''    
    database.execute(query)


# In[162]:


def  InsertDepartment(database):
    print("Insert Data into department.\n")
    
    df1 = pd.read_csv('datas/學測output.csv')
    df2 = pd.read_csv('datas/指考.csv')
    df3 = pd.read_csv("datas/department2group.csv")
    df4 = pd.read_csv("datas/name2ID.csv")
    
    name2ID = dict()
    
    for i in zip(df4['ID'],df4['name']):
        name2ID[i[1]] = str(i[0]).zfill(3)
  
    department2group = dict()
    
    for j in df3['University']:
        department2group[name2ID[j]] = dict()
    
    for (i,j,k) in zip( df3['University'],df3['DEPARTMENT'],df3['(code)Group']):
         department2group[name2ID[i]][j] = k.split(')')[1][1:-2]
        

    query = '''INSERT INTO department \n Values '''
    
    for i in dep:
        for j in dep[i]: 
            if(department2group.get(i,None)!=None):
                flag = 0
                for k in department2group[i]:
                    if(j in k): 
                        query+= "('"+i+str(dep[i][j]).zfill(3) +"','"+j +"','"+i+"','"+department2group[i][k]+"')"+",\n"
                        flag =1
                        break
                if(flag==0):
                    query+= "('"+i+str(dep[i][j]).zfill(3) +"','"+j +"','"+i+"','"+'unknown'+"')"+",\n"
            else:
                query+= "('"+i+str(dep[i][j]).zfill(3) +"','"+j +"','"+i+"','"+'unknown'+"')"+",\n"
    query = query[:-2]
    query += ';'
   
    database.execute(query)


# In[163]:


def CreateGSAT(database):
    print("Create Table GSAT.")
 
    query = '''Create Table GSAT(
                    id VARCHAR NOT NULL,
                    quota SMALLINT,
                    
                    chinese SMALLINT NOT NULL,
                    english SMALLINT  NOT NULL,
                    math    SMALLINT NOT NULL,
                    society SMALLINT  NOT NULL,
                    science SMALLINT NOT NULL,
                    
                    
                    FOREIGN KEY (id) REFERENCES department(id),
                    PRIMARY KEY (id) 
                   
                    );'''

    database.execute(query)
    


# In[164]:


def  InsertGSAT(database):
    print("Insert Data into GSAT.\n")
    
    table = dict() 
    for i in zip(range(6),['--','底','後','均','前','頂']):
        table[i[1]] = str(i[0])
    
    df1 = pd.read_csv('datas/學測output.csv')
    
    

   
            
    query = '''INSERT INTO GSAT \n Values '''
    
    for i in zip(df1['Code'],df1['name'],df1['num'],df1['s_Chinese'],df1['s_English'],df1['s_Math'],df1['s_Society'],df1['s_Science']):               
        code = str(i[0]).zfill(6)[:3]
      
        temp = list()
        for index in range(3,8):
            temp.append(table[i[index]])
        query+= "('"+code+str(dep[code][i[1]]).zfill(3) +"',"+ str(i[2])+","+ ','.join(temp)+")"+",\n"
        
    query = query[:-2]
    query += ';'
   
    database.execute(query)


# In[165]:


def CreateAST(database):
    print("Create Table AST.")
    
   
    query = '''Create Table AST(
                    id VARCHAR NOT NULL,
                    quota SMALLINT,
                    
                    chinese FLOAT NOT NULL,
                    english FLOAT NOT NULL,
                    math1   FLOAT NOT NULL,
                    math2  FLOAT NOT NULL,
                    
                    physical FLOAT NOT NULL,
                    chemistry FLOAT NOT NULL,
                    biological FLOAT NOT NULL,
                    
                    history FLOAT NOT NULL,
                    geography FLOAT NOT NULL,
                    citizen FLOAT NOT NULL,
                    
                    
                    FOREIGN KEY (id) REFERENCES department(id),
                    PRIMARY KEY (id) 
                   
                    );'''

    database.execute(query)
    


# In[166]:


def  InsertAST(database):
    print("Insert Data into AST.\n")
    
 
    df3 =pd.read_csv('datas/name2ID.csv')

    name2id = dict()
    for i in zip(df3['ID'],df3['name']):
        name2id[i[1]]= str(i[0]).zfill(3)

    df1 = pd.read_excel('datas/count.xlsx').dropna()

    qta = dict()
    for i in df1['學校名稱']:
        qta[name2id[i.strip()]]=dict()
    for i in zip(df1['學校名稱'], df1['學系組名稱'],df1['回流後考試\n分發總名額']):
        qta[name2id[i[0].strip()]][i[1].strip()] = i[2]



    df3 = pd.read_csv('datas/指考.csv')

    temp = list()
    for i in zip(df3['代碼'] ,df3['學系']):
        for j in qta[str(i[0]).zfill(5)[:3]]:
            if(i[1].split('(')[0] in j):   
                temp.append(qta[str(i[0]).zfill(5)[:3]][j])


   
            
    query = '''INSERT INTO AST \n Values '''
    
    for i in range(len(df3['代碼'])):
        code = str(df3.iloc[i][0]).zfill(5)[:3]
      
        temp = list()
        for index in range(2,12):
            if(df3.iloc[i][index] == '--'):          
                temp.append('0')
            else:
                temp.append(str(float(df3.iloc[i][index][1:])))
        
        temp_qta = 0
        
        for j in qta[code]:
            if(df3.iloc[i][1].split('(')[0] in j):   
                temp_qta = qta[code][j]
                
                break
     
        query+= "('"+code+str(dep[code][df3.iloc[i][1]]).zfill(3) +"',"+ str(temp_qta)+","+ ','.join(temp)+")"+",\n"
      
    query = query[:-2]
    query += ';'
    
    database.execute(query)


# In[177]:


def CreateCareer(database):
    print("Create Table career.")
    
    query = '''Create Table career(
                    id VARCHAR NOT NULL,
                    career1 VARCHAR ,
                    career2 VARCHAR,
                    career3 VARCHAR,
                    
                    
                    FOREIGN KEY (id) REFERENCES department(id),
                    PRIMARY KEY (id) 
                   
                    );'''

    database.execute(query)
    


# In[178]:


def  InsertCareer(database):
    print("Insert Data into career.\n")
    
 
    df3 =pd.read_csv('datas/name2ID.csv')

    name2id = dict()
    for i in zip(df3['ID'],df3['name']):
        name2id[i[1]]= str(i[0]).zfill(3)

    car = pd.read_csv('datas/職業output.csv').dropna()

    
    query = '''INSERT INTO Career \n Values '''
    keys = list()
    for i in range(len(car)):
        sch = car.iloc[i][0].replace('私立','')
        sch = sch.split('(')[0]
      
        if(sch not in name2id):
            continue
            
        code = name2id[sch]
        rw = car.iloc[i]
        if(code not in dep):
            continue
        
        temp = list()
        for index in range(2,5):
            if(rw[index]!=''):
                temp.append("'"+rw[index]+"'")
                
        
            d = str()
           
            for dd  in dep[code]:
                if ( rw[1] in dd  ):
                    d = str(dep[code][dd]).zfill(3)
                    
        if(len(temp)!=0 and d!='' and (code+d) not in keys):    
            while(len(temp)<3):
                temp.append("null")

      
            query+= "('"+code+d +"',"+ ','.join(temp)+")"+",\n"
            keys.append(code+d)
         
    query = query[:-2]
    query += ';'
   
    database.execute(query)


# In[179]:


def CreateFuture(database):
    print("Create Table future.")
    query = '''Create Table future(
                    id VARCHAR NOT NULL,
                    work_ratio FLOAT ,
                    
                    
                    FOREIGN KEY (id) REFERENCES department(id),
                    PRIMARY KEY (id) 
                   
                    );'''

    database.execute(query)
    


# In[176]:


def  InsertFuture(database):
    print("Insert Data into future.\n")
    
 
    df3 =pd.read_csv('datas/name2ID.csv')

    name2id = dict()
    for i in zip(df3['ID'],df3['name']):
        name2id[i[1]]= str(i[0]).zfill(3)

    fu = pd.read_csv('datas/比率output.csv').dropna()

    
    query = '''INSERT INTO Future \n Values '''
    
    keys = list()
    for i in range(len(fu)):
        rw = fu.iloc[i]
        sch = rw[0].replace('私立','')
        sch = sch.split('(')[0]
      
        if(sch not in name2id):
            continue
            
        code = name2id[sch]
        
        if(code not in dep):
            continue
        


        d = str()

        for dd  in dep[code]:
            if ( rw[1] in dd  ):
                d = str(dep[code][dd]).zfill(3)
        if(d!='' and (code+d) not in keys):
            query+= "('"+code+d +"',"+str(float(rw[2]/100))+")"+",\n"
            keys.append(code+d)
         
    query = query[:-2]
    query += ';'
    
    database.execute(query)


# In[171]:

# In[182]:


def run(options):

    database = ConnectDatabase(options.database, options.name, options.password, options.ip, options.port )
   
    CreateUniversity(database)
    InsertUniversity(database)
        
    CreateAcademy(database)
    InsertAcademy(database)
    
    CreateMainDepartment(database)
    InsertMainDepartment(database)
    
    CreateDepartment(database)
    InsertDepartment(database)
    
    CreateGSAT(database)
    InsertGSAT(database)
    
    CreateAST(database)
    InsertAST(database)
    
    CreateCareer(database)
    InsertCareer(database)
    
    CreateFuture(database)
    InsertFuture(database)
    
    print("Finish")


# In[ ]:
def get_options(args = None):
    parser = argparse.ArgumentParser()
    parser.add_argument("-d","--database",dest = "database",type = str, help = "The name of the database")
    parser.add_argument("-n","--name",dest = "name", type = str, help ="The name of the user")
    parser.add_argument("-password","--password",dest = "password", type = str,help = "The password of the user" )
    parser.add_argument("-ip","--ip",dest = "ip", help = "The ip of the database server" ,type = str,default="localhost")
    parser.add_argument("-p", "--port", dest = "port", help = "The port of the database server",type = int, default=5432 )
    
   # (options, args) = parser.parse_args(args = args)
    
    return parser.parse_args()
def main(options):
    

    df1 = pd.read_csv('datas/學測output.csv')
    df2 = pd.read_csv('datas/指考.csv')
    

    global dep  
    dep = dict() 

    for i in df2['代碼']:
        dep[str(i).zfill(5)[:3]]=  dict()
    for i in df1['Code']:
        dep[str(i).zfill(6)[:3]]=  dict()

    for (i,j) in zip(df2['代碼'],df2['學系']):
        dep[str(i).zfill(5)[:3]][j] = 0
    for (i,j) in zip(df1['Code'],df1['name']):
        dep[str(i).zfill(6)[:3]][j] =  0

    for i in dep:
        for (k,l) in zip(range(1,len(dep[i])+1),dep[i].keys()):
            dep[i][l]=k
    run(options)

if (__name__ == "__main__"):
    if (not main(get_options())):
        sys.exit(1)




import sqlite3
'''
content list format:-

[ [subtitle1, text1], [subtitle2, text2] ]
'''
'''
table structure

pathName    title    description     
'''
class Content():
    def __init__(self):
        self.executeSQL(""" CREATE TABLE IF NOT EXISTS content (
                        pathName TEXT NOT NULL PRIMARY KEY,
                        title TEXT NOT NULL,
                        description TEXT

        ); """)

    def executeSQL(self,sql, extraValues=(), fetch=False):
        conn=sqlite3.connect("data/data.db")
        rows=None
        if not fetch:
            if not extraValues:
                conn.execute(sql)
            else:
                conn.execute(sql,extraValues)
            conn.commit()
            
        else:
            cur = conn.cursor()
            if not extraValues:
                cur.execute(sql)
            else:
                cur.execute(sql,extraValues)
            rows = cur.fetchall()
        conn.close()
        return rows

    def addContent(self,pathName, title, content):
        ''' Takes the title and content 
        list as input'''
        self.executeSQL("INSERT INTO content (pathName, title, description) VALUES (?, ?, ?)", (pathName, title, content))

    def fetchContent(self,pathName):
        ''' Fetches the data from the table
          and returns it as a content list'''
        return self.executeSQL("SELECT * FROM content WHERE pathName = ?;", extraValues=(pathName,), fetch=True)
    
    def fetchAll(self):
        return self.executeSQL("SELECT * FROM content ORDER BY pathName", fetch=True)
        
    def deleteContent(self, pathName):
        self.executeSQL("DELETE FROM content WHERE pathName=?;", extraValues=(pathName,))
    
    def editContentField(self, pathName, field, value):
        self.executeSQL(f"UPDATE users SET {field}=? WHERE userId=?;", extraValues=( value, pathName,))
    
    def editContent(self, pathName, fields, values):
        errorList = []
        for f in range(len(fields)):
            try:
                self.editContentField(pathName, fields[f], values[f])
            except:
                errorList.append(fields[f])

if __name__=="__main__":
    c=Content()
    c.addContent("dune_2021", "Dune part 1 (2021)", "Description for Dune part 1")
    x = c.fetchContent('dune_2021')
    #c.deleteContent('dune_2021')
    print(x)

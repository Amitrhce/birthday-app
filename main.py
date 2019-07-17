
import sqlite3
from flask import Flask
from flask import jsonify
from datetime import date
from datetime import datetime as dt
app = Flask(__name__)

def validateDate(date_text):
    try:
        present = dt.now().date()
        date_user = dt.strptime(date_text, "%Y-%m-%d").date()
        diff=(date_user-present).days
        if(diff>=0):
            raise Exception(date_text+' must be a date before the today date')
    except ValueError:
        raise ValueError(date_text+" Incorrect data format, should be YYYY-MM-DD")
        
def validateUser(user_text):
    if(user_text.isalpha()==False):
        raise Exception(user_text+' must contain only letters')


@app.route('/hello/<username>',methods = ['GET'])
def hello_world_get(username):

    conn = sqlite3.connect('user.db')
    c = conn.cursor()
    try:
        c.execute('CREATE TABLE USER (date text, name text)')
    except:
        pass
    finally:
        query = c.execute("select date from USER where name= '"+username+"' COLLATE NOCASE limit 1")
        # Save (commit) the changes
        rows = c.fetchall()
        finalStr=''
        present = dt.now().date()
        for row in rows:
            finalStr=str(row[0])
            date_user = dt.strptime(finalStr, "%Y-%m-%d").date()
            date_user=date_user.replace(year = (present.year))
            diff=(date_user-present).days
            if(diff==0):
                finalStr="Hello, "+username+"! Happy Birthday! "
            elif(diff<0): 
                date_user=date_user.replace(year = (present.year + 1))
                diff=(date_user-present).days
                finalStr="Hello, "+username+"! Your Birthday is in "+str(diff)+" day("+"s)! "
            else:
                finalStr="Hello, "+username+"! Your Birthday is in "+str(diff)+" day("+"s)! "
        conn.close()  
        if(finalStr==''):
            finalStr="No records found"
        response_data = {
        "result": finalStr,
        "sucess": True,
        "status_code": 200
        }
        return jsonify(response_data), 200

    
@app.route('/hello/<username>/<dateOfBirth>',methods = ['PUT'])
def hello_world_put(username,dateOfBirth):
        
        validateUser(username)
        validateDate(dateOfBirth)
        conn = sqlite3.connect('user.db')
        c = conn.cursor()
        try:
            c.execute('CREATE TABLE USER (date text, name text)')
        except:
            pass
        finally:
            query = c.execute("select name from USER where name= '"+username+"' COLLATE NOCASE limit 1")
            # Save (commit) the changes
            rows = c.fetchall()
            finalStr=''
            for row in rows:
                finalStr=str(row[0])
            if (finalStr.casefold() == username.casefold()):
                c.execute("UPDATE USER SET date='"+dateOfBirth+"' where name='"+username+"' COLLATE NOCASE")
            else:
                print("Inside else")
                c.execute("INSERT INTO USER VALUES ('"+dateOfBirth+"','"+username+"')")
            conn.commit()
            conn.close()    
            response_data = {
                "sucess": True,
                "status_code": 204
            }
            return jsonify(response_data), 204
    
if __name__ == "__main__":
    app.run()


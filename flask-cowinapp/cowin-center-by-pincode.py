# import required libraries
import requests
import os
from json2html import json2html
from flask import Flask,render_template,request,redirect
 
#intantiate flask application 
app = Flask(__name__)

# use app route to redirect to and from html page 
@app.route('/', methods=['POST','GET'])

# define method to take date adn pincode from form 
def form():
    if request.method == 'POST':
        pincode = request.form['pincode']
        currentdate = str(request.form['currentdate'])
        year=currentdate[0:4]
        month=currentdate[5:7]
        day=currentdate[8:]
        print(pincode)
        date=str(day+'-'+month+'-'+year)

 # get json from COWIN API       
        url='https://cdn-api.co-vin.in/api/v2/appointment/sessions/public/calendarByPin?pincode='+pincode+'&date='+date
        dat = requests.get(url)
        dat_json=dat.json()

 # if there are not centers print error       
        if not dat_json['centers']:
            
            f= open(os.getcwd()+'/flask-cowinapp/templates/' + 'report.html','w')
            f.write('''
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>COWIN CENTER SEARCH</title>
            </head>
            <body>
                <h2> ============ There are No Centers Available for Search results for
                date 
                
                
            ''')
            f.write(currentdate + ' and Pincode ' + pincode )
            f.write('============ </h2>')
            f.write('''
                        <form action="/">
                        <input type='submit'  action='index.html' value='Return to mainpage'>
                        </form>
                        </body>
                        </html>''')
            f.close()
            return render_template('report.html')

# if there are centers , print centers in table format 

        else:
            html_data= json2html.convert(json=dat_json)
            f= open(os.getcwd()+'/flask-cowinapp/templates/' + 'report.html','w')
            f.write('''============
            <!DOCTYPE html>
            <html lang="en">
            <head>
                <meta charset="UTF-8">
                <meta http-equiv="X-UA-Compatible" content="IE=edge">
                <meta name="viewport" content="width=device-width, initial-scale=1.0">
                <title>COWIN CENTER SEARCH</title>
            </head>
            <body>
                <h1></H>Search results for date {{date}} and pincode{{pincode}}</h1>
                <table>
                
            ''')
            f.write('''<h1>============Search results for date ''')
            f.write(currentdate + ' and Pincode ' + pincode )
            f.write('============ </h1>')
            f.write('''
                    <form action="/">
                    <input type='submit'  action='index.html' value='Return to mainpage'>
                    </form>''')
            f.write(html_data)
            f.write('''</table>
                        </body>
                        </html>''')
            f.close()
            return render_template('report.html')
        
    else:
        return render_template('index.html')

if __name__ == '__main__':
    app.run()






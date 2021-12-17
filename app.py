from flask import Flask
from flask_restful import Resource, Api
from api_co import dataProcessor
from tkinter import *

global covid_cases
global b
covid_cases = "1"
root = Tk()
root.title('COVID19 REPRESENTATION')
root.geometry("500x500")

app = Flask(__name__)
api = Api(app)


class Global_data(Resource):
    '''
    It is the class of first endpoint '/'
    It has a get funtion that return a list of json
    of corona virus status scraped from
    https://www.worldometers.info/coronavirus/

    The first item in list is a dictionary of world
    covid-19 status.
    The second item in list is a list of dictionary
    of covid-19 status in each country's of the world.
    The third item in the list are dictionary's of
    covid-19 status by continent.
    '''

    def get(self):

      self.datum = dataProcessor().globalwise()
      global a
      a = self.datum
      #covid_cases = a[0][clicked.get()]
      return self.datum


class Continent_data(Resource):
    '''
    It is the class of third endpoint '/continent=<string:continent>'
    It has a get funtion that return a json
    of corona virus status scraped from
    https://www.worldometers.info/coronavirus/
    
    country is the parameter passed to the endpoint.
    Example
    GET apicovid2019.herokuapp.com/continent=Asia
    It returns info of covid-19 status in the requested
    continent of the world.
    
    The available continents names are as:
    Africa
    Asia
    Europe
    Oceania
    North America
    South America
    ''' 
   
    def get(self,continent):
        self.continent=continent
        self.datum=dataProcessor().continentwise()
        b= self.datum
        
        try:
            for i in self.datum:
                if i['Country/other']== self.continent:
                    self.cont_y=i
                    break
            return self.cont_y
        except:
            return "Make sure to enter proper input and its method"

      
#endpoints of the api
api.add_resource(Global_data, '/')
api.add_resource(Continent_data,'/continent=<string:continent>')

Global_data().get()
#covid_cases = a[0][clicked.get()]
#print (covid_cases)
 

options = [
  "- Select -",
  "CoronavirusCases",
  "NewCases",
  "TotalDeaths",
  "NewDeaths",
  "TotalRecovered",
  "NewRecovered",
  "ActiveCases",
  "Serious",
  "Totalcases/1Mpop",
   "Deaths/1Mpop",
]
clicked = StringVar()
clicked.set(options[1])

options1 = [
  "Africa",
    "Asia",
    "Europe",
    "Oceania",
    "North America",
    "South America",
    ]



clicked1= StringVar()
#clicked1.set(options1[0])


drop = OptionMenu(root, clicked, *options)
drop2 = OptionMenu(root, clicked1, *options1)
def submit():
    #Clear the text boxe
    covid_cases = a[0][clicked.get()]
    parameter_show = Label(root, text= covid_cases)
    parameter_show.grid(row= 8, column=2)
    
    
    clicked.set(options[0])
    clicked1.set(options1[0])
    
    
    

f_name = drop2
f_name.grid(row=0, column= 1, padx = 20)
l_name = drop 
l_name.grid(row=5, column= 1, padx = 20)

f_name_label = Label(root, text = "Country Name- ")
f_name_label.grid(row= 0, column=0)
l_name_label = Label(root, text = "Parameter Choice-  ")
l_name_label.grid(row= 5, column=0)

submit_btn = Button(root, text= "SUBMIT", command = submit)
submit_btn.grid(row =6, column=0, columnspan=2, pady=10, padx=10, ipadx=100)




root.mainloop()
if __name__ == '__main__':
   app.run(debug=True)





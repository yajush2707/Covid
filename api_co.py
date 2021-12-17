import os
from bs4 import BeautifulSoup
import requests


class dataProcessor:
    '''
    This is the class that scrapes the data from the site:
    "https://www.worldometers.info/coronavirus".
   '''

    def __init__(self):
        '''
        For every request to the site creates a new instance of 
        the dataprocessor class.
        '''
        # gets request to the main site and follows its response
        res = requests.get("https://www.worldometers.info/coronavirus")
        h_source = res.text
        # preparing a soup for analysing the data recieved
        self.soup = BeautifulSoup(h_source, 'html.parser')
        self.soup = self.soup.find_all(attrs={'id': "main_table_countries_today"})[
            0]  # future extension

        self.title = ["Country/other",
                      "TotalCases",
                      "NewCases",
                      "TotalDeaths",
                      "NewDeaths",
                      "TotalRecovered",
                      "NewRecovered",
                      "ActiveCases",
                      "Serious",
                      "Totalcases/1Mpop",
                      "Deaths/1Mpop",
                      "TotalTests",
                      "Tests/1Mpop",
                      "Population"
                      ]

    def globalwise(self):
        '''
        This method returns a list of overall covid-19 cases
        data along with all country's and continent data.
        '''
        t = [
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

        self.t_value = []

        self.global_list = self.soup.find_all(
            attrs={"class": "total_row", "class": "total_row_body"})

        self.temporary_t_val = self.global_list[0].find(
            "td").findNext("td").findNext("td")
        for i in range(0, 10):  # new 10 columns
            self.t_value.append(str(self.temporary_t_val.string.strip()))
            self.temporary_t_val = self.temporary_t_val.findNext("td")

        self.msg0 = dict(list((n, v) for n, v in zip(t, self.t_value)))

        return [self.msg0]

    def continentwise(self):
        '''
        This method returns a list of all continents
        (as specified by worldometers)
        covid-19 cases data.
        '''
        self.changed_title = self.title[:9]
        self.continent_list = self.soup.find_all(
            attrs={'class': "total_row_world row_continent"})
        self.continentnames = []  # list of continent names
        for index, name in enumerate(self.continent_list):
            '''
            Gets continent name(s) used in the worldometers site.
            '''
            if index <= 5:  # gets todays data only from the continent_list
                self.continentnames.append(name.find("nobr").string)
            else:
                break

        self.continentspecific_val = []
        self.msg2 = []  # list of continent wise data
        for continent in self.continentnames:
            self.continentspecific_val.append(continent)
            self.next_v = self.soup.find("tbody").find("nobr", text=continent)
            for i in range(0, 10):
                self.next_v = self.next_v.findNext("td")
                self.continentspecific_val.append(
                    str(self.next_v.string).strip())

            pre_msg = dict([(x, y) for x, y in zip(
                self.changed_title, self.continentspecific_val)])
            self.msg2.append(pre_msg)
            del self.continentspecific_val[:]
        return self.msg2

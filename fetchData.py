import pandas as pd
import requests
from bs4 import BeautifulSoup
import logging
from typing import *

logs = "./info.logs"
logging.basicConfig(filename=logs, format='%(asctime)s:%(levelname)s:%(message)s', datefmt='%m/%d/%Y %I:%M:%S %p',
                    filemode='w', level=logging.INFO)
logger = logging.getLogger(__name__)


def getData(url: str) -> Optional[str]:
    try:
        Response = requests.models.Response
        response: Response = requests.get(url)
        if response.status_code == 200:
            logger.info(
                "Successfully fetched data from {} with response {}".format(url, response.status_code))
            return parseHtml(response.text)
        logger.info("The status code returned {} while trying to fetch data".format(response.status_code))
        return
    except Exception as e:
        logger.error("Unable to get data for url {}, with exception {}".format(url, e))
        return


def parseHtml(response: str) -> Optional[str]:
    try:
        if response is not None:
            soup: BeautifulSoup = BeautifulSoup(response, 'html.parser')
            table: str = soup.find('table', {'class': 'wikitable'})
            return table
        return
    except Exception as e:
        logger.error("Unable to parse html with exception {}".format(e))
        return


def convertHtmlToDataFrame(data: str) -> Optional[pd.DataFrame]:
    try:
        df = pd.read_html(str(data))
        df = pd.DataFrame(df[0])
        logger.info("Successfully converted the html to a DataFrame")
        return df
    except Exception as e:
        logger.error("Failed to convert html to DataFrame with exception {}".format(e))
        return


def cleanDataFrame(data: pd.DataFrame, sort: bool = True,
                   sortBy: str = "Road deaths per Million Inhabitants") -> Optional[pd.DataFrame]:
    try:
        logger.info("The columns in the dataFrame are {}".format(data.columns))
        data["Year"] = 2018
        cols: Dict[str, str] = {'Area (thousands of km2)[24]': 'Area',
                                'Population in 2018[25]': 'Population',
                                'GDP per capita in 2018[26]': 'GDP per capita',
                                'Population density (inhabitants per km2) in 2017[27]': 'Population density',
                                'Vehicle ownership (per thousand inhabitants) in 2016[28]': 'Vehicle ownership',
                                'Total Road Deaths in 2018[30]': 'Total road deaths',
                                'Road deaths per Million Inhabitants in 2018[30]': 'Road deaths per Million Inhabitants'
                                }
        data.rename(columns=cols, inplace=True)
        if sort:
            data.sort_values(sortBy, inplace=True)
        newData = data[['Country', 'Year', 'Area', 'Population', 'GDP per capita', 'Population density',
                        'Vehicle ownership', 'Total road deaths', 'Road deaths per Million Inhabitants']]
        logger.info("Successfully cleaned the DataFrame")
        return newData
    except Exception as e:
        logger.error("An error occurred while trying to clean DataFrame with exception {}".format(e))
        return

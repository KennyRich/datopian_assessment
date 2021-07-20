from fetchData import *


def main():
    htmlData = getData("https://en.wikipedia.org/wiki/Road_safety_in_Europe")
    dataFrame = convertHtmlToDataFrame(htmlData)
    df = cleanDataFrame(dataFrame)
    df.to_csv("data.csv")


if __name__ == '__main__':
    main()

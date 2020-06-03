import os
import requests
from bs4 import BeautifulSoup


def scrape(cars):
    for i in range(len(cars[0])):
        make = cars[0][i]
        model = cars[1][i]
        print('make = ', make)
        print('model = ', model)

        imgLinkList = []

        for page_n in range(1, 31, 1):
            link = 'https://www.autotrader.co.uk/car-search?sort=relevance&postcode=LE77SS&radius=1500&make=' + make + '&model=' + model + '&year-from=2019&year-to=2019&page=' + str(
                page_n)
            page = requests.get(link)
            soup = BeautifulSoup(page.content, 'html.parser')

            for imgLink in soup.find_all('img', {"loading": "lazy", "data-label": "search appearance click "}):

                if imgLink.has_attr('src') and (imgLink.has_attr('alt') == False):

                    partialLink = imgLink['src']

                    if partialLink[-3:] == 'jpg':
                        imgLinkList.append(partialLink)

        print('n images = ', len(imgLinkList))

        if os.path.isdir(
                '/Users/craigsmith/PycharmProjects/image_classification/car_images/' + make + '_' + model) == False:
            os.mkdir('/Users/craigsmith/PycharmProjects/image_classification/car_images/' + make + '_' + model)
        else:
            print('folder exists')

        os.chdir('/Users/craigsmith/PycharmProjects/image_classification/car_images/' + make + '_' + model)

        for ii, i in enumerate(imgLinkList):
            rawImage = requests.get(i, stream=True)
            filename = i.split("/")[-1]

            with open(filename, 'wb') as fd:
                for chunk in rawImage.iter_content(chunk_size=1024):
                    fd.write(chunk)

            os.rename(filename, str(ii) + '.jpg')

    os.chdir('/Users/craigsmith/PycharmProjects/image_classification')
    return

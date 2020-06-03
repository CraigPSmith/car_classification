import os
import requests
from bs4 import BeautifulSoup


def scrape(types = ['dress', 'jacket', 'jeans', 'shoes', 'bags']):

    for type in types:
        print(type)

        os.chdir('/Users/craigsmith/PycharmProjects/image_classification/images/' + type)

        for page_n in range(1, 6 ,1):
            print(page_n)
            if type == 'dress':
                link = 'https://www.very.co.uk/women/dresses/e/b/1655.end?pageNumber=' + str(page_n) + '&numProducts=99'

            elif type == 'jacket':
                link = 'https://www.next.co.uk/shop/gender-women-category-coatsandjackets'

            elif type == 'jeans':
                link = 'https://www.next.co.uk/shop/gender-women-category-jeans'

            elif type == 'shoes':
                link = 'https://www.next.co.uk/shop/gender-women-productaffiliation-footwear'

            elif type == 'bags':
                link = 'https://www.next.co.uk/shop/gender-women-productaffiliation-accessories/category-bags-category-luggage-category-purses'
            print(link)
            page = requests.get(link, timeout=20)
            soup = BeautifulSoup(page.content, 'html.parser')

            imgLinkList = []
            for imgLink in soup.find_all('img'):

                if imgLink.has_attr('data-search-image'):
                    partialLink = imgLink['data-search-image']

                else:
                    partialLink = imgLink['src']

                if 'jpg' in partialLink and partialLink[-3:] == 'jpg':
                    imgLinkList.append(partialLink)
                elif 'jpg' in partialLink and partialLink[-3:] == 'X56':

                    imgLinkList.append(partialLink[:-4])

        for ii, i in enumerate(imgLinkList):
            rawImage = requests.get(i, stream=True)
            filename = i.split("/")[-1]

            with open(filename, 'wb') as fd:
                for chunk in rawImage.iter_content(chunk_size=1024):
                    fd.write(chunk)

            os.rename(filename, str(ii) + '.jpg')

        print(len(imgLinkList))

    os.chdir('/Users/craigsmith/PycharmProjects/image_classification')
    return

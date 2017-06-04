from bs4 import BeautifulSoup
import requests
import writeCards as _write

wiki = r"https://en.wikipedia.org"

worldSeriesURL = wiki + "/wiki/List_of_World_Series_champions"
nbaFinalsURL = wiki + "/wiki/List_of_NBA_champions"
stanleyCupURL = wiki + "/wiki/List_of_Stanley_Cup_champions"

# TODO
superbowlURL = r"https://en.wikipedia.org/wiki/List_of_Super_Bowl_champions"
ncaaBasketballURL = r"https://en.wikipedia.org/wiki/List_of_NCAA_Division_I_men%27s_basketball_champions"

def getBaseball(start, end):
    years = list(map(str, range(start, end+1)))

    html = requests.get(worldSeriesURL).text
    soup = BeautifulSoup(html, 'lxml')

    trivia = []

    for yr in years:
        try:

            series = soup.find_all('a', {'title': yr + ' World Series'})[0]['href']
            moreSoup = BeautifulSoup(requests.get(wiki + series).text, 'lxml')

            infobox = moreSoup.find_all('table', {'class':'infobox'})

            winner = infobox[1].find_all('a')[1].text
            loser = infobox[1].find_all('a')[3].text

            rows = infobox[0].find_all('th')
            findMVP = lambda x: 'Valuable' in str(x)
            mvp = list(filter(findMVP, rows))[0].fetchNextSiblings()[0].text

            _write.writeSeries(yr, winner, loser, mvp, 'baseball')

            trivia.append((winner, loser, mvp))
        except:
            print(yr)

    print(trivia)



def getNBA(start, end):
    years = list(map(str, range(start, end+1)))

    html = requests.get(nbaFinalsURL).text
    soup = BeautifulSoup(html, 'lxml')

    trivia = []

    for yr in years:
        try:
            series = soup.find_all('a', {'title': yr + ' NBA Finals'})[0]['href']
            moreSoup = BeautifulSoup(requests.get(wiki + series).text, 'lxml')

            infobox = moreSoup.find_all('table', {'class':'infobox'})

            winner = infobox[0].find_all('td')[1].find_all('td')[0].text
            loser = infobox[0].find_all('td')[1].find_all('td')[3].text

            mvp = infobox[0].find_all('td')[9].text.replace('\n', ' ')

            _write.writeSeries(yr, winner, loser, mvp, 'basketball')

            trivia.append((winner, loser, mvp))
        except:
            print(yr)

    print(trivia)


def getStanleyCup(start, end):
    years = list(map(str, range(start, end+1)))

    html = requests.get(stanleyCupURL).text
    soup = BeautifulSoup(html, 'lxml')

    trivia = []

    for yr in years:
        try:
            series = soup.find_all('a', {'title': yr + ' Stanley Cup Finals'})[0]['href']
            moreSoup = BeautifulSoup(requests.get(wiki + series).text, 'lxml')

            infobox = moreSoup.find_all('table', {'class':'infobox'})

            teams = [x.text for x in infobox[0].find_all('td')[1].find_all('a')]
            boldInTable = infobox[0].find_all('td')[1].find_all('b')

            winner = list(filter(lambda x: x.find_all('a'), boldInTable))[0].text
            teams.remove(winner)
            loser = teams[0]

            mvpRow = infobox[0].find_all('a', {'title':'Conn Smythe Trophy'})[0]
            mvp = mvpRow.parent.find_next_sibling().text

            _write.writeSeries(yr, winner, loser, mvp, 'hockey')            

            trivia.append((winner, loser, mvp))
        except:
            print(yr)

    print(trivia)
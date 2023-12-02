#MuddyUS2020_Fox_extract

# Fox doesn't report results of write-in candidates; only those listed on ballot

from requests import get
from lxml import html
import numpy as np
import pandas as pd

domain = 'https://www.foxnews.com'
url = '/elections/2020/general-results'
response = get(domain + url)

tree = html.fromstring(response.content)
states = tree.xpath('//div[@class="content state-list"]//div[@class="state"]//a/@href')
full_US = []
for st in states:
    #do all the things
    #start from url
    #go to each state's individual page
    source = get(domain + st)
    #source = get('https://www.foxnews.com/elections/2020/general-results/state/california')
    tree1 = html.fromstring(source.content)
    #pull all parties, candidates, votes, percentages
    test = tree1.xpath('//div[@data-table="race-table-president-county"]//span[1]/text()')
    #pull all county names into a separate list
    cty = tree1.xpath('//div[@data-table="race-table-president-county"]//div[@class="content race-table"]//span[@class="county"]/text()')
    fips = tree1.xpath('//div[@data-table="race-table-president-county"]//div[@class="content race-table"]//table/@data-county-fips')

    tab = [item for item in test if item not in ['In', 'CLOSED', ' Polls are closed']]
    tab = [item for item in tab if item not in cty]
    mat = []

    while tab != []:
        mat.append(tab[:4])
        tab = tab[4:]

    mat = np.asarray(mat)
    mat = pd.DataFrame(mat)
    
    cty = cty * int(len(mat) / len(cty))
    cty.sort()
    fips = fips * int(len(mat) / len(fips))
    fips.sort()

    mat[4] = cty
    mat[5] = fips
    mat[6] = st.rsplit('/', 1)[-1].replace('-', ' ').title() #state name only, title case
    mat = mat.reindex(columns=[5, 6, 4, 0, 1, 2, 3])
    mat.columns = ['FIPS', 'State', 'County', 'Party', 'Candidate', 'Votes', 'Percent']

    mat = mat.astype('string')
    mat['Votes'] = mat['Votes'].str.replace(',', '').astype(int)

    #append st to list of dataframes
    full_US.append(mat)
# export list to csv
full_US.to_csv('~/home/nathan/Documents/FOXMuddyUS2020.csv', index=False)

#extract data for:
#   all states
#   all counties
#   all candidates
#   all votes
#   all percentage





# from bs4 import BeautifulSoup
# html_soup = BeautifulSoup(response.text, 'html.parser')
# type(html_soup)

# county_containers = html_soup.find_all('g', id='ca-counties')

# from requests_html import HTMLSession  
  
# def render_JS(URL):
#     session = HTMLSession()
#     r = session.get(URL)
#     r.html.render()
#     return r.html.text

# soup1 = render_JS('https://static.foxnews.com/static/orion/scripts/fox-news/elections/external/embed.js')
# soup1 = BeautifulSoup(soup1, 'html.parser')


# source = get('https://www.foxnews.com/elections/2020/general-results/state/california')
# soup = BeautifulSoup(source.text, 'html.parser')
# cont = soup.find_all('table', {'data-state': 'CA'})[0:57] #only 1st 58 tables are county pres races
# soup.find_all('table', {'data-county-fips': ['6001', '6003']})
# cont[0].span.text.strip() # = 'Alameda'
# #cont[0].find('table', {'class': 'data-county-fips'}) # != '6001' yet
# cont[0].find_all('span', {'class': 'is-long'})[0].text.strip() # = 'Joe Biden'
# cont[0].find_all('span', {'class': 'count'})[0].text.strip() # = '617,659'
# cont[0].find_all('span', {'class': 'percent'})[0].text.strip() # = '80.20%'

# county = tree.xpath('//div[@data-table="race-table-president-county"]//span[@class="county"]/text()')
# candidate = tree.xpath('//div[@data-table="race-table-president-county"]//span[@class="is-long"]/text()')
# for i in range(len(county)):
#     candidate.remove('Incumbent') #removes all cases of 'Incumbent'

# votes = tree.xpath('//div[@data-table="race-table-president-county"]//span[@class="count"]/text()')
# percent = tree.xpath('//div[@data-table="race-table-president-county"]//span[@class="percent"]/text()')
# # party = tree.xpath('//div[@data-table="race-table-president-county"]//td[@class="name"]//span[1]/text()')

# county1 = county * int(len(candidate)/len(county))
# county1.sort()

# ca2020 = pd.DataFrame([county1, candidate, votes, percent])
# ca2020 = ca2020.T
# ca2020.columns = ['County', 'Candidate', 'Votes', 'Percent']

#generalize 25 step (n candidates * 4 values (party, name, votes, pct) + 1 county)
# testlist = []
# for i in range(58):
#     testlist.append(list(test[(i * 25 + 1):((i + 1) * 25)]))

# testdf = pd.DataFrame(testlist)
# for i in range(24):
#     if np.mod(i,4) == 0:
#         testdf[i][0]

# list(testdf.loc[0,::4])

# test1 = []
# for i in range(58):
#     test1.append(list(test[(i * 25 + 1):((i + 1) * 25):4]))

# test2 = []
# for sublist in test1:
#     for item in sublist:
#         test2.append(item)



#Then pulling each remaining column out should be much easier
# test5 = []
# for j in range(4):
#     test3 = []
#     for i in range(58):
#         test3.append(test[(i * 25 + j + 1):((i + 1) * 25):4])
#     test4 = []
#     for sublist in test3:
#         for item in sublist:
#             test4.append(item)
#     test5.append(test4)

# testdf1 = pd.DataFrame(test5).T

# cty = test[::25] * 6
# cty.sort()

# testdf1['County'] = cty
# testdf1 = testdf1.reindex(columns=['County', 0, 1, 2, 3])
# testdf1.columns = ['County', 'Party', 'Candidate', 'Votes', 'Percent']

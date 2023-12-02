#MuddyUS2020_Fox_extract

from requests import get
url = 'https://www.foxnews.com/elections/2020/general-results'
response = get(url)
# print(response.text[:250])

tree1 = html.fromstring(response.content)
states = tree1.xpath('//div[@class="content state-list"]//div[@class="state"]//a/@href')
# for st in state:
    #do all the things

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

#start from url
#go to each state's individual page
#extract data for:
#   county/fips?
#   all candidates (test case: Biden, Trump)
#   all votes (test case: Biden, Trump)
#   all percentage (test case: Biden, Trump)


from lxml import html
source = get('https://www.foxnews.com/elections/2020/general-results/state/california')
# Fox doesn't report results of write-in candidates; only those listed on ballot
tree = html.fromstring(source.content)
# county = tree.xpath('//div[@data-table="race-table-president-county"]//span[@class="county"]/text()')
# candidate = tree.xpath('//div[@data-table="race-table-president-county"]//span[@class="is-long"]/text()')
# for i in range(len(county)):
#     candidate.remove('Incumbent') #removes all cases of 'Incumbent'

# votes = tree.xpath('//div[@data-table="race-table-president-county"]//span[@class="count"]/text()')
# percent = tree.xpath('//div[@data-table="race-table-president-county"]//span[@class="percent"]/text()')
# # party = tree.xpath('//div[@data-table="race-table-president-county"]//td[@class="name"]//span[1]/text()')

# county1 = county * int(len(candidate)/len(county))
# county1.sort()

import pandas as pd
# ca2020 = pd.DataFrame([county1, candidate, votes, percent])
# ca2020 = ca2020.T
# ca2020.columns = ['County', 'Candidate', 'Votes', 'Percent']

test = tree.xpath('//div[@data-table="race-table-president-county"]//span[1]/text()')
cty1 = tree.xpath('//div[@class="content race-table"]//span[@class="county"]/text()')

for i in range(58):
    test.remove('In')
    test.remove('CLOSED')
    test.remove(' Polls are closed')

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



#Can I pull all county names out into a separate list first? 
[item for item in test if item not in cty1]
#Then pulling each remaining column out should be much easier
test5 = []
for j in range(4):
    test3 = []
    for i in range(58):
        test3.append(test[(i * 25 + j + 1):((i + 1) * 25):4])
    test4 = []
    for sublist in test3:
        for item in sublist:
            test4.append(item)
    test5.append(test4)

testdf1 = pd.DataFrame(test5).T

cty = test[::25] * 6
cty.sort()

testdf1['County'] = cty
testdf1 = testdf1.reindex(columns=['County', 0, 1, 2, 3])
testdf1.columns = ['County', 'Party', 'Candidate', 'Votes', 'Percent']

testdf1 = testdf1.astype('string')
testdf1['Votes'] = testdf1['Votes'].str.replace(',', '').astype(int)

testdf1.to_csv('~/home/nathan/Documents/FOXMuddyCA2020.csv', index=False)

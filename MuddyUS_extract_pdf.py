#importing/reshaping CA county data from 2020 US Pres election
import tabula
import pandas as pd

file1="https://www.presidency.ucsb.edu/sites/default/files/election_data/ca-2020.pdf"

table = tabula.read_pdf(file1, pages="22-27")

table[0]
table1 = table

tab1 = pd.concat([table1[i] for i in range(3)], ignore_index=True)

tab2 = pd.concat([table1[i+3] for i in range(3)], ignore_index=True)

tab3 = pd.merge(tab1, tab2, on='Unnamed: 0')
tab3 = tab3.drop_duplicates()
tab3 = tab3.rename(columns={'Unnamed: 0': 'County'})
tab3 = tab3.query('`County` != "Percent"')
tab3 = tab3.query('`County` != "State Totals"')

party = tab3.iloc[0]
party = party[1:]
party = party.rename_axis('Candidate')
party = pd.DataFrame({'Party': party})
party = party.assign(Candidate=party.index)
party.index = [i for i in range(11)]
party = party[['Candidate', 'Party']]

tab3 = tab3.loc[1:]
tab3.index = [i for i in range(58)]
tab3.loc[38] = tab3.loc[38].fillna(value=0)

tab4 = tab3.melt(id_vars=['County'], var_name='Candidate', value_name='Votes')

tab5 = pd.merge(tab4, party)
tab5 = tab5[['County', 'Candidate', 'Party', 'Votes']]
tab5 = tab5.astype('string')
tab5['Votes'] = tab5['Votes'].str.replace(',', '').astype(int)

tab5 = tab5.sort_values(by=['County', 'Votes'], ascending = [True, False])

tab6 = tab5.groupby('County')['Votes'].sum().sort_values(ascending=False)

tab5.to_csv('~/home/nathan/Documents/MuddyCA2020.csv', index=False)

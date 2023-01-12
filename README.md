# Which countries have the best boxers?

Here you'll find code for a Python streamlit dashboard I made for fun. It uses data I scraped from the amazing community led resource [Boxrec.com](https://boxrec.com/). The data was collected late December 2022.

I have cleaned the data. 'Fighting record' is a text column with wins losses and draws lumped together (E.g. "30 2 1"). Boxer location is a free text box that varies in how much information it contains. I have parsed both of these, extracting country of origin. I have also engineered features such as "percentage of fights won".

It uses Pandas, Matplotlib, Seaborn libraries. The code is formatted using Black.

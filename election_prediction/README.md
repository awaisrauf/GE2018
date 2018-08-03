# Prediction of Seats of National Assembly of Pakistan for General Election 2018
Repository contains winner code for national level [Election Prediction Contest](https://www.facebook.com/events/1841498585916176/) held by
[Ignite](ignite.org.pk) (Formerly National ICT R&D Fund), [Redbuffer](www.redbuffer.net) and [DeepLinks](http://deeplinks.pk).

[Winner's Profile](https://awaisrauf.github.io/)

## Website
- For more information visit [website]()
## Method
#### Problem 
Predict winner of 272 national assembly constituencies for [General Election 2018](https://en.wikipedia.org/wiki/Pakistani_general_election,_2018) of Pakistan. 
#### Solution
Core of the solution is to find probability of win for each candidate in each constituency
from different data sources. For example, if a constituency have 4 candidates then vector containing their win probabilities will be as follows;

[0.1 0.2 0.5 0.2]

For each constituency, such vectors are produced from 11 different data sources. To combine all of these vector for final solution, election results for 10 secure constituencies are assumed and then Bayesian Optimization is used to combine these probabilities. 
<div align="center" >
<img src="https://raw.githubusercontent.com/awaisrauf/GE2018/master/imgs/solution.png"  alt="Block Diagram" width="800" height="250" >
<figcaption> Block Diagram of the solution </figcaption>
</div>

#### Data Sources
- Twitter Analysis to find probability of each party over 20 days before the election
- 1997 Election Result
- 2002 Election Result
- 2008 Election Result
- 2013 Election Result
- Gallup 2017 Survey 1
- Gallup 2017 Survey 2
- Gallup 2018 Survey 1
- Gallup 2018 Survey 2
- IPOR 2018 Survey
- Dunya News Survey 2018

## File Description
- main.py: run this to get results in result folder
- ml.py: contains code for Bayesian Optimization
- preprocessing.py: preprocessing of the data
- predict.py: Contains functions to return win probabilities based on different data sources
- utils.py: extra functions
- data: all the data used 
- previous_results_preprocessed: some preprocessed results are saved as csv
- results: results in submission format as well as in some other formats 

## Contributions
- Muhammad Awais
- Iqra Akarm
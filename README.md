# portfolio

## Time Tracking App (Python): 

This is a python app that I created to replace a time tracking service I was paying for (https://www.hourstimetracking.com/). I use it on a daily basis to keep track of how much time I spend on various activities throughout the day (reading, studying, etc.) and all the data is saved to a csv file (hours.csv) that I can then analyze with R or Python. I run the app through Apple's Terminal. 

## Baby Names (R): 

Takes all of the name counts for Males and Females back to 1880 and provides three possible outputs from the baby function which takes the following inputs: 
1. input
2. fun (pop_num, pop_prop, ex_num)
3. gender (M, F, both)
4. year (c(start date, end date))

Example: baby(input = "Nathan", fun = "pop_num", gender = "M", year = c(1880,2014))

Data file came from Kaggle (https://www.kaggle.com/kaggle/us-baby-names)

## March Madness Visualizations (R):

Takes data from Kaggle (https://www.kaggle.com/c/march-machine-learning-mania-2016) and display some graphs using ggplot. 
Two functions, seed_density and seed_matchup, will produce varying graphs based on inputs. Seed_density will show a density of teams seeds by round. Seed_matchup shows a graph of seed matchups by round. Examples of how these are used are provided in the code. 


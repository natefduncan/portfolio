# portfolio

Time Tracking App (Python): This is a python app that I created to replace a time tracking service I was paying for (https://www.hourstimetracking.com/). I use it on a daily basis to keep track of how much time I spend on various activities throughout the day (reading, studying, etc.) and all the data is saved to a csv file (hours.csv) that I can then analyze with R or Python. I run the app through Apple's Terminal. 

Baby Names (R): Takes all of the name counts for Males and Females back to 1880 and provides three possible outputs from the baby function. 
  input = <text>
  
  fun = "pop_num" - shows a graph of aggregate <name> counts through time. 
        "pop_prop" - shows a graph of proportion of <name> counts through time. 
        "ex_num" - shows a list of the top 20 most popular names in time period. If input is a letter, it will show only names in that letter.
  
  gender = "M" - Male
          "F" - Female
          "both" - Male and Female
  
  year = c(start date, end date). If you want only one year, input the same value twice. 
  
  Examples: baby(input = "Benjamin", fun = "pop_num", gender = "M", year = c(1880,2014))
            baby(input = "C", fun = "ex_num", gender = "both", year = c(1880, 2010))
            baby(input = "Nathan", fun = "pop_prop", gender = "F", year = c(2014, 2014))
            

rm(list=ls())
setwd("~/Desktop/Programming/")

#Load Packages. 

library("dplyr")
library("ggplot2")
library("reshape2")

####Clean Data####

#Read in the data. 

teams = read.csv("Teams.csv", header = TRUE, sep = ",")
results = read.csv("TourneyCompactResults.csv", header = TRUE, sep = ",")
seeds = read.csv("TourneySeeds.csv", header = TRUE, sep = ",")
slots = read.csv("TourneySlots.csv", header = TRUE, sep = ",")

data = select(results, Season, Wteam, Wscore, Lteam, Lscore)

#Add winning team seed and losing team seed to data. 

year = 1985:2015
d = data.frame()
for (i in year) {
  for (j in length(year)) {
    x = filter(data, Season == i)
    y = filter(seeds, Season == i)
    
    a = data.frame(y[match(x$Wteam, y$Team), 2])
    b = data.frame(y[match(x$Lteam, y$Team), 2])
    
    c = cbind(i, a, b)
    d = rbind(d,c)
  }
}

names(d) = c("Season", "Wseed", "Lseed")

data = data.frame(data$Season, data$Wteam, d$Wseed, data$Wscore, data$Lteam, d$Lseed, data$Lscore)

#Change the names of the data dataframe. 

names(data) = c("Season", "Wteam", "Wseed", "Wscore", "Lteam", "Lseed", "Lscore")

#Add the region each team is in. 

data = mutate(data, Wregion = substr(data$Wseed, 1, 1)) %>%
  mutate(Lregion = substr(data$Lseed, 1, 1))

#Rearrange to they're in order. 

data = select(data, Season, Wteam, Wseed, Wregion, Wscore, Lteam, Lseed, Lregion, Lscore)

#Remove the region from the seeding. 

data$Wseed = substring(data$Wseed, 2)
data$Lseed = substring(data$Lseed, 2)

#Take off the a's and b's from the seeding. 

data$Wseed = if (nchar(data$Wseed > 2)) {
  substr(data$Wseed, 1, 2)
}

data$Lseed = if (nchar(data$Lseed > 2)) {
  substr(data$Lseed, 1, 2)
}

#Change all seeding to numeric. 

data$Lseed = as.numeric(data$Lseed)
data$Wseed = as.numeric(data$Wseed)

str(data)

#Change Wteam, Lteam, and Region to factor.

data$Wteam = as.factor(data$Wteam)
data$Lteam = as.factor(data$Lteam)
data$Wregion = as.factor(data$Wregion)
data$Lregion = as.factor(data$Lregion)

str(data)

rm(a)
rm(b)
rm(c)
rm(d)
rm(x)
rm(y)

#Add the Round: 1, 2, 3, 4, 5, 6. to data.

#134 = Pre Round = 0 
#136 - 137 = 1st Round = 1 
#138 - 139 = 2nd Round = 2
#143 - 144 = Elite Eight = 3
#145-146 = Final Four = 4 
#152 = Semi-Final = 5
#154 = Final = 6

results$Round = NA
x = data.frame()
y = data.frame()

for (i in 1:1983) {
  x = results[i,]
  
  if (x$Daynum == 134) {
    x$Round = 0
  } else if (x$Daynum == 136 | x$Daynum == 137) {
    x$Round = 1
  } else if (x$Daynum == 138 | x$Daynum == 139) {
    x$Round = 2
  } else if (x$Daynum == 143 | x$Daynum == 144) {
    x$Round = 3
  } else if (x$Daynum == 145 | x$Daynum == 146) {
    x$Round = 4
  } else if (x$Daynum == 152) {
    x$Round = 5
  } else if (x$Daynum == 154) {
    x$Round = 6
  }
  y = rbind(y, x)
}

results = y

data = cbind(data, Round = results$Round)

#Change all NA's to Round 0. They're only play in matches on different days. 

data$Round[is.na(data$Round)] = 0

#Add the point margin to the end of data. 

data = mutate(data, pt_diff = Wscore - Lscore)

rm(x)
rm(y)

####Graphs####

#Density of seed wins and losses. 

win_loss = select(data, Season, Wseed, Lseed, Round) 
win_loss = melt(data = win_loss, id.vars = c("Season", "Round"))
names(win_loss) = c("Season", "Round", "W_L", "Seed")

#W/L Density

ggplot(win_loss, aes(x = Seed)) + geom_density(aes(color = W_L)) + 
  ggtitle("W/L Seeds") + labs(x = "Seed", y = "Density", color = "Win/Lose") + theme_bw()

#Seed Density

ggplot(filter(win_loss, Round >=1), aes(x = Seed)) + geom_density(aes(color = as.factor(Round))) +
  ggtitle("Seeds in Each Round of Tournament 1985-2015") + 
  labs(x = "Seed", y = "Density", color = "Round") + theme_bw()

ggplot(filter(win_loss, Season >= 2000 & Round >= 1), aes(x = Seed)) + geom_density(aes(color = as.factor(Round))) +
  ggtitle("Seeds in Each Round of Tournament 2000-2015") + 
  labs(x = "Seed", y = "Density", color = "Round") + theme_bw()

#Function showing seed density - select year range, round range, and outcome. 

seed_density = function(dat, season, round, outcome = "win") {
  year = as.numeric(season)
  temp_1  = data.frame()
  temp_2= data.frame()
  
  temp_1 = filter(dat, Season %in% season) 
  data_temp = filter(temp_1, Round %in% round)
  
  if (outcome == "win") {
    data_temp = filter(data_temp, W_L == "Wseed")
  } else if (outcome == "loss") {
    data_temp = filter(data_temp, W_L == "Lseed")
  } else if (outcome == "both") {
    data_temp = data_temp
  } else {
  }
  
  plot = ggplot(data_temp, aes(x = Seed)) + geom_density(aes(color = as.factor(Round))) + 
    ggtitle((paste("Seeds in Tournament Rounds ", min(year),"-", max(year), sep = ""))) + 
    labs(x = "Seed", y = "Density", color = "Round") + theme_bw()
  
  return(plot)
  
}

seed_density(win_loss, season = 1985:2015, round = 1:6, outcome = "both")

#Function to show seed matchups by round. 

ggplot(data, aes(x = Wseed, y = Lseed)) + geom_jitter(aes(color = as.factor(Round))) + 
  scale_x_continuous(breaks = scales::pretty_breaks(n = 15)) +
  scale_y_continuous(breaks = scales::pretty_breaks(n = 15)) + 
  labs(x = "Winning Seed", y = "Losing Seed", color = "Rounds") +
  theme_bw()

seed_matchup = function(dat, season, round) {
  temp = filter(dat, Season %in% season) %>%
    filter(Round %in% round)
  
  plot =  ggplot(temp, aes(x = Wseed, y = Lseed)) + geom_jitter(aes(color = as.factor(Round))) + 
    scale_x_continuous(breaks = scales::pretty_breaks(n = 15)) +
    scale_y_continuous(breaks = scales::pretty_breaks(n = 15)) + 
    labs(x = "Winning Seed", y = "Losing Seed", color = "Rounds") + 
    ggtitle((paste("Seed Matchups ", min(season),"-", max(season), sep = ""))) +
    theme_bw()
  
  
  return(plot)
}

seed_matchup(data, 2000:2015, 0:6)

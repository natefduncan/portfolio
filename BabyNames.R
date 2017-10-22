rm(list=ls())
setwd("~/Desktop/Programming/")

library("dplyr")

data = read.table("NationalNames.csv", header = TRUE, sep = ",")
year = 1880:2014

#Clean up the data.

data = select(data, Name, Year, Gender, Count)
male_temp = vector()
fem_temp = vector()

for (i in 1:135) {
  t <- filter(data, Year == year[i]) 
  aggregate(Count ~ Gender, data = t, FUN = sum) #2,2 = M, 1,2 = F
  male_temp[i] <- aggregate(Count ~ Gender, data = t, FUN = sum)[2,2]
  fem_temp[i] <- aggregate(Count ~ Gender, data = t, FUN = sum)[1,2]
}

totals <- data.frame(Year = year, m = male_temp, f = fem_temp)
totals <- mutate(totals, total = m + f)

rm(t)
rm(fem_temp)
rm(male_temp)
rm(i)

#Name popularity over time, letter popularity over time, most popular names for given year.

baby <- function(input, fun, 
                  gender = "both", year = c(1880, 2014)) {
  
  if (fun == "pop_num") {
   temp <- filter(data, Name == input) %>%
     filter(Year >= year[1] & Year <= year[2])
  if (gender != "both") {
   temp <- filter(temp, Gender == gender)
  } 
   temp <- select(temp, Year, Count)
   temp <- aggregate(Count ~ Year, data = temp, FUN = sum)
   return(plot(temp, type = "l", main = paste("Popularity of name '", input,"'", 
      sep = "")))
  }
  
  if (fun == "pop_prop") {
    temp <- filter(data, Name == input) %>%
      filter(Year >= year[1] & Year <= year[2])
    temp_tot <- totals
    if (gender != "both") {
      temp <- filter(temp, Gender == gender)
      temp_tot$total <- totals[, tolower(gender)]
    } 
    temp <- select(temp, Year, Count)
    temp <<- aggregate(Count ~ Year, data = temp, FUN = sum)
    temp_tot <<- temp_tot[temp_tot$Year %in% temp$Year,]
    temp$Count <- temp$Count / temp_tot$total
    return(plot(temp, type = "l", main = paste("Popularity of name '", input,"'", 
                                               sep = "")))
  }
  
  if (fun == "ex_num") {
    
    temp <- filter(data, Year >= year[1] & Year <= year[2])
    if (gender != "both") {
      temp <- filter(temp, Gender == gender)
    }
    if (nchar(input) == 1) {
    temp <- temp[(substring(temp[,1], 1, 1) == input),]
    }
    temp <- arrange(aggregate(Count ~ Name, data = temp, FUN = sum), desc(Count))
    
    return(temp[1:20,])
  }

} 

baby(input = "Nathan", fun = "pop_num", gender = "M", year = c(1880,2014))

library(maps)
library(usmap)
library(dplyr)
library(tigris)
library(ggplot2)
library(stringr)
library(mapproj)
library(blscrapeR)
library(prismatic)

ca2020 <- read.csv("Documents/MuddyCA2020.csv") %>% as_tibble()
ca2020_calc <- ca2020 %>% 
    group_by(County) %>% 
    summarise(Total_Votes = sum(Votes)) %>%
    left_join(ca2020) %>%
    select(County, Candidate, Party, Votes, Total_Votes) %>%
    mutate(Pct = Votes/Total_Votes)

ca2020_calc %>% 
    group_by(County) %>% 
    summarise(
        winner = ca2020_calc$Party[ca2020_calc$Pct == max(Pct)]
        )

ca2020_calc2 <- 
    ca2020_calc %>% 
    filter(Party %in% c('DEM', 'REP')) %>%
    group_by(County) %>% 
    summarise(AdjTotal=sum(Votes)) %>% 
    left_join(ca2020_calc) %>% 
    mutate(
        AdjPct = Votes/AdjTotal,
        Vmargin = abs(2*Votes - AdjTotal),
        Pmargin = abs(2*AdjPct - 1)
        ) %>%
    filter(AdjPct >= 0.50) %>%
    select(County, Party, Vmargin, Pmargin, AdjTotal)

maps::area.map
m = map("county", "california,*", fill = TRUE, plot = FALSE, projection = "azequalarea")
area.map(m, regions=m$names, sqmi=TRUE)

county_map_data
#need area in sq mi or sq km of each county

us_map <- county_map_data
ggplot() +
    geom_map(
        data = us_map,
        map = us_map,
        aes(
            x=long,
            y=lat,
            map_id=id,
            group=group,
            fill="#ffffff",
            color="#0e0e0e",
            linewidth=0.15)
        )

m = map(
    'county', 
    'california', 
    fill=TRUE, 
    col=palette(), 
    plot=FALSE
    )


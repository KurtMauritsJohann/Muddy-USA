library(maps)
library(usmap)
library(dplyr)
library(tigris)
library(ggplot2)
library(stringr)
library(mapproj)
library(snakecase)
library(blscrapeR)
library(prismatic)
library(plotwidgets)

ca2020 <- read.csv("Documents/MuddyCA2020.csv") %>% as_tibble()
ca2020_calc <- ca2020 #%>% 
    # group_by(County) %>% 
    # summarise(Total_Votes = sum(Votes)) %>%
    # left_join(ca2020) %>%
    # select(County, Candidate, Party, Votes, Total_Votes) %>%
    # mutate(Pct = Votes/Total_Votes)

# ca2020_calc %>% 
#     group_by(County) %>% 
#     summarise(
#         winner = ca2020_calc$Party[ca2020_calc$Pct == max(Pct)]
#         )

ca2020_calc2 <- 
    ca2020_calc %>% 
    filter(Party %in% c('DEM', 'REP')) %>%
    group_by(County) %>% 
    summarise(AdjTotal=sum(Votes)) %>% 
    left_join(ca2020_calc) %>% 
    mutate(
        AdjPct = Votes/AdjTotal,
        #Vmargin = abs(2*Votes - AdjTotal),
        Pmargin = abs(2*AdjPct - 1)
        ) %>%
    filter(AdjPct >= 0.50) %>%
    select(County, Party, Pmargin, AdjTotal)

ca2020_calc2 <- 
    ca2020_calc %>% 
    mutate(
        AdjPct = Votes/AdjTotal, 
        Pmargin = abs(2 * AdjPct - 1)
        ) %>% 
    filter(AdjPct >= 0.50) %>% 
    select(County, Party, Pmargin, AdjTotal)

m = map(
    "county", 
    "california,*", 
    fill = TRUE, 
    plot = FALSE, 
    projection = "azequalarea"
    )

countyarea <- 
    area.map(
        m, 
        regions=m$names, 
        sqmi=TRUE
        ) %>% as.data.frame()

colnames(countyarea) <- "Area" #square miles
countyarea$County <- rownames(countyarea)
rownames(countyarea) <- 1:nrow(countyarea)
countyarea <- countyarea %>% select(County, Area)

ca2020_calc2 <- 
    ca2020_calc2 %>% 
    mutate(
        County = paste0(
            "california,", 
            tolower(County)
            )
        ) %>%
    left_join(countyarea) %>%
    mutate(
        Vdensity = AdjTotal/Area
        ) %>%
    select(County, Party, Pmargin, Vdensity)

#upperfence of vote density for all US counties in 2020: 50.66 sq km = 19.56 sq mi
upperfence = 19.56
#upper fence: Q3 + 3 * IQR
#summary(ca2020_calc2$Vdensity)
#IQR(ca2020_calc2$Vdensity)

#muddycolor = hsl2col(
#clr_extract_hue(ifelse(ca2020_piv2$Candidate == "Biden", "#0000ff", "#ff0000")),
#ca2020_piv2$Pmargin,
#ifelse((2 - ca2020_piv2$Vdensity/upperfence) * 50 <= 50, 50, (2 - ca2020_piv2$Vdensity/upperfence) * 50) / 100
#)
#hue: red or blue
#saturation: % margin of victory (Dem % + Rep % only) (0-100%)
#lightness: vote density up to upper fence, adjusted to % (Dem + Rep votes only) (50-100%)
#(2 - Vdensity/upperfence) * 50

mapcol <- matrix(
    c(
        clr_extract_hue(
            ifelse(
                ca2020_calc2$Party == 'DEM', 
                '#0000ff', 
                '#ff0000'
                )
            ),
        ca2020_calc2$Pmargin,
        ifelse(
            (2 - ca2020_calc2$Vdensity/upperfence) * 50 <= 50, 
            50, 
            (2 - ca2020_calc2$Vdensity/upperfence) * 50
            ) / 100
    ),
    ncol = 3
    ) %>%
    t() %>%
    hsl2col()

m1 = map(
  "county", 
  regions = ca2020_calc2$County, 
  #projection = "azequalarea",
  fill = TRUE, 
  col = mapcol,
  plot = TRUE, 
  #border = 
  )

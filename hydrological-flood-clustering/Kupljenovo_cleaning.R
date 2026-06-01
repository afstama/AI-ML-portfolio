library(readr)
library(tidyverse)
library(lubridate)
library(ggplot2)
library(zoo)
library(fda)
library("writexl")
library(lfstat)

INPUT_FILE <- "Kupljenovo_dnevniQ-1964-2021.csv"
df <- read_csv(INPUT_FILE)


# pretvaranje datuma u čitljiv format, ako je flow == Na, onda postavljam flow = 0

names(df) <- c("date", "flow")
df <- df[-1, ]
df <- df[-1, ]
df %>% mutate(date = as.Date(date, "%d.%m.%Y"),
              flow = ifelse(is.na(flow), 0, substr(flow, 1, nchar(flow)-1))) -> df


# računanje baznog dotoka

data <- data.frame(day=as.numeric(format(df$date,format="%d")),
                   month=as.numeric(format(df$date,format="%m")),
                   year=as.numeric(format(df$date,format="%Y")),
                   flow=df$flow,
                   date=df$date)


Kupljenovo_bf <- createlfobj(data, hyearstart=10, baseflow=TRUE)
plot(Kupljenovo_bf$flow, type="l")
lines(Kupljenovo_bf$baseflow, col=2)

df <- as.data.frame(Kupljenovo_bf)
df %>% mutate(date = make_date(year = year, month = month, day = day)) -> df
df$day <- NULL
df$month <- NULL
df$year <- NULL
colnames(df)[2] = "h_year"
df <- df[, c(4,2,1,3)]
write.csv(df, "Kupljenovo_dnevniQ_1960_2019_clean.csv")


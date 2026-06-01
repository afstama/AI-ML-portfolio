library(readr)
library(tidyverse)
library(lubridate)
library(ggplot2)
library(zoo)
library(fda)
library("writexl")
library(lfstat)

INPUT_FILE <- "Kupljenovo_dnevniQ_1960_2019_clean.csv"
df <- read_csv(INPUT_FILE)

df$season = as.character(NA)
df[(month(df$date) %in% 4:5) | (month(df$date) == 3 & day(df$date) >= 21) | (month(df$date) == 6 & day(df$date) <=20), ]$season <- "spring"
df[(month(df$date) %in% 7:8) | (month(df$date) == 6 & day(df$date) >= 21) | (month(df$date) == 9 & day(df$date) <=22), ]$season <- "summer"
df[(month(df$date) %in% 10:11) | (month(df$date) == 9 & day(df$date) >= 23) | (month(df$date) == 12 & day(df$date) <=20), ]$season <- "fall"
df[(month(df$date) %in% 1:2) | (month(df$date) == 12 & day(df$date) >= 21) | (month(df$date) == 3 & day(df$date) <=20), ]$season <- "winter"

df <- filter(df, !is.na(baseflow))
df$flowdiff <- df$flow - df$baseflow


# peaks

df %>% filter(flow > 100) %>% group_by(h_year) %>% summarise(date = date, flow = max(flow)) -> dfMax
dfMax %>% group_by(h_year) %>% summarise(date = min(date), flowDesc = "peak", flowDay = 0) %>% full_join(df) -> df
df %>% filter(!is.na(flowDesc)) %>% mutate(peak_number = 1:n()) %>% full_join(df) -> df

#df %>% filter(flow > 100) %>% group_by(h_year) %>% summarise(flow = max(flow), flowDesc = "peak") %>% mutate(flowDay = 0, peak_number = 1:n()) -> dfMax
df %>% filter(h_year == 2000) %>% ggplot(aes(x = date, y = flowdiff)) + geom_line()


# segments

#df_temp <- df
df <- df_temp

peakDates <- filter(df, !is.na(flowDesc)) %>% pull(date) %>% as.character
peak_num <- 0

for (peak in peakDates) {
  peak <- as.Date(peak)
  peak_num <- peak_num + 1
  
  # looking for waveStart, leftSegment
  
  df %>% filter(df$date < peak & round(flowdiff, 0) <= 100) %>% pull(date) -> lowdiff_dates
  lowdiffIndex <- which(abs(lowdiff_dates-peak) == min(abs(lowdiff_dates-peak)))
  
  if (!is.na(df[df$date == lowdiff_dates[lowdiffIndex], ]$flowDesc)) {
    print(lowdiff_dates[lowdiffIndex])
    df %>% filter(df$date < peak & round(flowdiff, 0) <= 100 & df$date != lowdiff_dates[lowdiffIndex]) %>% pull(date) -> lowdiff_dates
    lowdiffIndex <- which(abs(lowdiff_dates-peak) == min(abs(lowdiff_dates-peak)))
    peak_num <- peak_num - 1
    print(lowdiff_dates[lowdiffIndex])
  }
  
  waveStart <- lowdiff_dates[lowdiffIndex]
  
  df %>% mutate(is.date = date < peak & date >= waveStart,
                flowDesc = ifelse(is.date, "leftSegment", flowDesc),
                h_year = ifelse(is.date, df[df$date == peak, ]$h_year, h_year),
                peak_number = ifelse(is.date, peak_num, peak_number),
                flowDay = ifelse(is.date, as.numeric(date-peak), flowDay)) -> df
  df[df$date == waveStart, ]$flowDesc <- "waveStart"
  
  # looking for waveEnd, rightSegment
  
  df %>% filter(df$date > peak & round(flowdiff, 0) <= 100) %>% pull(date) -> lowdiff_dates
  lowdiffIndex <- which(abs(lowdiff_dates-peak) == min(abs(lowdiff_dates-peak)))
  
  waveEnd <- lowdiff_dates[lowdiffIndex]
  
  df %>% mutate(is.date = date > peak & date <= waveEnd,
                flowDesc = ifelse(is.date, "rightSegment", flowDesc),
                h_year = ifelse(is.date, df[df$date == peak, ]$h_year, h_year),
                peak_number = ifelse(is.date, peak_num, peak_number),
                flowDay = ifelse(is.date, as.numeric(date-peak), flowDay)) -> df
  df[df$date == waveEnd, ]$flowDesc <- "waveEnd"
}
df$is.date <- NULL

#df %>% filter(flowDesc == "waveStart" | flowDesc == "waveEnd") -> df_help

# exstensions

#df_checkpoint_1 <- df
df <- df_checkpoint_1

leftmostDay <- df %>% filter(flowDesc=="waveStart") %>% pull(flowDay) %>% min
rightmostDay <- df %>% filter(flowDesc=="waveEnd") %>% pull(flowDay) %>% max

waveStartDates <- df %>% filter(flowDesc == "waveStart") %>% pull(date) %>% as.character
waveEndDates <- df %>% filter(flowDesc == "waveEnd") %>% pull(date) %>% as.character

for (d in waveStartDates) {
  dd <- as.Date(d)
  yearNo <- df %>% filter(date == d) %>% pull(h_year)
  peakNo <- df %>% filter(date == d) %>% pull(peak_number)
  leftDay <- df %>% filter(date == d) %>% pull(flowDay)
  print(str_c(yearNo, peakNo, leftDay, sep = " "))
  
  while (leftDay > leftmostDay) {
    leftDay <- leftDay - 1
    dd <- dd - 1
    df %>% mutate(is.date = date == dd,
                  flowDesc = ifelse(is.date, "extensionLeft", flowDesc), 
                  peak_number = ifelse(is.date, peakNo, peak_number),
                  h_year = ifelse(is.date, yearNo, h_year),
                  flowDay = ifelse(is.date, leftDay, flowDay),
                  flowdiff = ifelse(is.date, 0, flowdiff)) -> df
  }
}

for (d in waveEndDates) {
  dd <- as.Date(d)
  yearNo <- df %>% filter(date == d) %>% pull(h_year)
  peakNo <- df %>% filter(date == d) %>% pull(peak_number)
  rightDay <- df %>% filter(date == d) %>% pull(flowDay)
  print(str_c(yearNo, peakNo, rightDay, sep = " "))
  
  while (rightDay < rightmostDay) {
    rightDay <- rightDay + 1
    dd <- dd + 1
    df %>% mutate(is.date = date == dd,
                  flowDesc = ifelse(is.date, "extensionRight", flowDesc), 
                  peak_number = ifelse(is.date, peakNo, peak_number),
                  h_year = ifelse(is.date, yearNo, h_year),
                  flowDay = ifelse(is.date, rightDay, flowDay),
                  flowdiff = ifelse(is.date, 0, flowdiff)) -> df
  } 
}

df$is.date <- NULL


# removing rows without waves

#df_checkpoint2 <- df
df <- df_checkpoint2

#df %>% filter(!is.na(flowDesc)) %>% group_by(h_year) %>% summarise(min = min(flowDay), max = max(flowDay)) -> df_help

df <- filter(df, !is.na(flowDesc))
# ovo zapravo ne treba na ovom datasetu jer su datumi ok, ali nek stoji radi potpunosti
df %>% group_by(h_year) %>% summarise(min = min(flowDay), max = max(flowDay)) %>% filter(min != leftmostDay | max != rightmostDay ) %>% pull(h_year) -> removeYears
df %>% filter(!h_year %in% removeYears) -> df

#df_checkpoint_3 <- df
df <- df_checkpoint_3


# exploratory analysis

write_xlsx(df, "Kupljenovo_dnevniQ_1964_2021_exp_filt_reshaped.xlsx")

df %>% ggplot(aes(x = flowDay, y = flowdiff, col = as.factor(peak_number))) + geom_line() + theme(legend.position = "none")
df %>% ggplot(aes(x = flowDay, y = flowdiff)) + geom_line() + facet_wrap(~h_year,  ncol=10)

# y-value normalization

AUC <- function(x, y) {
  abs(sum(diff(x)*rollmean(y,2)))
}
df %>% group_by(h_year) %>% summarise(auc = AUC(flowDay, flowdiff)) %>% full_join(df) -> df
df$flowScaled <- df$flowdiff / df$auc
df %>% ggplot(aes(x = flowDay, y = flowScaled)) + geom_line() + facet_wrap(~h_year,  ncol=10)


# B-splines

POINTS <- rightmostDay-leftmostDay+1

Bspline.basis.4 <- create.bspline.basis(c(0, POINTS), 4)
Bspline.basis.10 <- create.bspline.basis(c(0, POINTS), 10)
fourier.basis.4 <- create.fourier.basis(c(0, POINTS), 4)
fourier.basis.10 <- create.fourier.basis(c(0, POINTS), 10)

# sanity check

obs <- df %>% filter(h_year == 1972) %>% pull(flowScaled)
flow.fd.1960.b4 <- smooth.basis(y = obs, fdParobj=Bspline.basis.4)
flow.fd.1960.b10 <- smooth.basis(y = obs, fdParobj=Bspline.basis.10)
flow.fd.1960.f4 <- smooth.basis(y = obs, fdParobj=fourier.basis.4)
flow.fd.1960.f10 <- smooth.basis(y = obs, fdParobj=fourier.basis.10)
plot(obs)
lines(flow.fd.1960.b4, col = "red")
lines(flow.fd.1960.b10, col = "blue")
lines(flow.fd.1960.f4, col = "purple")
lines(flow.fd.1960.f10, col = "green")

# sanity check 2

obs <- df %>% filter(h_year == 1989) %>% pull(flowScaled)
flow.fd.1982.b4 <- smooth.basis(y = obs, fdParobj=Bspline.basis.4)
flow.fd.1982.b10 <- smooth.basis(y = obs, fdParobj=Bspline.basis.10)
flow.fd.1982.f4 <- smooth.basis(y = obs, fdParobj=fourier.basis.4)
flow.fd.1982.f10 <- smooth.basis(y = obs, fdParobj=fourier.basis.10)
plot(obs)
lines(flow.fd.1982.b4, col = "red")
lines(flow.fd.1982.b10, col = "blue")
lines(flow.fd.1982.f4, col = "purple")
lines(flow.fd.1982.f10, col = "green")

# graphs
obsAll <- df %>% pull(flowScaled) %>% matrix(ncol = POINTS, byrow = T)
flow.fd <- smooth.basis(y = t(obsAll), fdParobj=fourier.basis.10)
plot(flow.fd)

wavesCoef.fourier <- as_tibble(t(coef(flow.fd)))
flow.fd <- smooth.basis(y = t(obsAll), fdParobj=Bspline.basis.10)
plot(flow.fd)

wavesCoef.bspline <- as_tibble(t(coef(flow.fd)))


# K-means clustering

k3 <- kmeans(wavesCoef.fourier, centers = 3, nstart = 25)
clustersFourier <- k3$cluster

k3 <- kmeans(wavesCoef.bspline, centers = 3, nstart = 25)
clustersBspline <- k3$cluster

df %>% filter(flowDesc == "peak") %>% dplyr::select(peak_number) %>% 
  mutate(clusterFourier = as.factor(clustersFourier),
         clusterBspline = as.factor(clustersBspline)) %>% full_join(df) -> df

df %>% ggplot(aes(x = flowDay, y = flowScaled, col = clusterFourier)) + geom_line() + facet_wrap(~h_year,  ncol=10)
df %>% ggplot(aes(x = flowDay, y = flowdiff, col = clusterBspline)) + geom_line() + facet_wrap(~h_year,  ncol=10)

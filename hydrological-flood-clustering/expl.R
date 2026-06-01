library(readr)
library(tidyverse)
library(lubridate)
library(ggplot2)
library(zoo)
library(fda)
library("writexl")

# loading data

INPUT_FILE <- "Zagreb_dnevniQ-1960-2019.csv"
INPUT_FILE_BASEFLOW <- "Zagreb_baseflow.csv"
df <- read_csv(INPUT_FILE)
df_base <- read_csv(INPUT_FILE_BASEFLOW)


# transforming columns, removing NA rows, translating year
# e.g. if hydrological_year=2022/2023 then h_year=2023

names(df) <- c("date", "flow")
df$date <- dmy(df$date)
df$h_year <- year(df$date)
df[month(df$date) >= 10, ]$h_year <- df[month(df$date) >= 10, ]$h_year + 1

df$baseflow <- df_base$baseflow
df <- filter(df, !is.na(baseflow))
df$flowdiff <- df$flow - df$baseflow


# finding peaks and adding to df

df %>% group_by(h_year) %>% summarise(flow = max(flow), flowDesc = "peak") %>% mutate(flowDay = 0, peak_number = 1:n()) -> dfMax
df %>% full_join(dfMax) -> df
#df %>% ggplot(aes(x = date, y = flowdiff)) + geom_line()



# assigning segments

#df_temp <- df
df <- df_temp

peakDates <- filter(df, !is.na(flowDesc)) %>% pull(date) %>% as.character
peak_num <- 0

for (peak in peakDates) {
  peak <- as.Date(peak)
  peak_num <- peak_num + 1

  # looking for waveStart, leftSegment
  
  df %>% filter(df$date < peak & round(flowdiff, 0) == 0) %>% pull(date) -> lowdiff_dates
  lowdiffIndex <- which(abs(lowdiff_dates-peak) == min(abs(lowdiff_dates-peak)))
  
  if (!is.na(df[df$date == lowdiff_dates[lowdiffIndex], ]$flowDesc)) {
    print(lowdiff_dates[lowdiffIndex])
    df %>% filter(df$date < peak & round(flowdiff, 0) == 0 & df$date != lowdiff_dates[lowdiffIndex]) %>% pull(date) -> lowdiff_dates
    lowdiffIndex <- which(abs(lowdiff_dates-peak) == min(abs(lowdiff_dates-peak)))
    peak_numb <- peak_num - 1
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
  
  df %>% filter(df$date > peak & round(flowdiff, 0) == 0) %>% pull(date) -> lowdiff_dates
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

# lengthening wave tails -> we want them uniform

#df_checkpoint_1 <- df
df <- df_checkpoint_1

leftmostDay <- df %>% filter(flowDesc=="waveStart") %>% pull(flowDay) %>% min
rightmostDay <- df %>% filter(flowDesc=="waveEnd") %>% pull(flowDay) %>% max


# assigning leftExstension, rightExtension

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

#df_checkpoint_2 <- df
df <- df_checkpoint_2

df <- filter(df, !is.na(flowDesc))
df %>% group_by(h_year) %>% summarise(min = min(flowDay), max = max(flowDay)) %>% filter(min != leftmostDay | max != rightmostDay ) %>% pull(h_year) -> removeYears
df %>% filter(!h_year %in% removeYears) -> df
#df %>% group_by(h_year) %>% summarise(min = min(flowDay), max = max(flowDay)) %>% filter(min != leftmostDay | max != rightmostDay ) %>% pull(h_year)

#df_checkpoint_3 <- df
df <- df_checkpoint_3



# Exploratory analysis

write_xlsx(df, "Zagreb_dnevniQ_1960_2019_exp_filt_reshaped.xlsx")

df %>% ggplot(aes(x = flowDay, y = flowdiff, col = as.factor(peak_number))) + geom_line() + theme(legend.position = "none")
df %>% ggplot(aes(x = flowDay, y = flowdiff)) + geom_line() + facet_wrap(~h_year,  ncol=10)


# y-value normalization

AUC <- function(x, y) {
  sum(diff(x)*rollmean(y,2))
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

obs <- df %>% filter(h_year == 1960) %>% pull(flowScaled)
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

obs <- df %>% filter(h_year == 1964) %>% pull(flowScaled)
flow.fd.1960.b4 <- smooth.basis(y = obs, fdParobj=Bspline.basis.4)
flow.fd.1960.b10 <- smooth.basis(y = obs, fdParobj=Bspline.basis.10)
flow.fd.1960.f4 <- smooth.basis(y = obs, fdParobj=fourier.basis.4)
flow.fd.1960.f10 <- smooth.basis(y = obs, fdParobj=fourier.basis.10)
plot(obs)
lines(flow.fd.1960.b4, col = "red")
lines(flow.fd.1960.b10, col = "blue")
lines(flow.fd.1960.f4, col = "purple")
lines(flow.fd.1960.f10, col = "green")

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

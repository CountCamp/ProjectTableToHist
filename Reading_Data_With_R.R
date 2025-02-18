################################################################################
################################################################################
################################################################################
##################### Reading and Transforming Data ############################
################################################################################
################################################################################
################################################################################


# Set seed for reproducability:
set.seed(1975)

# Set working directory
setwd("~/Desktop/ManimProjects/ProjectTableToHist/Data")

library(tidyverse)
library(haven)
qol_data <- read_sav("qol_data.sav")
kvl_data <- qol_data %>% 
  select(sex, QoL) %>% 
  group_by(sex) %>% 
  sample_n(50) %>% 
  ungroup() %>% 
  mutate(QoL = round(QoL, digits = 0),
         Condition = factor(sex, 
                            levels = c(0,1),
                            labels = c("Short Walk", "Mindfullness"))) %>% 
  sample_frac(1) %>% 
  mutate(id = 1:n()) %>% 
  select(id, Condition, QoL)
  
# Look at DataFrame
glimpse(kvl_data)  

# Saving File:
write.csv(kvl_data, "kvl_data.csv", row.names = FALSE)

# Create very skewed data file for one group:
kvl_data

# Update specific QoL values based on ID
kvl_skew_data <- kvl_data %>%
  mutate(QoL = case_when(
    id == 45 ~ 27,  
    id == 27 ~ 34,  
    id == 97 ~ 32, 
    id == 17 ~ 41,
    TRUE ~ QoL       # Keep all other values unchanged
  ))

write.csv(kvl_skew_data, "kvl_skew_data.csv", row.names = FALSE)

#!/usr/bin/env python
# coding: utf-8

# ### Note
# * Instructions have been included for each segment. You do not have to follow them exactly, but they are included to help you think through the steps.

# In[1]:


# Dependencies
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


# In[2]:


# Load in file
purchase_data = "Resources/purchase_data.csv"

# Read Heroes of Pymoli purchase data and store into Pandas data frame
HOP_purchase_data = pd.read_csv(purchase_data)
HOP_purchase_data.head()


# ## Player Count

# * Display the total number of players
# 

# In[3]:


#use the .nunique command to find all unique instances of players and then display the count
player_count = HOP_purchase_data["SN"].nunique()
#we want to display the player count in dataframe format, so we need to place it into a dataframe and we can use
#a dictionary to hold the value
show_player_count = pd.DataFrame({"Total Number of Players":[player_count]})
show_player_count


# ## Purchasing Analysis (Total)

# * Run basic calculations to obtain number of unique items, average price, etc.
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame
# 

# In[4]:


#we want the number of unique items, avg price, number of purchases, and the total revenue
#we can use the item name and price columns to yield this using .nunique and .sum probably
unique_items = HOP_purchase_data["Item Name"].nunique()
average_purchase = HOP_purchase_data["Price"].mean()
number_of_purchases = len(HOP_purchase_data["Item Name"])
total_revenue = HOP_purchase_data["Price"].sum()
#since the number of purchases can include repeat purchases, we don't want to use unique counts

#make a df the same way as before
item_purchases = pd.DataFrame({"Number of Unique Items":[unique_items],
                              "Average Price":[average_purchase],
                              "Number of Purchases":[number_of_purchases],
                              "Total Revenue":[total_revenue]})

#for data cleaning we can use the mapping activity as a reference
item_purchases["Total Revenue"] = item_purchases["Total Revenue"].map("${:.2f}".format)
item_purchases["Average Price"] = item_purchases["Average Price"].map("${:.2f}".format)
item_purchases = item_purchases[["Number of Unique Items", "Average Price", "Number of Purchases", "Total Revenue"]]
item_purchases


# ## Gender Demographics

# * Percentage and Count of Male Players
# 
# 
# * Percentage and Count of Female Players
# 
# 
# * Percentage and Count of Other / Non-Disclosed
# 
# 
# 

# In[5]:


#from pandas documentation, we can use DataFrame.drop_duplicates to get rid of any duplicate entries
no_duplicates = HOP_purchase_data.drop_duplicates(subset = "SN", keep = "first", inplace=False)
total_people = no_duplicates["Gender"].count()
male_gender = no_duplicates["Gender"].value_counts()["Male"]
female_gender = no_duplicates["Gender"].value_counts()["Female"]
other_gender = total_people - male_gender - female_gender

#find the percent of players and then throw it in a df
percent_male = (male_gender/total_people)*100
percent_female = (female_gender/total_people)*100
percent_other = (other_gender/total_people)*100

gender_df = pd.DataFrame({" ":["Male", "Female", "Other/Non-Disclose"], "Total Count":[male_gender, female_gender, other_gender], 
                          "Percentage of Players":[percent_male, percent_female, percent_other]})
gender_df["Percentage of Players"] = gender_df["Percentage of Players"].map("{:.2f}%".format)
gender_df = gender_df.set_index(" ")
gender_df


# 
# ## Purchasing Analysis (Gender)

# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. by gender
# 
# 
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[6]:


#everything by gender, use groupby
grouped_gender = HOP_purchase_data.groupby(["Gender"])
purchase_count = grouped_gender["SN"].count()
avg_purchase_price = grouped_gender["Price"].mean()
total_purchase_value = grouped_gender["Price"].sum()

#we need to delete duplicates (if there are any) for the purchase per person then re-group the new data by gender
no_duplicates_2 = HOP_purchase_data.drop_duplicates(subset = "SN", keep = "first", inplace=False)
grouped_gender_no_duplicates = no_duplicates_2.groupby(["Gender"])
avg_total_purchase = grouped_gender["Price"].sum()/grouped_gender_no_duplicates["SN"].count()
#place into a df
all_gender_data_df = pd.DataFrame({"Purchase Count":purchase_count, "Average Purchase Price":avg_purchase_price,
                                  "Total Purchase Value":total_purchase_value, "Average Purchase Total Per Person":avg_total_purchase})
#clean the data with mapping
all_gender_data_df["Average Purchase Price"] = all_gender_data_df["Average Purchase Price"].map("${:.2f}".format)
all_gender_data_df["Total Purchase Value"] = all_gender_data_df["Total Purchase Value"].map("${:.2f}".format)
all_gender_data_df["Average Purchase Total Per Person"] = all_gender_data_df["Average Purchase Total Per Person"].map("${:.2f}".format)
all_gender_data_df = all_gender_data_df[["Purchase Count", "Average Purchase Price", "Total Purchase Value",
                                        "Average Purchase Total Per Person"]]
all_gender_data_df


# ## Age Demographics

# * Establish bins for ages
# 
# 
# * Categorize the existing players using the age bins. Hint: use pd.cut()
# 
# 
# * Calculate the numbers and percentages by age group
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: round the percentage column to two decimal points
# 
# 
# * Display Age Demographics Table
# 

# In[7]:


#Use bins to divide up age groups: <10, 10-14, 15-19, 20-24, 25-29, 30-34, 35-39, 40+
age_bins = [0, 9.9, 14.9, 19.9, 24.9, 29.9, 34.9, 39.9, 100]
bin_titles = ["Under 10", "10 to 14", "15 to 19", "20 to 24", "25 to 29", "30 to 34", "35 to 39", "Over 40"]
#Cut the bins up by age using pd.cut() to categorize
HOP_purchase_data["Age Groups"] = pd.cut(HOP_purchase_data["Age"], age_bins, labels = bin_titles)
agegroup_bins = HOP_purchase_data.groupby(["Age Groups"])
total_age = agegroup_bins["SN"].nunique()
#we can use the total players from the first cell for total and to calculate the percentages
percent_of_players = (total_age / player_count)*100
#create summary table
age_distributions = pd.DataFrame({"Total Count":total_age, "Percentage of Players":percent_of_players})
#round the percentage to two places with mapping
age_distributions["Percentage of Players"] = age_distributions["Percentage of Players"].map("{:.2f}%".format)
age_distributions


# ## Purchasing Analysis (Age)

# * Bin the purchase_data data frame by age
# 
# 
# * Run basic calculations to obtain purchase count, avg. purchase price, avg. purchase total per person etc. in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display the summary data frame

# In[8]:


#make purchase bins for categories: Purchase Count, Avg. Purchase Price, Total Purchase Value, Avg. Total Purchase Per Person
#we have already grouped by age in the prvious cell
purchase_count_age = agegroup_bins["Purchase ID"].nunique()
average_purchase_price_age = agegroup_bins["Price"].mean()
total_purchase_value_age = agegroup_bins["Price"].sum()
average_total_purchase_per_person_age = (total_purchase_value_age / total_age)
age_purchase_summary = pd.DataFrame({"Purchase Count":purchase_count_age,
                                    "Average Purchase Price":average_purchase_price_age,
                                    "Total Purchase Value":total_purchase_value_age,
                                    "Average Total Purchase Per Person":average_total_purchase_per_person_age})
#round all money columns to two
age_purchase_summary["Average Purchase Price"] = age_purchase_summary["Average Purchase Price"].map("${:.2f}".format)
age_purchase_summary["Total Purchase Value"] = age_purchase_summary["Total Purchase Value"].map("${:.2f}".format)
age_purchase_summary["Average Total Purchase Per Person"] = age_purchase_summary["Average Total Purchase Per Person"].map("${:.2f}".format)
age_purchase_summary


# ## Top Spenders

# * Run basic calculations to obtain the results in the table below
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the total purchase value column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[9]:


#create a summary table highlighting the top 5 spenders with:
#SN, Purchase Count, Average Purchase Price, Total Purchase Value
#we can do this the same way as before, but now we groupby the SN(screenname)
big_spenders = HOP_purchase_data.groupby(["SN"])
purchase_count_spenders = big_spenders["Purchase ID"].nunique()
average_purchase_price_spenders = big_spenders["Price"].mean()
total_purchase_value_spenders = big_spenders["Price"].sum()
top_spenders = pd.DataFrame({"Purchase Count":purchase_count_spenders,
                            "Average Purchase Price":average_purchase_price_spenders,
                            "Total Purchase Value":total_purchase_value_spenders})
#display top 5 spenders with sort_values()
biggest_spenders = top_spenders.sort_values(["Total Purchase Value"], ascending = False).head(5)
biggest_spenders["Average Purchase Price"] = biggest_spenders["Average Purchase Price"].map("${:.2f}".format)
biggest_spenders["Total Purchase Value"] = biggest_spenders["Total Purchase Value"].map("${:.2f}".format)
biggest_spenders


# ## Most Popular Items

# * Retrieve the Item ID, Item Name, and Item Price columns
# 
# 
# * Group by Item ID and Item Name. Perform calculations to obtain purchase count, item price, and total purchase value
# 
# 
# * Create a summary data frame to hold the results
# 
# 
# * Sort the purchase count column in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the summary data frame
# 
# 

# In[10]:


#Item ID, Item Name, Item Price, groupby the ID and Name
items_items = HOP_purchase_data[["Item ID", "Item Name", "Price"]]
grouped_items = HOP_purchase_data.groupby(["Item ID", "Item Name"])
purchase_count_items = grouped_items["Item Name"].count()
total_purchase_value_items = grouped_items["Price"].sum()
indiv_item_price = (total_purchase_value_items / purchase_count_items)
best_items = pd.DataFrame({"Purchase Count":purchase_count_items,
                            "Item Price":indiv_item_price,
                            "Total Purchase Value":total_purchase_value_items})
#the top 5 again
popular_items = best_items.sort_values(["Purchase Count"], ascending = False).head(5)
popular_items["Item Price"] = popular_items["Item Price"].map("${:.2f}".format)
popular_items["Total Purchase Value"] = popular_items["Total Purchase Value"].map("${:.2f}".format)
popular_items


# ## Most Profitable Items

# * Sort the above table by total purchase value in descending order
# 
# 
# * Optional: give the displayed data cleaner formatting
# 
# 
# * Display a preview of the data frame
# 
# 

# In[11]:


#just re-sort the table by total purchase value instead
popular_itemsv2 = best_items.sort_values(["Total Purchase Value"], ascending = False).head(5)
popular_itemsv2["Item Price"] = popular_itemsv2["Item Price"].map("${:.2f}".format)
popular_itemsv2["Total Purchase Value"] = popular_itemsv2["Total Purchase Value"].map("${:.2f}".format)
popular_itemsv2


# In[ ]:





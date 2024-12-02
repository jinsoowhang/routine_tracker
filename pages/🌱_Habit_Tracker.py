import streamlit as st
import pandas as pd
import numpy as np
import altair as alt
from datetime import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import seaborn as sns
import gspread
from datetime import timedelta
from oauth2client.service_account import ServiceAccountCredentials
from collections import Counter
from pytz import timezone
import pytz

# Initialize connection
conn = st.connection("postgresql", type="sql")

# Perform query.
df = conn.query('SELECT * FROM stg__rhythm;', ttl="10m")

###########################
####### Title Page ########
###########################

st.title("""🌱Habit Tracker""")

st.divider()

##############################
####### Data Cleaning ########
##############################

df['date'] = pd.to_datetime(df['rhythm_date']).dt.date

####################
####### UDF ########
####################

def addlabels(x, y):
    for i in range(len(x)):
        plt.text(x[i], y[i], y[i], fontsize=13, ha='center', va='bottom')

def addlabels2(x, y):
    for i in range(len(x)):
        plt.text(x[i], y[i], y[i], fontsize=13, ha='center', va='bottom', color='red')

def addlabels3(x, y):
    for i in range(len(x)):
        plt.text(x[i], y[i], y[i], fontsize=13, ha='center', va='bottom', color='blue')

def addrotatedlabels(x, y):
    for i in range(len(x)):
        plt.text(x[i], y[i], y[i], fontsize=13, ha='center', va='bottom', rotation='vertical')

def addrotatedlabels2(x, y):
    for i in range(len(x)):
        plt.text(x[i], y[i], y[i], fontsize=13, ha='center', va='bottom', rotation='vertical', color='red')

def addrotatedlabels3(x, y):
    for i in range(len(x)):
        plt.text(x[i], y[i], y[i], fontsize=13, ha='center', va='bottom', rotation='vertical', color='blue')

##########################
####### Variables ########
##########################

love = 3.0
study = 2.6
side_hustle = 2.4
work = 2.2
read = 1.9
exercise = 1.65
learn = 1.65
church = 1.5
productive = 1.2
meet = 1.2
call = 1.0
cook = 1.0
walk = 1.0
grocery = 0.9
clean = 0.9
walk = 0.65
eat = 0.65
shopping = 0.65
hygiene = 0.65
hangout = 0.65
prepare = 0.65
sick = 0.65
travel = 0.65
wake_up = 0.65
commute = 0.35

#######################
####### Params ########
#######################

# New columns
df['date'] = pd.to_datetime(df['date'])
df['weekNumber'] = df['date'].dt.isocalendar().apply(lambda x: f"{x[0]}-W{x[1]:02}", axis=1)
df['values'] = 1

# Adjusted columns
df['adj_date'] = pd.to_datetime(df['adj_date'])
df['adj_weekNumber'] = df['adj_date'].dt.isocalendar().apply(lambda x: f"{x[0]}-W{x[1]:02}", axis=1)

# Data Cleaning
df['attribute_1'] = df['attribute_1'].astype('category')

for column in df.columns:
    if df[column].dtypes == 'O':
        df[column] = df[column].str.strip()
    if df[column].dtype.name == 'category':
        df[column] = df[column].str.strip()

##############################
####### Weekly Trends ########
##############################

st.header('Weekly Trends and Score')

dfu_weekly = df.groupby('adj_weekNumber')['attribute_1'].value_counts().unstack()
dfu_weekly.fillna(0, inplace=True)
this_week = pd.Timestamp.now(tz=pytz.utc).astimezone(timezone('US/Pacific')).strftime('%W')
next_week_num = int(this_week) + 1
dfu_weekly = dfu_weekly[dfu_weekly.index != next_week_num]

dfu_weekly['rating'] = 0

for attribute in dfu_weekly:
    if attribute == 'work':
        dfu_weekly['rating'] = dfu_weekly['rating'] + work * dfu_weekly[attribute]
    if attribute == 'study':
        dfu_weekly['rating'] = dfu_weekly['rating'] + study * dfu_weekly[attribute]
    if attribute == 'exercise':
        dfu_weekly['rating'] = dfu_weekly['rating'] + exercise * dfu_weekly[attribute]
    if attribute == 'side hustle':
        dfu_weekly['rating'] = dfu_weekly['rating'] + side_hustle * dfu_weekly[attribute]
    if attribute == 'learn':
        dfu_weekly['rating'] = dfu_weekly['rating'] + learn * dfu_weekly[attribute]
    if attribute == 'church':
        dfu_weekly['rating'] = dfu_weekly['rating'] + church * dfu_weekly[attribute]
    if attribute == 'grocery':
        dfu_weekly['rating'] = dfu_weekly['rating'] + grocery * dfu_weekly[attribute]
    if attribute == 'eat':
        dfu_weekly['rating'] = dfu_weekly['rating'] + eat * dfu_weekly[attribute]
    if attribute == 'read':
        dfu_weekly['rating'] = dfu_weekly['rating'] + read * dfu_weekly[attribute]
    if attribute == 'cook':
        dfu_weekly['rating'] = dfu_weekly['rating'] + cook * dfu_weekly[attribute]
    if attribute == 'hangout':
        dfu_weekly['rating'] = dfu_weekly['rating'] + hangout * dfu_weekly[attribute]
    if attribute == 'call':
        dfu_weekly['rating'] = dfu_weekly['rating'] + call * dfu_weekly[attribute]
    if attribute == 'productive':
        dfu_weekly['rating'] = dfu_weekly['rating'] + productive * dfu_weekly[attribute]
    if attribute == 'meet':
        dfu_weekly['rating'] = dfu_weekly['rating'] + meet * dfu_weekly[attribute]
    if attribute == 'love':
        dfu_weekly['rating'] = dfu_weekly['rating'] + love * dfu_weekly[attribute]
    if attribute == 'walk':
        dfu_weekly['rating'] = dfu_weekly['rating'] + walk * dfu_weekly[attribute]
    if attribute == 'clean':
        dfu_weekly['rating'] = dfu_weekly['rating'] + clean * dfu_weekly[attribute]
    if attribute == 'commute':
        dfu_weekly['rating'] = dfu_weekly['rating'] + commute * dfu_weekly[attribute]
    if attribute == 'shopping':
        dfu_weekly['rating'] = dfu_weekly['rating'] + shopping * dfu_weekly[attribute]
    if attribute == 'hangout':
        dfu_weekly['rating'] = dfu_weekly['rating'] + hangout * dfu_weekly[attribute]
    if attribute == 'walk':
        dfu_weekly['rating'] = dfu_weekly['rating'] + walk * dfu_weekly[attribute]
    if attribute == 'prepare':
        dfu_weekly['rating'] = dfu_weekly['rating'] + prepare * dfu_weekly[attribute]
    if attribute == 'hygiene':
        dfu_weekly['rating'] = dfu_weekly['rating'] + hygiene * dfu_weekly[attribute]

dfu_weekly['rating'] = dfu_weekly['rating']/7

# Get the current year and week number
current_date = pd.Timestamp.now(tz=pytz.utc).astimezone(timezone('US/Pacific'))
current_year = current_date.isocalendar().year
this_week = f"{current_year}-W{current_date.isocalendar().week:02d}"  # Ensure two-digit week number

# Formula for weekly ranking
weekly_ranking = dfu_weekly.copy()
weekly_ranking['week_ranking'] = weekly_ranking['rating'].rank(ascending=False)

# Print this week's Score
try:
    current_week_data = weekly_ranking.loc[this_week]

    week_score = round(float(current_week_data['rating']), 1)
    week_rank = int(current_week_data['week_ranking'])
    total_weeks = int(weekly_ranking['week_ranking'].max())

    # Calculate percentile
    percentile = (1 - (week_rank / total_weeks)) * 100

    st.write(f"Week {this_week} score:          {week_score}")
    st.write(f"Week {this_week} all-time Rank:  {week_rank} out of {total_weeks}")
    st.write(f"Week {this_week} Percentile:     {percentile:.2f}%")

except KeyError:
    st.write(f"No data available for Week {this_week}.")

st.divider()

###########################################
####### Daily Proportion Pie Chart ########
###########################################

st.header('Daily Proportion Pie Chart')
today_activity = df[df['adj_date'] == pd.Timestamp.now(tz=pytz.utc).astimezone(timezone('US/Pacific')).strftime('%Y-%m-%d')]['attribute_1']
activity_tracker = today_activity.value_counts().sort_values()

fig, axes = plt.subplots(1, 4, figsize=(20,16),dpi=144)
labels = list(df['attribute_1'].unique()) # attribute_1 label list

# tracking activity - today
today_activity = df[df['adj_date'] == pd.Timestamp.now(tz=pytz.utc).astimezone(timezone('US/Pacific')).strftime('%Y-%m-%d')]['attribute_1']
activity_tracker = today_activity.value_counts()

# create pie chart
axes[0].pie(activity_tracker, labels = activity_tracker.index, autopct='%1.0f%%', shadow=True, counterclock = False)
axes[0].set_title('Today', fontsize = 20, bbox={'facecolor':'0.8', 'pad':5})


# tracking activity - yesterday
yesterday = pd.Timestamp.now(tz=pytz.utc).astimezone(timezone('US/Pacific')).date() - timedelta(days=1)
yesterday_activity = df[df['adj_date'] == yesterday.strftime('%Y-%m-%d')]['attribute_1']
activity_tracker = yesterday_activity.value_counts()

# create pie chart
axes[1].pie(activity_tracker, labels = activity_tracker.index, autopct='%1.0f%%', shadow=True, counterclock = False)
axes[1].set_title(yesterday.strftime('%A'), fontsize = 20, bbox={'facecolor':'0.8', 'pad':5})

# tracking activity - two_days_ago
two_days_ago = pd.Timestamp.now(tz=pytz.utc).astimezone(timezone('US/Pacific')).date() - timedelta(days=2)
two_days_ago_activity = df[df['adj_date'] == two_days_ago.strftime('%Y-%m-%d')]['attribute_1']
activity_tracker = two_days_ago_activity.value_counts()

# create pie chart
axes[2].pie(activity_tracker, labels = activity_tracker.index, autopct='%1.0f%%', shadow=True, counterclock = False)
axes[2].set_title(two_days_ago.strftime("%A"), fontsize = 20, bbox={'facecolor':'0.8', 'pad':5})


# tracking activity - one_week_ago
three_days_ago = pd.Timestamp.now(tz=pytz.utc).astimezone(timezone('US/Pacific')).date() - timedelta(days=3)
three_days_ago_activity = df[df['adj_date'] == three_days_ago.strftime('%Y-%m-%d')]['attribute_1']
activity_tracker = three_days_ago_activity.value_counts()

# create pie chart
axes[3].pie(activity_tracker, labels = activity_tracker.index, autopct='%1.0f%%', shadow=True, counterclock = False)
axes[3].set_title(three_days_ago.strftime('%A'), fontsize = 20, bbox={'facecolor':'0.8', 'pad':5})

st.set_option('deprecation.showPyplotGlobalUse', False)
st.pyplot()

st.divider()

#######################################################
####### Daily Proportion Pie Chart (Last Week) ########
#######################################################

st.header('Daily Proportion Pie Chart (Last Week)')
today_activity = df[df['date'] == pd.Timestamp.now(tz=pytz.utc).astimezone(timezone('US/Pacific')).date().strftime('%Y-%m-%d')]['attribute_1']
activity_tracker = today_activity.value_counts().sort_values()

fig, axes = plt.subplots(1, 4, figsize=(20,16),dpi=144)
labels = list(df['attribute_1'].unique()) # attribute_1 label list

# tracking activity - today
one_week_ago = pd.Timestamp.now(tz=pytz.utc).astimezone(timezone('US/Pacific')).date() - timedelta(days=7)
one_week_ago_activity = df[df['date'] == one_week_ago.strftime('%Y-%m-%d')]['attribute_1']
activity_tracker = one_week_ago_activity.value_counts()

# create pie chart
axes[0].pie(activity_tracker, labels = activity_tracker.index, autopct='%1.0f%%', shadow=True, counterclock = False)
axes[0].set_title('last '+one_week_ago.strftime('%A'), fontsize = 20, bbox={'facecolor':'0.8', 'pad':5})


# tracking activity - yesterday
yesterday = pd.Timestamp.now(tz=pytz.utc).astimezone(timezone('US/Pacific')).date() - timedelta(days=8)
yesterday_activity = df[df['date'] == yesterday.strftime('%Y-%m-%d')]['attribute_1']
activity_tracker = yesterday_activity.value_counts()

# create pie chart
axes[1].pie(activity_tracker, labels = activity_tracker.index, autopct='%1.0f%%', shadow=True, counterclock = False)
axes[1].set_title('last '+yesterday.strftime('%A'), fontsize = 20, bbox={'facecolor':'0.8', 'pad':5})


# tracking activity - two_days_ago
two_days_ago = pd.Timestamp.now(tz=pytz.utc).astimezone(timezone('US/Pacific')).date() - timedelta(days=9)
two_days_ago_activity = df[df['date'] == two_days_ago.strftime('%Y-%m-%d')]['attribute_1']
activity_tracker = two_days_ago_activity.value_counts()

# create pie chart
axes[2].pie(activity_tracker, labels = activity_tracker.index, autopct='%1.0f%%', shadow=True, counterclock = False)
axes[2].set_title('last '+two_days_ago.strftime("%A"), fontsize = 20, bbox={'facecolor':'0.8', 'pad':5})

# tracking activity - one_week_ago
one_week_ago = pd.Timestamp.now(tz=pytz.utc).astimezone(timezone('US/Pacific')).date() - timedelta(days=10)
one_week_ago_activity = df[df['date'] == one_week_ago.strftime('%Y-%m-%d')]['attribute_1']
activity_tracker = one_week_ago_activity.value_counts()

# create pie chart
axes[3].pie(activity_tracker, labels = activity_tracker.index, autopct='%1.0f%%', shadow=True, counterclock = False)
axes[3].set_title('last '+one_week_ago.strftime('%A'), fontsize = 20, bbox={'facecolor':'0.8', 'pad':5})

st.pyplot()

st.divider()
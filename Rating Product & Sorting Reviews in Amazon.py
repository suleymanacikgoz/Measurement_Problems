
import pandas as pd
import numpy as np
import datetime as dt

pd.set_option('display.max_columns', None)
pd.set_option('display.width',500)
pd.set_option('display.float_format', lambda x: '%.4f' % x)
from sklearn.preprocessing import MinMaxScaler


df["overall"].value_counts()

df_=pd.read_csv("C:/Users/suley/OneDrive/Masaüstü/Miuul/Kodlarım/Odevler/4.Hafta/amazon_review.csv")

df=df_.copy()

df.head()

df["overall"].mean()


df.info()


df.loc[df["day_diff"] <= 30, "overall"].mean()

df.loc[(df["day_diff"] > 30) & (df["day_diff"] <= 98), "overall"].mean()

df.loc[(df["day_diff"] > 90) & (df["day_diff"] <= 180), "overall"].mean()

df.loc[(df["day_diff"] > 180), "overall"].mean()


time_based_weighted_average=df.loc[df["day_diff"] <= 30, "overall"].mean()*28/100+ \
df.loc[(df["day_diff"] > 30) & (df["day_diff"] <= 98), "overall"].mean()*26/100+ \
df.loc[(df["day_diff"] > 90) & (df["day_diff"] <= 180), "overall"].mean()*24/100+ \
df.loc[(df["day_diff"] > 180), "overall"].mean()*22/100





 veri setinde helpful_no değişkeni yoktur, var olan değişkenler üzerinden üretilmesi gerekmektedir.

df["helpful_no"]=df["total_vote"]-df["helpful_yes"]
df[df["helpful_no"]>0]



df["score_pos_neg_diff"]=df["helpful_yes"]-df["helpful_no"]

df[df["score_pos_neg_diff"]>0]


df["score_average_rating"]=(df["helpful_yes"]/df["total_vote"])

df[df["score_average_rating"]>0]




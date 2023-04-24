
###################################################
# PROJE: Rating Product & Sorting Reviews in Amazon
###################################################

###################################################
# İş Problemi
###################################################

# E-ticaretteki en önemli problemlerden bir tanesi ürünlere satış sonrası verilen puanların doğru şekilde hesaplanmasıdır.
# Bu problemin çözümü e-ticaret sitesi için daha fazla müşteri memnuniyeti sağlamak, satıcılar için ürünün öne çıkması ve satın
# alanlar için sorunsuz bir alışveriş deneyimi demektir. Bir diğer problem ise ürünlere verilen yorumların doğru bir şekilde sıralanması
# olarak karşımıza çıkmaktadır. Yanıltıcı yorumların öne çıkması ürünün satışını doğrudan etkileyeceğinden dolayı hem maddi kayıp
# hem de müşteri kaybına neden olacaktır. Bu 2 temel problemin çözümünde e-ticaret sitesi ve satıcılar satışlarını arttırırken müşteriler
# ise satın alma yolculuğunu sorunsuz olarak tamamlayacaktır.

###################################################
# Veri Seti Hikayesi
###################################################

# Amazon ürün verilerini içeren bu veri seti ürün kategorileri ile çeşitli metadataları içermektedir.
# Elektronik kategorisindeki en fazla yorum alan ürünün kullanıcı puanları ve yorumları vardır.

# Değişkenler:
# reviewerID: Kullanıcı ID’si
# asin: Ürün ID’si
# reviewerName: Kullanıcı Adı
# helpful: Faydalı değerlendirme derecesi
# reviewText: Değerlendirme
# overall: Ürün rating’i
# summary: Değerlendirme özeti
# unixReviewTime: Değerlendirme zamanı
# reviewTime: Değerlendirme zamanı Raw
# day_diff: Değerlendirmeden itibaren geçen gün sayısı
# helpful_yes: Değerlendirmenin faydalı bulunma sayısı
# total_vote: Değerlendirmeye verilen oy sayısı


import pandas as pd
import numpy as np
import datetime as dt

pd.set_option('display.max_columns', None)
pd.set_option('display.width',500)
pd.set_option('display.float_format', lambda x: '%.4f' % x)
from sklearn.preprocessing import MinMaxScaler

###################################################
# GÖREV 1: Average Rating'i Güncel Yorumlara Göre Hesaplayınız ve Var Olan Average Rating ile Kıyaslayınız.
###################################################

df["overall"].value_counts()

# Paylaşılan veri setinde kullanıcılar bir ürüne puanlar vermiş ve yorumlar yapmıştır.
# Bu görevde amacımız verilen puanları tarihe göre ağırlıklandırarak değerlendirmek.
# İlk ortalama puan ile elde edilecek tarihe göre ağırlıklı puanın karşılaştırılması gerekmektedir.


###################################################
# Adım 1: Veri Setini Okutunuz ve Ürünün Ortalama Puanını Hesaplayınız.
###################################################
df_=pd.read_csv("C:/Users/suley/OneDrive/Masaüstü/Miuul/Kodlarım/Odevler/4.Hafta/amazon_review.csv")

df=df_.copy()

df.head()

df["overall"].mean()

###################################################
# Adım 2: Tarihe Göre Ağırlıklı Puan Ortalamasını Hesaplayınız.
###################################################

df.info()
#df["reviewTime"]=pd.to_datetime((df["reviewTime"]))

#df["reviewTime"].max()

#current_date=pd.to_datetime("2014-12-09 0:0:0")


df.loc[df["day_diff"] <= 30, "overall"].mean()

df.loc[(df["day_diff"] > 30) & (df["day_diff"] <= 98), "overall"].mean()

df.loc[(df["day_diff"] > 90) & (df["day_diff"] <= 180), "overall"].mean()

df.loc[(df["day_diff"] > 180), "overall"].mean()


time_based_weighted_average=df.loc[df["day_diff"] <= 30, "overall"].mean()*28/100+ \
df.loc[(df["day_diff"] > 30) & (df["day_diff"] <= 98), "overall"].mean()*26/100+ \
df.loc[(df["day_diff"] > 90) & (df["day_diff"] <= 180), "overall"].mean()*24/100+ \
df.loc[(df["day_diff"] > 180), "overall"].mean()*22/100





###################################################
# Görev 2: Ürün için Ürün Detay Sayfasında Görüntülenecek 20 Review'i Belirleyiniz.
###################################################


###################################################
# Adım 1. helpful_no Değişkenini Üretiniz
###################################################

# Not:
# total_vote bir yoruma verilen toplam up-down sayısıdır.
# up, helpful demektir.
# veri setinde helpful_no değişkeni yoktur, var olan değişkenler üzerinden üretilmesi gerekmektedir.

df["helpful_no"]=df["total_vote"]-df["helpful_yes"]
df[df["helpful_no"]>0]


###################################################
# Adım 2. score_pos_neg_diff, score_average_rating ve wilson_lower_bound Skorlarını Hesaplayıp Veriye Ekleyiniz
###################################################

df["score_pos_neg_diff"]=df["helpful_yes"]-df["helpful_no"]

df[df["score_pos_neg_diff"]>0]


df["score_average_rating"]=(df["helpful_yes"]/df["total_vote"])

df[df["score_average_rating"]>0]

##################################################
# Adım 3. 20 Yorumu Belirleyiniz ve Sonuçları Yorumlayınız.
###################################################



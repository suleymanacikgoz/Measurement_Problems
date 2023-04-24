#####################################################
# AB Testi ile BiddingYöntemlerinin Dönüşümünün Karşılaştırılması
#####################################################

#####################################################
# İş Problemi
#####################################################

# Facebook kısa süre önce mevcut "maximumbidding" adı verilen teklif verme türüne alternatif
# olarak yeni bir teklif türü olan "average bidding"’i tanıttı. Müşterilerimizden biri olan bombabomba.com,
# bu yeni özelliği test etmeye karar verdi veaveragebidding'in maximumbidding'den daha fazla dönüşüm
# getirip getirmediğini anlamak için bir A/B testi yapmak istiyor.A/B testi 1 aydır devam ediyor ve
# bombabomba.com şimdi sizden bu A/B testinin sonuçlarını analiz etmenizi bekliyor.Bombabomba.com için
# nihai başarı ölçütü Purchase'dır. Bu nedenle, istatistiksel testler için Purchasemetriğine odaklanılmalıdır.




#####################################################
# Veri Seti Hikayesi
#####################################################

# Bir firmanın web site bilgilerini içeren bu veri setinde kullanıcıların gördükleri ve tıkladıkları
# reklam sayıları gibi bilgilerin yanı sıra buradan gelen kazanç bilgileri yer almaktadır.Kontrol ve Test
# grubu olmak üzere iki ayrı veri seti vardır. Bu veri setleriab_testing.xlsxexcel’ininayrı sayfalarında yer
# almaktadır. Kontrol grubuna Maximum Bidding, test grubuna AverageBiddinguygulanmıştır.

# impression: Reklam görüntüleme sayısı
# Click: Görüntülenen reklama tıklama sayısı
# Purchase: Tıklanan reklamlar sonrası satın alınan ürün sayısı
# Earning: Satın alınan ürünler sonrası elde edilen kazanç



#####################################################
# Proje Görevleri
#####################################################

######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################

# 1. Hipotezleri Kur
# 2. Varsayım Kontrolü
#   - 1. Normallik Varsayımı (shapiro)
#   - 2. Varyans Homojenliği (levene)
# 3. Hipotezin Uygulanması
#   - 1. Varsayımlar sağlanıyorsa bağımsız iki örneklem t testi
#   - 2. Varsayımlar sağlanmıyorsa mannwhitneyu testi
# 4. p-value değerine göre sonuçları yorumla
# Not:
# - Normallik sağlanmıyorsa direkt 2 numara. Varyans homojenliği sağlanmıyorsa 1 numaraya arguman girilir.
# - Normallik incelemesi öncesi aykırı değer incelemesi ve düzeltmesi yapmak faydalı olabilir.

import pandas as pd
import numpy as np
import datetime as dt
from scipy.stats import shapiro
from scipy.stats import levene
from scipy.stats import ttest_ind
pd.set_option('display.max_columns', None)
pd.set_option('display.width',500)
pd.set_option('display.float_format', lambda x: '%.4f' % x)




#####################################################
# Görev 1:  Veriyi Hazırlama ve Analiz Etme
#####################################################

# Adım 1:  ab_testing_data.xlsx adlı kontrol ve test grubu verilerinden oluşan veri setini okutunuz. Kontrol ve test grubu verilerini ayrı değişkenlere atayınız.

kontrol=pd.read_excel("C:/Users/suley/OneDrive/Masaüstü/Miuul/Kodlarım/Odevler/4.Hafta/ab_testing.xlsx", sheet_name="Control Group")
test=pd.read_excel("C:/Users/suley/OneDrive/Masaüstü/Miuul/Kodlarım/Odevler/4.Hafta/ab_testing.xlsx", sheet_name="Test Group")

#test.columns=["Impression_Test","Click_Test","Purchase_Test","Earning_Test"]
#kontrol.columns=["Impression_Control","Click_Control","Purchase_Control","Earning_Control"]

test["x"]="Test"
kontrol["x"]="Kontrol"

test.head()
kontrol.head()


# Adım 2: Kontrol ve test grubu verilerini analiz ediniz.

test.describe().T
kontrol.describe().T


# Adım 3: Analiz işleminden sonra concat metodunu kullanarak kontrol ve test grubu verilerini birleştiriniz.


df=pd.concat([kontrol,test],axis=0)

#df.reset_index()
#df=df.reset_index()

df["Purchase"]

#####################################################
# Görev 2:  A/B Testinin Hipotezinin Tanımlanması
#####################################################

# Adım 1: Hipotezi tanımlayınız.

#H0: M1=M2(satın alımlar arasında anlamlı bir fark yoktur)
#H1: M1!=M2(anlamlı bir fark vardır)

# Adım 2: Kontrol ve test grubu için purchase(kazanç) ortalamalarını analiz ediniz

df.groupby("x").agg({"Purchase":"mean"})

#####################################################
# GÖREV 3: Hipotez Testinin Gerçekleştirilmesi
#####################################################

######################################################
# AB Testing (Bağımsız İki Örneklem T Testi)
######################################################


# Adım 1: Hipotez testi yapılmadan önce varsayım kontrollerini yapınız.Bunlar Normallik Varsayımı ve Varyans Homojenliğidir.

# Kontrol ve test grubunun normallik varsayımına uyup uymadığını Purchase değişkeni üzerinden ayrı ayrı test ediniz

test_stats,pvalue=shapiro(df.loc[df["x"]=="Test","Purchase"].dropna())
print("Test stat=%.4f,p-value=%.4f" %(test_stats,pvalue))

test_stats,pvalue=shapiro(df.loc[df["x"]=="Kontrol","Purchase"].dropna())
print("Test stat=%.4f,p-value=%.4f" %(test_stats,pvalue))

#p-value 0,05 ten büyük o yüzden büyük o yüzden H0'ı reddedemiyoruz

# Adım 2: Normallik Varsayımı ve Varyans Homojenliği sonuçlarına göre uygun testi seçiniz

# Varyans homojenliği

#H0=Varyanslar homojendir
#H1=Varyanslar homojen değildir


test_stats,pvalue=levene(df.loc[df["x"]=="Test","Purchase"].dropna(),
                         df.loc[df["x"]=="Kontrol","Purchase"].dropna())

print("Test stat=%.4f,p-value=%.4f" %(test_stats,pvalue))

#H0 reddedilemez

#varsayımlar sağlandığı için parametrik test kullanılacak


test_stats, pvalue=ttest_ind(df.loc[df["x"]=="Test","Purchase"],
                         df.loc[df["x"]=="Kontrol","Purchase"],
                             equal_var=True)
print("Test stat=%.4f,p-value=%.4f" %(test_stats,pvalue))


# Adım 3: Test sonucunda elde edilen p_value değerini göz önünde bulundurarak kontrol ve test grubu satın alma
# ortalamaları arasında istatistiki olarak anlamlı bir fark olup olmadığını yorumlayınız.

# pvalue değerini 0,05 ten büyük olduğu için anlamlı bir fark olmadığı kanaatine vardık.

##############################################################
# GÖREV 4 : Sonuçların Analizi
##############################################################

# Adım 1: Hangi testi kullandınız, sebeplerini belirtiniz.




# Adım 2: Elde ettiğiniz test sonuçlarına göre müşteriye tavsiyede bulununuz.


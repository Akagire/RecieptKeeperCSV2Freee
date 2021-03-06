#for python3
import pandas as pd
import numpy as np
import math
import datetime
import sys
import os
import re

#initialize
dealHead = ["収支区分","管理番号","発生日","支払期日","取引先","勘定科目","税区分","金額","税計算区分","税額","備考","品目","部門","メモタグ","支払日","支払口座","支払金額"]
transHead = ["振替日","振替元口座","振替先口座","備考","金額"]

#出力するデータフレームを作成
df = pd.DataFrame(index=[], columns = dealHead)
tf = pd.DataFrame(index=[], columns = transHead)

#define method
def dealrec(dt, dep, arr, pay, note):
    bumon = "電車"

    bik = ""
    if dep == "":
        reg_match = re.findall('バス|路面電車', note)
        if len(reg_match) > 0:
            bumon = reg_match[0]
    elif arr != "":
        bik = dep + "〜" + arr
    else:
        bik = dep

    return pd.DataFrame([[
            "支出",
            "",
            str(dt.strftime('%Y%m%d')),
            "",
            "",
            "旅費交通費",
            "課対仕入8%",
            str(int(pay)),
            "内税",
            "",
            bik,
            "",
            bumon,
            "",
            str(dt.strftime('%Y%m%d')),
            paymentWallet,
            str(int(pay))
        ]], columns = dealHead)

def transrec(dt, chg):
    return pd.DataFrame([[
        str(dt.strftime('%Y%m%d')),
        chargeSource,
        paymentWallet,
        "",
        str(int(chg))
    ]], columns = transHead)


print("入力するRecieptKeeper出力のCSVを指定してください:")
filePath = input()

if filePath == "":
    print ("ファイルを指定してください。")
    sys.exit()

if not os.path.isfile(filePath):
    print ("指定したファイルが存在しません。")
    sys.exit()

tlog = pd.read_csv(filePath, encoding="utf-8")

if len(tlog.index) < 1:
    print ("レコードがありません。")
    sys.exit()

#Nanを空白に置き換え
tlog = tlog.replace(np.nan, '', regex = True)

print("交通系ICへチャージする際に使用する口座を入力してください:")
chargeSource = input()
if chargeSource == "":
    print ("口座を指定しないため終了します。")
    sys.exit()

print("交通系ICの口座を入力してください:")
paymentWallet = input()
if paymentWallet == "":
    print ("口座を指定しないため終了します。")
    sys.exit()

c = 1
for i, v in tlog.iterrows():
    recDate = datetime.datetime.strptime(v["日付"], "%Y/%m/%d")
    stationDep = v["入場駅"]
    stationArr = v["出場駅"]
    walletCharge = v["チャージ"]
    walletPay = v["支払い"]
    walletRemain = v["残額"]
    bikou = v["備考"]

    if str(walletCharge) != "":
        print(str(int(c)) + ":チャージ")
        tf = tf.append(transrec(recDate, walletCharge))
    elif str(walletPay) != "":
        print(str(int(c)) + ":乗車")
        df = df.append(dealrec(recDate, stationDep, stationArr, walletPay, bikou)
            ,ignore_index = True)
    else:
        print(str(int(c)) + ":不明")

    c += 1

if len(df.index) > 0:
    df.to_csv("支払.csv", index = False, encoding = "shift_jis")

if len(tf.index) > 0:
    tf.to_csv("振替.csv", index = False, encoding = "shift_jis")

print ("done!")

import pandas as pd

# Load the data
df_users = pd.read_json("./data/users.json", lines=True)
df_brands = pd.read_json("./data/brands.json", lines=True)
df_receipts = pd.read_json("./data/receipts.json", lines=True)

#################################
##### Quick inspection
#################################

print("Users dataset shape ===>")
print(df_users.shape)
print("Users dataset info ===>")
print(df_users.info())
print("Users dataset first five rows ===>")
print(df_users.head(5))

print("Brands dataset shape ===>")
print(df_brands.shape)
print("Brands dataset info ===>")
print(df_brands.info())
print("Brands dataset first five rows ===>")
print(df_brands.head(5))

print("Receipts dataset shape ===>")
print(df_receipts.shape)
print("Receipts dataset info ===>")
print(df_receipts.info())
print("Receipts dataset first five rows ===>")
print(df_receipts.head(5))


#################################
##### Check for Missing Values
#################################


print("\nMissing Values in Users:\n", df_users.isna().sum())
#################################
# Missing Values in Users:
#  _id              0
# active           0
# createdDate      0
# lastLogin       62
# role             0
# signUpSource    48
# state           56
# dtype: int64
#################################

print("\nMissing Values in Brands:\n", df_brands.isna().sum())
#################################
# Missing Values in Brands:
# _id               0
# barcode           0
# category        155
# categoryCode    650
# cpg               0
# name              0
# topBrand        612
# brandCode       234
# dtype: int64
#################################


print("\nMissing Values in Receipts:\n", df_receipts.isna().sum())
#################################
# Missing Values in Receipts:
# _id                          0
# bonusPointsEarned          575
# bonusPointsEarnedReason    575
# createDate                   0
# dateScanned                  0
# finishedDate               551
# modifyDate                   0
# pointsAwardedDate          582
# pointsEarned               510
# purchaseDate               448
# purchasedItemCount         484
# rewardsReceiptItemList     440
# rewardsReceiptStatus         0
# totalSpent                 435
# userId                       0
#dtype: int64
#################################



#################################
##### Check for Duplicates
#################################

print("\nDuplicate _id in Users:", df_users.duplicated(subset=['_id']).sum())
#################################
# Duplicate _id in Users: 283
#################################

print("Duplicate _id in Brands:", df_brands.duplicated(subset=['_id']).sum())
#################################
# Duplicate _id in Brands: 0
#################################

print("Duplicate _id in Receipts:", df_receipts.duplicated(subset=['_id']).sum())
#################################
# Duplicate _id in Receipts: 0
#################################


#################################
##### Check for Logical / Business Rule
#################################

# 1. Validate userId in receipts actually exists in users
invalid_user_refs = df_receipts[~df_receipts['userId'].isin(df_users['_id'])]
print("\nReceipt rows referencing invalid userId:\n", invalid_user_refs)

#################################
# Receipt rows referencing invalid userId:
#                                         _id  bonusPointsEarned                            bonusPointsEarnedReason  ... rewardsReceiptStatus totalSpent                    userId
# 0     {'$oid': '5ff1e1eb0a720f0523000575'}              500.0  Receipt number 2 completed, bonus point schedu...  ...             FINISHED      26.00  5ff1e1eacfcf6c399c274ae6
# 1     {'$oid': '5ff1e1bb0a720f052300056b'}              150.0  Receipt number 5 completed, bonus point schedu...  ...             FINISHED      11.00  5ff1e194b6a9d73a3a9f1052
# 2     {'$oid': '5ff1e1f10a720f052300057a'}                5.0                         All-receipts receipt bonus  ...             REJECTED      10.00  5ff1e1f1cfcf6c399c274b0b
# 3     {'$oid': '5ff1e1ee0a7214ada100056f'}                5.0                         All-receipts receipt bonus  ...             FINISHED      28.00  5ff1e1eacfcf6c399c274ae6
# 4     {'$oid': '5ff1e1d20a7214ada1000561'}                5.0                         All-receipts receipt bonus  ...             FINISHED       1.00  5ff1e194b6a9d73a3a9f1052
# ...                                    ...                ...                                                ...  ...                  ...        ...                       ...
# 1114  {'$oid': '603cc0630a720fde100003e6'}               25.0                        COMPLETE_NONPARTNER_RECEIPT  ...             REJECTED      34.96  5fc961c3b8cfca11a077dd33
# 1115  {'$oid': '603d0b710a720fde1000042a'}                NaN                                                NaN  ...            SUBMITTED        NaN  5fc961c3b8cfca11a077dd33
# 1116  {'$oid': '603cf5290a720fde10000413'}                NaN                                                NaN  ...            SUBMITTED        NaN  5fc961c3b8cfca11a077dd33
# 1117  {'$oid': '603ce7100a7217c72c000405'}               25.0                        COMPLETE_NONPARTNER_RECEIPT  ...             REJECTED      34.96  5fc961c3b8cfca11a077dd33
# 1118  {'$oid': '603c4fea0a7217c72c000389'}                NaN                                                NaN  ...            SUBMITTED        NaN  5fc961c3b8cfca11a077dd33

# [1119 rows x 15 columns]
#################################

# 2. purchaseDate and dateScanned should not be in future
def get_date(val):
    if isinstance(val, dict) and "$date" in val:
        return val["$date"]
    return None  # or handle other edge cases
df_receipts["purchaseDate"] = df_receipts["purchaseDate"].apply(get_date)
# Convert the extracted numeric milliseconds to datetime
df_receipts["purchaseDate"] = pd.to_datetime(df_receipts["purchaseDate"], unit="ms", errors="coerce")
today = pd.to_datetime("today")
future_purchases = df_receipts[df_receipts["purchaseDate"] > today]
print("\nReceipts with purchaseDate in the future:\n", future_purchases)

#################################
# Receipts with purchaseDate in the future:
#  Empty DataFrame
# Columns: [_id, bonusPointsEarned, bonusPointsEarnedReason, createDate, dateScanned, finishedDate, modifyDate, pointsAwardedDate, pointsEarned, purchaseDate, purchasedItemCount, rewardsReceiptItemList, rewardsReceiptStatus, totalSpent, userId]
# Index: []

# No future purchases found
#################################

df_receipts["dateScanned"] = df_receipts["dateScanned"].apply(get_date)
# Convert the extracted numeric milliseconds to datetime
df_receipts["dateScanned"] = pd.to_datetime(df_receipts["dateScanned"], unit="ms", errors="coerce")
today = pd.to_datetime("today")
future_scans = df_receipts[df_receipts["dateScanned"] > today]
print("\nReceipts with dateScanned in the future:\n", future_scans)

#################################
# Receipts with dateScanned in the future:
#  Empty DataFrame
# Columns: [_id, bonusPointsEarned, bonusPointsEarnedReason, createDate, dateScanned, finishedDate, modifyDate, pointsAwardedDate, pointsEarned, purchaseDate, purchasedItemCount, rewardsReceiptItemList, rewardsReceiptStatus, totalSpent, userId]
# Index: []

# No future scans found
#################################


# 3. totalSpend should not be negative or very large
negative_spend = df_receipts[(df_receipts['totalSpent'] < 0)]
print("\nReceipts with negative totalSpent:\n", negative_spend)

#################################
# Receipts with negative or very large totalSpent:
#  Empty DataFrame
# Columns: [_id, bonusPointsEarned, bonusPointsEarnedReason, createDate, dateScanned, finishedDate, modifyDate, pointsAwardedDate, pointsEarned, purchaseDate, purchasedItemCount, rewardsReceiptItemList, rewardsReceiptStatus, totalSpent, userId]
# Index: []

# No negative totalSpend found!
#################################

very_large_spend = df_receipts[(df_receipts['totalSpent'] > 1000)]
print("\nReceipts with very large totalSpent:\n", very_large_spend)

#################################
# Receipts with very large totalSpent:
#                                        _id  bonusPointsEarned                            bonusPointsEarnedReason  ... rewardsReceiptStatus totalSpent                    userId
# 314  {'$oid': '60025cb80a720f05f300008d'}              750.0  Receipt number 1 completed, bonus point schedu...  ...             FINISHED    1177.84  60025c65fb296c4ef805d9e6
# 318  {'$oid': '600260210a720f05f300008f'}              750.0  Receipt number 1 completed, bonus point schedu...  ...             FINISHED    1043.18  60025fe0e257124ec6b99a87
# 407  {'$oid': '60099c3c0a7214ad89000135'}              750.0  Receipt number 1 completed, bonus point schedu...  ...             FINISHED    1083.24  60099c1450b33111fd61f702
# 419  {'$oid': '600996ac0a720f05fa000134'}              750.0  Receipt number 1 completed, bonus point schedu...  ...             FINISHED    1198.68  6009969150b33111fd61f6d9
# 423  {'$oid': '600a1a8d0a7214ada2000008'}              750.0  Receipt number 1 completed, bonus point schedu...  ...             FINISHED    1183.10  600a1a457d983a124e9adb9b
# 431  {'$oid': '600ba6ae0a7214ada2000010'}              750.0  Receipt number 1 completed, bonus point schedu...  ...             FINISHED    1107.82  600ba68e7d983a124e9ae1d3
# 446  {'$oid': '600f24970a720f053500002f'}                NaN                                                NaN  ...              FLAGGED    4368.80  600f20c15edb787dce060911
# 447  {'$oid': '600f0cc70a720f053500002c'}                NaN                                                NaN  ...              FLAGGED    2084.82  600f00d05edb787dce05fb84
# 469  {'$oid': '600f39c30a7214ada2000030'}              750.0  Receipt number 1 completed, bonus point schedu...  ...             FINISHED    4721.95  600f35015edb782098e2ac1b
# 543  {'$oid': '600f2fc80a720f0535000030'}              750.0  Receipt number 1 completed, bonus point schedu...  ...             FINISHED    4566.17  600f29a64329897eac239049

# [10 rows x 15 columns]

# Found 10 very large totalSpend if we define totalSpend > 1000 as the very large totalSpend
#################################


# 4. dataScanned should not be before purchaseDate
def get_date(val):
    if isinstance(val, dict) and "$date" in val:
        return val["$date"]
    return None  # or handle other edge cases

# Transform 'dateScanned' and 'purchaseDate' columns to numeric timestamps
df_receipts["dateScanned"] = df_receipts["dateScanned"].apply(get_date)
df_receipts["purchaseDate"] = df_receipts["purchaseDate"].apply(get_date)

# Convert the numeric timestamps to datetime
df_receipts["dateScanned"] = pd.to_datetime(df_receipts["dateScanned"], unit="ms", errors="coerce")
df_receipts["purchaseDate"] = pd.to_datetime(df_receipts["purchaseDate"], unit="ms", errors="coerce")

inverted_dates = df_receipts[
    df_receipts["dateScanned"] < df_receipts["purchaseDate"]
]
print("\nReceipts with dateScanned < purchaseDate:\n", inverted_dates)

#################################
# Receipts with dateScanned < purchaseDate:
#                                        _id  bonusPointsEarned                            bonusPointsEarnedReason  ... rewardsReceiptStatus totalSpent                    userId
# 12   {'$oid': '5ff1e1b60a7214ada100055c'}              150.0  Receipt number 5 completed, bonus point schedu...  ...              FLAGGED      290.0  5ff1e194b6a9d73a3a9f1052
# 14   {'$oid': '5ff1e1b20a7214ada100055a'}              300.0  Receipt number 4 completed, bonus point schedu...  ...             FINISHED        1.0  5ff1e194b6a9d73a3a9f1052
# 85   {'$oid': '5ff4ce640a7214ada10005e0'}               25.0                        COMPLETE_NONPARTNER_RECEIPT  ...             FINISHED        1.0  5ff4ce33c3d63511e2a484b6
# 139  {'$oid': '5ff73be10a7214ada1000619'}                NaN                                                NaN  ...              FLAGGED      290.0  5ff73b90eb7c7d31ca8a452b
# 158  {'$oid': '5ff873f10a720f052300064f'}              500.0  Receipt number 2 completed, bonus point schedu...  ...              FLAGGED      290.0  5ff873d1b3348b11c9337716
# 190  {'$oid': '5ffcb4900a720f0515000002'}              250.0  Receipt number 3 completed, bonus point schedu...  ...              FLAGGED      290.0  5ffcb47d04929111f6e9256c
# 244  {'$oid': '5fff26ee0a720f05f300001a'}               25.0                        COMPLETE_NONPARTNER_RECEIPT  ...             FINISHED        1.0  5fff2698b3348b03eb45bb10
# 265  {'$oid': '5fff26f10a7214ad4c000018'}                NaN                                                NaN  ...              FLAGGED      290.0  5fff2698b3348b03eb45bb10
# 294  {'$oid': '6000d4bc0a7214ad4c000070'}                NaN                                                NaN  ...              FLAGGED      290.0  6000d46cfb296c121a81b20c
# 362  {'$oid': '600887560a720f05fa000098'}              250.0  Receipt number 3 completed, bonus point schedu...  ...             FINISHED        1.0  6008873eb6310511daa4e8eb
# 553  {'$oid': '60145a3d0a7214ad50000082'}              750.0  Receipt number 1 completed, bonus point schedu...  ...             FINISHED        1.0  60145a3c84231211ce796c5d
# 644  {'$oid': '60182f290a720f05f800032f'}              500.0  Receipt number 2 completed, bonus point schedu...  ...             FINISHED        1.0  60182f1dc8b50e11d84548c4
# 871  {'$oid': '602176c90a7214d8e9000028'}               25.0                        COMPLETE_NONPARTNER_RECEIPT  ...             FINISHED        1.0  6021768799409b11fcf8987f

# [13 rows x 15 columns]

# Found 13 records where dateScanned < dataPurchase
#################################


# 5. Check topBrand missing flag (i.e. they need to be either True or False, but not other values or empty)
invalid_top_brand = df_brands[~df_brands['topBrand'].isin([True, False])]
print("\nBrands with invalid topBrand value:\n", invalid_top_brand)

#################################
# Brands with invalid topBrand value:
#                                         _id       barcode             category  ...                       name topBrand                      brandCode
# 7     {'$oid': '5cdad0f5166eb33eb7ce0faa'}  511111104810  Condiments & Sauces  ...                 J.L. Kraft      NaN                     J.L. KRAFT
# 9     {'$oid': '5c408e8bcd244a1fdb47aee7'}  511111504788               Baking  ...                       test      NaN                           TEST
# 10    {'$oid': '5f4bf556be37ce0b4491554d'}  511111516354               Baking  ...  test brand @1598813526777      NaN  TEST BRANDCODE @1598813526777
# 11    {'$oid': '57c08106e4b0718ff5fcb02c'}  511111102540                  NaN  ...                MorningStar      NaN                            NaN
# 13    {'$oid': '5d6413156d5f3b23d1bc790a'}  511111205012            Magazines  ...       Entertainment Weekly      NaN                   511111205012
# ...                                    ...           ...                  ...  ...                        ...      ...                            ...
# 1157  {'$oid': '5332fa75e4b03c9a25efd221'}  511111303015                  NaN  ...                     DASANI      NaN                            NaN
# 1158  {'$oid': '5f628215be37ce78e6e2efab'}  511111716648               Baking  ...  test brand @1600291349042      NaN  TEST BRANDCODE @1600291349043
# 1162  {'$oid': '5f77274dbe37ce6b592e90c0'}  511111116752               Baking  ...  test brand @1601644365844      NaN                            NaN
# 1163  {'$oid': '5dc1fca91dda2c0ad7da64ae'}  511111706328   Breakfast & Cereal  ...        Dippin Dots® Cereal      NaN             DIPPIN DOTS CEREAL
# 1164  {'$oid': '5f494c6e04db711dd8fe87e7'}  511111416173       Candy & Sweets  ...  test brand @1598639215217      NaN  TEST BRANDCODE @1598639215217

# [612 rows x 8 columns]

# Found 162 records where topBrand flags are invalid
#################################
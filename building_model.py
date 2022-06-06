import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

df = pd.read_csv("Challenger_Ranked_Games_15minute.csv")


df=df.drop(["gameId",
            "blueCurrentGolds",
            "blueTotalLevel",
            "blueWardPlaced",
            "blueWardKills",
            "blueTowerKills",
            "blueDragnoType",
            "redWins",
            "redCurrentGolds",
            "redTotalLevel",
            "redWardPlaced",
            "redWardKills",
            "redTowerKills",
            "redDragnoType",
            "redWins"], axis=1)

df["GoldDiff"] = df.blueTotalGolds - df.redTotalGolds
df["KillDiff"] = df.blueKill - df.redKill
df["DeathDiff"] = df.blueDeath - df.redDeath
df["AssistDiff"] = df.blueAssist - df.redAssist
df["LvlDiff"] = df.blueAvgLevel - df.redAvgLevel
df["CsDiff"] = df.blueTotalMinionKills - df.redTotalMinionKills
df["JungleCsDiff"] = df.blueTotalJungleMinionKills - df.redTotalJungleMinionKills

df=df.drop(["blueTotalGolds",
            "redTotalGolds",
            "blueTotalMinionKills",
            "redTotalMinionKills",
            "blueTotalJungleMinionKills",
            "redTotalJungleMinionKills",
            "redFirstBlood"],axis=1)

df=df.drop(["blueKill",
            "blueDeath",
            "blueAssist",
            "redKill",
            "redDeath",
            "redAssist",
            "redFirstTower",
            "redRiftHeralds",
            "redDragon",
            "redFirstDragon",
            "redInhibitor",
            "redBotTowerKills",
            "redTopTowerKills",
            "redMidTowerKills",
            "redFirstTowerLane",
            "redFirstInhibitor",
            "redAvgLevel",
            "blueAvgLevel"],axis=1)

onehot_towers = pd.get_dummies(df.blueFirstTowerLane)
df=df.drop(["blueFirstTowerLane","GoldDiff"],axis=1)
df=pd.concat([df,onehot_towers],axis=1)
df.drop(["['BOT_LANE']","['MID_LANE']","['TOP_LANE']"],axis=1,inplace = True)
df["anyTower"] = df["[]"].map(lambda x: 0 if (x == 1) else 1)
df[df["blueWins"]==1].mean()
df.drop("[]",axis=1, inplace = True)
df.drop("anyTower",axis=1, inplace = True)

df.rename(columns = {'LvlDiff':'Lvl_Diff',
                     'CsDiff':'cs_Diff',
                     'JungleCsDiff':'jungle_cs_Diff',
                     'KillDiff':'Kills_Diff',
                     'AssistDiff':'Assist_Diff',
                     'DeathDiff':'Death_Diff',
                     'blueFirstBlood':'first_blood',
                     'blueRiftHeralds':'Heralds_amount',
                     'blueDragon':'Dragons_Amount',
                     'blueFirstDragon':'first_dragon',
                     'blueInhibitor':'inhibs_amount',
                     'blueBotTowerKills':'bot_towers_amount',
                     'blueMidTowerKills':'mid_towers_amount',
                     'blueTopTowerKills':'top_towers_amount',
                     'blueFirstInhibitor':'first_inhib',
                     'blueFirstTower':'first_tower'}, inplace = True)


from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
# Scoring functions
from sklearn.metrics import accuracy_score
from sklearn.metrics import classification_report
from sklearn.metrics import confusion_matrix

X=df.drop("blueWins",axis=1)
y=df["blueWins"]

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2,random_state=42)

RF = RandomForestClassifier(bootstrap=True,max_depth=8, max_features=6, max_leaf_nodes=None)
RF.fit(X_train,y_train)


plt.figure(figsize=(10,10))
importances = RF.feature_importances_
sorted_indices = np.argsort(importances)
importances[:] = [importances[i] for i in sorted_indices]
plt.barh(list(X_train.columns[sorted_indices]), importances)
plt.title('Feature Importances')
plt.show


import joblib

# save the model
joblib.dump(RF, "./random_forest.joblib")

print(classification_report(y_test,  RF.predict(X_test)))
print(confusion_matrix(y_test, RF.predict(X_test)))

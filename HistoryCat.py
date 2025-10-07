# HistoryCat.py
#RECORDS WHENEVER THE USER RUNS THE MODEL ON A NEW DATA SET SO THE MODEL WILL IMPROVE OVER TIME
import os
import pandas as pd
from tkinter import messagebox
from RegressionCat import PurrfectRegression

HistoryPath = r"C:\Users\mkb00\PROJECTS\GitRepos\Schrodingers_Cat_Cafe\Historical_Cat_Cafe_Data.csv" #MASTER CAT DATA CSV WHERE DATA WILL BE STORED WHENEVER THE MODEL IS RUN ON A NEW DATASET


def AppendToHistory(NewDF, HistorySavePath=HistoryPath): #LOAD  NEW CSV FILE TO A DF AND COMBINE WITH THE HISTORICAL DF
    """Append processed data (with predictions) to the master historical CSV."""
    try:
        if os.path.exists(HistorySavePath):
            ExistingDF = pd.read_csv(HistorySavePath)
            CombinedDF = pd.concat([ExistingDF, NewDF], ignore_index=True)
        else:
            CombinedDF = NewDF
        CombinedDF.to_csv(HistorySavePath, index=False)
        print(f"[HistoryCat] Appended {len(NewDF)} rows to {os.path.basename(HistorySavePath)}")
    except Exception as e:
        messagebox.showerror("FAIL", f"Can't update historical file right meow:\n{e}")
        raise


def RunHistoricalRegression(HistorySavePath=HistoryPath): #LOADS HISTORICAL FILE, RUNS REGRESSION USING PURRFECT REGRESSION, OVERWRITES THE SAME CSV WITH NEW PREDICTIONS
    if not os.path.exists(HistorySavePath):
        messagebox.showerror("LOST CAT", f"Cannot find historical data file right meow:\n{HistorySavePath}")
        return None
    try: #LOAD HISTORICAL CSV FILE AND RUN REGRESSION MODEL ON IT
        df = pd.read_csv(HistorySavePath)
        HistoryMeow = PurrfectRegression(df)
        results = HistoryMeow.RunRegression()
        # INCLUDE NEW PREDICTIONS INTO DF
        df["PredictedMood"] = HistoryMeow.Predictions.get("Mood", pd.Series([None]*len(df)))
        df["PredictedSass"] = HistoryMeow.Predictions.get("Sass", pd.Series([None]*len(df)))
        df["PredictedSurvival"] = HistoryMeow.Predictions.get("Survival", pd.Series([None]*len(df)))
        # CALCULATE RESIDUALS
        if "ActualMood" in df.columns and "PredictedMood" in df.columns:
            df["MoodEpsilon"] = df["ActualMood"] - df["PredictedMood"]
        if "ActualSass" in df.columns and "PredictedSass" in df.columns:
            df["SassEpsilon"] = df["ActualSass"] - df["PredictedSass"]
        if "ActualSurvival" in df.columns and "PredictedSurvival" in df.columns:
            df["SurvivalEpsilon"] = df["ActualSurvival"] - df["PredictedSurvival"]
        # ✅ OVERWRITE THE OLD VERSION
        df.to_csv(HistorySavePath, index=False)
        print(f"[HistoryCat] M ission Accomplished!. Overwrote {HistorySavePath}")
        return HistorySavePath

    except Exception as e:
        messagebox.showerror("FAIL", f"Can't do regression right meow:\n{e}")
        raise

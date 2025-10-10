# HistoryCat.py
#RECORDS WHENEVER THE USER RUNS THE MODEL ON A NEW DATA SET SO THE MODEL WILL IMPROVE OVER TIME
import os
import pandas as pd
from datetime import datetime
from tkinter import messagebox
from RegressionCat import PurrfectRegression
from ExcelCat import PurrfectWB
import numpy as np


HistoryPath = r"C:\Users\mkb00\PROJECTS\GitRepos\Schrodingers_Cat_Cafe\HistoricalCafeData\Historical_Cafe_Data.parquet"
CoefficientsHistoryPath = r"C:\Users\mkb00\PROJECTS\GitRepos\Schrodingers_Cat_Cafe\HistoricalCafeData\CatCoefficients.parquet"
MetricsHistoryPath = r"C:\Users\mkb00\PROJECTS\GitRepos\Schrodingers_Cat_Cafe\HistoricalCafeData\CatMetrics.parquet"

def CatArchive(NewDF, HistoryPath): #LOAD NEW CAFE FILE (with predictions) TO A DF AND COMBINE WITH THE HISTORICAL DF / PARQUET FILE / IF THE FILE DOESN"T EXIST, IT CREATES IT WITH THE SAME SCHEMA AS THE NEW DATA
    os.makedirs(os.path.dirname(HistoryPath), exist_ok=True) #ENSURE DIRECTORY EXISTS
    if os.path.exists(HistoryPath): #IF HISTORICAL FILE EXISTS, LOAD IT
        try:
            ExistingDF = pd.read_parquet(HistoryPath)
        except Exception:
            ExistingDF = pd.DataFrame() #FALLBACK IF FILE IS EMPTY OR CORRUPTED
    else:
        ExistingDF = pd.DataFrame()

    AllColumns = sorted(set(ExistingDF.columns).union(NewDF .columns)) #ALIGN COLUMNS
    ExistingDF = ExistingDF.reindex(columns=AllColumns, fill_value=None)
    NewDF = NewDF.reindex(columns=AllColumns, fill_value=None)

    CombinedDF = pd.concat([ExistingDF, NewDF], ignore_index=True) #APPEND AND RESET INDEX
    CombinedDF.to_parquet(HistoryPath, index=False) #SAVE BACK TO PARQUET
    print(f"🐾 Historical Parquet File is meow up-to-date: {HistoryPath}")

    return HistoryPath

def RunHistoricalRegression(HistoryPath, CoefficientsHistoryPath, MetricsHistoryPath):  #LOADS HISTORICAL PARQUET FILE, RUNS REGRESSION USING PURRFECT REGRESSION, OVERWRITES THE SAME PARQUET WITH NEW PREDICTIONS, UPDATES THE COEFFICIENTS AND METRICS PARQUET FILES, AND GENERATES A NEW EXCEL REPORT
    from main import StashCoefficients, GetMetricsDF, GetSurvivalEpsilon, SafetyCat_Subtract

    if not os.path.exists(HistoryPath): #MAKE SURE HISTORY FILE EXISTS
        messagebox.showerror("MISSING CAT", f"Cannot find historical data right meow:\n{HistoryPath}")
        return None
    try: # 🧮 LOAD HISTORICAL PARQUET FILE AND RUN REGRESSION MODEL ON IT
        df = pd.read_parquet(HistoryPath)
        if os.path.exists(CoefficientsHistoryPath): #LOAD HISTORICAL COEFFICIENTS DF IF IT EXISTS
            CoefficientsDF = pd.read_parquet(CoefficientsHistoryPath)
        else: #CREATE IF NOT
            CoefficientsDF = pd.DataFrame(columns=["Feature", "MoodImportance", "SassImportance", "SurvivalImportance", "FeatureInsights"])

        if os.path.exists(MetricsHistoryPath): #LOAD HISTORICAL METRICS DF IF IT EXISTS
            MetricsDF = pd.read_parquet(MetricsHistoryPath)
        else: #CREATE IF NOT
            MetricsDF = pd.DataFrame(columns=["Metric", "Mood", "Sass", "Survival", "ModelInsights"])

        CatRegression = PurrfectRegression(df) #RUN REGRESSION
        results = CatRegression.RunRegression()
         # INCLUDE NEW PREDICTIONS INTO HISTORICAL DF
        df["PredictedMood"] = CatRegression.Predictions.get("Mood", pd.Series([None] * len(df)))
        df["PredictedSass"] = CatRegression.Predictions.get("Sass", pd.Series([None] * len(df)))
        df["PredictedSurvival"] = CatRegression.Predictions.get("Survival", pd.Series([None] * len(df)))
         # CALCULATE RESIDUALS (WITH NAN SAFETY)
        df["MoodEpsilon"] = df.apply(lambda r: SafetyCat_Subtract(r["ActualMood"], r["PredictedMood"]), axis=1)
        df["SassEpsilon"] = df.apply(lambda r: SafetyCat_Subtract(r["ActualSass"], r["PredictedSass"]), axis=1)

# --- Survival cleanup ---
        def normalize_actual_survival(x, obs):
            if obs == 0:
                return "Unknown"
            try:
                if x is None or (isinstance(x, str) and x.strip() == ""):
                    return "Unknown"
                return float(x)
            except Exception:
                return "Unknown"

        df["Observer"] = pd.to_numeric(df["Observer"], errors="coerce").fillna(0).astype(int)
        df["ActualSurvival"] = df.apply(
            lambda r: normalize_actual_survival(r.get("ActualSurvival"), r.get("Observer")), axis=1
        )
        df["PredictedSurvival"] = df["PredictedSurvival"].astype("object")
        df.loc[df["Observer"] == 0, "PredictedSurvival"] = "Unknown"



        df["SurvivalEpsilon"] = df.apply(GetSurvivalEpsilon, axis=1).astype("object")

        # Fill NaNs safely (don’t overwrite Unknown)
        df = df.replace({np.nan: None})

        # Overwrite parquet
        df.to_parquet(HistoryPath, index=False)
        print(f"[HistoryCat] Historical regression complete. Updated {HistoryPath}")

        # Update coefficients + metrics
        if os.path.exists(CoefficientsHistoryPath):
            CoefficientsDF = pd.read_parquet(CoefficientsHistoryPath)
        else:
            CoefficientsDF = pd.DataFrame(columns=["Feature", "MoodImportance", "SassImportance", "SurvivalImportance", "FeatureInsights"])
        CoefficientsDF, MeltedCoeffs = StashCoefficients(CoefficientsDF, CatRegression, CoefficientsHistoryPath)

        if os.path.exists(MetricsHistoryPath):
            MetricsDF = pd.read_parquet(MetricsHistoryPath)
        else:
            MetricsDF = pd.DataFrame(columns=["Metric", "Mood", "Sass", "Survival", "ModelInsights"])
        MetricsDF, MeltedMetrics = GetMetricsDF(CatRegression, MetricsHistoryPath)

        # Excel report
        TimeStamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        ReportPath = HistoryPath.replace(".parquet", f"_Report_{TimeStamp}.xlsx")
        HistoryMeow = PurrfectWB(df, ReportPath, CatRegression.ScatterPlots, CatRegression.RegressionPlots, CatRegression.FeatureImportances)
        HistoryMeow.DataKitten()
        HistoryMeow.ScatterKitten()
        HistoryMeow.MoodResultsKitten()
        HistoryMeow.SassResultsKitten()
        HistoryMeow.InsightsKitten()

        print(f"[HistoryCat] Excel report created: {ReportPath}")
        return ReportPath

    except Exception as e:
        messagebox.showerror("FAIL", f"Cannot run regression right meow:\n{e}")
        raise


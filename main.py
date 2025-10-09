#WELCOME TO SCHRODINGERS CAT CAFE!
# INDEPENDENT VARIABLES / FEATURES:
#	BOXTEMP = AFFECTS COMFORT AND DECAY RATE OF QUANTUM PARTICLES
#	DECAYRATE = PROBABILITY OF POISON RELEASE MECHANISM TRIGGERING
#	PHOTONS = MEASURES QUANTUM ACTIVITY INSIDE THE BOX
#	STABILITY = HOW STABLE THE CAT’S QUANTUM STATE IS
#	ENTANGLEMENT = DEGREE OF ENTANGLEMENT WITH EXTERNAL SYSTEMS
#	OBSERVER = BINARY: 0 = UNOBSERVED, 1 = OBSERVED
#	MATERIAL = CATEGORICAL: CARDBOARD, LEAD, QUANTUM FOAM, OR VELVET

# TARGETS:
#   CAT MOOD SCORE / VARIABLE NAME: “MOODSCORE”
# ○	    FLOAT FROM 0 TO 100
# ○	    INTERPRETATION: REPRESENTS THE CAT’S EMOTIONAL STATE BEFORE DECOHERENCE
# ○	    0 = EXISTENTIAL DREAD, 100 = QUANTUM BLISS
# ○	    INFLUENCED BY BOXTEMP, DECAYRATE, PHOTONS, AND MATERIAL
# •	QUANTUM SASS INDEX / VARIABLE NAME: “SASSINDEX”
# ○	    FLOAT FROM 0 TO 100
# ○	    100 = SUPER SASSY. 0 = NOT SASSY AT ALL
#		INFLUENCED BY ENTANGLEMENT AND BOXTEMP
#  ALIVE PROBABILITY / VARIABLE NAME: “SURVIVALRATE”
# ○	    (0.0–1.0): REPRESENTS THE LIKELIHOOD THE CAT IS ALIVE
# ○	    USE OBSERVER PRESENCE (BOOLEAN) TO SIMULATE WAVEFUNCTION COLLAPSE: WHEN OBSERVER PRESENCE = 1
# ○	    INFLUENCED BY OBSERVER PRESENCE ONLY


#---------------------- FOR TESTING ----------------------
#InputCSV = "C:\\Users\\mkb00\\PROJECTS\\GitRepos\\Schrodingers_Cat_Cafe\\Test\\CafeData.csv"
#OutputPath = "C:\\Users\\mkb00\\PROJECTS\\GitRepos\\Schrodingers_Cat_Cafe\\Test\\CafeOutput.xlsx"
#MasterDataPath = "C:\\Users\\mkb00\\PROJECTS\\GitRepos\\Schrodingers_Cat_Cafe\\Test\\MasterData.csv"
 
#UserName = "Mary Kathryn Barriault"
#name_parts = UserName.split()
#if len(name_parts) < 2:
#    messagebox.showerror("Invalid Name", "Please enter at least a first and last name.")
#first_initial = name_parts[0][0].upper()
#last_initial = name_parts[-1][0].upper()
#middle_initial = name_parts[1][0].upper() if len(name_parts) > 2 else "" # MIDDLE INITIAL = OPTIONAL
#initials = first_initial + middle_initial + last_initial # COMBINE INITIALS

#TodaysDate = datetime.today().strftime("%Y%m%d")

#HistoryPath = "C:\Users\mkb00\PROJECTS\GitRepos\Schrodingers_Cat_Cafe\HistoricalCafeData\Historical_Cafe_Data.parquet"
#CoefficientsHistoryPath = "C:\Users\mkb00\PROJECTS\GitRepos\Schrodingers_Cat_Cafe\HistoricalCafeData\CatCoefficients.parquet"
#MetricsHistoryPath = "C:\Users\mkb00\PROJECTS\GitRepos\Schrodingers_Cat_Cafe\HistoricalCafeData\CatMetrics.parquet"

# main.py
from DataCat import GetNewCatData, ScaleCatData
from RegressionCat import PurrfectRegression
from ExcelCat import PurrfectWB
from HistoryCat import CatArchive, RunHistoricalRegression, HistoryPath
from tkinter import messagebox
import pandas as pd
import os
from datetime import datetime
from CatForms import CatCafeMenu

def normalize_headers(df, AliasMap):
    RenameMap = {}
    for aliases, standard_name in AliasMap.items():
        for alias in aliases.split("|"):
            if alias in df.columns:
                RenameMap[alias] = standard_name
    return df.rename(columns=RenameMap)

def StashCoefficients(CoefficientsDF, RegressionMeow, SavePath=None): #UPDATES COEFFICIENT DF WITH NEW FEATURES IMPORTANCES FROM REGRESSION RUN / BUILDS A TIDY LONG FORM VERSION FOR PLOTTING OR HISTORICAL TRACKING / OPTIONALLY SAVES BOTH WIDE AND LONG DATASETS TO PARQUETS
    for idx, row in CoefficientsDF.iterrows(): #UPDATE WIDE FORM COEFFICIENTS
        feat = row["Feature"]
        for target in ["Mood", "Sass", "Survival"]:
            imp_dict = RegressionMeow.FeatureImportances.get(target, {})
            if feat in imp_dict:
                CoefficientsDF.at[idx, f"{target}Importance"] = imp_dict[feat]

    MeltedRows = [] #BUILD LONG FORM DF FOR ANAYLYTICS OR PLOTTING
    for target in ["Mood", "Sass", "Survival"]:
        for _, row in CoefficientsDF.iterrows():
            val = row.get(f"{target}Importance", None)
            if pd.notna(val) and val not in ["N/A", None]:
                try:
                    val = float(val)
                except Exception:
                    continue
                MeltedRows.append({
                    "Target": target,
                    "Feature": row["Feature"],
                    "Coefficient": val
                })

    MeltedDF = pd.DataFrame(MeltedRows)

    if SavePath: #OPTIONALLY SAVE TO PARQUET
        try:
            CoefficientsDF.to_parquet(SavePath, index=False)
            print(f"🐾 Saved updated wide coefficients to: {SavePath}")
        except Exception as e:
            print(f"⚠️ Could not save coefficients to {SavePath}: {e}")
    return CoefficientsDF, MeltedDF #COEFFICIENTS DF IS WIDE FORM TABLE DESIGNED FOR INSIGHTS TAB / MELTED DF IS LONG FORM FOR ANALYTICS, PLOTTING, AND TRACKING

def CompleteDataCat(InputDF, RegressionMeow):
    InputDF["PredictedMood"] = RegressionMeow.CatPrediction #THIS IS TO FILL IN THE REST OF THE DATA TAB
    InputDF["MoodEpsilon"] = InputDF["ActualMood"] - InputDF["PredictedMood"]
    InputDF["PredictedSass"] = RegressionMeow.CatPrediction
    InputDF["SassEpsilon"] = InputDF["ActualSass"] - InputDF["PredictedSass"]

    InputDF["Observer"] = pd.to_numeric(InputDF["Observer"], errors="coerce").fillna(0).astype(int) #CONVERT OBSERVER TO NUMERIC

    InputDF["ActualSurvival"] = InputDF["ActualSurvival"].replace({"": None, None: None}) #IF OBSERVER IS NOT PRESENT, SURVIVAL IS UNKNOWN
    InputDF.loc[InputDF["Observer"] == 0, "ActualSurvival"] = "Unknown"

    InputDF["ActualSurvival"] = InputDF["ActualSurvival"].apply( #CONVERT TO NUMERIC IF OBSERVER IS PRESENT
                lambda x: float(x) if str(x).replace(".", "", 1).isdigit() else "Unknown")

    PredictedSurvival = RegressionMeow.Predictions.get("Survival") #PREDICTED SURVIVAL
    if PredictedSurvival is None:
        PredictedSurvival = pd.Series([None] * len(InputDF), index=InputDF.index)
    if not isinstance(PredictedSurvival, pd.Series):
        PredictedSurvival = pd.Series(PredictedSurvival, index=InputDF.index)

    InputDF["PredictedSurvival"] = PredictedSurvival  # NUMERIC VALUE
    InputDF["PredictedSurvival"] = InputDF["PredictedSurvival"].astype("object")  # TO ALLOW FOR STRINGS AND NUMBERS
    InputDF.loc[InputDF["Observer"] == 0, "PredictedSurvival"] = "Unknown"

    def GetSurvivalEpsilon(row): #SURVIVAL RESIDUAL
        if row["Observer"] == 0 or row["PredictedSurvival"] == "Unknown" or row["ActualSurvival"] == "Unknown":
            return "Unknown"
        try:
            return float(row["ActualSurvival"]) - float(row["PredictedSurvival"])
        except Exception:
            return "Unknown"

    InputDF["SurvivalEpsilon"] = InputDF.apply(GetSurvivalEpsilon, axis=1).astype("object")

    # --- Observer display cleanup ---
    InputDF["Observer"] = InputDF["Observer"].map({1: "YES", 0: "NO"})
    return InputDF

def GetMetricsDF(RegressionMeow, SavePath=None): # BUILDS AND OPTIONALLY SAVES A CLEAN METRICS DF FOR MOOD, SASS, AND SURVIVAL / RETURNS BOTH WIDE AND LONG FORM DFs
    CatMetrics = ["R2", "Intercept", "MAE", "MSE", "RMSE", "Accuracy", "Precision", "Recall", "F1", "AUC"] #DEFINE METRICS IN CONSISTENT ORDER

    MetricsDF = pd.DataFrame({ # 🧮  BUILD WIDE METRICS DF
        "Metric": CatMetrics,
        "Mood": [RegressionMeow.Metrics.get("Mood", {}).get(key.lower(), "N/A") for key in CatMetrics],
        "Sass": [RegressionMeow.Metrics.get("Sass", {}).get(key.lower(), "N/A") for key in CatMetrics],
        "Survival": [RegressionMeow.Metrics.get("Survival", {}).get(key.lower(), "N/A") for key in CatMetrics],
        "ModelInsights": [""] * len(CatMetrics)
    })
    for col in ["Mood", "Sass", "Survival"]: #🧹 CLEAN NUMERIC VALUES(CONVERT IF POSSIBLE)
        MetricsDF[col] = pd.to_numeric(MetricsDF[col], errors="coerce").fillna(0)
    MeltedRows = [] # 🧾 BUILD LONG FOR ANALYSIS AND PLOTTING
    for _, row in MetricsDF.iterrows():
        for target in ["Mood", "Sass", "Survival"]:
            MeltedRows.append({
                "Target": target,
                "Metric": row["Metric"],
                "Value": row[target]
            })
    MeltedDF = pd.DataFrame(MeltedRows)

    if SavePath: # 💾 OPTIONALLY SAVE WIDE FOR PARQUET
        try:
            MetricsDF.to_parquet(SavePath, index=False)
            print(f"📊 Saved updated metrics to: {SavePath}")
        except Exception as e:
            print(f"⚠️ Could not save metrics to {SavePath}: {e}")
    return MetricsDF, MeltedDF

def GenerateNewData(UserName, RowQTY):#CREATES A CSV FILE WITH  'RANDOMLY' GENERATED DATA AND RETURNS A DF AND CSV PATH
    Initials = "".join([p[0].upper() for p in UserName.split() if p])
    df, CSVName = GetNewCatData(int(RowQTY), Initials)
    return df, CSVName

def AnalyzeNewData(InputCSV, OutputPath, HistoryPath, CoefficientsHistoryPath, MetricsHistoryPath, IncludeHistory=False): #RUNS REGRESSION ON NEW DATA, SAVES TO EXCEL, UPDATES THE HISTORICAL DATA FILE / USES HISTORICAL DATA IF USER CHECKS YES ON THE USER FORM
    try:
        InputDF = pd.read_csv(InputCSV)    
        ScaledDF = ScaleCatData(InputDF) #SCALES THE DATA SO IT WILL PLAY NICELY WITH REGRESSION MODEL
        InputRenameMap = { 
            "Box Temperature (C)": "BoxTemp",
            "Radioactive Decay Rate": "DecayRate",
            "Photon Count per Minute": "Photons",
           "Wavefunction Stability": "Stability",
            "Quantum Entanglement Index": "Entanglement",
           "Observer Presence": "Observer",
          "Box Material": "Material",
            "Actual Mood Score": "ActualMood",
            "Actual Sass Index": "ActualSass",
            "Actual Survival": "ActualSurvival"
        }

        InputDF = normalize_headers(InputDF, InputRenameMap)
        CatDataHeaders= [
            "BoxTemp",
            "DecayRate",
            "Photons",
            "Stability",
            "Entanglement",
            "Observer",
            "Material",
            "ActualMood",
            "PredictedMood",
            "MoodEpsilon",
            "ActualSass",
            "PredictedSass",
            "SassEpsilon",
            "ActualSurvival",
            "PredictedSurvival",
            "SurvivalEpsilon"
            ]
        for col in CatDataHeaders: #MAKE SURE EXPECTED COLUMNS EXIST
            if col not in InputDF.columns:
                InputDF[col] = None 
        InputDF = InputDF[CatDataHeaders] 

        if IncludeHistory: #LOAD HISTORICAL DATA
            if os.path.exists(HistoryPath):
                HistoricalDF = pd.read_parquet(HistoryPath)
            else:
                HistoricalDF = pd.DataFrame(columns=CatDataHeaders)
            CombinedDF = pd.concat([HistoricalDF, InputDF], ignore_index=True) #COMBINE HISTORICAL DATA WITH NEW DATA
            ScaledDF = ScaleCatData(CombinedDF) #SCALE DATA
            RegressionMeow = PurrfectRegression(ScaledDF) #RUN REGRESSION ON HISTORICAL DATA AND NEW DATA
            RegressionMeow.RunRegression()
            CombinedDF.to_parquet(HistoryPath, index=False) # UPDATE HISTORICAL PARQUET WITH APPENDED ROWS
            ReportDF = CombinedDF #OUTPUT DF
        else: #ONLY NEW DATASET
            ScaledDF = ScaleCatData(InputDF) #SCALE DATA
            RegressionMeow = PurrfectRegression(ScaledDF) #RUN REGRESSION ON NEW DATA ONLY
            RegressionMeow.RunRegression()
            ReportDF = InputDF #OUTPUT DF

        CoefficientsDF = pd.DataFrame({ # BLANK DF TO HOUSE COEFFICIENTS FOR INSIGHTS TAB - HEADERS WILL NOT BE INCLUDED
            "Feature": ["BoxTemp", "DecayRate", "Photons", "Stability", "Entanglement", "Observer", "Material_Cardboard", "Material_Lead", "Material_QuantumFoam", "Material_Velvet"], 
            "MoodImportance": [0, 0, 0, 0, "N/A", "N/A", 0, 0, 0, 0],
            "SassImportance": [0, "N/A", "N/A", "N/A", 0, "N/A", "N/A", "N/A", "N/A", "N/A"],
            "SurvivalImportance": ["N/A", "N/A", "N/A", "N/A", "N/A", 0, "N/A", "N/A", "N/A", "N/A"],
            "FeatureInsights": [""]*10
            })
        CoefficientsDF, _ = StashCoefficients(CoefficientsDF, RegressionMeow)
        ReportDF = CompleteDataCat(ReportDF, RegressionMeow) #FOR EXCEL CAT
        # CREATE EXCEL REPORT
        ExcelMeow = PurrfectWB(ReportDF, OutputPath, RegressionMeow.ScatterPlots, RegressionMeow.RegressionPlots, RegressionMeow.FeatureImportances)
        ExcelMeow.DataKitten()
        ExcelMeow.ExcelLitter(OutputPath)
        ExcelMeow.InsightsKitten()

        MetricsDF, _ = GetMetricsDF(RegressionMeow) #GET THE R2, INTERCEPT, MAE, MSE, RMSE, ACCURACY, PRECISION, RECALL, F1, AND AUC
        ExcelMeow.GetCoefficientsAndMetrics(CoefficientsDF, MetricsDF) # ADD METRICS TO EXCEL REPORT
        ExcelMeow.CatWisdom(CoefficientsDF, MetricsDF) # ADD INTERPRETATIONS TO INSIGHTS COLUMN IN INSIGHTS TAB
        return OutputPath
    except Exception as e:
        messagebox.showerror("FAIL", f"Something went wrong analyzing new data:\n{e}")
        raise
  
  #*************** VIEW HISTORICAL DATA IS BROKEN 10/9/2025 ******************
def ViewHistoricalModel(HistoryPath, CoefficientsHistoryPath, MetricsHistoryPath): #RUNS REGRESSION ON HISTORICAL DATA, UPDATES COEFFCIENTS AND METRICS PARQUETS, GENERATES EXCEL REPORT WITH TIMESTAMP FOR VIEWING
    import os
    from tkinter import messagebox
    from HistoryCat import RunHistoricalRegression

    if not os.path.exists(HistoryPath): #MAKE SURE HISTROICAL FILE EXISTS
        messagebox.showerror("Missing Data", f"No historical data file found at:\n{HistoryPath}")
        return

    MissingFiles = [] #CHECK OPTIONAL SUPPORTING PARQUETS
    for PatheLabel, path in {
        "Coefficients": CoefficientsHistoryPath,
        "Metrics": MetricsHistoryPath
    }.items():
        if not os.path.exists(path):
            MissingFiles.append(f"{PatheLabel} Parquet:\n{path}")

    if MissingFiles:
        WarningMessage = "\n\n".join(MissingFiles)
        messagebox.showwarning("Missing Supporting Files",
            f"Some supporting Parquet files were not found:\n\n{WarningMessage}\n\n"
            f"They will be created automatically if possible.")

    try: #RUN HISTORICAL REGRESSION
        ResultsPath = RunHistoricalRegression(HistoryPath, CoefficientsHistoryPath, MetricsHistoryPath)
        messagebox.showinfo(
            "Purrfect Historical Regression!",
            f"Regression on historical data is meow complete.\n"
            f"You can meow view the results here:\n{ResultsPath}"
        )
    except Exception as e:
        messagebox.showerror("Cat-tastrophe!", f"Something went wrong running the historical model:\n\n{e}")
  
#*************** PREDICT DINING EXPERIENCE IS BROKEN 10/9/2025 ******************
def PredictDiningExperience(FeaturesDictionary): #TAKES A DISCTONARY OF INPUT FEATURES, LOADS HISTORICAL MODEL, AND RETURNS PREDICTED MOOD, SASS, AND SURVIVAL
    df = pd.read_csv(HistoryPath) #LOAD HISTORICAL DATA INTO A DATAFRAME
    RegressionMeow = PurrfectRegression(df) #RUN REGRESSION ON HISTORICAL DATA
    RegressionMeow.RunRegression()

    InputDF = pd.DataFrame([FeaturesDictionary]) #BUILD A SINGLE-ROW DATAFRAME

    MoodModel = RegressionMeow.Models.get("Mood") #MAKE PREDICTIONS USING THE TRAINED MODELS
    SassModel = RegressionMeow.Models.get("Sass")
    SurvivalModel = RegressionMeow.Models.get("Survival")

    CatPredictions = {
        "Mood": float(MoodModel.predict(InputDF[["BoxTemp", "DecayRate", "Photons", "Stability",
                                                   "Material_Cardboard", "Material_Lead",
                                                   "Material_QuantumFoam", "Material_Velvet"]])[0])
                 if MoodModel else None,
        "Sass": float(SassModel.predict(InputDF[["BoxTemp", "Entanglement"]])[0])
                 if SassModel else None,
        "Survival": float(SurvivalModel.predict_proba(InputDF[["Observer"]])[:, 1][0])
                 if SurvivalModel else None,
    }
    return CatPredictions

def main():
    import tkinter as tk
    from CatForms import UploadForm
    from HistoryCat import HistoryPath
    CoefficientsHistoryPath = HistoryPath.replace("Historical_Cafe_Data.parquet", "CatCoefficients.parquet") # 🧾 HISTORICAL PATH FOR COEFFICIENTS
    MetricsHistoryPath = HistoryPath.replace("Historical_Cafe_Data.parquet", "CatMetrics.parquet") # 🧾 HISTORICAL PATH FOR METRICS

    app = CatCafeMenu() # OPEN MENU
    app.mainloop()

if __name__ == "__main__":
    main()

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






import pandas as pd
from datetime import datetime
from tkinter import messagebox
from RegressionCat import PurrfectRegression
from ExcelCat import TipToe, PurrfectWB, CreateWB
from DataGenerator import ScaleCatData

#---------------------- FOR TESTING ----------------------
InputCSV = "C:\\Users\\mkb00\\PROJECTS\\GitRepos\\Schrodingers_Cat_Cafe\\Test\\CafeData.csv"
OutputPath = "C:\\Users\\mkb00\\PROJECTS\\GitRepos\\Schrodingers_Cat_Cafe\\Test\\CafeOutput.xlsx"
MasterDataPath = "C:\\Users\\mkb00\\PROJECTS\\GitRepos\\Schrodingers_Cat_Cafe\\Test\\MasterData.csv"

UserName = "Mary Kathryn Barriault"
name_parts = UserName.split()
if len(name_parts) < 2:
    messagebox.showerror("Invalid Name", "Please enter at least a first and last name.")
first_initial = name_parts[0][0].upper()
last_initial = name_parts[-1][0].upper()
middle_initial = name_parts[1][0].upper() if len(name_parts) > 2 else "" # MIDDLE INITIAL = OPTIONAL
initials = first_initial + middle_initial + last_initial # COMBINE INITIALS

TodaysDate = datetime.today().strftime("%Y%m%d")


def normalize_headers(df, AliasMap):
    RenameMap = {}
    for aliases, standard_name in AliasMap.items():
        for alias in aliases.split("|"):
            if alias in df.columns:
                RenameMap[alias] = standard_name
    return df.rename(columns=RenameMap)



def StashCoefficients(CoefficientsDF, RegressionMeow): #HELPER FUNCTION
    for idx, row in CoefficientsDF.iterrows():
        feat = row["Feature"]
        # Mood Coeffs
        if feat in RegressionMeow.FeatureImportances.get("Mood", {}):
            CoefficientsDF.at[idx, "MoodImportance"] = RegressionMeow.FeatureImportances["Mood"][feat]
        # Sass Coeffs
        if feat in RegressionMeow.FeatureImportances.get("Sass", {}):
            CoefficientsDF.at[idx, "SassImportance"] = RegressionMeow.FeatureImportances["Sass"][feat]
        # Survival Coeffs
        if feat in RegressionMeow.FeatureImportances.get("Survival", {}):
            CoefficientsDF.at[idx, "SurvivalImportance"] = RegressionMeow.FeatureImportances["Survival"][feat]
    return CoefficientsDF


def GetMetricsDF(RegressionMeow):
    MetricsDF = pd.DataFrame({
        "Metric": ["R2", "Intercept", "MAE", "MSE", "RMSE", "Accuracy", "Precision", "Recall", "F1", "AUC"],
        "Mood": [
            RegressionMeow.Metrics.get("Mood", {}).get("r2", "N/A"),
            RegressionMeow.Metrics.get("Mood", {}).get("intercept", "N/A"),
            RegressionMeow.Metrics.get("Mood", {}).get("mae", "N/A"),
            RegressionMeow.Metrics.get("Mood", {}).get("mse", "N/A"),
            RegressionMeow.Metrics.get("Mood", {}).get("rmse", "N/A"),
            RegressionMeow.Metrics.get("Mood", {}).get("accuracy", "N/A"), # FOR SURVIVAL ONLY
            RegressionMeow.Metrics.get("Mood", {}).get("precision", "N/A"), # FOR SURVIVAL ONLY
            RegressionMeow.Metrics.get("Mood", {}).get("recall", "N/A"), # FOR SURVIVAL ONLY
            RegressionMeow.Metrics.get("Mood", {}).get("f1", "N/A"), # FOR SURVIVAL ONLY
            RegressionMeow.Metrics.get("Mood", {}).get("auc", "N/A"), # FOR SURVIVAL ONLY
        ],
        "Sass": [
            RegressionMeow.Metrics.get("Sass", {}).get("r2", "N/A"),
            RegressionMeow.Metrics.get("Sass", {}).get("intercept", "N/A"),
            RegressionMeow.Metrics.get("Sass", {}).get("mae", "N/A"),
            RegressionMeow.Metrics.get("Sass", {}).get("mse", "N/A"),
            RegressionMeow.Metrics.get("Sass", {}).get("rmse", "N/A"),
            RegressionMeow.Metrics.get("Sass", {}).get("accuracy", "N/A"),  # FOR SURVIVAL ONLY
            RegressionMeow.Metrics.get("Sass", {}).get("precision", "N/A"), # FOR SURVIVAL ONLY 
            RegressionMeow.Metrics.get("Sass", {}).get("recall", "N/A"), # FOR SURVIVAL ONLY
            RegressionMeow.Metrics.get("Sass", {}).get("f1", "N/A"), # FOR SURVIVAL ONLY
            RegressionMeow.Metrics.get("Sass", {}).get("auc", "N/A"), # FOR SURVIVAL ONLY
        ],
        "Survival": [
            RegressionMeow.Metrics.get("Survival", {}).get("r2", "N/A"),
            RegressionMeow.Metrics.get("Survival", {}).get("intercept", "N/A"),
            RegressionMeow.Metrics.get("Survival", {}).get("mae", "N/A"),
            RegressionMeow.Metrics.get("Survival", {}).get("mse", "N/A"),
            RegressionMeow.Metrics.get("Survival", {}).get("rmse", "N/A"),
            RegressionMeow.Metrics.get("Survival", {}).get("accuracy", "N/A"),  # FOR SURVIVAL ONLY
            RegressionMeow.Metrics.get("Survival", {}).get("precision", "N/A"), # FOR SURVIVAL ONLY
            RegressionMeow.Metrics.get("Survival", {}).get("recall", "N/A"), # FOR SURVIVAL ONLY
            RegressionMeow.Metrics.get("Survival", {}).get("f1", "N/A"), # FOR SURVIVAL ONLY
            RegressionMeow.Metrics.get("Survival", {}).get("auc", "N/A"), # FOR SURVIVAL ONLY
        ],
        "ModelInsights": [""]*10
    })
    return MetricsDF

def main():
    InputDF = pd.read_csv("CafeData.csv")
    ScaledInputDF = ScaleCatData(InputDF)
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
 
    CoefficientsDF = pd.DataFrame({ #INSIGHTS TAB - HEADERS WILL NOT BE INCLUDED
        "Feature": ["BoxTemp", "DecayRate", "Photons", "Stability", "Entanglement", "Observer", "Material_Cardboard", "Material_Lead", "Material_QuantumFoam", "Material_Velvet"], 
        "MoodImportance": [0, 0, 0, 0, "N/A", "N/A", 0, 0, 0, 0],
        "SassImportance": [0, "N/A", "N/A", "N/A", 0, "N/A", "N/A", "N/A", "N/A", "N/A"],
        "SurvivalImportance": ["N/A", "N/A", "N/A", "N/A", "N/A", 0, "N/A", "N/A", "N/A", "N/A"],
        "FeatureInsights": [""]*10
        })
    

    RegressionMeow = PurrfectRegression(ScaledInputDF) #RUN REGRESSION MODEL ON THE SCALED DF
    RegressionMeow.RunRegression()

    CoefficientsDF = StashCoefficients(CoefficientsDF, RegressionMeow) #THIS IS FOR THE INSIGHTS TAB

    InputDF["PredictedMood"] = RegressionMeow.CatPrediction #THIS IS TO FILL IN THE REST OF THE DATA TAB
    InputDF["MoodEpsilon"] = InputDF["ActualMood"] - InputDF["PredictedMood"]
    InputDF["PredictedSass"] = RegressionMeow.CatPrediction
    InputDF["SassEpsilon"] = InputDF["ActualSass"] - InputDF["PredictedSass"]

    InputDF["Observer"] = pd.to_numeric(InputDF["Observer"], errors="coerce").fillna(0).astype(int) #CONVERT OBSERVER TO NUMERIC

    InputDF["ActualSurvival"] = InputDF["ActualSurvival"].replace({"": None, None: None}) #IF OBSERVER IS NOT PRESENT, SURVIVAL IS UNKNOWN
    InputDF.loc[InputDF["Observer"] == 0, "ActualSurvival"] = "Unknown"

    InputDF["ActualSurvival"] = InputDF["ActualSurvival"].apply( #CONVERT TO NUMERIC IF OBSERVER IS PRESENT
        lambda x: float(x) if str(x).replace(".", "", 1).isdigit() else "Unknown"
    )

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



    ExcelMeow = PurrfectWB(InputDF, OutputPath, RegressionMeow.ScatterPlots, RegressionMeow.RegressionPlots, RegressionMeow.FeatureImportances)
    ExcelMeow.DataKitten()
    ExcelMeow.ExcelLitter(OutputPath)
    ExcelMeow.InsightsKitten()


    MetricsDF = GetMetricsDF(RegressionMeow) #GET METRICS INTO DF FOR INSIGHTS TAB
    r2_mood = RegressionMeow.Metrics["Mood"]["r2"]
    intercept_mood = RegressionMeow.Metrics["Mood"]["intercept"]
    mae_mood = RegressionMeow.Metrics["Mood"]["mae"]
    mse_mood = RegressionMeow.Metrics["Mood"]["mse"]
    rmse_mood = RegressionMeow.Metrics["Mood"]["rmse"]

    r2_sass = RegressionMeow.Metrics["Sass"]["r2"]
    intercept_sass = RegressionMeow.Metrics["Sass"]["intercept"]
    mae_sass = RegressionMeow.Metrics["Sass"]["mae"]
    mse_sass = RegressionMeow.Metrics["Sass"]["mse"]
    rmse_sass = RegressionMeow.Metrics["Sass"]["rmse"]

    accuracy_survival = RegressionMeow.Metrics["Survival"]["accuracy"]
    precision_survival = RegressionMeow.Metrics["Survival"]["precision"]
    recall_survival = RegressionMeow.Metrics["Survival"]["recall"]
    f1_survival = RegressionMeow.Metrics["Survival"]["f1"]
    auc_survival = RegressionMeow.Metrics["Survival"]["auc"]

    if intercept_mood > 0:
        MoodDefault = "Quantum Bliss 😸✨"
    else:
        MoodDefault = "existential dread 😿"

    if intercept_sass > 0:
        SassDefault = "Less sass"
    else:
        SassDefault = "Sass Pants"


    MetricsDF = pd.DataFrame({
        "Metric": ["R2", "Beta", "MAE", "MSE", "RMSE", "Accuracy", "Precision", "Recall", "F1", "AUC"],
        "Mood": [r2_mood, intercept_mood, mae_mood, mse_mood, rmse_mood,"N/A", "N/A", "N/A", "N/A", "N/A"],
        "Sass": [r2_sass, intercept_sass, mae_sass, mse_sass, rmse_sass, "N/A", "N/A", "N/A", "N/A", "N/A"],
        "Survival": ["N/A", "N/A", "N/A", "N/A", "N/A", accuracy_survival, precision_survival, recall_survival, f1_survival, auc_survival],
        "ModelInsights": [
            f"Model explains: {r2_mood * 100:.2f}% of mood / {r2_sass * 100:.2f}% of sass variation 💅",
            f"Cats default to {MoodDefault} and {SassDefault}",
            f"On average, predictions miss by {mae_mood:.2f} mood points and {mae_sass:.2f} Sass points 🐱🔮",
            f"Model errors (squared) average {mse_mood:.2f} for mood and {mse_sass:.2f} for Sass",
            f"Predictions are typically within ±{rmse_mood:.2f} of true cat mood and ±{rmse_sass:.2f} of true cat sass 😻✅",
            f"Survival Accuracy: {accuracy_survival}",
            f"Survival Precision: {precision_survival}",
            f"Survival Recall: {recall_survival}",
            f"Survival F1: {f1_survival}",
            f"Survival auc: {auc_survival}"
        ]
    })





    ExcelMeow.GetCoefficientsAndMetrics(CoefficientsDF, MetricsDF)
    ExcelMeow.CatWisdom(CoefficientsDF, MetricsDF)



if __name__ == "__main__":
    main()

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


def Headers():

    #----------------------INSIGHTS TAB----------------------
    InsightsDF = pd.DataFrame({ #This is for the top half of the INSIGHTS tab but the headers will not be included in the output due to formatting
        "Feature": ["BoxTemp", "DecayRate", "Photons", "Stability", "Entanglement", "Observer", "Material_Cardboard", "Material_Lead", "Material_Quantumfoam", "Material_Velvet"], 
        "MoodImportance": [0, 0, 0, 0, "N/A", "N/A", 0, 0, 0, 0],
        "SassImportance": [0, "N/A", "N/A", "N/A", 0, "N/A", "N/A", "N/A", "N/A", "N/A"],
        "SurvivalImportance": ["N/A", "N/A", "N/A", "N/A", "N/A", 0, "N/A", "N/A", "N/A", "N/A"],
        "FeatureInsights": ["N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A", "N/A"]
        })

    FeatureOutput = [ # This is for the INSIGHTS tab.  The values on the left will be what's on the workbook and the values on the right are how they're named in the data frame
        ("BOX TEMP (Celsius)", "BoxTemp"),
        ("RADIOACTIVE DECAY RATE", "DecayRate"),
        ("PHOTON COUNT (per min)", "Photons"),
        ("WAVEFUNCTION STABILITY", "Stability"),
        ("ENTANGLEMENT INDEX", "Entanglement"),
        ("OBSERVER PRESENCE", "Observer"),
        ("CARDBOARD BOX", "Material_Cardboard"),
        ("LEAD BOX", "Material_Lead"),
        ("QUANTUM FOAM BOX", "Material_Quantumfoam"),
        ("VELVET BOX", "Material_Velvet"),
    ]

    MetricsDF = pd.DataFrame({ #this is for the MODEL INSIGHTS section of the INSIGHTS tab in the output 
        "Metric": ["R2,", "Beta", "MAE", "MSE", "RMSE"],
        "Mood": [0, 0, 0, 0, 0],
        "Sass": [0, 0, 0, 0, 0],
        "Survival": [0, 0, 0, 0, 0],
        "ModelInsights": ["N/A", "N/A", "N/A", "N/A", "N/A"]
        })

    MetricsHeaders = ["METRIC", "MOOD SCORE", "SASS INDEX", "SURVIVAL RATE", "INSIGHTS"] #This will be for row 17 in the INSIGHTS tab on the output

    MetricsRenameMap = { #This is for A18:A22 in the INSIGHTS tab of the output
        "R2": "Coefficient of Determination:",
        "Beta": "Intercept:",
        "MAE": "Mean Absolute Error",
        "MSE": "Mean Squared Error",
        "RMSE": "Root Mean Squared Error"
    }

    #----------------------DATA TAB----------------------
    DataTabHeaders = ["BOX\nTEMPERATURE\n(Celsius)", "RADIOACTIVE\nDECAY RATE", "PHOTON COUNT\n(PER MINUTE)", "WAVEFUNCTION\nSTABILITY", "ENTANGLEMENT\nINDEX", "OBSERVER\nPRESENT?", "BOX\nMATERIAL", "ACTUAL\nMOOD SCORE", "PREDICTED\nMOOD SCORE", "MOOD SCORE\nRESIDUAL", "ACTUAL\nSASS INDEX", "PREDICTED\nSASS INDEX", "SASS INDEX\nRESIDUAL", "ACTUAL\nSURVIVAL", "PREDICTED\nSURVIVAL", "SURVIVAL RATE\nRESIDUAL"] #Data tab headers in order

    

    #----------------------SCATTER PLOT TAB----------------------
    ScatterHeaders = ["", "MOOD SCORE", "", "SASS INDEX", "", "SURVIVAL RATE", ""]  #Headers for scatter plot tab - will be inserted into row 2 / A, C, E, and G are blanks


    #----------------TARGET / FEATURES

    MoodFeatures = ["BoxTemp", "DecayRate", "Photons", "Stability", "Material"]
    SassFeatures = ["BoxTemp", "Entanglement"]
    SurvivalFeatures = ["Observer"]


        # Registry of targets and their settings

def normalize_headers(df, AliasMap):
    RenameMap = {}
    for aliases, standard_name in AliasMap.items():
        for alias in aliases.split("|"):
            if alias in df.columns:
                RenameMap[alias] = standard_name
    return df.rename(columns=RenameMap)

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
 
    print(InputDF)
    print(ScaledInputDF)
    print(InputDF["Observer"])


    RegressionMeow = PurrfectRegression(ScaledInputDF)
    RegressionMeow.RunRegression()

    InputDF["PredictedMood"] = RegressionMeow.CatPrediction
    InputDF["MoodEpsilon"] = InputDF["ActualMood"] - InputDF["PredictedMood"]
    InputDF["PredictedSass"] = RegressionMeow.CatPrediction
    InputDF["SassEpsilon"] = InputDF["ActualSass"] - InputDF["PredictedSass"]
    
    InputDF["Observer"] = pd.to_numeric(InputDF["Observer"], errors="coerce").fillna(0).astype(int) #OBSERVER = NUMERIC

    InputDF["ActualSurvival"] = InputDF["ActualSurvival"].replace({"": None, None: None}).astype(object) #NORMALIZE BLANKS/NON AND MARK UNOBSERVED ROWS AS UNKNOWN
    mask_unobserved = InputDF["Observer"] == 0
    InputDF.loc[mask_unobserved, "ActualSurvival"] = "Unknown"

    InputDF["ActualSurvivalNum"] = pd.to_numeric(InputDF["ActualSurvival"].replace({"Unknown": None}), errors="coerce").astype(float) #CREATE NUMERIC COLUMN FOR MODELING - UNKNOWNS BECME NAN

    mask_observed = (InputDF["Observer"] == 1) & InputDF["ActualSurvivalNum"].notna() #MASK NUMERIC COLUMN
    mask_unobserved = InputDF["Observer"] == 0

    InputDF["PredictedSurvival"] = None #ENSURE EXISTENCE OF COLUMNS
    InputDF["SurvivalEpsilon"] = None

    InputDF.loc[mask_unobserved, "PredictedSurvival"] = "Unknown" #DISPLAY VALUES FOR UNOBSERVED ROWS
    InputDF.loc[mask_unobserved, "SurvivalEpsilon"] = "Unknown"

    preds = RegressionMeow.Predictions.get("Survival")  # GET PREDICTIONS - pd SERIES 
    if preds is None:
        preds = pd.Series([None] * len(InputDF), index=InputDF.index)
    if not isinstance(preds, pd.Series): #IF PREDICTIONS IS NUMPY ARRAY -> CONVERT TO SERIES W/O CHANGING INDEX
        preds = pd.Series(preds, index=InputDF.index)

    InputDF.loc[mask_observed, "PredictedSurvival"] = preds.loc[mask_observed].astype(float) #NUMERIC PREDICTIONS AND COMPUTE RESIDUALS
    InputDF.loc[mask_observed, "SurvivalEpsilon"] = (
        InputDF.loc[mask_observed, "ActualSurvivalNum"].astype(float)
        - InputDF.loc[mask_observed, "PredictedSurvival"].astype(float)
    )

    print(InputDF)


    if "ActualSurvivalNum" in InputDF.columns and "ActualSurvival" in InputDF.columns:
        InputDF = InputDF.copy() #SAFETY COPY
        mask_known_num = InputDF["ActualSurvivalNum"].notna() #USE NUMBERS WHERE POSSIBLE, IF NOT, USE UNKNOWN
        InputDF["ActualSurvival_Display"] = InputDF["ActualSurvival"].astype(object) #SET DISPLAY COLUMN TO TEXTUAL VALUES (including "Unknown")
        InputDF.loc[mask_known_num, "ActualSurvival_Display"] = InputDF.loc[mask_known_num, "ActualSurvivalNum"] #OVERWRITE NUMERIC ONLY VALUS 
        InputDF["ActualSurvival"] = InputDF["ActualSurvival_Display"] #REPLACE OF COLUMN WITH DISPLAY COLUMN
        InputDF = InputDF.drop(columns=["ActualSurvival_Display", "ActualSurvivalNum"])




        # Prepare Excel
    ExcelMeow = PurrfectWB(InputDF, OutputPath, RegressionMeow.ScatterPlots, RegressionMeow.RegressionPlots)
    ExcelMeow.DataKitten()
    ExcelMeow.ExcelLitter(OutputPath)

if __name__ == "__main__":
    main()

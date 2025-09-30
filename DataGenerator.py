import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from datetime import datetime
import csv


def GetNewCatData(RowQTY, Initials): #RowQTY and Initials will come from user form
    np.random.seed(42)
    n = RowQTY  # Number of rows

    #Get the name for new CSV file
    TodaysDate = datetime.today().strftime("%Y%m%d")
    CSVname = f"NewCatCafeData_{TodaysDate}_{Initials}.csv" #Initials will come from a user form


    BoxTemp = np.round(np.random.normal(loc=24, scale=5, size=n), 2) # Box Temperature (°C) / Generate 100 box temperatures with a normal distribution / Affects comfort and decay rate of quantum particles
    Photons = np.random.poisson(lam=300, size=n) # Photon Count per Minute / Poisson distribution for discrete quantum events / Measures quantum activity inside the box
    Entanglement = np.round(np.random.beta(a=2, b=1.5, size=n), 3) # Quantum Entanglement Index (0.0 to 1.0, skewed toward higher entanglement) / Degree of entanglement with external systems
    Observer = np.random.choice([0, 1], size=n, p=[0.35, 0.65])  # Observer Presence (0 = unobserved, 1 = observed) /  Mostly unobserved
    DecayRate = np.round(np.random.uniform(0.1, 0.9, size=n), 3) # Radioactive Decay Rate / Probability of poison release mechanism triggering / 0.0 to 1.0, higher means more likely to trigger poison
    Stability = np.round(np.random.normal(loc=0.6, scale=0.15, size=n), 3) # Wavefunction Stability / How stable the cat’s quantum state is / 0.0 to 1.0, higher = more stable
    Stability= np.clip(Stability, 0, 1)
    Materials = ['Cardboard', 'Lead', 'Graphene', 'Velvet', 'Quantum Foam'] # Box Material (categorical) / Categorical: cardboard, lead, graphene, etc.
    Material = np.random.choice(Materials, size=n)

    df = pd.DataFrame({ # CREATE DF - Headers are for the output csv
        'Box Temperature (C)': BoxTemp,
        'Radioactive Decay Rate': DecayRate,
        'Photon Count per Minute': Photons,
        'Wavefunction Stability': Stability,
        'Quantum Entanglement Index': Entanglement,
        'Observer Presence': Observer,
        'Box Material': Material
    })

    df["Observer Presence"] = df["Observer Presence"].astype(int)

    #POPULATE SYTHETIC MOOD SCORES - between 0 and 100
    MaterialMap = { 
        "Cardboard": 2.0,
        "Lead": -5.0,
        "Velvet": 5.0,
        "QuantumFoam": 8.0
        }

    MaterialScore = df["Box Material"].map(MaterialMap).fillna(0.0)
    MoodNoise = np.random.normal(loc=0.0, scale=5.0, size=len(df))

    MoodScore = (
        1.7 * df["Box Temperature (C)"] +
        -20 * df["Radioactive Decay Rate"] +
        0.05 * df["Photon Count per Minute"] +
        30 * df["Wavefunction Stability"] +
        MaterialScore +
        MoodNoise

    )
    MoodScore = np.clip(MoodScore, 0, 100) 
    df["Actual Mood Score"] = MoodScore.round(2)

    SassNoise = np.random.normal(loc=0.0, scale=10.0, size=len(df)) # POPULATE SYNTHETIC ACTUAL SASS INDEX - based on temp and entanglement
    SassIndex = (
        70 * df["Quantum Entanglement Index"] +
        0.8 * df["Box Temperature (C)"] +
        SassNoise
    )
    SassIndex = np.clip(SassIndex, 0, 100)
    df["Actual Sass Index"] = SassIndex.round(2)

    SurvivalRate = [] # POPULATE SYNTHETIC SURVIVAL RATE - EITHER DEAD OR ALIVE / 1, 0
    for obs in df["Observer Presence"]:
        if obs == 0:
            SurvivalRate.append("Unknown")
        else:
            SurvivalRate.append(np.random.choice([0, 1]))  # 50/50 alive or dead
    df["Actual Survival"] = SurvivalRate

    df.to_csv(CSVname, index=False) # Save to CSV
    return df, CSVname



def ScaleCatData(InputCSV, Initials):
    """
    Scales numeric features using StandardScaler (default).
    Returns scaled dataframe and fitted scaler (for later inverse transform).
    """
    InputDF = pd.read_csv(InputCSV)
    TodaysDate = datetime.today().strftime("%Y%m%d")
    ScaledCSVname = f"ScaledCatCafeData_{TodaysDate}_{Initials}.csv"
    FeaturesToScale = ["BoxTemp", "DecayRate", "Photons", "Stability", "Entanglement"]


    def ScaleDF(InputDF, features=FeaturesToScale, scaler=None):
        if scaler is None:
            scaler = StandardScaler()
            ScaledDF = scaler.fit_transform(InputDF[features])
        else:
            ScaledDF = scaler.transform(InputDF[features])
        
        ScaledDF = pd.DataFrame(ScaledDF, columns=features, index=InputDF.index)
        
        # keep non-scaled columns
        FinalScaledDF = InputDF.copy()
        for col in features:
            FinalScaledDF[col] = ScaledDF[col]
        return FinalScaledDF, scaler
    
    InputDF = InputDF.rename(columns={ #The data generated has the headers on the left.  Converting to headers on the right for ease of use.
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
    })

    for col in ["PredictedMood", "PredictedSass", "PredictedSurvival", "MoodEpsilon", "SassEpsilon", "SurvivalEpsilon"]:
        InputDF[col] = None  # PLACEHOLDERS FOR PREDICTIONS AND ERRORS

    ScaledCatDF, scaler = ScaleDF(InputDF)
        
    NumericalColumns = ["BoxTemp", "DecayRate", "Photons", "Stability", "Entanglement", "ActualMood", "ActualSass"]
    #BooleanColumns = ["Observer", "ActualSurvival"]

    ScaledCatDF[NumericalColumns] = ScaledCatDF[NumericalColumns].astype(float)
    #ScaledCatDF[BooleanColumns] = ScaledCatDF[BooleanColumns].astype(bool)

    ScaledCatDF.to_csv(ScaledCSVname, index=False, float_format="%.6f") # Save to CSV

    return ScaledCatDF, ScaledCSVname





Initials = "MKB"
RowQTY = 10
NewCatData = GetNewCatData(RowQTY, Initials)
CatDF = NewCatData[0]
InputCSV = NewCatData[1]
NewScaledCatData = ScaleCatData(InputCSV, Initials)
NewScaledCatDF = NewScaledCatData[0]
NewScaledCSV = NewScaledCatData[1]























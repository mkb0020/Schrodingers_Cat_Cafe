import numpy as np
import pandas as pd
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from datetime import datetime
import csv


def GetNewCatData(RowQTY, Initials): #ROW QTY AND INITIALS WILL ULTIMATELY COME FROM USER FORM
    np.random.seed(42)
    n = RowQTY  

    TodaysDate = datetime.today().strftime("%Y%m%d") #THIS WILL BE USED FOR THE NAME OF THE OUTPUT CSV FILE IF NEEDED
    CSVname = f"NewCatCafeData_{TodaysDate}_{Initials}.csv" #INITIALS WILL COME FROM USER FORM


    BoxTemp = np.round(np.random.normal(loc=24, scale=5, size=n), 2) # BOX TEMPERATURE (°C) / GENERATE 100 BOX TEMPERATURES WITH A NORMAL DISTRIBUTION / AFFECTS COMFORT AND DECAY RATE OF QUANTUM PARTICLES
    Photons = np.random.poisson(lam=300, size=n) # PHOTON COUNT PER MINUTE / POISSON DISTRIBUTION FOR DISCRETE QUANTUM EVENTS / MEASURES QUANTUM ACTIVITY INSIDE THE BOX
    Entanglement = np.round(np.random.beta(a=2, b=1.5, size=n), 3) # QUANTUM ENTANGLEMENT INDEX (0.0 TO 1.0, SKEWED TOWARD HIGHER ENTANGLEMENT) / DEGREE OF ENTANGLEMENT WITH EXTERNAL SYSTEMS
    Observer = np.random.choice([0, 1], size=n, p=[0.35, 0.65])  # OBSERVER PRESENCE (0 = UNOBSERVED, 1 = OBSERVED) / MOSTLY UNOBSERVED
    DecayRate = np.round(np.random.uniform(0.1, 0.9, size=n), 3) # RADIOACTIVE DECAY RATE / PROBABILITY OF POISON RELEASE MECHANISM TRIGGERING / 0.0 TO 1.0, HIGHER MEANS MORE LIKELY TO TRIGGER POISON
    Stability = np.round(np.random.normal(loc=0.6, scale=0.15, size=n), 3) # WAVEFUNCTION STABILITY / HOW STABLE THE CAT’S QUANTUM STATE IS / 0.0 TO 1.0, HIGHER = MORE STABLE
    Stability= np.clip(Stability, 0, 1)
    Materials = ['Cardboard', 'Lead', 'Graphene', 'Velvet', 'QuantumFoam'] # BOX MATERIAL (CATEGORICAL) / CATEGORICAL: CARDBOARD, LEAD, GRAPHENE, ETC.

    Material = np.random.choice(Materials, size=n)

    df = pd.DataFrame({# CREATE DF - HEADERS ARE FOR THE OUTPUT CSV

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

def ScaleCatData(InputDF):
    """
    Scales numeric features using StandardScaler (default).
    Returns scaled dataframe and fitted scaler (for later inverse transform).
    """
    FeaturesToScale = ["BoxTemp", "DecayRate", "Photons", "Stability", "Entanglement"]
    def ScaleDF(InputDF, features=FeaturesToScale, scaler=None):
        if scaler is None:
            scaler = StandardScaler()
            ScaledDF = scaler.fit_transform(InputDF[features])
        else:
            ScaledDF = scaler.transform(InputDF[features])
        
        ScaledDF = pd.DataFrame(ScaledDF, columns=features, index=InputDF.index)
        
        FinalScaledDF = InputDF.copy() # KEEP NON-SCALED COLUMNS
        for col in features:
            FinalScaledDF[col] = ScaledDF[col]
        return FinalScaledDF, scaler
    
    InputDF = InputDF.rename(columns={ 
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
    ScaledCatDF[NumericalColumns] = ScaledCatDF[NumericalColumns].astype(float)
    return ScaledCatDF


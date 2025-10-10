import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression, LogisticRegression
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score, accuracy_score
from sklearn.metrics import precision_score, recall_score, f1_score, roc_auc_score

class PurrfectRegression:
    def __init__(self, df):
        self.df = df.copy()
        # --- CONTAINERS ---
        self.ScatterPlots = {}
        self.RegressionPlots = {}
        self.Models = {}    #STORES MODEL OBJECTS KEYED BY TARGET SHORT NAME       
        self.Linears = {}    #ONLY LINEAR MODELS KEYED BY TARGET WHERE APPLICABLE          
        self.Predictions = {}  #PER TARGET PREDICTIONS (ARRAY)         
        self.CatPrediction = None       
        self.EncodedDF = None #DF FOR ONE HOT ENCODING MATERIALS
        self.Metrics = {} # METRICS PER TARGET
        self.FeatureImportances = {} # COEFFICIENT PER TARGET (DICT OF DICTS) 
        self.InsightFeatures = [ # INSIGHTS FEATURE ORDER FOR EXCEL / INSIGHTS TAB
            "BoxTemp",
            "DecayRate",
            "Photons",
            "Stability",
            "Entanglement",
            "Observer",
            "Material_Cardboard",
            "Material_Lead",
            "Material_QuantumFoam",
            "Material_Velvet",
        ]
        self.PlotTitles = {  # EXCELCAT FRIENDLY PLOT TITLES
            # MOOD
            "BoxTemp_Mood": "Box Temperature vs Mood Score",
            "DecayRate_Mood": "Decay Rate vs Mood Score",
            "Photons_Mood": "Photon Count vs Mood Score",
            "Stability_Mood": "Stability vs Mood Score",
            "Material_Cardboard_Mood": "Cardboard Box vs Mood Score",
            "Material_Lead_Mood": "Lead Box vs Mood Score",
            "Material_QuantumFoam_Mood": "Quantum Foam Box vs Mood Score",
            "Material_Velvet_Mood": "Velvet Box vs Mood Score",
            # SASS
            "BoxTemp_Sass": "Box Temperature vs Sass Index",
            "Entanglement_Sass": "Entanglement vs Sass Index",
            # SURVIVAL
            "Observer_Survival": "Observer Presence vs Survival Rate",
        }

    def RunRegression(self): #CREATES SCATTER PLOTS, FITS LINEAR REGRESSIN MODELS, GETS METRICS / FEATURE IMPORTANCES / COEFFICIENTS
        self.ItsGettingHotInHere()
        self.GetScatters()
        self.MoodFitting()
        self.SassFitting()
        self.SurvivalFitting()
        # --- FOR USE IN MAIN ---
        if "Mood" in self.Predictions:
            self.CatPrediction = self.Predictions["Mood"]
        elif "Sass" in self.Predictions:
            self.CatPrediction = self.Predictions["Sass"]
        elif "Survival" in self.Predictions:
            self.CatPrediction = self.Predictions["Survival"]
        self.InsightFeatures = [     # PREP FEATURES FOR INSIGHTS TAB (list of (label, columnname) pairs) 
            ("BOX TEMP (Celsius)", "BoxTemp"),
            ("RADIOACTIVE DECAY RATE", "DecayRate"),
            ("PHOTON COUNT (per min)", "Photons"),
            ("WAVEFUNCTION STABILITY", "Stability"),
            ("ENTANGLEMENT INDEX", "Entanglement"),
            ("OBSERVER PRESENCE", "Observer"),
            ("CARDBOARD BOX", "Material_Cardboard"),
            ("LEAD BOX", "Material_Lead"),
            ("QUANTUM FOAM BOX", "Material_QuantumFoam"),
            ("VELVET BOX", "Material_Velvet"),
        ]
        return {       #SUMMARY DICT FOR PROGRAMMATIC USE
            "models": self.Models,
            "metrics": self.Metrics,
            "predictions": self.Predictions,
            "plots": {"scatter": self.ScatterPlots, "regression": self.RegressionPlots},
            "feature_importances": self.FeatureImportances,
        }

        # --- HELPERS ---
    def ItsGettingHotInHere(self): #ONE HOT ENCODING FOR BOX MATERIALS
        df = self.df.copy()
        if "Material" in df.columns:
            EncodedDF = pd.get_dummies(df, columns=["Material"], prefix="Material")
        else:
            EncodedDF = df.copy()

        ExpectedBoxMaterials = [
            "Material_Cardboard",
            "Material_Lead",
            "Material_Velvet",
            "Material_QuantumFoam",
        ]
        for col in ExpectedBoxMaterials:
            if col not in EncodedDF.columns:
                EncodedDF[col] = 0

        if "Observer" in EncodedDF.columns: # OBSERVER = NUMERIC / 1 or 0
            EncodedDF["Observer"] = EncodedDF["Observer"].apply(lambda v: 1 if v in [1, True, "YES", "Yes", "yes", "Y", "y"] else (0 if v in [0, False, "NO", "No", "no", "N", "n"] else (1 if v == True else 0)))

        if "ActualSurvival" in EncodedDF.columns: 
            EncodedDF["ActualSurvival"] = pd.to_numeric(EncodedDF["ActualSurvival"], errors="coerce") #ACTUAL SURVIVAL = NUMERIC UNLESS IT's "UNKNOWN" WHICH = NAN

        self.EncodedDF = EncodedDF

    def GetScatters(self): #SCATTER PLOTS
        df = self.df.copy()

        def StashScatter(key, fig): # HELPER - CREATE AND STORE FIG 
            self.ScatterPlots[key] = fig
            plt.close(fig)

        if "ActualMood" in df.columns: # MOOD FEATURES (names expected by ExcelCat)
            # --- BOX TEMP ---
            fig, ax = plt.subplots()
            fig.set_size_inches(3.83, 2.18)
            sns.scatterplot(data=df, x="BoxTemp", y="ActualMood", ax=ax)
            ax.set_title("Box Temperature vs Mood Score")
            ax.set_ylabel("MOOD SCORE")
            fig.tight_layout()
            StashScatter("Box Temperature vs Mood Score", fig)
            # --- DECAY RATE ---
            fig, ax = plt.subplots()
            fig.set_size_inches(3.83, 2.18)
            sns.scatterplot(data=df, x="DecayRate", y="ActualMood", ax=ax)
            ax.set_title("Decay Rate vs Mood Score")
            ax.set_ylabel("MOOD SCORE")
            fig.tight_layout()
            StashScatter("Decay Rate vs Mood Score", fig)
            # --- PHOTON COUNT ---
            fig, ax = plt.subplots()
            fig.set_size_inches(3.83, 2.18)
            sns.scatterplot(data=df, x="Photons", y="ActualMood", ax=ax)
            ax.set_title("Photon Count vs Mood Score")
            ax.set_ylabel("MOOD SCORE")
            fig.tight_layout()
            StashScatter("Photon Count vs Mood Score", fig)
            # --- WAVE FUNCTION STABILITY---
            fig, ax = plt.subplots()
            fig.set_size_inches(3.83, 2.18)
            sns.scatterplot(data=df, x="Stability", y="ActualMood", ax=ax)
            ax.set_title("Stability vs Mood Score")
            ax.set_ylabel("MOOD SCORE")
            fig.tight_layout()
            StashScatter("Stability vs Mood Score", fig)
        
            if "Material" in df.columns:   # --- BOX MATERIAL (categorical) ---
                order = pd.Categorical(df["Material"]).categories
                x = pd.Categorical(df["Material"]).codes
                fig, ax = plt.subplots()
                fig.set_size_inches(3.83, 2.18)
                sns.scatterplot(x=x, y=df["ActualMood"], ax=ax)
                ax.set_xticks(range(len(order)))
                ax.set_xticklabels(order, rotation=30)
                ax.set_title("Material vs Mood Score")
                ax.set_ylabel("MOOD SCORE")
                fig.tight_layout()
                StashScatter("Material vs Mood Score", fig)

        if "ActualSass" in df.columns: #SASS FEATURES
            fig, ax = plt.subplots()
            fig.set_size_inches(3.83, 2.18)
            sns.scatterplot(data=df, x="BoxTemp", y="ActualSass", ax=ax)
            ax.set_title("Box Temperature vs Sass Index")
            ax.set_ylabel("SASS INDEX")
            fig.tight_layout()
            StashScatter("Box Temperature vs Sass Index", fig)

            fig, ax = plt.subplots()
            fig.set_size_inches(3.83, 2.18)
            sns.scatterplot(data=df, x="Entanglement", y="ActualSass", ax=ax)
            ax.set_title("Entanglement vs Sass Index")
            ax.set_ylabel("SASS INDEX")
            fig.tight_layout()
            StashScatter("Entanglement vs Sass Index", fig)

        if "ActualSurvival" in df.columns and "Observer" in df.columns: #SURVIVAL FEATURE = OBSERVER
            fig, ax = plt.subplots()
            fig.set_size_inches(3.83, 2.18)
            order = pd.Categorical(df["Observer"]).categories if "Observer" in df else None
            sns.scatterplot(data=df, x="Observer", y="ActualSurvival", ax=ax) #PLOT NUMERIC OBSERVER VALUES
            ax.set_title("Observer Presence vs Survival Rate")
            ax.set_ylabel("SURVIVAL RATE")
            fig.tight_layout()
            StashScatter("Observer Presence vs Survival Rate", fig)

    # --- HELPERS FOR MODEL FITTING
    def MoodFitting(self): # STORES MODEL UNDER KEY MOOD - LINEAR REGRESSION FOR ACTUAL MOOD USING BOX TEMP, DECAY RATE, PHOTON COUNT, STABILITY, AND ONE-HOT-ENCODED MATERIALS.  
        if "ActualMood" not in self.EncodedDF.columns:
            self.Models["Mood"] = None
            return

        ExpectedBoxMaterials = [
            "Material_Cardboard",
            "Material_Lead",
            "Material_Velvet",
            "Material_QuantumFoam",
        ]
        MoodFeatures = ["BoxTemp", "DecayRate", "Photons", "Stability"] + ExpectedBoxMaterials
        X = self.EncodedDF.reindex(columns=MoodFeatures, fill_value=0)
        y = self.EncodedDF["ActualMood"].fillna(0)
        model = LinearRegression().fit(X, y)
        preds = model.predict(X)
        intercept = float(model.intercept_)
        r2 = float(r2_score(y, preds))
        mae = float(mean_absolute_error(y, preds))
        mse = float(mean_squared_error(y, preds))
        rmse = float(np.sqrt(mse))

        self.Models["Mood"] = model
        self.Linears["Mood"] = model
        self.Predictions["Mood"] = preds
        self.Metrics["Mood"] = {
            "intercept": intercept,
            "r2": r2,
            "mae": mae,
            "mse": mse,
            "rmse": rmse,
            "accuracy": "N/A",
            "precision": "N/A",
            "recall": "N/A",
            "f1": "N/A",
            "auc": "N/A"
        }
        Coefficient = list(model.coef_)
        self.FeatureImportances["Mood"] = {feat: float(coef) for feat, coef in zip(X.columns.tolist(), Coefficient)}
        self.GetLinears(X["BoxTemp"], y, "Box Temperature vs Mood Score", figsize=(6.1, 3.02))
        self.GetLinears(X["DecayRate"], y, "Decay Rate vs Mood Score", figsize=(6.1, 3.02))
        self.GetLinears(X["Photons"], y, "Photon Count vs Mood Score", figsize=(6.1, 3.02))
        self.GetLinears(X["Stability"], y, "Stability vs Mood Score", figsize=(6.1, 3.02))
        self.GetLinears(X["Material_Cardboard"], y, "Cardboard Box vs Mood Score", figsize=(2.95, 2.2)) #ONE-HOT-ENCODED MATERIALS
        self.GetLinears(X["Material_Lead"], y, "Lead Box vs Mood Score", figsize=(2.95, 2.2)) #ONE-HOT-ENCODED MATERIALS
        self.GetLinears(X["Material_QuantumFoam"], y, "Quantum Foam Box vs Mood Score", figsize=(2.95, 2.2)) #ONE-HOT-ENCODED MATERIALS
        self.GetLinears(X["Material_Velvet"], y, "Velvet Box vs Mood Score", figsize=(2.95, 2.2)) #ONE-HOT-ENCODED MATERIALS

    def SassFitting(self): # STORES MODEL UNDER KEY SASS - LINEAR REGRESSION FOR ACTUAL SASS USING BOX TEMP, AND ENTANGLEMENT INDEX
        if "ActualSass" not in self.EncodedDF.columns:
            self.Models["Sass"] = None
            return

        X = self.EncodedDF.reindex(columns=["BoxTemp", "Entanglement"], fill_value=0)
        y = self.EncodedDF["ActualSass"].fillna(0)
        model = LinearRegression().fit(X, y)
        preds = model.predict(X)
        # --- METRICS ---
        intercept = float(model.intercept_)
        r2 = float(r2_score(y, preds))
        mae = float(mean_absolute_error(y, preds))
        mse = float(mean_squared_error(y, preds))
        rmse = float(np.sqrt(mse))

        self.Models["Sass"] = model
        self.Linears["Sass"] = model
        self.Predictions["Sass"] = preds
        self.Metrics["Sass"] = {
            "intercept": intercept,
            "r2": r2,
            "mae": mae,
            "mse": mse,
            "rmse": rmse,
            "accuracy": "N/A",
            "precision": "N/A",
            "recall": "N/A",
            "f1": "N/A",
            "auc": "N/A"
        }
        # --- COEFFICIENTS ---
        Coefficient = list(model.coef_)
        self.FeatureImportances["Sass"] = {feat: float(coef) for feat, coef in zip(X.columns.tolist(), Coefficient)}
        # --- REGRESSION PLOTS ---
        self.GetLinears(X["BoxTemp"], y, "Box Temperature vs Sass Index", figsize=(5.78, 3.22))
        self.GetLinears(X["Entanglement"], y, "Entanglement vs Sass Index", figsize=(5.78, 3.22))

    def SurvivalFitting(self):
        if "ActualSurvival" not in self.EncodedDF.columns or "Observer" not in self.EncodedDF.columns:
            self.Models["Survival"] = None
            return

        df = self.EncodedDF.copy()
        df["ActualSurvival"] = pd.to_numeric(df["ActualSurvival"], errors="coerce")
        df = df[df["ActualSurvival"].isin([0, 1])]
        if df.empty:
            self.Models["Survival"] = None
            return

        X = df[["Observer"]].astype(float)
        y = df["ActualSurvival"].astype(int)
        model = LogisticRegression(solver="liblinear").fit(X, y)
        PredictionsLabel = model.predict(X)
        PredictionsProb = model.predict_proba(X)[:, 1]

        # --- METRICS ---
        accuracy = float(accuracy_score(y, PredictionsLabel))
        precision = float(precision_score(y, PredictionsLabel, zero_division=0))
        recall = float(recall_score(y, PredictionsLabel, zero_division=0))
        f1 = float(f1_score(y, PredictionsLabel, zero_division=0))
        auc = float(roc_auc_score(y, PredictionsProb))

        self.Metrics["Survival"] = {
            "r2": "N/A",
            "intercept": "N/A",
            "mae": "N/A",
            "mse": "N/A",
            "rmse": "N/A",
            "accuracy": accuracy,
            "precision": precision,
            "recall": recall,
            "f1": f1,
            "auc": auc
        }

        coef = float(model.coef_.ravel()[0])  #FEATURE IMPORTANCE --
        self.FeatureImportances["Survival"] = {"Observer": coef}
        self.Predictions["Survival"] = pd.Series(PredictionsProb, index=df.index) #SAVE PREDICTIONS 
        self.GetLinears(X["Observer"], y, "Observer Presence vs Survival Rate", figsize=(6.88, 3.63), logistic=True)       # OBSERVER VS SURVIVAL - REGRESSION - /  OG FULL EncodedDF TO ALIGN INDEX

    def GetLinears(self, x_series, y_series, title, figsize=(4.0, 2.4), logistic=False): # PLOTTING UTILITY - CREATES AND STASHES REGRESSION-STYLE PLOT / FIG SIZE IS WIDTH IN INCHES, HEIGHT IN INCHES
        fig, ax = plt.subplots()
        fig.set_size_inches(figsize[0], figsize[1])
        try:
            sns.regplot(x=x_series, y=y_series, ax=ax, scatter_kws={"s": 20})
        except Exception: #FALL BACK TO SCATTER 
            sns.scatterplot(x=x_series, y=y_series, ax=ax)
        ax.set_title(title)
        ax.set_xlabel("")
        ax.set_ylabel(title.split(" vs ")[-1])
        fig.tight_layout()
        self.RegressionPlots[title] = fig # STORE W/ TITLE EXCELCAT WILL CALL
        plt.close(fig)
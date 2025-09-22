import pandas as pd
import sys
import os
import io
import tkinter as tk
import subprocess
import re
from tkinter import Tk, Label, Entry, Button, filedialog, simpledialog, messagebox, ttk
from tkinter import *
from datetime import datetime
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side, numbers
from openpyxl.drawing.image import Image
from CatDrip import DrippyKit
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import OneHotEncoder
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error

#---------------------------- CLASSES TO COLLECT INFO, CLEAN DATA, AND GET THE HEADERS ---------------------------- 
DF_HEADERS = [
    "BoxTemp",
    "Photons",
    "Entanglement",
    "Observer",
    "DecayRate",
    "Stability",
    "Material"
]

INPUT_HEADERS = {
    "Box Temperature (Â°C)|Box_Temp|box temp|Box Temperature (°C)": "BoxTemp",
    "Photon Count per Minute": "Photons",
    "Quantum Entanglement Index": "Entanglement", 
    "Observer Presence": "Observer", 
    "Radioactive Decay Rate": "DecayRate", 
    "Wavefunction Stability": "Stability",
    "Box Material": "Material"
    }

DATA_TAB_HEADERS = {
    "BoxTemp":"BOX TEMP\n(Celsius)", 
    "Photons": "PHOTON COUNT\n(per  minute)", 
    "Entanglement": "ENTANGLEMENT\nINDEX", 
    "Observer": "OBSERVER\nPRESENT?", 
    "DecayRate": "RADIOACTIVE\nDECAY RATE", 
    "Stability": "WAVEFUNCTION\nSTABILITY", 
    "Material": "BOX\nMATERIAL"
    }

REGRESSION_HEADERS = {
    'BoxTemp', 
    'Photons', 
    'Entanglement',                
    'Observer', 
    'DecayRate', 
    'Stability', 
    'Material'
    }

#Clean Data
class PurrfectData:
    def __init__(self, df, InputHeaders, DFHeaders, OutputHeaders):
        self.df = df.copy()
        self.InputHeaders = InputHeaders
        self.DFHeaders = DFHeaders
        self.OutputHeaders = OutputHeaders
    
    def CleanDataRightMeow(self):
        self.df = self.df.drop_duplicates()

        numeric_cols = self.df.columns[:6]  # Columns A–F
        string_col = self.df.columns[6]     # Column G

        self.df[numeric_cols] = self.df[numeric_cols].apply(pd.to_numeric, errors='coerce')
        self.df[string_col] = self.df[string_col].astype(str)

        self.df = self.df.dropna() #Handle missing values (none expected, but good practice) or use 

        #valid_materials = ['Cardboard', 'Lead', 'Graphene', 'Velvet', 'Quantum Foam'] #Validate categorical values
        #df = df[df['box_material'].isin(valid_materials)]

        #df['observer_presence'] = df['observer_presence'].astype(bool) #Convert observer presence to boolean
    

    def normalize_headers(self):
        rename_map = {}
        for aliases, standard_name in self.InputHeaders.items():
            for alias in aliases.split("|"):
                if alias in self.df.columns:
                    rename_map[alias] = standard_name
        self.df = self.df.rename(columns=rename_map)

    def groom(self):
        self.CleanDataRightMeow()
        self.normalize_headers()
        self.df = self.df.rename(columns=DATA_TAB_HEADERS)
        return self.df

class GetInfo:
   
    def GetUserInfo():
        UserInfo = {}

        def on_submit():
            UserInfo["Name"] = Name.get()
            UserInfo["DateToday"] = datetime.today().strftime("%Y%m%d")
            root.quit()
            root.destroy()

        def on_cancel():
            UserInfo["cancelled"] = True
            root.quit()
            root.destroy()
            print("User Canceled")
            sys.exit(1)

        root = Tk()
        root.title("Who are you?")
        root.geometry("300x100")
        root.configure(bg="#C2CAE8")

        label_style = {"bg": "#C2CAE8", "fg": "#000000", "font": ("Courier New", 11, "bold")}
        entry_style = {"bg": "#ffffff", "fg": "#000000", "font": ("Arial", 11)}

        # Name label and entry
        Label(root, text="Your Name:", **label_style).grid(row=0, column=0, sticky="e", padx=10, pady=10)
        Name = Entry(root, width=20, **entry_style)
        Name.grid(row=0, column=1, sticky="w", padx=10, pady=10)

        # Button frame for centering
        button_frame = Frame(root, bg="#C2CAE8")
        button_frame.grid(row=1, column=0, columnspan=2, pady=10)

        Button(
            button_frame,
            text="Cancel",
            command=on_cancel,
            bg="#CBCEDF",
            fg="#000000",
            font=("Arial", 11),
            relief="raised",
            padx=15, pady=5
        ).pack(side=LEFT, padx=10)

        Button(
            button_frame,
            text="Submit",
            command=on_submit,
            bg="#CBCEDF",
            fg="#000000",
            font=("Arial", 11),
            relief="raised",
            padx=15, pady=5
        ).pack(side=RIGHT, padx=10)

        root.eval('tk::PlaceWindow . center')
        root.mainloop()

        return UserInfo

    def GetInputFile():
        if len(sys.argv) > 1:
            # Drag-and-drop case
            InputFile = sys.argv[1]
            if not os.path.isfile(InputFile):
                print("The dropped file is not valid.")
                sys.exit(1)
        else:
            # No drag-and-drop → open file picker
            root = Tk()
            root.withdraw()  # hide main Tkinter window
            InputFile = filedialog.askopenfilename(
                title="Select CSV file",
                filetypes=[("CSV Files", "*.csv")]
            )
            if not InputFile:
                print("No file selected. Exiting.")
                sys.exit(0)

        print(f"Processing file: {InputFile}")
        return InputFile

    def GetDF(InputFile):
        df = pd.read_csv(InputFile)
        return df

    def GetSavePath(UserInput):
        """Generate and verify save path using subscription reference ID from B3."""
    # Load subscription reference ID from Summary tab
        
        UserName = UserInput["Name"]
        BaseName = f"Cat_Cafe_Result_{UserName}_{UserInput['DateToday']}.xlsx"

        Tk().withdraw()
        SavePath = filedialog.asksaveasfilename(defaultextension=".xlsx", initialfile=BaseName)

        if SavePath and os.path.exists(SavePath):
            version = simpledialog.askstring("Version", "Enter version number:") or "2"
            BaseName = f"Cat_Cafe_Result_{UserName}_{UserInput['DateToday']}_v{version}.xlsx"
            SavePath = os.path.join(os.path.dirname(SavePath), BaseName)

        OutputFileName = SavePath
        return OutputFileName

#---------------------------- REGRESSION CLASS ---------------------------- 
class QuantumCafeModel:
    def __init__(self, df):
        self.df = df.copy()
        self.model = None
        self.feature_columns = ['BoxTemp', 'Photons', 'Entanglement',
                                'Observer', 'DecayRate', 'Stability', 'Material']

    def encode_features(self):
        """One-hot encode categorical Material column."""
        X = self.df[self.feature_columns]
        X = pd.get_dummies(X, columns=['Material'], drop_first=True)
        return X

    def split(self, target_col, test_size=0.2, random_state=42):
        """Split data into train and test sets."""
        X = self.encode_features()
        y = self.df[target_col]
        return train_test_split(X, y, test_size=test_size, random_state=random_state)

    def train(self, target_col, model=None):
        """Train a regression model on the given target."""
        X_train, X_test, y_train, y_test = self.split(target_col)

        # Use given model or default to LinearRegression
        self.model = model if model else LinearRegression()
        self.model.fit(X_train, y_train)

        # Predictions and metrics
        y_pred = self.model.predict(X_test)
        r2 = r2_score(y_test, y_pred)
        mse = mean_squared_error(y_test, y_pred)

        print(f"📊 Results for {target_col}:")
        print(f"R²: {r2:.3f}")
        print(f"MSE: {mse:.3f}")

        return self.model, (r2, mse)

    def feature_importance(self, target_col):
        """Print feature coefficients/importance (for linear models)."""
        X = self.encode_features()
        feature_names = X.columns

        if hasattr(self.model, "coef_"):
            coefs = pd.Series(self.model.coef_, index=feature_names)
            print(f"\n🔍 Feature importance for {target_col}:")
            print(coefs.sort_values(ascending=False))
        else:
            print("This model does not provide coefficients.")

#---------------------------- CREATE THE INITIAL WORKBOOK AND DF ----------------------------
#UserInfo = GetInfo.GetUserInfo()
#InputFile = GetInfo.GetInputFile()
InputFile = "cat_cafe_dataset.csv"
Purr = PurrfectData(
    df = GetInfo.GetDF(InputFile),
    DFHeaders=DF_HEADERS,
    InputHeaders=INPUT_HEADERS,
    OutputHeaders=DATA_TAB_HEADERS
)
DataDF = Purr.groom()

#OutputFileName = GetInfo.GetSavePath(UserInfo)
OutputFileName = "output.xlsx"
if not OutputFileName:
    print("No save location chosen. Exiting.")

#df.to_excel('OutputFileName.xlsx', index=False)
with pd.ExcelWriter(OutputFileName, engine="openpyxl") as writer:
    DataDF.to_excel(writer, sheet_name="CAT_DATA", index=False)

drip = DrippyKit(filepath=OutputFileName, sheet_name="CAT_DATA")
HeaderRow = next(drip.ws.iter_rows(min_row=1, max_row=1))
LastColumn = drip.ws.max_column + 1
FirstItemsRow = 2  # Just use the row number
LastRow = drip.ws.max_row
drip.HeaderLewk()
drip.ItemsLewk()
drip.ColumnWidths()
drip.ThiccBorder()
drip.wb.save(OutputFileName)

#---------------------------- SAVE ----------------------------
wb = load_workbook(OutputFileName)
wb.save(OutputFileName)
print(f"DONE")
#print("DataFrame Headers:", list(DataDF.columns))
wb = load_workbook(OutputFileName) # Load Excel back in with openpyxl
ws = wb["CAT_DATA"]
excel_headers = [cell.value for cell in ws[1]]  # First row is headers
#print("Excel Headers:", excel_headers)


#---------------------------- REGRESSION MODELING ---------------------------- 
#RegressionDF = DataDF.rename(columns=REGRESSION_HEADERS)
#CatWhisperer = QuantumCafeModel(RegressionDF) # Initialize with dataframe
#CatWhisperer.train("MoodScore") # Train for MoodScore
#CatWhisperer.train("SurvivalRate") # Train for SurvivalRate
#CatWhisperer.train("SassIndex") # Train for SassIndex
#CatWhisperer.feature_importance("MoodScore") # Look at feature influence for MoodScore




#---------------------------- END MESSAGE ---------------------------- 
def show_completion_popup(OutputFileName):
    def open_file():
        try:
            os.startfile(OutputFileName)  # Windows
        except AttributeError:
            subprocess.call(["open", OutputFileName])  # macOS fallback
        popup.destroy()
        sys.exit(0)

    def close_popup():
        popup.destroy()
        sys.exit(0)

    popup = tk.Tk()
    popup.title("Purrrrrfect!")
    popup.geometry("420x160")
    popup.configure(bg="#C2CAE8")

    label = tk.Label(
        popup,
        text=f"New Cat Report, who dis!\n\nSaved to:\n{OutputFileName}",
        bg="#C2CAE8",
        fg="#000000",
        font=("Arial", 11),
        justify="center",
        wraplength=380
    )
    label.pack(pady=10)

    button_frame = tk.Frame(popup, bg="#C2CAE8")
    button_frame.pack(pady=5)

    tk.Button(button_frame, text="View File", command=open_file, bg="#CBCEDF", font=("Arial", 10)).pack(side="left", padx=10)
    tk.Button(button_frame, text="OK", command=close_popup, bg="#CBCEDF", font=("Arial", 10)).pack(side="right", padx=10)

    popup.eval('tk::PlaceWindow . center')
    popup.mainloop()

OutputFileName = os.path.abspath(OutputFileName)
show_completion_popup(OutputFileName)
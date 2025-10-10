# CatForms.py
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
from tkinter import *
import sys
import os
import webbrowser
from datetime import datetime
from PIL import Image, ImageTk
import pandas as pd


def patch_generate(ImBaby):
    from main import GenerateNewData
    def patched():
        user = ImBaby.UserName.get().strip()
        qty = ImBaby.RowQTY.get().strip()
        df, csv_path = GenerateNewData(user, qty)
        FlawlessVictoryPopup(ImBaby.master, csv_path)
        ImBaby.destroy()
    ImBaby.NewDataSubmitButton.configure(command=patched)

#STYLE FOR POPUPS
LabelDrip = {"bg": "#C2CAE8", "fg": "#000000", "font": ("Arial", 11)}
EntryDrip = {"bg": "#ffffff", "fg": "#000000", "font": ("Arial", 11)}
ButtonDrip = {"bg": "#FFFFFF", "fg": "#000000", "font": ("Arial", 11)}
BackgroundDrip = "#C2CAE8"
DefaultWidth = 420
MaxHeight = 800

def OpenInCenter(win, width, height): #USER FORM OPENS IN THE MIDDLE OF THE SCREEN
    win.update_idletasks()
    sw = win.winfo_screenwidth()
    sh = win.winfo_screenheight()
    x = int((sw - width) / 2)
    y = int((sh - height) / 2)
    win.geometry(f"{width}x{height}+{x}+{y}")

def FlawlessVictoryPopup(Daddy, SavePath): #FINAL MESSAGE POP UP / SHOWS SAVE PATH AND ALLOWS USER TO VIEW THE NEW DOCUMENT FROM THE POP UP
    FinalPopup = tk.Toplevel(Daddy)
    FinalPopup.title("Flawless Victory!")
    FinalPopup.configure(bg=BackgroundDrip)
    FinalPopup.transient(Daddy)
    FinalPopup.resizable(False, False)

    FinalFormFrame = tk.Frame(FinalPopup, bg=BackgroundDrip, padx=16, pady=12)
    FinalFormFrame.pack(fill="both", expand=True)

    FinalLabel = tk.Label(FinalFormFrame, text="Process is meow Complete!", **LabelDrip)
    FinalLabel.pack(anchor="w", pady=(0, 6))

    FinalPathLabel = tk.Label(FinalFormFrame, text=f"Saved to:\n{SavePath}", **LabelDrip, justify="left")
    FinalPathLabel.pack(anchor="w", pady=(0, 12))

    FinalButtonFrame = tk.Frame(FinalFormFrame, bg=BackgroundDrip)
    FinalButtonFrame.pack(fill="x", pady=(6,0))

    def PeepReport(): #FOR THE "VIEW FILE" BUTTON
        try:
            if os.name == "nt":
                os.startfile(SavePath)
            else:
                webbrowser.open(f"file://{os.path.abspath(SavePath)}")  #AGNOSTIC PLATFOM
        except Exception:
            messagebox.showerror("Open file failed", f"Could not open file: {SavePath}") #FALL BACK
        finally:# KEEP POPUP OPEN SO USER CAN STILL CLICK OK
            return

    def Okaaaay(): #CLICK OK TO CLOSE OUT OF POPUP
        FinalPopup.destroy()

    PeepButton = tk.Button(FinalButtonFrame, text="View File", width=12, command=PeepReport) #VIEW FILE BUTTON
    PeepButton.configure(**ButtonDrip)
    PeepButton.pack(side="left", padx=6)

    OkaaaayButton = tk.Button(FinalButtonFrame, text="OK", width=12, command=Okaaaay) #OK BUTTON
    OkaaaayButton.configure(**ButtonDrip)
    OkaaaayButton.pack(side="left", padx=6)

    FinalPopup.update_idletasks() #OPEN POPUP IN CENTER 
    RequiredWidth = max(DefaultWidth, FinalPopup.winfo_reqwidth() + 20) #MAKE POPUP CORRECT SIZE
    RequiredHeight = FinalPopup.winfo_reqheight() + 20
    OpenInCenter(FinalPopup, RequiredWidth, RequiredHeight) #OPEN POPUP IN CENTER 
    FinalPopup.grab_set()
    return FinalPopup

def MakePredictionPopup(Daddy): # PLACEHOLDER - THIS WILL BE FILLED IN LATER WITH THE ACTUAL PREDICTIONS
    PredictionPopup = tk.Toplevel(Daddy)
    PredictionPopup.title("Prediction")
    PredictionPopup.configure(bg=BackgroundDrip)
    PredictionPopup.transient(Daddy)
    PredictionPopup.resizable(False, False)

    PredictionFrame = tk.Frame(PredictionPopup, bg=BackgroundDrip, padx=16, pady=12)
    PredictionFrame.pack(fill="both", expand=True)

    lbl = tk.Label(PredictionFrame, text="Your meal will be determined by Quantum Features!", **LabelDrip, justify="left", wraplength=480)
    lbl.pack(anchor="w", pady=(0, 12))

    def Okaaaaaay():
        PredictionPopup.destroy()

    OkaaaaaayButton = tk.Button(PredictionFrame, text="OK", width=12, command=Okaaaaaay)
    OkaaaaaayButton.configure(**ButtonDrip)
    OkaaaaaayButton.pack(pady=(6,0))

    PredictionPopup.update_idletasks()
    RequiredWidth = max(360, PredictionPopup.winfo_reqwidth() + 20)
    RequiredHeight = PredictionPopup.winfo_reqheight() + 50
    OpenInCenter(PredictionPopup, RequiredWidth, RequiredHeight)
    PredictionPopup.grab_set()
    return PredictionPopup

class CatCafeMenu(tk.Tk): #USER CLICKS ON APP AND OPENS THIS MENU WITH OPTIONS: GENERATE NEW DATA SET (CSV), LOAD A CSV FILE TO RUN REGRESSION ON, RUN A REPORT ON THE HISTORICAL DATA (PARQUET FILE), OR INPUT FEATURE VALUES TO MAKE A PREDICTION
    def __init__(self):
        super().__init__()
        self.title("SCHRODINGER'S CAT CAFE LUNCH SPECIALS")
        self.configure(bg=BackgroundDrip)
        MenuHeader = tk.Label(self, text="Please click a button below to place your order", **LabelDrip)
        MenuHeader.pack(pady=(20, 10))
        self.MenuButtonFrame = tk.Frame(self, bg=BackgroundDrip)
        self.MenuButtonFrame.pack(padx=20, pady=(0,20))

        CafeMenu = [ # OPTIONS
            ("Generate New Cat Café Data", self.OpenGenerateForm),
            ("Create Report with New Data", self.OpenUploadForm),
            ("Predict Dining Experience", self.OpenPredictForm),
            ("View Historical Model", self.OpenViewHistoricalForm),
            ("Cancel", self.quit)
        ]

        for label, command in CafeMenu:
            MenuButton = tk.Button(self.MenuButtonFrame, text=label, width=36, command=command)
            MenuButton.configure(**ButtonDrip)
            MenuButton.pack(fill="x", pady=5)

        self.SquarePlumpAndFit() # SIZE CORRECTLY

    def OpenChildHideMenu(self, child_ctor): #WHEN YOU SELECT A MENU ITEM, A NEW FORM WILL APPEAR AND CLOSE THE MENU
        self.withdraw()
        ImBaby = child_ctor(self) #CHILD FORM

        def CloseMenu():
            try:
                self.deiconify()
            finally:
                if ImBaby.winfo_exists():
                    ImBaby.destroy()

        ImBaby.protocol("WM_DELETE_WINDOW", CloseMenu)
        return ImBaby

    def OpenGenerateForm(self): # FOR GENERATING A NEW DATA SET
        self.OpenChildHideMenu(GenerateForm)

    def OpenUploadForm(self): # FOR LOADING A DATA SET AND RUNNING REGRESSION MODEL AND GETTING A REPORT ABOUT IT
        self.OpenChildHideMenu(UploadForm)

    def OpenPredictForm(self): # FOR INPUTTING FEATURE VALUES AND PREDICTING DINING EXPERIENCE
        self.OpenChildHideMenu(PredictForm)
 
    def OpenViewHistoricalForm(self): #FOR RUNNING REGRESSION ON HISTORICAL DATA
        self.OpenChildHideMenu(ViewHistoryForm)

    def SquarePlumpAndFit(self): #FINALIZE AND CENTER
        self.update_idletasks()
        w = DefaultWidth
        h = self.winfo_reqheight()
        h = min(h, MaxHeight)
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = int((sw - w) / 2)
        y = int((sh - h) / 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

class BaseForm(tk.Toplevel):
    def __init__(self, HistoricalCatData, title):
        super().__init__(HistoricalCatData)
        self.title(title)
        self.configure(bg=BackgroundDrip)
        self._content = tk.Frame(self, bg=BackgroundDrip)
        self._content.pack(fill="both", expand=True, padx=10, pady=10)
        self.columnconfigure(0, weight=1)

    def AddTextBoxes(self, LabelText, VariableName): #TEXT BOXES
        lbl = tk.Label(self._content, text=LabelText, **LabelDrip)
        lbl.pack(anchor="w", padx=10, pady=(8, 0))
        entry = tk.Entry(self._content)
        entry.configure(**EntryDrip)
        entry.pack(fill="x", padx=10, pady=(2, 4))
        setattr(self, VariableName, entry)

    def CheckYesJuliet(self, LabelText, VariableName): #CHECK BOXES
        var = tk.BooleanVar()
        lbl = tk.Label(self._content, text=LabelText, **LabelDrip)
        lbl.pack(anchor="w", padx=10, pady=(8, 0))
        CheckCheck = tk.Checkbutton(self._content, variable=var, bg=BackgroundDrip)
        CheckCheck.pack(anchor="w", padx=10, pady=(2, 4))
        setattr(self, VariableName, var)

    def DropTheBass(self, LabelText, options, VariableName, default=None): #DROP DOWNS
        DropDownLabel = tk.Label(self._content, text=LabelText, **LabelDrip)
        DropDownLabel.pack(anchor="w", padx=10, pady=(8, 0))
        var = tk.StringVar(value=default if default is not None else "")
        PopLockAndDropIt = ttk.Combobox(self._content, textvariable=var, values=options, state="readonly") #DROP DOWN
        PopLockAndDropIt.pack(fill="x", padx=10, pady=(2, 4))
        if default is None and options:
            PopLockAndDropIt.set(options[0])
            var.set(options[0])
        setattr(self, VariableName, var)

    def AddButtons(self, SubmitCommand): #BUTTONS
        ButtonFrame = tk.Frame(self._content, bg=BackgroundDrip)
        ButtonFrame.pack(pady=(12,6))
        SubmitButton = tk.Button(ButtonFrame, text="SUBMIT", width=12, command=SubmitCommand) #SUBMIT BUTTON
        SubmitButton.configure(**ButtonDrip)
        SubmitButton.pack(side="left", padx=6)
        CancelButton = tk.Button(ButtonFrame, text="CANCEL", width=12, command=self.ClickCancel) #CANCEL BUTTON
        CancelButton.configure(**ButtonDrip)
        CancelButton.pack(side="left", padx=6)
        self.SquarePlumpAndFit()

    def ClickCancel(self): #EXIT APP
        self.destroy()

    def SquarePlumpAndFit(self): #ALLOW GEOMETRY TO SETTLE
        self.update_idletasks()
        w = DefaultWidth
        h = self.winfo_reqheight()
        h = min(h, MaxHeight)
        # if content is very narrow, ensure a minimum width
        RequiredWidth = self.winfo_reqwidth()
        if RequiredWidth > w:
            w = RequiredWidth + 20
        sw = self.winfo_screenwidth()
        sh = self.winfo_screenheight()
        x = int((sw - w) / 2)
        y = int((sh - h) / 2)
        self.geometry(f"{w}x{h}+{x}+{y}")

class GenerateForm(BaseForm): #CREATE NEW DATASET
    def __init__(self, HistoricalCatData):
        super().__init__(HistoricalCatData, "Generate New Cat Café Data")
        self.AddTextBoxes("Your Name:", "UserName")
        self.AddTextBoxes("How many rows?", "RowQTY")
        self.AddButtons(self.NewDataSubmitButton)

    def NewDataSubmitButton(self): #FOR GENERATING A NEW DATA SET
        from main import GenerateNewData
        InputName = self.UserName.get().strip()
        RowQuantityString = self.RowQTY.get().strip()

        try:
            RowQTY = int(RowQuantityString)
        except ValueError: #IF THE USER PUTS IN SOMETHING OTHER THAN A WHOLE NUMBER
            messagebox.showerror("HISS!", "Please enter an actual whole number")
            return

        try: #CALL BACK END GENERATOR
            df, save_path = GenerateNewData(InputName, RowQTY)
        except Exception as e:
            messagebox.showerror("FAIL", f"Can't generate data right meow:\n{e}")
            return

        self.master.deiconify() #SHOW FINAL POP UP
        self.destroy()
        FlawlessVictoryPopup(self.master, save_path)

class UploadForm(BaseForm):  # LOAD DATA AND RUN REGRESSION
    def __init__(self, HistoricalCatData):
        super().__init__(HistoricalCatData, "Upload New Cat Café Data")
        self.AddTextBoxes("Your Name:", "UserName")
        self.CheckYesJuliet("Include Historical Data?", "IncludeHistory")
        self.CheckYesJuliet("Write new data to master file?", "WriteMaster")
        self.AddButtons(self.UploadSubmitButton)

    def UploadSubmitButton(self):
        from main import AnalyzeNewData
        InputName = self.UserName.get().strip()
        IncludeHistory = self.IncludeHistory.get()
        UpdateMaster = self.WriteMaster.get()

        InputPath = filedialog.askopenfilename(  # SELECT CSV INPUT FILE
            title="Choose your CSV",
            filetypes=[("CSV files", "*.csv"), ("All files", "*.*")]
        )
        if not InputPath:
            return

        Today = datetime.now().strftime("%Y%m%d") #AUTO-GENERATE FILE NAME USING INITIALS + TODAY'S DATE
        name_parts = InputName.split()
        if len(name_parts) < 2:
            messagebox.showerror("Invalid Name", "Please enter at least a first and last name.")
        first_initial = name_parts[0][0].upper()
        last_initial = name_parts[-1][0].upper()
        middle_initial = name_parts[1][0].upper() if len(name_parts) > 2 else "" # MIDDLE INITIAL = OPTIONAL
        UserInitials = first_initial + middle_initial + last_initial # COMBINE INITIALS
        OutputFileName = f"Cat_Cafe_Report_{Today}_{UserInitials}.xlsx"
        SaveFolder = os.path.dirname(InputPath) #SAVE IN SAME FOLDER AS INPUT FILE *** CHANGE THIS LATER TO LET USER SELECT A SAVE LOCATION
        SavePath = os.path.join(SaveFolder, OutputFileName)

        try:
            from HistoryCat import HistoryPath  # THIS IS FOR UTILIZING HISTORICAL DATA
            CoefficientsHistoryPath = os.path.join(os.path.dirname(HistoryPath), "CatCoefficients.parquet")
            MetricsHistoryPath = os.path.join(os.path.dirname(HistoryPath), "CatMetrics.parquet")
            CafeReport = AnalyzeNewData(
                InputCSV=InputPath,
                OutputPath=SavePath,
                HistoryPath=HistoryPath,
                CoefficientsHistoryPath=CoefficientsHistoryPath,
                MetricsHistoryPath=MetricsHistoryPath,
                IncludeHistory=IncludeHistory
            )
        except Exception as e:
            messagebox.showerror("FAIL", f"Cannot process file right meow:\n{e}")
            return
        self.master.deiconify() #SHOW FINAL POPUP
        self.destroy()
        FlawlessVictoryPopup(self.master, CafeReport)

#************ THIS NEEDS TO BE FIXED 10/9/25 ******************
class PredictForm(Toplevel): #THIS IS IF THE USER WOULD LIKE TO INPUT THE VALUES FOR THE FEATURES AND PREDICT THEIR DINING EXPERIENCE
    def __init__(self, master=None):
        super().__init__(master)
        self.title("Predict Dining Experience")
        self.geometry("600x800")
        self.resizable(False, False)
        #self.update_idletasks()
        #RequiredWidth = max(420, self.winfo_reqwidth() + 20)
        #RequiredHeight = min(MaxHeight, self.winfo_reqheight() + 50)
        #OpenInCenter(self, RequiredWidth, RequiredHeight)

        #BackgroundPath = r"C:\Users\mkb00\PROJECTS\GitRepos\Schrodingers_Cat_Cafe\Assets\CatCafeBG.png" #OPTIONAL BACKGROUN IMAGE - WILL ADD LATER
        #if os.path.exists(BackgroundPath):
        #    BackgroundPic = Image.open(BackgroundPath).resize((500, 550))
        #    self.bg_photo = ImageTk.PhotoImage(BackgroundPic)
        #    BackgroundLabel = Label(self, image=self.bg_photo)
        #    BackgroundLabel.place(x=0, y=0, relwidth=1, relheight=1)

        Label(self, text="Cat Prediction Console", font=("Segoe UI", 16, "bold"), bg="#ffffff").pack(pady=10)

        self.BoxTemp = DoubleVar(value=25) # 🌡️ AMBIENT TEMPERATURE INSIDE THE BOX - IN DEGREES CELSIUS - RANGE -50 DEGREES C to 150 DEGREES C
        Scale(self, from_=-50, to=150, orient=HORIZONTAL,
              label="Box Temperature (°C)", variable=self.BoxTemp, resolution=1).pack(pady=8)

        self.DecayRate = DoubleVar(value=50000) # ☢️ RADIOACTIVE DECAY RATE OF THE ISOTOPE USED IN THE EXPERIMENT - SUB-MEGABECQUEREL RANGE: 0 to 1,000,000 Bq
        Scale(self, from_=0, to=1_000_000, orient=HORIZONTAL,
              label="Decay Rate (Bq)", variable=self.DecayRate, resolution=1000).pack(pady=8)

        self.Photons = DoubleVar(value=1000) # 💡 PHOTON EMISSION COUNT - DIM TO VERY BRIGHT ENERGY FLUCTUATIONS - RANGE: 0 to 10,000
        Scale(self, from_=0, to=10_000, orient=HORIZONTAL,
              label="Photon Count per Min", variable=self.Photons, resolution=100).pack(pady=8)

        self.Entanglement = DoubleVar(value=0.5) #  🌀 ENTANGLEMENT INDEX - DEGREE OF QUANTUM INTANGLEMENT BETWEEN PAIRED CATS - RANGE 0 to 1
        Scale(self, from_=0, to=1, resolution=0.01, orient=HORIZONTAL,
              label="Entanglement Index", variable=self.Entanglement).pack(pady=8)

        self.Stability = DoubleVar(value=50)  # ⚖️ WAVEFUNCTION STABILITY - PERCENTAGE 0 = FULLLY DECOHERED CHAOS / 100 = PERFECTLY STABLE SUPERPOSITION
        Scale(self, from_=0, to=100, orient=HORIZONTAL,
              label="Wavefunction Stability", variable=self.Stability).pack(pady=8)

        self.Material = StringVar(value="Cardboard")  # default
        Label(self, text="Box Material", bg="#ffffff").pack(pady=5)
        OptionMenu(self, self.Material, "Cardboard", "Lead", "QuantumFoam", "Velvet").pack(pady=5)


        self.Observer = BooleanVar(value=True) # 👁️ OBSERVER CHECKBOX 
        Checkbutton(self, text="Observer Present?", variable=self.Observer).pack(pady=5)

        Button(self, text="Predict Outcome", font=("Segoe UI", 12, "bold"),
               command=self.RunPrediction).pack(pady=15)

        # -------------------------------------------------------------
    def RateDiningExperience(self, MoodScore, SassInex, SurvivalRate):   # 🧠 HELPER TO INTERPRET THE MODEL OUTPUTS
        #DECISION RULES:
	        #MOOD SCORE (0 - 100)
                #LOW: MOOD < 33  / CAT IS EXPERIENCING EXISTENTIAL DREAD
                #MEDIUM: 33 ≤ MOOD < 67 / CAT IS INDIFFERENT
                #HIGH: MOOD ≥ 67 / CAT IS IN QUANTUM BLISS
            #SASS INDEX (0 - 100)
                #LOW: sass < 33 / FRIENDLY STAFF
                #MEDIUM:  3 ≤ sass < 67 / A LITTLE CATTITUDE BUT BEARABLE
                #HIGH: ≥ 67 / VERY SASSY - POOR SERVICE
            #SURVIVAL PROBABILITY (0-1)
                #PROBABLY ALIVE: SURVIVAL PROBABILITY ≥ 0.5 / CAFE IS OPEN
                #PROBABLY NOT ALIVE:  SURVIVAL PROBABILITY  < 0.5 / CAFE IS CLOSED
        def CatBucket(value, low, high): #TO GROUP MOOD SCORE AND SASS INDEX INTO BUCKETS OF HIGH, MEDIUM, LOW PER THE DECISION RULES ABOVE
            if value < low:
                return "Low"
            elif value < high:
                return "Medium"
            else:
                return "High"
        CatMood = CatBucket(MoodScore, 33, 67)
        CatSass = CatBucket(SassInex, 33, 67)
        if SurvivalRate is None: #MAKE SURE SURVIVAL RATE IS NOT NONE
            CatAliveState = "Unknown"
        else:
            CatAliveState = "Alive" if SurvivalRate >= 0.5 else "NotAlive"
        

        CatKey = (CatMood, CatSass, CatAliveState)
        CatMap = { #ALL THE OUTCOMES AND INTERPRETATIONS - 18 COMBOS - (3 FOR MOOD x 3 FOR SASS x 2 FOR SURVIVAL)
            #CAFE IS OPEN FOR BUSINESS! AKA CAT IS ALIVE
            ("High","Low","Alive"): ("Michelin 3-Star Experience",
                "Gourmet bliss & gracious service — a sublime meal."),
            ("High","Medium","Alive"): ("Excellent Food, Slight Attitude",
                "Amazing food; service has personality."),
            ("High","High","Alive"): ("Great Food, Rude Service",
                "Top-notch cuisine but the crew brings attitude."),
            ("Medium","Low","Alive"): ("Solid Casual Dining",
                "Decent food and friendly service."),
            ("Medium","Medium","Alive"): ("Mixed Bag",
                "Ok food, mixed service — moderate experience."),
            ("Medium","High","Alive"): ("Tasty but Rude",
                "Food is acceptable but staff may sour the visit."),
            ("Low","Low","Alive"): ("Disappointing Comfort Food",
                "Bland dishes but polite staff."),
            ("Low","Medium","Alive"): ("Cold Food, Mixed Service",
                "Poor food quality combined with indifferent service."),
            ("Low","High","Alive"): ("Avoid — Culinary Disaster",
                "Terrible food and rude staff — do not eat here."),
            # CLOSED VARIANTS - IF THE CAFE IS CLOSED / AKA IF THE CAT IS UN-ALIVE
            ("High","Low","NotAlive"): ("Closed — Exceptional Promise",
                "Would be phenomenal, but the café is closed today."),
            ("High","Medium","NotAlive"): ("Closed — Keep Hopes",
                "Delicious menu, but not open right now."),
            ("High","High","NotAlive"): ("Closed & Chaotic",
                "Great food in theory, but not open — and staff questionable."),
            ("Medium","Low","NotAlive"): ("Temporarily Closed",
                "Could be decent when open; currently closed."),
            ("Medium","Medium","NotAlive"): ("Closed — Meh",
                "Average experience in theory, but likely not open."),
            ("Medium","High","NotAlive"): ("Closed & Testy",
                "Service attitude plus closure — avoid today."),
            ("Low","Low","NotAlive"): ("Closed & Poor Reputation",
                "Low food quality and shutdown — skip."),
            ("Low","Medium","NotAlive"): ("Closed & Unimpressive",
                "Not open, and not worth waiting for."),
            ("Low","High","NotAlive"): ("Abandoned Catastrophe",
                "Closed, and if open would be awful — major red flags.")
        }
        CafeStatus, Interpretation = CatMap.get(CatKey, ("Undetermined", "Ambiguous results — exercise caution."))

        return {
            "Status": CafeStatus,
            "Interpretation": Interpretation,
            "CatMood": CatMood,
            "CatSass": CatSass,
            "CatAliveState": CatAliveState,
        }

    def RunPrediction(self):
        from main import PredictDiningExperience
        InputFeatureValues = { # 🧩 COLLECT ALL THE INPUT VALUES
            "BoxTemp": self.BoxTemp.get(),
            "DecayRate": self.DecayRate.get(),
            "Photons": self.Photons.get(),
            "Stability": self.Stability.get(),
            "Entanglement": self.Entanglement.get(),
            "Observer": int(self.Observer.get()),
        }
        material = self.Material.get() #ADD ONE HOT ENCODED MATERIALS FROM THE DROP DOWN
        for m in ["Cardboard", "Lead", "QuantumFoam", "Velvet"]:
            InputFeatureValues[f"Material_{m}"] = 1 if material == m else 0
        print(InputFeatureValues)


        try: #PREDICTION LOGIC
            PredictionResult = PredictDiningExperience(InputFeatureValues) #PREDICT DINING EXPERIENCE IS IN MAIN
            PredictedMood = PredictionResult["Mood"]
            PredictedSass = PredictionResult["Sass"]
            PredictedSurvival = PredictionResult["Survival"]

            CafeVerdict = self.RateDiningExperience(PredictedMood, PredictedSass, PredictedSurvival)

            PopupMessage = (
                f"🐾 {CafeVerdict['Status']} 🐾\n\n"
                f"{CafeVerdict['Interpretation']}\n\n"
                f"— Mood: {PredictedMood:.1f} ({CafeVerdict['CatMood']})\n"
                f"— Sass: {PredictedSass:.1f} ({CafeVerdict['CatSass']})\n"
                f"— Survival Probability: {PredictedSurvival*100:.1f}% ({CafeVerdict['CatAliveState']})"
            )

            messagebox.showinfo("Predicted Dining Experience", PopupMessage)

        except Exception as e:
            messagebox.showerror("FAIL", f"Cannot make prediction right meow:\n{e}")

#************ THIS NEEDS TO BE FIXED 10/9/25 ******************
class ViewHistoryForm(BaseForm): #THIS IS IF THE USER WOULD LIKE TO VIEW A REPORT WITH ALL HISTORICAL DATA
    def __init__(self, HistoricalCatData):
        super().__init__(HistoricalCatData, "View Historical Model")
        self.AddTextBoxes("Your Name:", "UserName")
        self.AddButtons(self.HistorySubmitButton)
    
    def HistorySubmitButton(self): #READS HISTORICAL FILE, RUNS REGRESSION USING BACK ENDm OVERWRITES PREVIOUS VERSION, THEN FINAL POP UP
        from main import ViewHistoricalModel
        InputName = self.UserName.get().strip()  #CLICK SUBMIT - COLLECT USER'S NAME

        try:
            from HistoryCat import HistoryPath, CoefficientsHistoryPath, MetricsHistoryPath
            CoefficientsHistoryPath = HistoryPath.replace("Historical_Cafe_Data.parquet", "CatCoefficients.parquet")
            MetricsHistoryPath = HistoryPath.replace("Historical_Cafe_Data.parquet", "CatMetrics.parquet")
            ResultsPath = ViewHistoricalModel(HistoryPath, CoefficientsHistoryPath, MetricsHistoryPath)
        except Exception as e:
            messagebox.showerror("FAIL", f"Cannot run regression right meow:\n{e}")
            return

        self.master.deiconify()
        self.destroy()
        if ResultsPath:
            FlawlessVictoryPopup(self.master, ResultsPath)

# CatForms.py
import tkinter as tk
from tkinter import filedialog, ttk, messagebox
import sys
import os
import webbrowser

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

    def PeepReport():
        try:
            if os.name == "nt":
                os.startfile(SavePath)
            else:
                # Try using platform-agnostic opener
                webbrowser.open(f"file://{os.path.abspath(SavePath)}")
        except Exception:
            # fallback to messagebox if opener fails
            messagebox.showerror("Open file failed", f"Could not open file: {SavePath}")
        finally:
            # keep popup open so user can still click OK
            return

    def Okaaaay():
        FinalPopup.destroy()

    PeepButton = tk.Button(FinalButtonFrame, text="View File", width=12, command=PeepReport)
    PeepButton.configure(**ButtonDrip)
    PeepButton.pack(side="left", padx=6)

    OkaaaayButton = tk.Button(FinalButtonFrame, text="OK", width=12, command=Okaaaay)
    OkaaaayButton.configure(**ButtonDrip)
    OkaaaayButton.pack(side="left", padx=6)

    # size to content and center on screen
    FinalPopup.update_idletasks()
    RequiredWidth = max(DefaultWidth, FinalPopup.winfo_reqwidth() + 20)
    RequiredHeight = FinalPopup.winfo_reqheight() + 20
    OpenInCenter(FinalPopup, RequiredWidth, RequiredHeight)
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
    RequiredHeight = PredictionPopup.winfo_reqheight() + 20
    OpenInCenter(PredictionPopup, RequiredWidth, RequiredHeight)
    PredictionPopup.grab_set()
    return PredictionPopup

class CatCafeMenu(tk.Tk): #USER CLICKS ON APP AND OPENS THIS MENU WITH OPTIONS: GENERATE NEW DATA SET, LOAD A CSV FILE TO RUN REGRESSION ON, RUN A REPORT ON THE HISTORICAL DATA, OR INPUT FEATURE VALUES TO MAKE A PREDICTION
    def __init__(self):
        super().__init__()
        self.title("SCHRODINGER'S CAT CAFE LUNCH SPECIALS")
        self.configure(bg=BackgroundDrip)

        MenuHeader = tk.Label(self, text="Please click a button below to place your order", **LabelDrip)
        MenuHeader.pack(pady=(20, 10))

        self.MenuButtonFrame = tk.Frame(self, bg=BackgroundDrip)
        self.MenuButtonFrame.pack(padx=20, pady=(0,20))

        CafeMenu = [
            ("Generate New Cat Café Data", self.OpenGenerateForm),
            ("Upload New Cat Café Data", self.OpenUploadForm),
            ("Predict Meal Experience", self.OpenPredictForm),
            ("View Master Model", self.OpenViewMasterForm),
            ("Cancel", self.quit)
        ]

        for label, command in CafeMenu:
            MenuButton = tk.Button(self.MenuButtonFrame, text=label, width=36, command=command)
            MenuButton.configure(**ButtonDrip)
            MenuButton.pack(fill="x", pady=5)

        self.SquarePlumpAndFit()

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
 
    def OpenViewMasterForm(self): #FOR RUNNING REGRESSION ON HISTORICAL DATA
        self.OpenChildHideMenu(ViewMasterForm)

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

    def NewDataSubmitButton(self):
        InputName = self.UserName.get().strip()
        RowQuantityString = self.RowQTY.get().strip()
        try:
            RowQTY = int(RowQuantityString)
        except ValueError:
            messagebox.showerror("Invalid input", "Please enter a valid integer for How many rows?")
            return
        SavePath = filedialog.asksaveasfilename(title="Save Report As", defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx"), ("All files", "*.*")])
        if not SavePath: #SAVE PATH 
            return
        messagebox.showinfo("Generate Process", f"Generate New Cat Cafe Data Process\n\nUserName: {InputName}\nRowQTY: {RowQTY}\nNew Cat Data Saved To: {SavePath}")
        self.destroy()


class UploadForm(BaseForm): #LOAD DATA AND RUN REGRESSION
    def __init__(self, HistoricalCatData):
        super().__init__(HistoricalCatData, "Upload New Cat Café Data")
        self.AddTextBoxes("Your Name:", "UserName")
        self.CheckYesJuliet("Include Historical Data?", "IncludeHistory")
        self.CheckYesJuliet("Write new data to master file?", "WriteMaster")
        self.AddButtons(self.UploadSubmitButton)

    def UploadSubmitButton(self): #CLICK SUBMIT - COLLECT THE INPUT INFO AND THE CSV THAT WILL BE RUN THROUGH THE MODEL
        InputName = self.UserName.get().strip()
        IncludeHistory = self.IncludeHistory.get()
        UpdateMaster = self.WriteMaster.get()
        InputPath = filedialog.askopenfilename(title="Select CSV File", filetypes=[("CSV files", "*.csv"), ("All files", "*.*")])
        if not InputPath:
            return
        SavePath = filedialog.asksaveasfilename(title="Save Report As", defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx"), ("All files", "*.*")])
        if not SavePath: #SAVE PATH 
            return
        messagebox.showinfo(
            "Upload Process",
            f"Upload New Cat Café Data Process\n\nUserName: {InputName}\nIncludeHistoricalData: {IncludeHistory}\nWriteNewDataToMaster: {UpdateMaster}\nSelectedFile: {InputPath}\nSave Location: {SavePath}"
        )
        self.destroy()

class PredictForm(BaseForm): #THIS IS IF THE USER WOULD LIKE TO INPUT THE VALUES FOR THE FEATURES AND PREDICT THEIR DINING EXPERIENCE
    def __init__(self, HistoricalCatData):
        super().__init__(HistoricalCatData, "Predict Meal Experience")
        self.AddTextBoxes("Your Name:", "UserName")
        self.AddTextBoxes("Box Temperature (Celsius):", "BoxTemp")
        self.AddTextBoxes("Radioactive Decay Rate:", "DecayRate")
        self.AddTextBoxes("Photon Count (per minute):", "Photons")
        self.AddTextBoxes("Wavefunction Stability:", "Stability")
        self.AddTextBoxes("Entanglement Index:", "Entanglement")
        self.CheckYesJuliet("Observer Present?", "Observer")
        self.DropTheBass("Box Material:", ["Cardboard", "Lead", "Quantum Foam", "Velvet"], "Material", default="Velvet")
        self.AddButtons(self.PredictSubmitButton)

    def PredictSubmitButton(self): #COLLECT THE USER INPUTS WHEN CLICKING SUBMIT
        InputName = self.UserName.get().strip()
        UserInputs = {
            "BoxTemp": self.BoxTemp.get().strip(),
            "DecayRate": self.DecayRate.get().strip(),
            "Photons": self.Photons.get().strip(),
            "Stability": self.Stability.get().strip(),
            "Entanglement": self.Entanglement.get().strip(),
            "Observer": self.Observer.get(),
            "Material": self.Material.get()
        }
        messagebox.showinfo("Predict Process", f"Predict Meal Experience Process\n\nUserName: {InputName}\n" + "\n".join(f"{k}: {v}" for k, v in UserInputs.items()))
        self.destroy()

class ViewMasterForm(BaseForm): #THIS IS IF THE USER WOULD LIKE TO VIEW A REPORT WITH ALL HISTORICAL DATA
    def __init__(self, HistoricalCatData):
        super().__init__(HistoricalCatData, "View Master Model")
        self.AddTextBoxes("Your Name:", "UserName")
        self.AddButtons(self.MasterSubmitButton)

    def MasterSubmitButton(self): #CLICK SUBMIT - COLLECT USER'S NAME AND LET THEM SELECT A SAVE DESTINATION
        InputName = self.UserName.get().strip()
        SavePath = filedialog.asksaveasfilename(title="Save Report As", defaultextension=".xlsx", filetypes=[("Excel", "*.xlsx"), ("All files", "*.*")])
        if not SavePath: #SAVE PATH IS BECASUE IT WILL BE GENERATING A NEW REPORT - THE HISTORICAL DATA WILL JUST BE SAVED IN A RAW CSV SO THAT RAW CSV WILL BASICALLY BE RUN THROUGH THE SAME PROCESS AS THE "LOAD NEW CAT DATA" OPTION
            return
        messagebox.showinfo("View Master Process", f"View Master Model Process\n\nUserName: {InputName}\nSavePath: {SavePath}")
        self.destroy()

#if __name__ == "__main__":
#    app = CatCafeMenu()
#    app.mainloop()
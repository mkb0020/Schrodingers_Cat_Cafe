import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl import Workbook, load_workbook
from openpyxl.drawing.image import Image
from io import BytesIO
import pandas as pd
from RegressionCat import PurrfectRegression
from PIL import Image as PILImage
import tempfile
import os



class TipToe:
    # ---------------------------- STYLE DEFINITIONS ----------------------------
    PurpleyBlue = "4B1395"
    DarkishGrey = "75788B"
    LightBlueGrey = "CBCEDF"
    White = "FFFFFF"
    Black = "000000"
    SuperLightPink = "FFEFFF"
    SuperLightBlue = "E2E9FE"
    SuperLightPurp = "F0E1FF"

    PurpleFill = PatternFill(start_color=PurpleyBlue, end_color=PurpleyBlue, fill_type="solid")
    GreyFill = PatternFill(start_color=DarkishGrey, end_color=DarkishGrey, fill_type="solid")
    WhiteFill = PatternFill(start_color=White, end_color=White, fill_type="solid")
    BlueGreyFill = PatternFill(start_color=LightBlueGrey, end_color=LightBlueGrey, fill_type="solid")
    LightPinkFill = PatternFill(start_color=SuperLightPink, end_color=SuperLightPink, fill_type="solid")
    LightBlueFill = PatternFill(start_color=SuperLightBlue, end_color=SuperLightBlue, fill_type="solid")
    LightPurpleFill = PatternFill(start_color=SuperLightPurp, end_color=SuperLightPurp, fill_type="solid")

    BigBoldWhite = Font(name="Aptos Display", bold=True, color=White, size=14)
    BoldWhite = Font(name="Aptos Narrow", bold=True, color=White, size=11)
    BoldBlack = Font(name="Aptos Narrow", bold=True, color=Black, size=11)
    RegularBlack = Font(name="Aptos Narrow", bold=False, color=Black, size=11)

    Middle = Alignment(horizontal="center", vertical="center", wrap_text=True)
    Lefty = Alignment(horizontal="left", vertical="center", indent=1)
    Righty = Alignment(horizontal="right", vertical="center", indent=1)

    IttyBitty = Side(style="thin", color=Black)
    SheThicc = Side(style="thick", color=Black)
    Double = Side(style="double", color=Black)
    DoubleBottom = Border(bottom=Double)

    # ---------------------------- WALK-IN CLOSET / STYLES / Named after Riff Raff Albums ----------------------------
    PurpleIcon = {
        "font": BigBoldWhite,
        "alignment": Middle,
        "fill": PurpleFill,
        "border": Border(left=SheThicc, right=SheThicc, top=SheThicc, bottom=Double)
    }

    PurpleIconChopped = {
        "font": BoldWhite,
        "alignment": Middle,
        "fill": PurpleFill,
        "border": Border(left=IttyBitty, right=IttyBitty, top=IttyBitty, bottom=Double)
    }

    TheWhiteWest = {
        "font": BoldWhite,
        "alignment": Middle,
        "fill": GreyFill,
        "border": Border(left=IttyBitty, right=IttyBitty, top=IttyBitty, bottom=Double)
    }

    TheWhiteWestChopped = {
        "font": BoldWhite,
        "alignment": Middle,
        "fill": GreyFill,
        "border": Border(left=None, right=None, top=None, bottom=Double)
    }

    CoolBlueJewels = {
        "font": BoldBlack,
        "alignment": Lefty,
        "fill": BlueGreyFill,
        "border": Border(left=IttyBitty, right=IttyBitty, top=IttyBitty, bottom=IttyBitty)
    }

    VanillaGorillaMids = {
        "font": RegularBlack,
        "alignment": Middle,
        "fill": WhiteFill,
        "border": Border(left=IttyBitty, right=IttyBitty, top=IttyBitty, bottom=IttyBitty)
    }

    VanillaGorillaLefts = {
        "font": RegularBlack,
        "alignment": Lefty,
        "fill": WhiteFill,
        "border": Border(left=IttyBitty, right=IttyBitty, top=IttyBitty, bottom=IttyBitty)
    }

    PinkPython = {
        "font": RegularBlack,
        "alignment": Middle,
        "fill": LightPinkFill,
        "border": Border(left=IttyBitty, right=IttyBitty, top=IttyBitty, bottom=IttyBitty)
    }

    AquaberryAquarius = {
        "font": RegularBlack,
        "alignment": Middle,
        "fill": LightBlueFill,
        "border": Border(left=IttyBitty, right=IttyBitty, top=IttyBitty, bottom=IttyBitty)
    }

    LilacLightning = {
        "font": RegularBlack,
        "alignment": Middle,
        "fill": LightPurpleFill,
        "border": Border(left=IttyBitty, right=IttyBitty, top=IttyBitty, bottom=IttyBitty)
    }

    TurquoiseTornado = {
        "font": RegularBlack,
        "alignment": Middle,
        "fill": BlueGreyFill
    }

    # ---------------------------- INIT ----------------------------
    def __init__(self, wb, ws):
        self.wb = wb
        self.ws = ws
    # ---------------------------- HELPERS ----------------------------
    @staticmethod
    def Flex(cell, font=None, alignment=None, fill=None, border=None):
        if font:
            cell.font = font
        if alignment:
            cell.alignment = alignment
        if fill:
            cell.fill = fill
        if border:
            cell.border = border

    def Thicc(self, FirstRow, LastRow, FirstColumn, LastColumn):
        """Apply a thick border around the given cell range."""
        for row in self.ws.iter_rows(min_row=FirstRow, max_row=LastRow,
                                     min_col=FirstColumn, max_col=LastColumn):
            for cell in row:
                left, right, top, bottom = cell.border.left, cell.border.right, cell.border.top, cell.border.bottom
                if cell.row == FirstRow:
                    top = TipToe.SheThicc
                if cell.row == LastRow:
                    bottom = TipToe.SheThicc
                if cell.column == FirstColumn:
                    left = TipToe.SheThicc
                if cell.column == LastColumn:
                    right = TipToe.SheThicc
                cell.border = Border(left=left, right=right, top=top, bottom=bottom)

    def ColorBackGround(self, FirstRow, LastRow, FirstColumn, LastColumn):
        """Apply background color behind the plots."""
        for row in self.ws.iter_rows(min_row=FirstRow, max_row=LastRow,
                                     min_col=FirstColumn, max_col=LastColumn):
            for cell in row:
                cell.fill = TipToe.BlueGreyFill

    def SetColumnWidths(self, ThiccColumns, ThiccWidth, SpacerColumns, SpacerWidth):
        for col in ThiccColumns:
            self.ws.column_dimensions[col].width = ThiccWidth
        for col in SpacerColumns:
            self.ws.column_dimensions[col].width = SpacerWidth

    def Title(self, FirstRow):
        self.ws.row_dimensions[FirstRow].height = 25
        TitleRow = next(self.ws.iter_rows(min_row=FirstRow, max_row=FirstRow))
        for cell in TitleRow:
            TipToe.Flex(cell, **TipToe.PurpleIcon)

    def SubHeader(self, Row=2):  # SCATTER AND RESULTS TABS
        self.ws.row_dimensions[Row].height = 20
        SubHeaderRow = next(self.ws.iter_rows(min_row=Row, max_row=Row))
        for cell in SubHeaderRow:
            TipToe.Flex(cell, **TipToe.TheWhiteWestChopped)


    # ---------------------------- WORKBOOK STYLING ----------------------------
    def InsightsDrip(self):
        FirstBorderRow = 1
        FirstColumn = 1
        LastRow = 22
        LastColumn = 5
        ThiccColumns = ["E"]
        ThiccWidth = 80
        SpacerColumns = ["B", "C", "D"]
        SpacerWidth = 17
        FirstFeatureRow = 3
        LastFeatureRow = 14
        FisrtMetricsRow = 16
        LastMetricsRow = 22
        self.Title(FirstBorderRow)
        self.SetColumnWidths(ThiccColumns, ThiccWidth, SpacerColumns, SpacerWidth)
        self.ws.column_dimensions["A"].width = 30
        self.Thicc(FirstBorderRow, LastRow, FirstColumn, LastColumn)
        self.Thicc(FirstFeatureRow, LastFeatureRow, FirstColumn, LastColumn)
        self.Thicc(FisrtMetricsRow, LastMetricsRow, FirstColumn, LastColumn)
        
    def DataDrip(self):
        ws = self.ws
        FirstBorderRow = 1
        FirstColumn = 1
        LastRow = self.ws.max_row
        LastColumn = self.ws.max_column
        ThiccColumns = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N", "O", "P"]
        ThiccWidth = 15
        SpacerColumns = []
        SpacerWidth = 0
        self.ws.row_dimensions[1].height = 50
        HeaderRow = next(self.ws.iter_rows(min_row=1, max_row=1))
        for cell in HeaderRow:
            self.Flex(cell, **self.PurpleIconChopped)
        for row in range(FirstBorderRow+1, LastRow + 1):
            self.ws.row_dimensions[row].height = 15
            for col in range(FirstColumn, LastColumn + 1):
                cell = self.ws.cell(row, col)
                self.Flex(cell, **self.VanillaGorillaMids)
        self.SetColumnWidths(ThiccColumns, ThiccWidth, SpacerColumns, SpacerWidth)
        self.Thicc(FirstBorderRow, LastRow, FirstColumn, LastColumn)

    def PlotsDrip(self):
        ws = self.ws
        PlotTabs = ["SCATTER PLOTS", "MOOD RESULTS" "SASS RESULTS", "SURVIVAL RESULTS"]
        for tab in PlotTabs:
            tab = self.ws.title
            if tab == "SCATTER PLOTS":
                FirstBorderRow = 1
                FirstBGRow = 3
                FirstColumn = 1
                LastRow = 63
                LastColumn = 7
                ThiccColumns = ["B", "D", "F"]
                ThiccWidth = 50
                SpacerColumns = ["A", "C", "E", "G"]
                SpacerWidth = 3
            elif tab == "MOOD RESULTS":
                FirstBorderRow = 1
                FirstBGRow = 3
                FirstColumn = 1
                LastRow =48
                LastColumn = 9
                ThiccColumns = ["B", "D", "F", "H"]
                ThiccWidth = 38.5
                SpacerColumns = ["A", "C", "E", "G", "I"]
                SpacerWidth = 2
            elif tab == "SASS RESULTS":
                FirstBorderRow = 1
                FirstBGRow = 3
                FirstColumn = 1
                LastRow =23
                LastColumn = 5
                ThiccColumns = ["B", "D"]
                ThiccWidth = 75
                SpacerColumns = ["A", "C", "E"]
                SpacerWidth = 3
            elif tab == "SURVIVAL RESULTS":
                FirstBorderRow = 1
                FirstBGRow = 3
                FirstColumn = 1
                LastRow =23
                LastColumn = 3
                ThiccColumns = ["B"]
                ThiccWidth = 90
                SpacerColumns = ["A", "C"]
                SpacerWidth = 10
            self.Title(FirstBorderRow)
            self.SubHeader()
            self.SetColumnWidths(ThiccColumns, ThiccWidth, SpacerColumns, SpacerWidth)
            self.Thicc(FirstBorderRow, LastRow, FirstColumn, LastColumn)
            self.ColorBackGround(FirstBGRow, LastRow, FirstColumn, LastColumn)

    def Drip(self):
        self.InsightsDrip()
        self.DataDrip()
        self.PlotsDrip()
        self.wb.save(self)

def CreateWB(OutputPath, TabNames): #HELPER TO CREATE WORKBOOK
    wb = Workbook()
    if "Sheet" in wb.sheetnames: #REMOVE DEFAULT SHEET
        del wb["Sheet"]
    for name in TabNames:
        wb.create_sheet(title=name)
    wb.save(OutputPath)
    return wb

class PurrfectWB:
    def __init__(self, df, OutputPath, ScatterPlots, RegressionPlots):
        self.df = df
        self.OutputPath = OutputPath
        self.wb = openpyxl.Workbook()
        DefaultTab = self.wb.active # REMOVE DEFAULT TAB
        self.wb.remove(DefaultTab)

        self.sheets = ["INSIGHTS", "DATA", "SCATTER PLOTS", 
                       "MOOD RESULTS", "SASS RESULTS", "SURVIVAL RESULTS"]
        self.ws = {}
        for name in self.sheets: # CREATE TABS
            self.ws[name] = self.wb.create_sheet(title=name)
        self.wb.save(self.OutputPath)         # SAVE IMMEDIATELY SO IT'S WRITTEN ONTO DISK

        
        self.ScatterPlots = ScatterPlots
        self.RegressionPlots = RegressionPlots
        self.TempPics = []


    def SAVE(self): #SAVE CURRENT WB STATE
        self.wb.save(self.OutputPath)

    def GetWS(self, name):
        """Get a worksheet by name safely."""
        if name in self.ws:
            return self.ws[name]
        raise ValueError(f"Worksheet '{name}' not found in {self.OutputPath}")
    
    def InsightsKitten(self, ws=None):
        InsightsWS = self.GetWS("INSIGHTS")
        InsightsWS["A1"] = "CAFÉ ANALYSIS" #TITLE
        InsightsWS.merge_cells("A1:E1")
        InsightsWS.merge_cells("A2:E2") #SPACER

        Headers = [("A3", "FEATURE"), ("B3", "IMPORTANCE"), ("E3", "INSIGHTS")] #MAIN HEADERS
        for cell, text in Headers:
            InsightsWS[cell] = text
            TipToe.Flex(InsightsWS[cell], **TipToe.PurpleIconChopped)
        InsightsWS.merge_cells("B3:D3")

        for col, text in [("B4", "MOOD"), ("C4", "SASS"), ("D4", "SURVIVAL")]: #SUB HEADERS
            InsightsWS[col] = text
            TipToe.Flex(InsightsWS[col], **TipToe.TheWhiteWest)
        for col in ["A4", "E4"]: #BOOK-ENDS
            InsightsWS[col] = ""
            TipToe.Flex(InsightsWS[col], **TipToe.TheWhiteWest)

        Features = [ #FEATURE LIST
            "BOX TEMP (Celsius)",
            "RADIOACTIVE DECAY RATE",
            "PHOTON COUNT (per min)",
            "WAVEFUNCTION STABILITY",
            "ENTANGLEMENT INDEX",
            "OBSERVER PRESENCE",
            "CARDBOARD BOX",
            "LEAD BOX",
            "QUANTUM FOAM BOX",
            "VELVET BOX",
        ]
        for i, label in enumerate(Features, start=5):
            InsightsWS[f"A{i}"] = label
            TipToe.Flex(InsightsWS[f"A{i}"], **TipToe.CoolBlueJewels)

        InsightsWS.merge_cells("A15:E15")  #SPACER
        InsightsWS["A16"] = "MODEL INSIGHTS"
        TipToe.Flex(InsightsWS["A16"], **TipToe.PurpleIconChopped)
        InsightsWS.merge_cells("A16:E16")

        MetricLabels = [ #MODEL INSIGHTS METRICS
            "Coefficient of determination:",
            "Intercept:",
            "Mean Absolute Error:",
            "Mean Squared Error:",
            "Root Mean Squared Error:"
        ]
        for i, metric in enumerate(MetricLabels, start=18):
            InsightsWS[f"A{i}"] = metric
            TipToe.Flex(InsightsWS[f"A{i}"], **TipToe.CoolBlueJewels)

        MetricHeaders = [ # MODEL INSIGHTS ROW HEADERS ( ROW 17)
            ("A17", "METRIC"),
            ("B17", "MOOD"),
            ("C17", "SASS"),
            ("D17", "SURVIVAL"),
            ("E17", "INSIGHTS")
        ]
        for col, text in MetricHeaders:
            InsightsWS[col] = text
            TipToe.Flex(InsightsWS[col], **TipToe.TheWhiteWest)

        Drip = TipToe(self.wb, InsightsWS) #STYLE SHEET
        Drip.InsightsDrip()
        self.SAVE()

    def DataKitten(self, ws=None):
        ws = self.GetWS("DATA")
        DataTabHeaders = ["BOX\nTEMPERATURE\n(Celsius)", "RADIOACTIVE\nDECAY RATE", "PHOTON COUNT\n(PER MINUTE)", "WAVEFUNCTION\nSTABILITY", "ENTANGLEMENT\nINDEX", "OBSERVER\nPRESENT?", "BOX\nMATERIAL", "ACTUAL\nMOOD SCORE", "PREDICTED\nMOOD SCORE", "MOOD SCORE\nRESIDUAL", "ACTUAL\nSASS INDEX", "PREDICTED\nSASS INDEX", "SASS INDEX\nRESIDUAL", "ACTUAL\nSURVIVAL", "PREDICTED\nSURVIVAL", "SURVIVAL RATE\nRESIDUAL"] #Data tab headers in order
        for i, header in enumerate(DataTabHeaders, start=1): #PRETTY HEADERS
            cell = ws.cell(row=1, column=i, value=header)
        
        for r, row in enumerate(self.df.itertuples(index=False), start=2): #Paste DF rows by row into DATA tab
            for c, value in enumerate(row, start=1):
                ColumnName = self.df.columns[c - 1] #OBSERVER COLUMN (YES / NO)
                if ColumnName == "Observer":
                    if pd.isna(value):  # NAN FOR MISSING VALUES
                        display_value = ""
                    else:
                        display_value = "YES" if int(value) == 1 else "NO"
                else:
                    display_value = value
                ws.cell(row=r, column=c, value=display_value)
        Drip = TipToe(self.wb, ws)
        Drip.DataDrip()
        self.SAVE()

    def PlaceImage(self, ws, fig, AnchorCell, HeightIN, WidthIN):
        FosterCat = tempfile.NamedTemporaryFile(suffix=".png", delete=False)
        TempName = FosterCat.name
        FosterCat.close()
        fig.savefig(TempName, format="png", dpi=96, bbox_inches="tight")
        img = Image(TempName)
        img.width = int(WidthIN * 96)
        img.height = int(HeightIN * 96)
        img.anchor = AnchorCell
        ws.add_image(img)
        self.TempPics.append(TempName)

    def PlaceScatter(self, ws, fig, AnchorCell, HeightIN, WidthIN):
        self.PlaceImage(ws, fig, AnchorCell, HeightIN, WidthIN)

    def ScatterKitten(self, ws=None):
        ScatterWS = self.GetWS("SCATTER PLOTS")
        ScatterWS["A1"] = "SCATTER PLOTS"
        ScatterWS.merge_cells("A1:G1")
        ScatterWS["B2"] = "MOOD SCORE"
        ScatterWS["D2"] = "SASS INDEX"
        ScatterWS["F2"] = "SURVIVAL RATE"
        # --- MOOD ---
        self.PlaceScatter(ScatterWS, self.ScatterPlots["Box Temperature vs Mood Score"], "B4", 2.18, 3.83)
        self.PlaceScatter(ScatterWS, self.ScatterPlots["Decay Rate vs Mood Score"], "B16", 2.18, 3.83)
        self.PlaceScatter(ScatterWS, self.ScatterPlots["Photon Count vs Mood Score"], "B28", 2.18, 3.83)
        self.PlaceScatter(ScatterWS, self.ScatterPlots["Stability vs Mood Score"], "B40", 2.18, 3.83)
        self.PlaceScatter(ScatterWS, self.ScatterPlots["Material vs Mood Score"], "B52", 2.18, 3.83)
        # --- SASS ---
        self.PlaceScatter(ScatterWS, self.ScatterPlots["Box Temperature vs Sass Index"], "D4", 2.18, 3.83)
        self.PlaceScatter(ScatterWS, self.ScatterPlots["Entanglement vs Sass Index"], "D16", 2.18, 3.83)
        # --- SURVIVAL ---
        self.PlaceScatter(ScatterWS, self.ScatterPlots["Observer Presence vs Survival Rate"], "F4", 2.18, 3.83)
        
        Drip = TipToe(self.wb, ScatterWS)
        Drip.PlotsDrip()
        self.SAVE()

    def MoodResultsKitten(self, ws=None):
        MoodWS = self.wb["MOOD RESULTS"]
        MoodWS["A1"] = "LINEAR REGRESSION"
        MoodWS.merge_cells("A1:I1")
        MoodWS["A2"] = "MOOD SCORE"
        MoodWS.merge_cells("A2:I2")

        key = "Box Temperature vs Mood Score"
        if key in self.RegressionPlots and self.RegressionPlots[key] is not None:
            self.PlaceImage(MoodWS, self.RegressionPlots["Box Temperature vs Mood Score"], "B4", 3.02, 6.1)
        else:
            MoodWS["B4"] = "No Mood / Temp  model available"

        key = "Decay Rate vs Mood Score"
        if key in self.RegressionPlots and self.RegressionPlots[key] is not None:
            self.PlaceImage(MoodWS, self.RegressionPlots["Decay Rate vs Mood Score"], "F4", 3.02, 6.1)
        else:
            MoodWS["F4"] = "No Mood / Decay model available"

        key = "Photon Count vs Mood Score"
        if key in self.RegressionPlots and self.RegressionPlots[key] is not None:
            self.PlaceImage(MoodWS, self.RegressionPlots["Photon Count vs Mood Score"], "B20", 3.02, 6.1)
        else:
            MoodWS["B20"] = "No Mood / Photon  model available"

        key = "Stability vs Mood Score"
        if key in self.RegressionPlots and self.RegressionPlots[key] is not None:
            self.PlaceImage(MoodWS, self.RegressionPlots["Stability vs Mood Score"], "F20", 3.02, 6.1)
        else:
            MoodWS["F20"] = "No Mood / Stability model available"

        key = "Cardboard Box vs Mood Score"
        if key in self.RegressionPlots and self.RegressionPlots[key] is not None:
            self.PlaceImage(MoodWS, self.RegressionPlots["Cardboard Box vs Mood Score"], "B36", 2.2, 2.95)
        else:
            MoodWS["B36"] = "No Mood / Cardboard model available"

        key = "Lead Box vs Mood Score"
        if key in self.RegressionPlots and self.RegressionPlots[key] is not None:
            self.PlaceImage(MoodWS, self.RegressionPlots["Lead Box vs Mood Score"], "D36", 2.2, 2.95)
        else:
            MoodWS["D36"] = "No Mood / Lead model available"

        key = "Quantum Foam Box vs Mood Score"
        if key in self.RegressionPlots and self.RegressionPlots[key] is not None:
            self.PlaceImage(MoodWS, self.RegressionPlots["Quantum Foam Box vs Mood Score"], "F36", 2.2, 2.95)
        else:
            MoodWS["F36"] = "No Mood / Foam model available"

        key = "Velvet Box vs Mood Score"
        if key in self.RegressionPlots and self.RegressionPlots[key] is not None:
            self.PlaceImage(MoodWS, self.RegressionPlots["Velvet Box vs Mood Score"], "H36", 2.2, 2.95)
        else:
            MoodWS["H36"] = "No Mood / Velvet model available"

        Drip = TipToe(self.wb, MoodWS)
        Drip.PlotsDrip()
        self.SAVE()


    def SassResultsKitten(self, ws=None):
        SassWS = self.wb["SASS RESULTS"]
        SassWS["A1"] = "LINEAR REGRESSION PLOTS"
        SassWS.merge_cells("A1:E1")
        SassWS["A2"] = "SASS INDEX"
        SassWS.merge_cells("A2:E2")

        key = "Box Temperature vs Sass Index"
        if key in self.RegressionPlots and self.RegressionPlots[key] is not None:
            self.PlaceImage(SassWS, self.RegressionPlots["Box Temperature vs Sass Index"], "B4", 3.22, 5.78)
        else:
            SassWS["B4"] = "No Sass / Box Temp model available"

        key = "Entanglement vs Sass Index"
        if key in self.RegressionPlots and self.RegressionPlots[key] is not None:
            self.PlaceImage(SassWS, self.RegressionPlots["Entanglement vs Sass Index"], "D4", 3.22, 5.78)
        else:
            SassWS["D4"] = "No Sass / Entanglement  model available"

        Drip = TipToe(self.wb, SassWS)
        Drip.PlotsDrip()
        self.SAVE()


    def SurvivalResultsKitten(self, ws=None):
        SurvivialWS = self.wb["SURVIVAL RESULTS"]
        SurvivialWS["A1"] = "LINEAR REGRESSION PLOTS"
        SurvivialWS.merge_cells("A1:C1")
        SurvivialWS["A2"] = "SURVIVAL RATE"
        SurvivialWS.merge_cells("A2:C2")

        key = "Observer Presence vs Survival Rate"
        if key in self.RegressionPlots and self.RegressionPlots[key] is not None:
            self.PlaceImage(SurvivialWS, self.RegressionPlots[key], "B4", 3.63, 6.88)
        else:
            SurvivialWS["B4"] = "No survival model available"

        Drip = TipToe(self.wb, SurvivialWS)
        Drip.PlotsDrip()
        self.SAVE()

    def DeleteTemps(self):
        for path in getattr(self, "TempPics", []):
            try:
                os.remove(path)
            except Exception:
                pass
        self.TempPics = []

        
    def ExcelLitter(self, OutputPath):
        self.InsightsKitten() 
        #self.CatWisdom() #I will define this later
        #self.DataKitten() 
        self.ScatterKitten() 
        self.MoodResultsKitten()
        self.SassResultsKitten()
        self.SurvivalResultsKitten()
        self.SAVE()
        self.DeleteTemps()



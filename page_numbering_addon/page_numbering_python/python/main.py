import uno
import unohelper
import time
from com.sun.star.awt import XTopWindowListener

# Dictionary for possible numbering type options
NumTypeCollection = {'i,ii,iii,...': 3, 'I,II,III,...': 2, '1,2,3,...': 4, 'Α,Β,Γ,...':52, 'α,β,γ,...':53, 'a...aa...aaa':10, 'A...AA...AAA':9, 'a,b,c,...':1, 'A,B,C,...':0}





class oListenerTop_Class(XTopWindowListener,unohelper.Base):
    def __init__(self,):
        self.doc = None

    def setDocument(self, doc):
        self.doc = doc

# XModifyListener
    def windowOpened(self,oEvent):
        pass


    def windowClosed(self,oEvent):
        pass

    def windowClosing(self,oEvent):
        pass


    def windowMinimized(self,oEvent):
        pass

    def windowNormalized(self,oEvent):
        pass

    def windowActivated(self,oEvent):
        pass

    def windowDeactivated(self,oEvent):
        pass

# parent-interface XEventListener
    def disposing(self,oEvent):
        pass #normally not needed, but should be callable anyway



def main(*args):
    """Prints the string 'Hello World(in Python)' into the current document"""
    #get the doc from the scripting context which is made available to all scripts
    global continue_dlg
    ctx = uno.getComponentContext()
    smgr = ctx.ServiceManager

    Doc = XSCRIPTCONTEXT.getDocument()
    psm = uno.getComponentContext().ServiceManager
    dp = psm.createInstance("com.sun.star.awt.DialogProvider")
    dlg = dp.createDialog("vnd.sun.star.script:dialogs.PageNumberingDialog?location=application")

    # Initialize the required fields
    oDialog1Model = dlg.Model
    PositionListBox = oDialog1Model.getByName("Position")
    PositionListBox.StringItemList = ["Επικεφαλίδα","Υποσέλιδο"]
    PositionListBox.SelectedItems = [1]

    AlignmentListBox = oDialog1Model.getByName("Alignment")
    AlignmentListBox.StringItemList= ["Αριστερά","Δεξιά","Κέντρο"]
    AlignmentListBox.SelectedItems = [2]


    FirstNumberedPage = oDialog1Model.getByName("First_Numbered_Page")
    FirstNumberedIndex = oDialog1Model.getByName("First_Numbered_Index")
    FirstNumberedPage.Value = 1
    FirstNumberedIndex.Value = 1

    FontUsed = oDialog1Model.getByName("FontSelect")

# Get the default paragraph font from Standard paragraph style
    ParaStyles = Doc.StyleFamilies.getByName("ParagraphStyles")
    StdPara = ParaStyles["Standard"]
    DefaultFontSearch = StdPara.CharFontName


    oListenerTop = oListenerTop_Class()
    oListenerTop.setDocument(Doc)

    dlg.addTopWindowListener(oListenerTop)


    dlg.execute()

# inspection tool xRay
def xray(smgr, ctx, target):
    mspf = smgr.createInstanceWithContext("com.sun.star.script.provider.MasterScriptProviderFactory", ctx)
    script_provider = mspf.createScriptProvider("")
    script = script_provider.getScript("vnd.sun.star.script:XrayTool._Main.Xray?language=Basic&location=application")
    script.invoke((target,), (), ())

g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(
    oListenerTop_Class,
    'com.sun.star.awt.XTopWindowListener',()
)
g_exportedScripts = main,

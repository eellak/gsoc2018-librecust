import uno
import unohelper
import time
from com.sun.star.awt import XTopWindowListener
import itertools
import operator
import sys
from com.sun.star.beans.PropertyAttribute import READONLY

# Dictionary for possible numbering type options
NumTypeCollection = {'i,ii,iii,...': 3, 'I,II,III,...': 2, '1,2,3,...': 4, 'Α,Β,Γ,...': 52,
                     'α,β,γ,...': 53, 'a...aa...aaa': 10, 'A...AA...AAA': 9, 'a,b,c,...': 1, 'A,B,C,...': 0}


class oListenerTop_Class(XTopWindowListener, unohelper.Base):
    def __init__(self,):
        self.doc = None

    def setDocument(self, doc):
        self.doc = doc

# XModifyListener
    def windowOpened(self, oEvent):
        pass

    def windowClosed(self, oEvent):
        pass

    def windowClosing(self, oEvent):
        pass

    def windowMinimized(self, oEvent):
        pass

    def windowNormalized(self, oEvent):
        pass

    def windowActivated(self, oEvent):
        pass

    def windowDeactivated(self, oEvent):
        pass

# parent-interface XEventListener
    def disposing(self, oEvent):
        pass  # normally not needed, but should be callable anyway


def main(*args):
    """Prints the string 'Hello World(in Python)' into the current document"""
    # get the doc from the scripting context which is made available to all scripts
    global continue_dlg
    ctx = uno.getComponentContext()
    smgr = ctx.ServiceManager

    Doc = XSCRIPTCONTEXT.getDocument()
    psm = uno.getComponentContext().ServiceManager
    dp = psm.createInstance("com.sun.star.awt.DialogProvider")
    dlg = dp.createDialog(
        "vnd.sun.star.script:dialogs.PageNumberingDialog?location=application")

    # Initialize the required fields
    oDialog1Model = dlg.Model
    PositionListBox = oDialog1Model.getByName("Position")
    PositionListBox.StringItemList = ["Επικεφαλίδα", "Υποσέλιδο"]
    PositionListBox.SelectedItems = [1]

    AlignmentListBox = oDialog1Model.getByName("Alignment")
    AlignmentListBox.StringItemList = ["Αριστερά", "Δεξιά", "Κέντρο"]
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

    ListFontsRet = ListFonts(Doc, DefaultFontSearch)

    FontUsed = oDialog1Model.getByName("FontSelect")
    FontUsed.StringItemList = ListFontsRet[0]
    FontUsed.SelectedItems = [ListFontsRet[1]]

    FontSize = oDialog1Model.getByName("FontSize")
    # Get default char size/height from Standard Paragraph style

    FontSize.Value = StdPara.CharHeight

    # end initialization of fields

    if dlg.execute() == 0:
        return

    ViewCursor = Doc.CurrentController.getViewCursor()

    AlignmentEnum = AlignmentListBox.SelectedItems[0] #when having Listbox we get only one selection
    if AlignmentEnum == 2:
        AlignmentEnum = AlignmentEnum + 1  # center align for paradjust to overcome BLOCK option

    PageNumber = Doc.createInstance("com.sun.star.text.textfield.PageNumber")
    #xray(smgr,ctx,PageNumber)

    PageNumber.NumberingType = NumTypeCollection[oDialog1Model.getByName("NumberingTypeSelect").Text] #Just ARABIC numbering for now till implementation
    PageNumber.SubType = 1 # Which page does the textfield refer to

    PageStyles = Doc.StyleFamilies.getByName("PageStyles")

    NewStyle = Doc.createInstance("com.sun.star.style.PageStyle")

    ViewCursor.jumpToPage(FirstNumberedPage.Value)

    CurrentStyleName = ViewCursor.PageStyleName
    OldStyle = PageStyles.getByName(CurrentStyleName)

    copyUsingPropertySetInfo(OldStyle,NewStyle)


    xray(smgr, ctx, NewStyle)

# inspection tool xRay


def xray(smgr, ctx, target):
    mspf = smgr.createInstanceWithContext(
        "com.sun.star.script.provider.MasterScriptProviderFactory", ctx)
    script_provider = mspf.createScriptProvider("")
    script = script_provider.getScript(
        "vnd.sun.star.script:XrayTool._Main.Xray?language=Basic&location=application")
    script.invoke((target,), (), ())


def ListFonts(oDoc, SearchString):
    SearchIndex = -1
    uniqueFontNames = []
    oWindow = oDoc.getCurrentController().getFrame().getContainerWindow()
    oFonts = oWindow.getFontDescriptors()
    ctx = uno.getComponentContext()
    smgr = ctx.ServiceManager

    seen = set()
    uniqueFontDescriptors = [
        seen.add(obj.Name) or obj for obj in oFonts if obj.Name not in seen]
    uniqueFontDescriptors = sorted(
        uniqueFontDescriptors, key=lambda x: x.Name, reverse=False)

    for i in range(len(uniqueFontDescriptors)):
        uniqueFontNames.append(uniqueFontDescriptors[i].Name)
        if uniqueFontDescriptors[i].Name == SearchString:
            SearchIndex = i

    return (uniqueFontNames, SearchIndex)


def copyUsingPropertySetInfo(srcObj, dstObj):
    ctx = uno.getComponentContext()
    smgr = ctx.ServiceManager
    sPInfo = srcObj.getPropertySetInfo()
    dPInfo = dstObj.getPropertySetInfo()
    oProps = sPInfo.getProperties()

    for i in range(len(oProps)):
        oProp = oProps[i]
        try:
            if dPInfo.hasPropertyByName(oProp.Name):
                if oProp.Type.getName() == dPInfo.getPropertyByName(oProp.Name).Type.getName():
                    oSValue = srcObj.getPropertyValue(oProp.Name)
                    if canCopyTypeWithAssignment(oSValue):
                        if (uno.getConstantByName("com.sun.star.beans.PropertyAttribute.READONLY") and oProp.Attributes) == False:
                            if oProp.Name != "GridLines":
                                dstObj.setPropertyValue(oProp.Name, oSValue)
                    elif uno.IsArray(oSValue):
                        pass
                    else:
                        oDValue = dstObj.getPropertyValue(oProp.Name)
                        if oDValue== None or uno.IsEmpty(oDValue):
                            if (uno.getConstantByName("com.sun.star.beans.PropertyAttribute.READONLY") and oProp.Attributes) == False:
                                dstObj.setPropertyValue(oProp.Name, oSValue)
                            elif uno.HasUnoInterfaces(oSValue,"com.sun.star.beans.XPropertySet"):
                                if oSValue.SupportsService("com.sun.star.text.Text"):
                                    pass
                                else:
                                    copyUsingPropertySetInfo(oSValue,oDValue)
        except Exception as e:
            continue
    return

def canCopyTypeWithAssignment(oObj):
    case_check = uno.VarType(oObj)
    if case_check<=8:
        return True
    elif case_check == 11 or case_check == 35 or case_check == 36 or case_check == 37:
        return True
    elif case_check <= 23 and case_check >= 16:
        return True
    else:
        if uno.IsUnoStruct(oObj):
            return True
        else:
            return False

g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(
    oListenerTop_Class,
    'com.sun.star.awt.XTopWindowListener', ()
)
g_exportedScripts = main,

import uno
import unohelper
import time
from com.sun.star.awt import XTopWindowListener
import itertools
import operator
import sys
from com.sun.star.beans.PropertyAttribute import READONLY
from com.sun.star.beans.PropertyAttribute import MAYBEVOID
from com.sun.star.beans.PropertyAttribute import REMOVEABLE
from com.sun.star.beans.PropertyAttribute import MAYBEDEFAULT
from com.sun.star.beans import PropertyValue
import gettext
import os
from urllib.parse import urlparse
import urllib
from urllib import request
_ = gettext.gettext

# Dictionary for possible numbering type options
NumTypeCollection = {
    "i,ii,iii,...": 3,
    "I,II,III,...": 2,
    "1,2,3,...": 4,
    "Α,Β,Γ,...": 52,
    "α,β,γ,...": 53,
    "a...aa...aaa": 10,
    "A...AA...AAA": 9,
    "a,b,c,...": 1,
    "A,B,C,...": 0
}

def copyPropertySet(smgr,ctx,srcObj,dstObj):
    mspf = smgr.createInstanceWithContext("com.sun.star.script.provider.MasterScriptProviderFactory", ctx)
    script_provider = mspf.createScriptProvider("")
    script = script_provider.getScript("vnd.sun.star.script:PageStyleClone.PageStyle.copyPropertySet?language=Basic&location=application")
    script.invoke((srcObj,dstObj), (), ())
    return dstObj

def main(*args):
    ctx = uno.getComponentContext()
    smgr = ctx.ServiceManager
    try:
        ui_locale = gettext.translation('base',
                                        localedir=urllib.request.url2pathname(
                                            get_main_directory("com.addon.pagenumbering") +
                                            'python/locales'),
                                        languages=[getLanguage()]
                                        )
    except Exception as e:
        ui_locale = gettext.translation('base',
                                        localedir=urllib.request.url2pathname(
                                            get_main_directory("com.addon.pagenumbering") +
                                            'python/locales'),
                                        languages=["en"]
                                        )

    ui_locale.install()
    _ = ui_locale.gettext

    ''' get the doc from the scripting context which is made available to all scripts
    '''
    Doc = XSCRIPTCONTEXT.getDocument()
    UndoManager = Doc.getUndoManager()
    psm = uno.getComponentContext().ServiceManager
    dp = psm.createInstance("com.sun.star.awt.DialogProvider")
    dlg = dp.createDialog(
        "vnd.sun.star.script:dialogs.PageNumberingDialog?location=application")

    # Initialize the required fields
    oDialog1Model = dlg.Model

    oDialog1Model.Title = _("Page Numbering Title")

    # Cancel and OK button Labels
    CancelButton = oDialog1Model.getByName("CancelButton")
    CancelButton.Label = _("Cancel")

    OKButton = oDialog1Model.getByName("OKButton")
    OKButton.Label = _("OK")

    HelpButton = dlg.getControl("HelpButton")
    HelpButton.Label = _("Help")

    PositionLabel = oDialog1Model.getByName("PositionLabel")
    PositionLabel.Label = _("Position")
    PositionListBox = oDialog1Model.getByName("Position")
    PositionListBox.StringItemList = [_("Header"), _("Footer")]
    PositionListBox.SelectedItems = [1]

    AlignmentLabel = oDialog1Model.getByName("AlignmentLabel")
    AlignmentLabel.Label = _("Alignment")
    AlignmentListBox = oDialog1Model.getByName("Alignment")
    AlignmentListBox.StringItemList = [_("Left"), _("Right"), _("Centered")]
    AlignmentListBox.SelectedItems = [2]

    FirstPageLabel = oDialog1Model.getByName("FirstPageLabel")
    FirstPageLabel.Label = _("First Page")
    FirstNumberedPage = oDialog1Model.getByName("First_Numbered_Page")

    PageOffsetLabel = oDialog1Model.getByName("PageOffsetLabel")
    PageOffsetLabel.Label = _("Page Offset")
    FirstNumberedIndex = oDialog1Model.getByName("First_Numbered_Index")
    FirstNumberedPage.Value = 1
    FirstNumberedIndex.Value = 1

    TypeLabel = oDialog1Model.getByName("TypeLabel")
    TypeLabel.Label = _("Numbering Type")
    NumberingTypeSelectListBox = oDialog1Model.getByName("NumberingTypeSelect")

    NumberingTypeSelectListBox.StringItemList = [
        "i,ii,iii,...",
        "I,II,III,...",
        "1,2,3,...",
        "Α,Β,Γ,...",
        "α,β,γ,...",
        "a...aa...aaa",
        "A...AA...AAA",
        "a,b,c,...",
        "A,B,C,..."
    ]

    NumberingTypeSelectListBox.Text = "1,2,3,..."

    DecorLabel = oDialog1Model.getByName("DecorLabel")
    DecorLabel.Label = _("Decor")
    NumberingDecorationListBox = oDialog1Model.getByName("NumberingDecoration")
    NumberingDecorationListBox.StringItemList = ["#", "-#-", "[#]", "(#)"]
    NumberingDecorationListBox.Text = "#"

    # FontUsed = oDialog1Model.getByName("FontSelect")

# Get the default paragraph font from Standard paragraph style
    ParaStyles = Doc.StyleFamilies.getByName("ParagraphStyles")
    StdPara = ParaStyles["Standard"]
    DefaultFontSearch = StdPara.CharFontName

    oListenerTop = oListenerTop_Class()
    oListenerTop.setDocument(Doc)

    dlg.addTopWindowListener(oListenerTop)

    ListFontsRet = ListFonts(Doc, DefaultFontSearch)

    FontLabel = oDialog1Model.getByName("FontLabel")
    FontLabel.Label = _("Font")
    FontUsed = oDialog1Model.getByName("FontSelect")
    FontUsed.StringItemList = ListFontsRet[0]
    FontUsed.SelectedItems = [ListFontsRet[1]]

    SizeLabel = oDialog1Model.getByName("SizeLabel")
    SizeLabel.Label = _("Size")
    FontSize = oDialog1Model.getByName("FontSize")
    # Get default char size/height from Standard Paragraph style

    FontSize.Value = StdPara.CharHeight

    # end initialization of fields

    if dlg.execute() == 0:
        dlg.removeTopWindowListener(oListenerTop)
        return

    ViewCursor = Doc.CurrentController.getViewCursor()

    # when having Listbox we get only one selection
    AlignmentEnum = AlignmentListBox.SelectedItems[0]
    if AlignmentEnum == 2:
        # center align for paradjust to overcome BLOCK option
        AlignmentEnum = AlignmentEnum + 1

    PageNumber = Doc.createInstance("com.sun.star.text.textfield.PageNumber")

    PageNumber.NumberingType = NumTypeCollection[
        oDialog1Model.getByName(
            "NumberingTypeSelect").Text
    ]  # Just ARABIC numbering for now till implementation
    PageNumber.SubType = 1  # Which page does the textfield refer to

    PageStyles = Doc.StyleFamilies.getByName("PageStyles")

    NewStyle = Doc.createInstance("com.sun.star.style.PageStyle")

    ViewCursor.jumpToPage(FirstNumberedPage.Value)

    CurrentStyleName = ViewCursor.PageStyleName
    OldStyle = PageStyles.getByName(CurrentStyleName)

    copyPropertySet(smgr,ctx,OldStyle,NewStyle)
    DefNumberingStyleNum = 200

    oUDP = Doc.getDocumentProperties().UserDefinedProperties

    if oUDP.getPropertySetInfo().hasPropertyByName("NumberingStyleIndex") == False:
        maybevoid = uno.getConstantByName(
            "com.sun.star.beans.PropertyAttribute.MAYBEVOID")
        removeable = uno.getConstantByName(
            "com.sun.star.beans.PropertyAttribute.REMOVEABLE")
        maybedefault = uno.getConstantByName(
            "com.sun.star.beans.PropertyAttribute.MAYBEDEFAULT")
        oUDP.addProperty("NumberingStyleIndex", maybevoid +
                         removeable + maybedefault, DefNumberingStyleNum)
        oUDP = Doc.getDocumentProperties().UserDefinedProperties
        oUDP.NumberingStyleIndex = 0
    else:
        oUDP.NumberingStyleIndex = oUDP.NumberingStyleIndex + 1

    NewStyle.Hidden = True  # Do not polute page styles dialog
    NewStyle.FollowStyle = "PageNumbering-Start(" + str(
        FirstNumberedPage.Value) + ")-Index:" + str(oUDP.NumberingStyleIndex)

    if PageStyles.hasByName(NewStyle.FollowStyle) == False:
        PageStyles.insertByName(NewStyle.FollowStyle, NewStyle)

    # Whatever is Standard will get numbering
    NumberedPage = PageStyles.getByName(NewStyle.FollowStyle)

    FontSelected = FontUsed.SelectedItems[0]

    Num_Position = None
    if PositionListBox.SelectedItems[0] == 0:
        NumberedPage.HeaderIsOn = True
        Num_Position = NumberedPage.HeaderText
        NumberedPage.HeaderBodyDistance = 499
        NumberedPage.HeaderHeight = 0
    else:
        NumberedPage.FooterIsOn = True
        Num_Position = NumberedPage.FooterText
        NumberedPage.FooterBodyDistance = 499
        NumberedPage.FooterHeight = 0

    # For text insertion a Text cursor is needed
    NumCursor = Num_Position.Text.createTextCursor()

    '''There should be included all those changing operations that should be put in undo stack
    '''
    UndoManager.enterUndoContext(_("Page Numbering"))

    ViewCursor.jumpToPage(FirstNumberedPage.Value)

    '''Set index of first numbered page
    We cannot use PageNumber.Offset property because we may need bigger than total page number indexing
    '''
    ViewCursor.PageNumberOffset = FirstNumberedIndex.Value

    ''' Every numbered page will be of Standard Page style for now
    '''
    ViewCursor.PageDescName = NewStyle.FollowStyle

    NumCursor.ParaAdjust = AlignmentEnum
    NumCursor.CharFontName = FontUsed.SelectedItems[0]
    NumCursor.CharHeight = FontSize.Value

    AlignmentListBox = oDialog1Model.getByName("Alignment")

    NumberingDecorationComboBoxText = oDialog1Model.getByName(
        "NumberingDecoration").Text
    if NumberingDecorationComboBoxText == "#":
        Num_Position.insertTextContent(NumCursor, PageNumber, False)
    elif NumberingDecorationComboBoxText == "-#-":
        Num_Position.insertString(NumCursor, "-", False)
        Num_Position.insertTextContent(NumCursor, PageNumber, False)
        Num_Position.insertString(NumCursor, "-", False)
    elif NumberingDecorationComboBoxText == "[#]":
        Num_Position.insertString(NumCursor, "[", False)
        Num_Position.insertTextContent(NumCursor, PageNumber, False)
        Num_Position.insertString(NumCursor, "]", False)
    elif NumberingDecorationComboBoxText == "(#)":
        Num_Position.insertString(NumCursor, "(", False)
        Num_Position.insertTextContent(NumCursor, PageNumber, False)
        Num_Position.insertString(NumCursor, ")", False)
    else:
        raise Exception("Custom decoration unimplemented feature")
    UndoManager.leaveUndoContext()
    dlg.removeTopWindowListener(oListenerTop)


class oListenerTop_Class(XTopWindowListener, unohelper.Base):
    """
    Top window listener implementation (XTopWindowListener) 
    """

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


def get_main_directory(module_name):
    """
    Return a string that corresponds to the installation directory of 
    the module_name string (e.g. com.addon.pagenumbering )
    """
    ctx = uno.getComponentContext()
    srv = ctx.getByName(
        "/singletons/com.sun.star.deployment.PackageInformationProvider")

    return urlparse(srv.getPackageLocation(module_name)).path + "/"


def ListFonts(oDoc, SearchString):
    """
    Returns a tuple (Font_list string[] , index of SearchString font (int) ). 
    """
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
    """
    Cope the whole PropertySet of an UNO object to an other instance.
    """
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
                        if oDValue == None or uno.IsEmpty(oDValue):
                            if (uno.getConstantByName("com.sun.star.beans.PropertyAttribute.READONLY") and oProp.Attributes) == False:
                                dstObj.setPropertyValue(oProp.Name, oSValue)
                            elif uno.HasUnoInterfaces(oSValue, "com.sun.star.beans.XPropertySet"):
                                if oSValue.SupportsService("com.sun.star.text.Text"):
                                    pass
                                else:
                                    copyUsingPropertySetInfo(oSValue, oDValue)
        except Exception as e:
            continue
    return


def canCopyTypeWithAssignment(oObj):
    case_check = uno.VarType(oObj)
    if case_check <= 8:
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


'''Inspired by @sng at https://forum.openoffice.org/en/forum/viewtopic.php?f=45&t=81457
and Andrew Pitonyak pdf "Useful Useful Macro Information For OpenOffice.org"
'''


def getLanguage():
    """
    Get current user interface language in string format. Useful for
    UI locale checkong on l10n operations (e.g. gettext...) 
    """
    oProvider = "com.sun.star.configuration.ConfigurationProvider"
    oAccess = "com.sun.star.configuration.ConfigurationAccess"
    oConfigProvider = get_instance(oProvider)
    oProp = PropertyValue()
    oProp.Name = "nodepath"
    oProp.Value = "org.openoffice.Office.Linguistic/General"
    properties = (oProp,)
    key = "UILocale"
    oSet = oConfigProvider.createInstanceWithArguments(oAccess, properties)
    if oSet and (oSet.hasByName(key)):
        ooLang = oSet.getPropertyValue(key)

    if not (ooLang and not ooLang.isspace()):
        oProp.Value = "/org.openoffice.Setup/L10N"
        properties = (oProp,)
        key = "ooLocale"
        oSet = oConfigProvider.createInstanceWithArguments(oAccess, properties)
        if oSet and (oSet.hasByName(key)):
            ooLang = oSet.getPropertyValue(key)
    return ooLang


def get_instance(service_name):
    """
    Get a service shortcut. 
    """
    sm = uno.getComponentContext()
    ctx = sm.getServiceManager()
    try:
        service = ctx.createInstance(service_name)
    except:
        service = NONE
    return service


g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(
    oListenerTop_Class,
    "com.sun.star.awt.XTopWindowListener", ()
)
g_exportedScripts = main,

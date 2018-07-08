import uno
import unohelper
import itertools
import operator
import sys
from com.sun.star.beans.PropertyAttribute import READONLY
from com.sun.star.beans.PropertyAttribute import MAYBEVOID
from com.sun.star.beans.PropertyAttribute import REMOVEABLE
from com.sun.star.beans.PropertyAttribute import MAYBEDEFAULT
from com.sun.star.beans import PropertyValue

def main(*args):
    ctx = uno.getComponentContext()
    smgr = ctx.ServiceManager

    # get the doc from the scripting context which is made available to all scripts

    Doc = XSCRIPTCONTEXT.getDocument()
    UndoManager = Doc.getUndoManager()

    # FontUsed = oDialog1Model.getByName("FontSelect")

# Get the default paragraph font from Standard paragraph style
    ParaStyles = Doc.StyleFamilies.getByName("ParagraphStyles")
    StdPara = ParaStyles["Heading 1"]

#atomic operations combined in one undo stack item
    UndoManager.enterUndoContext("Change Paragraph style")  #There should be included all those changing operations that should be put in undo stack

    UndoManager.leaveUndoContext()

def insert_hd1(*args):
    ctx = uno.getComponentContext()
    smgr = ctx.ServiceManager

    # get the doc from the scripting context which is made available to all scripts

    Doc = XSCRIPTCONTEXT.getDocument()
    UndoManager = Doc.getUndoManager()
    ParaStyles = Doc.StyleFamilies.getByName("ParagraphStyles")
    #xray(smgr, ctx, ParaStyles)

    #Create view cursor to take current cursor position
    ViewCursor = Doc.CurrentController.getViewCursor()
    #xray(smgr, ctx, ViewCursor)
    UndoManager.enterUndoContext("Style to Heading 1")
    ViewCursor.ParaStyleName = "Heading 1"
    UndoManager.leaveUndoContext()

def insert_law(*args):
    #Inspect services for debugging purposes
    ctx = uno.getComponentContext()
    smgr = ctx.ServiceManager

    Doc = XSCRIPTCONTEXT.getDocument()
    UndoManager = Doc.getUndoManager()

    #Create view cursor to take current cursor position
    ViewCursor = Doc.CurrentController.getViewCursor()
    xray(smgr, ctx, ViewCursor)
    
    #There should be used the law API to get the law string
    #dialog to get the law
    ViewCursor.setString("HALLO")    

def xray(smgr, ctx, target):
    mspf = smgr.createInstanceWithContext(
        "com.sun.star.script.provider.MasterScriptProviderFactory", ctx)
    script_provider = mspf.createScriptProvider("")
    script = script_provider.getScript(
        "vnd.sun.star.script:XrayTool._Main.Xray?language=Basic&location=application")
    script.invoke((target,), (), ())


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

# Inspired by @sng at https://forum.openoffice.org/en/forum/viewtopic.php?f=45&t=81457
# and Andrew Pitonyak pdf "Useful Useful Macro Information For OpenOffice.org"
def getLanguage():
    oProvider = "com.sun.star.configuration.ConfigurationProvider"
    oAccess   = "com.sun.star.configuration.ConfigurationAccess"
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
        """ gets a service from Uno """
        sm = uno.getComponentContext()
        ctx = sm.getServiceManager()
        try:
            service = ctx.createInstance(service_name)
        except:
            service = NONE
        return service

g_ImplementationHelper = unohelper.ImplementationHelper()

g_exportedScripts = main,insert_hd1,insert_law,

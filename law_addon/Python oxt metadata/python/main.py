import uno
import unohelper
import itertools
import operator
import sys
import re
from com.sun.star.beans.PropertyAttribute import READONLY
from com.sun.star.beans.PropertyAttribute import MAYBEVOID
from com.sun.star.beans.PropertyAttribute import REMOVEABLE
from com.sun.star.beans.PropertyAttribute import MAYBEDEFAULT
from com.sun.star.beans import PropertyValue
from urllib.parse import urlparse
import urllib
from urllib import request

#file picker constants
from com.sun.star.ui.dialogs.TemplateDescription import FILEOPEN_PREVIEW

import json
import requests

import gettext
_ = gettext.gettext 

from com.sun.star.awt.MessageBoxType import MESSAGEBOX, INFOBOX, WARNINGBOX, ERRORBOX, QUERYBOX
from com.sun.star.awt.MessageBoxButtons import BUTTONS_OK, BUTTONS_OK_CANCEL, BUTTONS_ABORT_IGNORE_RETRY, BUTTONS_YES_NO_CANCEL, BUTTONS_YES_NO, BUTTONS_RETRY_CANCEL, DEFAULT_BUTTON_OK, DEFAULT_BUTTON_CANCEL, DEFAULT_BUTTON_RETRY, DEFAULT_BUTTON_YES, DEFAULT_BUTTON_NO, DEFAULT_BUTTON_IGNORE

ui_locale = None

def MessageBox(ParentWin, MsgText, MsgTitle, MsgType=MESSAGEBOX, MsgButtons=BUTTONS_OK):
  ctx = uno.getComponentContext()
  sm = ctx.ServiceManager
  sv = sm.createInstanceWithContext("com.sun.star.awt.Toolkit", ctx) 
  myBox = sv.createMessageBox(ParentWin, MsgType, MsgButtons, MsgTitle, MsgText)
  return myBox.execute()

def get_main_directory(module_name): #com.addon.lawaddon
    ctx = uno.getComponentContext()
    srv = ctx.getByName("/singletons/com.sun.star.deployment.PackageInformationProvider")
    return urlparse(srv.getPackageLocation(module_name)).path + "/"

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

# Shortcut for creating service in API
createUnoService = (
        XSCRIPTCONTEXT
        .getComponentContext()
        .getServiceManager()
        .createInstance 
                    )

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

def update_indices(*args):
    Doc = XSCRIPTCONTEXT.getDocument()
    Indexes = Doc.getDocumentIndexes()

    for x in Indexes:
        x.update()
    

def insert_law(*args):
    #Inspect services for debugging purposes
    ctx = uno.getComponentContext()
    smgr = ctx.ServiceManager
    global ui_locale
        #Get locale string and accordingly the ccorrespondign .mo file for l10n
    try:
        ui_locale = gettext.translation('base', localedir=urllib.request.url2pathname(get_main_directory("com.addon.lawaddon")+'python/locales'), languages=[getLanguage()])
    except Exception as e:
        ui_locale = gettext.translation('base', localedir=urllib.request.url2pathname(get_main_directory("com.addon.lawaddon")+'python/locales'), languages=["en"])

    ui_locale.install()
    _ = ui_locale.gettext

    Doc = XSCRIPTCONTEXT.getDocument()
    UndoManager = Doc.getUndoManager()

    #Create view cursor to take current cursor position
    ViewCursor = Doc.CurrentController.getViewCursor()
    
    #There should be used the law API to get the law string
    #dialog to get the law

    psm = uno.getComponentContext().ServiceManager
    
    dp = psm.createInstance("com.sun.star.awt.DialogProvider")
    dlg = dp.createDialog("vnd.sun.star.extension://com.addon.lawaddon/dialogs/InsertLaw.xdl")

    dlg.Title = _("Insert Law")

    # Get dialog Model
    oDialog1Model = dlg.Model

    TypeLabel = oDialog1Model.getByName("TypeLabel")
    TypeLabel.Label = _("Type")

    TypeField = oDialog1Model.getByName("TypeListBox")

    TypeField.StringItemList = ["ν.","π.δ."]
    TypeField.SelectedItems = [0]

    InsertFieldLabel = oDialog1Model.getByName("InsertFieldLabel")
    InsertFieldLabel.Label = _("Law ID")

    HelpLabel = oDialog1Model.getByName("HelpLabel")
    HelpLabel.Label = _("Use format [number]/[year] for searching in law database")

    ArticleLabel = oDialog1Model.getByName("ArticleLabel")
    ArticleLabel.Label = _("Article/s")

    InsertButton = oDialog1Model.getByName("InsertButton")
    InsertButton.Label = _("Insert")

    if dlg.execute() == 0:
        return



    doc_text = Doc.getCurrentController().getModel().getText()

    cursor = doc_text.createTextCursorByRange(ViewCursor)

    # Get user inputViewCursor.setString("Άρθρο "+ article_num + "\n")

    LawIDField = oDialog1Model.getByName("InsertLawField")
    LawIDString = LawIDField.Text
    
    if not re.search('\d+\s?\/\s?\d+',LawIDString):
        parentwin = Doc.getCurrentController().Frame.ContainerWindow
        MessageBox(parentwin, _("Law ID field not properly filled, please try again"), _('Law ID Error'),ERRORBOX)
        insert_law()
        return

    #LawIDString = LawIDString.replace(" ", "/")

    UndoManager = Doc.getUndoManager()
    
    
    LawTypeIndex = TypeField.SelectedItems[0]
    LawType = TypeField.getItemText(LawTypeIndex)

    # Start API communications, developers should apply different API here
    # Get data drom 3gm server
    response = requests.get("https://3gm.ellak.gr/get_law/"+ LawType +"/" +LawIDString)
    
    if response.status_code == 404 :
        parentwin = Doc.getCurrentController().Frame.ContainerWindow
        MessageBox(parentwin, _("Failure while communicating with server, please try later"), _('Error'),ERRORBOX)
        return
    
    try:
        Versions = json.loads(response.text)['versions']
        Articles = Versions[-1]['articles'] # Pythonic get the last inserted element in list
    except Exception as e:
        parentwin = Doc.getCurrentController().Frame.ContainerWindow
        MessageBox(parentwin, _("Failure while communicating with server, please try later"), _('Error'),ERRORBOX)
        return
    
    ViewCursor.gotoEnd(False)
    ViewCursor.setString(LawIDString+"\n")

    ArticleField = oDialog1Model.getByName("ArticleField")

    if re.search('\d+\s?\-\s?\d+',ArticleField.Text):
        article_re = re.match('(\d+)\s?\-\s?(\d+)',ArticleField.Text)
        article_left = int(article_re.groups()[0])
        article_right = int(article_re.groups()[1])

        UndoManager.enterUndoContext(_("Insert Law"))

        for art_i in range(article_left,article_right+1):
            ViewCursor.gotoEnd(False)
            ViewCursor.setString(_("Article")+" "+ str(art_i) + "\n")
            article_body = Articles[str(art_i)]
            
            print_paragraphs(article_body,ViewCursor)

        UndoManager.leaveUndoContext()
    elif re.search('\s?\d+\s?',ArticleField.Text):
            article_re = re.match('\s?(\d+)\s?',ArticleField.Text)
            article_num = int(article_re.groups()[0])

            UndoManager.enterUndoContext(_("Insert Law"))
        
            # Insert article
            ViewCursor.gotoEnd(False)
            ViewCursor.setString(_("Article")+" "+ str(article_num) + "\n")

            article_body = Articles[str(article_num)]
            print_paragraphs(article_body,ViewCursor)

            UndoManager.leaveUndoContext()

    elif re.search('\d+\s?,?\s?',ArticleField.Text):
        article_re = re.match('\d+\s?,?\s?',ArticleField.Text)
        
        UndoManager.enterUndoContext(_("Insert Law"))
        
        for art_i in article_re.groups():
            art_index = int(art_i)

            ViewCursor.gotoEnd(False)
            ViewCursor.setString(_("Article")+" "+ str(art_i) + "\n")
            article_body = Articles[str(art_i)]
            
            print_paragraphs(article_body,ViewCursor)

        UndoManager.leaveUndoContext()
    else:
        parentwin = Doc.getCurrentController().Frame.ContainerWindow
        MessageBox(parentwin, _("Empty or wrong Articles input, please try again"), _('Law ID Error'),ERRORBOX)
        insert_law()
        return

def print_paragraphs(article_body , ViewCursor):
    global ui_locale
    _ = ui_locale.gettext
    for paragraph_num,paragraph_body in sorted(article_body.items(),key=lambda x: int(x[0])):
        ViewCursor.gotoEnd(False)
        ViewCursor.setString(_("Paragraph")+ " " + paragraph_num + "\n")
        for sentence in paragraph_body:
            ViewCursor.gotoEnd(False)
            ViewCursor.setString(sentence + ".")
        ViewCursor.gotoEnd(False)
        ViewCursor.setString("\n")

def insert_contents(*args):
    ctx = uno.getComponentContext()
    smgr = ctx.ServiceManager
    dispatcher = smgr.createInstanceWithContext( "com.sun.star.frame.DispatchHelper", ctx)
    doc = XSCRIPTCONTEXT.getDocument().getCurrentController()
    dispatcher.executeDispatch(doc,  ".uno:InsertMultiIndex", "", 0, tuple())

def insert_external_document(*args):
    doc = XSCRIPTCONTEXT.getDocument()

    #Create view cursor to take current cursor position
    ViewCursor = doc.getCurrentController().getViewCursor()

    # Pending to open on pwd of document firing the execution
    url = FilePicker(None,FILEOPEN_PREVIEW)
    
    # No file was selected, aborting
    if url==None:
        return

    ctx = uno.getComponentContext()
    smgr = ctx.ServiceManager
    

    doc_text = doc.getCurrentController().getModel().getText()

    cursor = doc_text.createTextCursorByRange(ViewCursor)
    #For now
    string = 'EXTERNAL DOCUMENT'
    
    #After all insert the link in current cursor position
    cursor.setString(string)
    cursor.HyperLinkURL = url

    Bookmark = doc.createInstance("com.sun.star.text.Bookmark")
    
    #For now
    Bookmark.setName(url)
    doc_text.insertTextContent(cursor,Bookmark,False)
        
    '''
    Info about getting page number of certain bookmark
    Useful for document merging later on

    LibreOffice Basic macro from developers guide
    oVC.gotoRange(oBookmark.getAnchor(), False)

    REM Grab page number and then return view cursor to previous location
    pg = oVC.getPage()
    oVC.gotoRange(oTextCursor, False)

    '''

    #xray(smgr,ctx,doc.Bookmarks.getByIndex(0))
    


def xray(smgr, ctx, target):
    mspf = smgr.createInstanceWithContext(
        "com.sun.star.script.provider.MasterScriptProviderFactory", ctx)
    script_provider = mspf.createScriptProvider("")
    script = script_provider.getScript(
        "vnd.sun.star.script:XrayTool._Main.Xray?language=Basic&location=application")
    script.invoke((target,), (), ())

'''
Fire file picker http://api.libreoffice.org/docs/idl/ref/namespacecom_1_1sun_1_1star_1_1ui_1_1dialogs_1_1TemplateDescription.html
Constants are included from the previous link
'''
def FilePicker(path=None, mode=1):
    filepicker = createUnoService( "com.sun.star.ui.dialogs.OfficeFilePicker" )
    if path:
        filepicker.setDisplayDirectory(path )
    filepicker.initialize( ( mode,) )
    if filepicker.execute():
        return filepicker.getFiles()[0]  

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

g_exportedScripts = main,insert_hd1,insert_law,insert_contents,insert_external_document,update_indices,

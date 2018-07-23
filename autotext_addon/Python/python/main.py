import uno
import unohelper
from urllib.parse import urlparse
import gettext
_ = gettext.gettext 
from com.sun.star.beans import PropertyValue

from com.sun.star.awt.MessageBoxType import MESSAGEBOX, INFOBOX, WARNINGBOX, ERRORBOX, QUERYBOX
from com.sun.star.awt.MessageBoxButtons import BUTTONS_OK, BUTTONS_OK_CANCEL, BUTTONS_ABORT_IGNORE_RETRY, BUTTONS_YES_NO_CANCEL, BUTTONS_YES_NO, BUTTONS_RETRY_CANCEL, DEFAULT_BUTTON_OK, DEFAULT_BUTTON_CANCEL, DEFAULT_BUTTON_RETRY, DEFAULT_BUTTON_YES, DEFAULT_BUTTON_NO, DEFAULT_BUTTON_IGNORE

def MessageBox(ParentWin, MsgText, MsgTitle, MsgType=MESSAGEBOX, MsgButtons=BUTTONS_OK):
  ctx = uno.getComponentContext()
  sm = ctx.ServiceManager
  sv = sm.createInstanceWithContext("com.sun.star.awt.Toolkit", ctx) 
  myBox = sv.createMessageBox(ParentWin, MsgType, MsgButtons, MsgTitle, MsgText)
  return myBox.execute()

from com.sun.star.lang import (XSingleComponentFactory,
    XServiceInfo)

def get_parent_document():

    ctx = uno.getComponentContext()
    smgr = ctx.ServiceManager
    desktop = smgr.createInstanceWithContext( "com.sun.star.frame.Desktop",ctx)

    if desktop.CurrentFrame:
        parent = desktop.CurrentFrame.ContainerWindow
    else:
        enum = desktop.Components.createEnumeration()
        comps = []

        while enum.hasMoreElements():
            comps.append(enum.nextElement())

        doc = comps[0]
        parent = doc.CurrentController.Frame.ContainerWindow

    return desktop.CurrentComponent

def get_main_directory(module_name): #com.addon.pagenumbering
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


def xray(smgr, ctx, target):
    mspf = smgr.createInstanceWithContext(
        "com.sun.star.script.provider.MasterScriptProviderFactory", ctx)
    script_provider = mspf.createScriptProvider("")
    script = script_provider.getScript(
        "vnd.sun.star.script:XrayTool._Main.Xray?language=Basic&location=application")
    script.invoke((target,), (), ())


def toogle_autotext_sidebar(*args):
    RESOURCE_URL = "private:resource/dockingwindow/9809"
    oDoc = XSCRIPTCONTEXT.getDocument()
    layoutmgr = oDoc.getCurrentController().getFrame().LayoutManager
    if layoutmgr.isElementVisible(RESOURCE_URL):
        layoutmgr.hideElement(RESOURCE_URL)
    else:
        layoutmgr.requestElement(RESOURCE_URL)

sorted_by_title = []

def update_auto_list(oRange):
    global sorted_by_title
    indexes = range(oRange.getCount())
    combined_col = list(zip(oRange.Titles,indexes))
    combined_col.sort(key=lambda tup: tup[0])  # sorts in place
    sorted_by_title = combined_col
    sorted_to_listbox = [i[0] for i in sorted_by_title]
    return sorted_to_listbox


class Factory(unohelper.Base, XSingleComponentFactory, XServiceInfo):
    """ This factory instantiate new window content.
    Registration of this class have to be there under
    /org.openoffice.Office.UI/WindowContentFactories/Registered/ContentFactories.
    See its schema for detail. """

    # Implementation name should be match with name of
    # the configuration node and FactoryImplementation value.
    IMPLE_NAME = "com.addon.autotextaddon"
    SERVICE_NAMES = IMPLE_NAME,


    @classmethod
    def get_imple(klass):
        return klass, klass.IMPLE_NAME, klass.SERVICE_NAMES

    def __init__(self, ctx, *args):
        self.ctx = ctx

        print("init")

    # XSingleComponentFactory
    def createInstanceWithContext(self, ctx):
        # No way to get the parent frame, not called
        return self.createInstanceWithArgumentsAndContext((), ctx)

    def createInstanceWithArgumentsAndContext(self, args, ctx):
        try:
            return create_window(ctx, args)
        except Exception as e:
            print(e)

    # XServiceInfo
    def supportedServiceNames(self):
        return self.SERVICE_NAMES

    def supportsService(self, name):
        return name in self.SERVICE_NAMES

    def getImplementationName(self):
        return self.IMPLE_NAME


g_ImplementationHelper = unohelper.ImplementationHelper()
g_ImplementationHelper.addImplementation(*Factory.get_imple())


from com.sun.star.awt import WindowDescriptor, Rectangle
from com.sun.star.awt.WindowClass import SIMPLE
from com.sun.star.awt.WindowAttribute import SHOW, BORDER, SIZEABLE, MOVEABLE, CLOSEABLE
from com.sun.star.awt.VclWindowPeerAttribute import CLIPCHILDREN
from com.sun.star.awt.PosSize import POS, SIZE
from com.sun.star.beans import NamedValue


# Valid resource URL for docking window starts with
# private:resource/dockingwindow. And valid name for them are
# 9800 - 9809 (only 10 docking windows can be created).
# See lcl_checkDockingWindowID function defined in
# source/sfx2/source/dialog/dockwin.cxx.
# If the name of dockingwindow conflict with other windows provided by
# other extensions, strange result would be happen.
RESOURCE_URL = "private:resource/dockingwindow/9809"

EXT_ID = "com.addon.autotextaddon"

current_group = "mytexts"
group_ids = []
groups_to_insert = []

def create_window(ctx, args):
    """ Creates docking window.
        @param ctx component context
        @param args arguments passed by the window content factory manager.
        @return new docking window
    """
    def create(name):
        return ctx.getServiceManager().createInstanceWithContext(name, ctx)

    if not args: return None

    frame = None # frame of parent document window
    for arg in args:
        name = arg.Name
        if name == "ResourceURL":
            if arg.Value != RESOURCE_URL:
                return None
        elif name == "Frame":
            frame = arg.Value

    if frame is None: return None # ToDo: raise exception

    global current_locale

    # this dialog has no title and placed at the top left corner.
    dialog1 = "vnd.sun.star.extension://com.addon.autotextaddon/dialogs_autotext/Dialog1.xdl"
    window = None
    if True:
        ctx = uno.getComponentContext()
        smgr = ctx.ServiceManager
        
        try:
            ui_locale = gettext.translation('base', localedir=get_main_directory("com.addon.autotextaddon")+'python/locales', languages=[getLanguage()])
        except Exception as e:
            ui_locale = gettext.translation('base', localedir=get_main_directory("com.addon.autotextaddon")+'python/locales', languages=["en"])
        
        ui_locale.install()
        _ = ui_locale.gettext
        toolkit = create("com.sun.star.awt.Toolkit")
        parent = frame.getContainerWindow()

        # Creates outer window
        # title name of this window is defined in WindowState configuration.
        desc = WindowDescriptor(SIMPLE, "window", parent, 0, Rectangle(0, 0, 400, 400),
                SHOW | SIZEABLE | MOVEABLE | CLOSEABLE | CLIPCHILDREN)
        window = toolkit.createWindow(desc)

        # Create inner window from dialog
        dp = create("com.sun.star.awt.ContainerWindowProvider")
        child = dp.createContainerWindow(dialog1, "", window, None)

        psm = uno.getComponentContext().ServiceManager
        dps = psm.createInstance("com.sun.star.text.AutoTextContainer")

        oRange = dps.getByName(current_group)
        ctx = uno.getComponentContext()
        smgr = ctx.ServiceManager

        # Initialize Dialog items

        #Initialize listeners
        action_listener = ActionListener(ctx,child)
        mouse_listener = MouseListener(ctx)

        # Autotext Listbox
        Autotext_Label = child.getControl("LabelListbox")
        Autotext_Label.Text = _("Auto Texts")

        Preview_Label = child.getControl("LabelPreview")
        Preview_Label.Text = _("Preview")

        Autotext_ListBox = child.getControl("SavedAutotext") 

        # there should be sorted entries by title and not name!

        Autotext_ListBox.addItems(update_auto_list(oRange),0)
        
        Autotext_ListBox.addMouseListener(mouse_listener)
        #xray(smgr,ctx,Autotext_ListBox)
        OK_Button = child.getControl("OKButton")
        OK_Button.addActionListener(action_listener)
        OK_Button.setActionCommand('InsertAutoText')
        OK_Button.Label = _("Insert")

        AddSelection_Button = child.getControl("AddSelectionButton")
        AddSelection_Button.addActionListener(action_listener)
        AddSelection_Button.setActionCommand('AddSelectedAutoText')
        AddSelection_Button.Label = _("Add Selection")        
        
        More_Button = child.getControl("MoreButton")
        More_Button.addActionListener(action_listener)
        More_Button.setActionCommand('MoreDispatch')
        More_Button.Label = _("More...")

        TeamList = child.getControl("GroupListBox")
        TeamList.addActionListener(ListBoxActionListener(ctx,child))

        global groups_to_insert
        global group_ids 
        group_ids = dps.getElementNames()


        for x in group_ids:
            groups_to_insert[len(groups_to_insert):] = [dps.getByName(x).Title]
        
        TeamList.addItems(groups_to_insert,0)
        TeamList.getModel().SelectedItems = [group_ids.index(current_group)]
        
        child.setVisible(True)

        window.addWindowListener(WindowResizeListener(child))

        #child.setPosSize(0, 0, 0, 0, POS)  # if the dialog is not placed at
                                            # top left corner

    return window


from com.sun.star.awt import XWindowListener, XActionListener, XMouseListener, XItemListener

class MouseListener(unohelper.Base, XMouseListener):

    def __init__(self, ctx):
        self.ctx = ctx

    def disposing(self, ev):
        pass

    # XActionListener
    def mousePressed(self, ev):
        global sorted_by_title
        dialog = ev.Source.getContext()
        action_command = ev
        smgr = self.ctx.ServiceManager

        auto_list = dialog.getControl("SavedAutotext")
        selected_pos= auto_list.getSelectedItemPos()
        psm = uno.getComponentContext().ServiceManager
        dps = psm.createInstance("com.sun.star.text.AutoTextContainer")

        oRange = dps.getByName(current_group)

        selected_autotext = oRange.getByIndex(sorted_by_title[selected_pos][1])
        #getString

        preview_label = dialog.getControl("PreviewLabel")

        preview_label.setText(selected_autotext.getString())

    def mouseReleased():
        pass

    def mouseEntered():
        dialog = ev.Source.getContext()
        global sorted_by_title 
        autotext_listbox = dialog.getControl("SavedAutotext")
        current_autotexts = autotext_listbox.getItemCount()
        autotext_listbox.removeItems(0,current_autotexts) 
        autotext_listbox.addItems(update_auto_list(oRange),0)
        psm = uno.getComponentContext().ServiceManager
        dps = psm.createInstance("com.sun.star.text.AutoTextContainer")
        oRange = dps.getByName(current_group)

        pass

    def mouseExited():
        pass


class ActionListener(unohelper.Base, XActionListener):

    def __init__(self, ctx, child):
        self.ctx = ctx
        self.child = child # Pass child to get access to sub-window elements
    def disposing(self, ev):
        pass

    # XActionListener
    def actionPerformed(self, ev):
        dialog = ev.Source.getContext()
        ctx = uno.getComponentContext()
        action_command = ev.ActionCommand
        smgr = ctx.ServiceManager
        global sorted_by_title 
        if action_command == "InsertAutoText":
            auto_list = dialog.getControl("SavedAutotext")
            selected_pos= auto_list.getSelectedItemPos()

            if selected_pos == -1:
                parentwin = get_parent_document().getCurrentController().Frame.ContainerWindow
                MessageBox(parentwin, _("No autotext is selected. Please select autotext and then press Insert"), _('Error'),ERRORBOX)
                return

            psm = uno.getComponentContext().ServiceManager
            dps = psm.createInstance("com.sun.star.text.AutoTextContainer")

            oRange = dps.getByName(current_group)

            selected_autotext = oRange.getByIndex(sorted_by_title[selected_pos][1])
            ViewCursor = get_parent_document().getCurrentController().getViewCursor()
            selected_autotext.applyTo(ViewCursor)

        if action_command == "AddSelectedAutoText":
            try:
                ui_locale = gettext.translation('base', localedir=get_main_directory("com.addon.autotextaddon")+'python/locales', languages=[getLanguage()])
            except Exception as e:
                ui_locale = gettext.translation('base', localedir=get_main_directory("com.addon.autotextaddon")+'python/locales', languages=["en"])
        
            ui_locale.install()
            _ = ui_locale.gettext
            oCurs = get_parent_document().getCurrentSelection()
            psm = uno.getComponentContext().ServiceManager
            dps = psm.createInstance("com.sun.star.text.AutoTextContainer")
            ViewCursor = get_parent_document().getCurrentController().getViewCursor()
            if ViewCursor.getString() == "":
                parentwin = get_parent_document().getCurrentController().Frame.ContainerWindow
                MessageBox(parentwin, _("No content is selected. Please select content and then add to autotext list"), _('Error'),ERRORBOX)
                return
            oRange = dps.getByName(current_group)            
            
            dp = psm.createInstance("com.sun.star.awt.DialogProvider")
            dlg = dp.createDialog("vnd.sun.star.extension://com.addon.autotextaddon/dialogs_autotext/Dialog2.xdl")

            global groups_to_insert
            global group_ids
            dlg.Title = _("Add to category") +" "+ groups_to_insert[group_ids.index(current_group)]

            NameLabel = dlg.getControl("NameLabel")
            ShortcutLabel = dlg.getControl("ShortcutLabel")
            AddButton = dlg.getControl("AddButton")

            NameLabel.Text = _("Name")
            ShortcutLabel.Text = _("Shortcut")
            AddButton.Label = _("Add")

            if dlg.execute() == 0:
                return
            
            new_autotext_name = dlg.getControl("NameField").Text
            new_autotext_shortcut = dlg.getControl("ShortcutField").Text

            try:
                oRange.insertNewByName(new_autotext_shortcut,new_autotext_name,oCurs.getByIndex(0))
            except Exception as e:
                parentwin = get_parent_document().getCurrentController().Frame.ContainerWindow
                MessageBox(parentwin, _("Cannot add selection to category") +" "+ current_group, _('Error'),ERRORBOX)
            

            #refresh entries of main listbox
            oRange = dps.getByName(current_group)
            #xray(smgr, ctx, oRange)
            autotext_listbox = self.child.getControl("SavedAutotext")
            current_autotexts = autotext_listbox.getItemCount()
            autotext_listbox.removeItems(0,current_autotexts) 
            autotext_listbox.addItems(update_auto_list(oRange),0)

        if action_command == "MoreDispatch":
            # access the dispatcher
            dispatcher = smgr.createInstanceWithContext( "com.sun.star.frame.DispatchHelper", ctx)
            doc = get_parent_document().getCurrentController()
            dispatcher.executeDispatch(doc, ".uno:EditGlossary", "", 0, tuple())


class ListBoxActionListener(unohelper.Base, XActionListener):

    def __init__(self, ctx, child):
        self.ctx = ctx
        self.child = child # Pass child to get access to sub-window elements
    def disposing(self, ev):
        pass

    # XActionListener
    def actionPerformed(self, ev):
        dialog = ev.Source.getContext()
        ctx = uno.getComponentContext()
        action_command = ev.ActionCommand
        smgr = ctx.ServiceManager

        psm = uno.getComponentContext().ServiceManager
        dps = psm.createInstance("com.sun.star.text.AutoTextContainer")

        global sorted_by_title 
        global current_group
        global groups_to_insert
        global group_ids
        current_group = group_ids[groups_to_insert.index(action_command)]

        autotext_listbox = dialog.getControl("SavedAutotext")

        oRange = dps.getByName(current_group)
        #xray(smgr, ctx, oRange)
        autotext_listbox = dialog.getControl("SavedAutotext")
        current_autotexts = autotext_listbox.getItemCount()
        autotext_listbox.removeItems(0,current_autotexts) 
        autotext_listbox.addItems(update_auto_list(oRange),0)
        


class WindowResizeListener(unohelper.Base, XWindowListener):

    def __init__(self, dialog):
        self.dialog = dialog
    def disposing(self, ev):
        pass

    # XWindowListener
    def windowMoved(self, ev):
        pass
    def windowShown(self, ev):
        global sorted_by_title 
        autotext_listbox = dialog.getControl("SavedAutotext")
        current_autotexts = autotext_listbox.getItemCount()
        autotext_listbox.removeItems(0,current_autotexts) 
        autotext_listbox.addItems(update_auto_list(oRange),0)
        psm = uno.getComponentContext().ServiceManager
        dps = psm.createInstance("com.sun.star.text.AutoTextContainer")
        oRange = dps.getByName(current_group)

        pass
    def windowHidden(self, ev):
        global sorted_by_title 
        autotext_listbox = dialog.getControl("SavedAutotext")
        current_autotexts = autotext_listbox.getItemCount()
        autotext_listbox.removeItems(0,current_autotexts) 
        autotext_listbox.addItems(update_auto_list(oRange),0)
        psm = uno.getComponentContext().ServiceManager
        dps = psm.createInstance("com.sun.star.text.AutoTextContainer")
        oRange = dps.getByName(current_group)
        pass

    def windowResized(self, ev):
        # extends inner window to match with the outer window
        if self.dialog:
            self.dialog.setPosSize(0, 0, ev.Width, ev.Height, SIZE)

# for com.sun.star.comp.framework.TabWindowService based dockingwindow

from com.sun.star.awt import (XContainerWindowEventHandler,
        XActionListener)

class ContainerWindowHandler(unohelper.Base, XContainerWindowEventHandler, XActionListener):

    def __init__(self, ctx, frame):
        self.ctx = ctx
        self.frame = frame
        self.parent = None

    def create(self, name):
        return self.ctx.getServiceManager().createInstanceWithContext(name, self.ctx)

    # XContainerWindowEventHandler
    def callHandlerMethod(self, window, obj, name):
        if name == "external_event":
            if obj == "initialize":
                self._initialize(window)

    def getSupportedMethodNames(self):
        return "external_event",

    def _initialize(self, window):
        pass

    def disposing(self, ev):
        pass

    # XActionListener
    def actionPerformed(self, ev):
        pass

from com.sun.star.task import XJobExecutor

g_exportedScripts = toogle_autotext_sidebar,
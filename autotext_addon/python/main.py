import uno
import unohelper


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

    # this dialog has no title and placed at the top left corner.
    dialog1 = "vnd.sun.star.extension://com.addon.autotextaddon/dialogs_autotext/Dialog1.xdl"
    window = None
    if True:
        toolkit = create("com.sun.star.awt.Toolkit")
        parent = frame.getContainerWindow()

        # Creates outer window
        # title name of this window is defined in WindowState configuration.
        desc = WindowDescriptor(SIMPLE, "window", parent, 0, Rectangle(0, 0, 100, 100),
                SHOW | SIZEABLE | MOVEABLE | CLOSEABLE | CLIPCHILDREN)
        window = toolkit.createWindow(desc)

        # Create inner window from dialog
        dp = create("com.sun.star.awt.ContainerWindowProvider")
        child = dp.createContainerWindow(dialog1, "", window, None)

        psm = uno.getComponentContext().ServiceManager
        dps = psm.createInstance("com.sun.star.text.AutoTextContainer")
        oRange = dps.getByName("mytexts")
    #    ctx = uno.getComponentContext()
        smgr = ctx.ServiceManager

        child.getControl("SavedAutotext").addItems(oRange.Titles,0)

        action_listener = ActionListener(ctx,child)
        child.getControl("OKButton").addActionListener(action_listener)
        child.getControl("OKButton").setActionCommand('InsertAutoText')

        child.getControl("AddSelectionButton").addActionListener(action_listener)
        child.getControl("AddSelectionButton").setActionCommand('AddSelectedAutoText')        
        
        child.getControl("SavedAutotext").addMouseListener(MouseListener(ctx))
        #xray(smgr,ctx,child.getControl("SavedAutotext"))
        child.setVisible(True)

        window.addWindowListener(WindowResizeListener(child))


        #child.setPosSize(0, 0, 0, 0, POS)  # if the dialog is not placed at
                                            # top left corner

    return window

from com.sun.star.awt import XWindowListener, XActionListener, XMouseListener

class MouseListener(unohelper.Base, XMouseListener):

    def __init__(self, ctx):
        self.ctx = ctx

    def disposing(self, ev):
        pass

    # XActionListener
    def mousePressed(self, ev):
        dialog = ev.Source.getContext()
        action_command = ev
        smgr = self.ctx.ServiceManager

        auto_list = dialog.getControl("SavedAutotext")
        selected_pos= auto_list.getSelectedItemPos()
        psm = uno.getComponentContext().ServiceManager
        dps = psm.createInstance("com.sun.star.text.AutoTextContainer")

        oRange = dps.getByName("mytexts")

        selected_autotext = oRange.getByIndex(selected_pos)
        #getString

        preview_label = dialog.getControl("PreviewLabel")

        preview_label.setText(selected_autotext.getString())
        #xray(smgr, self.ctx, preview_label)

    def mouseReleased():
        pass

    def mouseEntered():
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
        #xray(smgr, ctx, action_command)

        if action_command == "InsertAutoText":
            auto_list = dialog.getControl("SavedAutotext")
            selected_pos= auto_list.getSelectedItemPos()

            psm = uno.getComponentContext().ServiceManager
            dps = psm.createInstance("com.sun.star.text.AutoTextContainer")

            oRange = dps.getByName("mytexts")

            selected_autotext = oRange.getByIndex(selected_pos)
            ViewCursor = get_parent_document().getCurrentController().getViewCursor()
            selected_autotext.applyTo(ViewCursor)

        if action_command == "AddSelectedAutoText":
            oCurs = get_parent_document().getCurrentSelection()
            psm = uno.getComponentContext().ServiceManager
            dps = psm.createInstance("com.sun.star.text.AutoTextContainer")
            ViewCursor = get_parent_document().getCurrentController().getViewCursor()
            oRange = dps.getByName("mytexts")            
            
            dp = psm.createInstance("com.sun.star.awt.DialogProvider")
            dlg = dp.createDialog("vnd.sun.star.extension://com.addon.autotextaddon/dialogs_autotext/Dialog2.xdl")


            if dlg.execute() == 0:
                return
            

            new_autotext_name = dlg.getControl("NameField").Text
            new_autotext_shortcut = dlg.getControl("ShortcutField").Text

            oRange.insertNewByName(new_autotext_shortcut,new_autotext_name,oCurs.getByIndex(0))

            #refresh entries of main listbox
            oRange = dps.getByName("mytexts")
            autotext_listbox = self.child.getControl("SavedAutotext")
            current_autotexts = autotext_listbox.getItemCount()
            autotext_listbox.removeItems(0,current_autotexts) 
            autotext_listbox.addItems(oRange.Titles,0)



class WindowResizeListener(unohelper.Base, XWindowListener):

    def __init__(self, dialog):
        self.dialog = dialog

    def disposing(self, ev):
        pass

    # XWindowListener
    def windowMoved(self, ev):
        pass
    def windowShown(self, ev):
        pass
    def windowHidden(self, ev):
        pass

    def windowResized(self, ev):
        # extends inner window to match with the outer window
        if self.dialog:
            self.dialog.setPosSize(0, 0, ev.Width, ev.Height, SIZE)
            # ToDo: resize dialog elements


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
#        btn = window.getControl("CommandButton1")
#        btn.setActionCommand("btn1")
#        btn.addActionListener(self)
        pass

    def disposing(self, ev):
        pass

    # XActionListener
    def actionPerformed(self, ev):
        pass
# Tool functions

def create_service(ctx, name, args=None):
    """ Create service with args if required. """
    smgr = ctx.getServiceManager()
    if args:
        return smgr.createInstanceWithArgumentsAndContext(name, args, ctx)
    else:
        return smgr.createInstanceWithContext(name, ctx)



from com.sun.star.task import XJobExecutor

g_exportedScripts = toogle_autotext_sidebar,
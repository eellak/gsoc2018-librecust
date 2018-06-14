import uno
import unohelper
import time

from com.sun.star.awt import XTopWindowListener

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

continue_dlg = 1

def HelloWorldPythons( ):
    """Prints the string 'Hello World(in Python)' into the current document"""
    #get the doc from the scripting context which is made available to all scripts

    ctx = uno.getComponentContext()
    smgr = ctx.ServiceManager

    Doc = XSCRIPTCONTEXT.getDocument()
    psm = uno.getComponentContext().ServiceManager
    dp = psm.createInstance("com.sun.star.awt.DialogProvider")
    dlg = dp.createDialog("vnd.sun.star.script:dialogs.PageNumberingDialog?location=application")
    #dlg.execute()

    oListenerTop = oListenerTop_Class()
    oListenerTop.setDocument(Doc)

    dlg.addTopWindowListener(oListenerTop)

    dlg.setVisible(1)

    #while continue_dlg=1:
    #    dlg.setVisible(true)
    #    time.sleep(0.02)
    #    pass

    #xray(smgr,ctx, oListenerTop)



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

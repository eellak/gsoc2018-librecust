---
title: Event listeners
permalink: /docs/Event-listeners/
---

# Event listeners
In this page, the main methodology concerning LibreOffice event listeners is outlined. 

## What is a listener
While we are describing listener structs of LibreOffice, the main principles apply to many fields and implementations. Generally, listeners are instances that are activated and execute methods whenever the suitable event is occurred. Their applications extend from simple programming implementations to user interface element interaction. For example, a listener can watch and execute whenever a dialog element is focused by mouse cursor.

In LibreOffice terms, every listener interface is a subclass of [XEventListener](https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1lang_1_1XEventListener.html). When working with interfaces, there are several class methods that must be implemented by the developer. As we can easily observe, the ancestor XEventListener requires the implementation of `disposing()` method along others defined by sub-interfaces.

## Window listeners
Listening to window events is mandatory for the creation of dialogs and wizards that offer a level of user interaction. The [XTopWindowListener](https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1awt_1_1XTopWindowListener.html) interface polls for window events such as when a window is opened, closed or minimized. The following code, part of Page Numbering Addon, illustrate a simple usage and implementation of window listeners:

### Basic
```Basic
sub Main
        DialogLibraries.LoadLibrary("PageNumberingAddon")
	oLib = DialogLibraries.GetByName("PageNumberingAddon")
        myDlg = oLib.GetByName("PageNumberingDialog")
        oDlg = CreateUnoDialog(myDlg)

	oListenerTop = createUnoListener("TopListen_", "com.sun.star.awt.XTopWindowListener")
	oDlg.addTopWindowlistener(oListenerTop) 
        ' ******DO STUFF****** '
        ' remove listener 
end sub

sub TopListen_WindowClosing
	Continue=0
end sub
sub  TopListen_windowOpened(e As Object)
	Dim oDialog1Model
	Dim oDialog1
' Initialize all dialog fields with default values here	
	oDialog1 = e.Source	
	oDialog1Model = oDialog1.Model  &apos;Load the Model of the Dialog
end sub
' Unused window Listeners for now
sub  TopListen_windowClosed
end sub
sub TopListen_windowMinimized
end sub
sub  TopListen_windowNormalized
end sub
sub  TopListen_windowActivated
end sub
sub  TopListen_windowDeactivated
end sub
sub  TopListen_disposing
end sub
```
In basic, there are no classes and objects so a prefix for the listener's methods is required. As seen in the first argument of `createUnoListener()` we use the prefix `TopListen_*`. This is not the case with Python implementation that offers object oriented principles.

### Python
```Python
from com.sun.star.awt import XTopWindowListener

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

```       
The listener constructor is where, exploiting Python function polymorphism, different arguments, after `self` can be passed. For defined by the interface functions the required arguments are included in the official interface documentation pages. As we can see in the Basic implementation, access to the window/dialog that the event took place is given through the `e` argument that is of type [EventObject](https://api.libreoffice.org/docs/idl/ref/structcom_1_1sun_1_1star_1_1lang_1_1EventObject.html).

Every LibreOffice listener is implemented using the aforementioned procedure. Next, some examples of different event listeners used in the `AutoText addon` and implemented in Python are shown:

## Mouse listeners
```Python
from com.sun.star.awt import XMouseListener

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

    def mouseReleased():
        pass

    def mouseEntered():
        pass

    def mouseExited():
pass
```

## Action listeners
```Python
from com.sun.star.awt import XActionListener

class ActionListener(unohelper.Base, XActionListener):

    def __init__(self, ctx, child):
        self.ctx = ctx
        self.child = child # Pass child to get access to sub-window elements

    def disposing(self, ev):
        pass

    # XActionListener
    def actionPerformed(self, ev):
        dialog = ev.Source.getContext()
        action_command = ev.ActionCommand

        if action_command == "InsertAutoText":
           	# DO SOME STUFF
        if action_command == "AddSelectedAutoText":
            # DO SOME STUFF

        if action_command == "MoreDispatch":
            # DO SOME STUFF
```

## Window resize listeners
```Python
from com.sun.star.awt import XWindowListener

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
```

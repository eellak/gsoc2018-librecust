# -*- coding: utf-8 -*-
#!/usr/bin/env python

# =============================================================================
#
# Write your code here
#
# =============================================================================

import uno
from com.sun.star.awt.MessageBoxButtons import BUTTONS_OK, BUTTONS_OK_CANCEL, BUTTONS_YES_NO, BUTTONS_YES_NO_CANCEL, BUTTONS_RETRY_CANCEL, BUTTONS_ABORT_IGNORE_RETRY
from com.sun.star.awt.MessageBoxButtons import DEFAULT_BUTTON_OK, DEFAULT_BUTTON_CANCEL, DEFAULT_BUTTON_RETRY, DEFAULT_BUTTON_YES, DEFAULT_BUTTON_NO, DEFAULT_BUTTON_IGNORE
from com.sun.star.awt.MessageBoxType import MESSAGEBOX, INFOBOX, WARNINGBOX, ERRORBOX, QUERYBOX
from com.sun.star.awt import XActionListener
from com.sun.star.awt import XMouseListener
import unohelper

from ui.Panel1_UI import Panel1_UI


import gettext
_ = gettext.gettext 
# ----------------- helpers for API_inspector tools -----------------

# uncomment for MRI
#def mri(ctx, target):
#    mri = ctx.ServiceManager.createInstanceWithContext("mytools.Mri", ctx)
#    mri.inspect(target)

# uncomment for Xray


sorted_by_title = []
current_group = "mytexts"
groups_to_insert = []
group_ids = []

from com.sun.star.uno import RuntimeException as _rtex
def xray(myObject):
    try:
        sm = uno.getComponentContext().ServiceManager
        mspf = sm.createInstanceWithContext("com.sun.star.script.provider.MasterScriptProviderFactory", uno.getComponentContext())
        scriptPro = mspf.createScriptProvider("")
        xScript = scriptPro.getScript("vnd.sun.star.script:XrayTool._Main.Xray?language=Basic&location=application")
        xScript.invoke((myObject,), (), ())
        return
    except:
        raise _rtex("\nBasic library Xray is not installed", uno.getComponentContext())


class Panel1(Panel1_UI):
    '''
    Class documentation...
    '''
    def __init__(self, panelWin):
        Panel1_UI.__init__(self, panelWin)

        
        # document
        self.ctx = uno.getComponentContext()
        self.smgr = self.ctx.ServiceManager
        self.desktop = self.smgr.createInstanceWithContext("com.sun.star.frame.Desktop", self.ctx)
        self.document = self.desktop.getCurrentComponent()

        global sorted_by_title 
        global current_group
        global groups_to_insert
        global group_ids


        self.child = self.DialogContainer

        psm = uno.getComponentContext().ServiceManager
        dps = psm.createInstance("com.sun.star.text.AutoTextContainer")
        oRange = dps.getByName(current_group)

        Autotext_ListBox = self.child.getControl("SavedAutotext") 


        Autotext_ListBox.addItems(update_auto_list(oRange),0) 


        mouse_listener = MouseListener(self.ctx)
        Autotext_ListBox.addMouseListener(mouse_listener)

        TeamList = self.child.getControl("GroupListBox")
        TeamList.addActionListener(ListBoxActionListener(self.ctx,self.child))
        
        group_ids = dps.getElementNames()

        groups_to_insert = []
        
        for x in group_ids:
            groups_to_insert[len(groups_to_insert):] = [dps.getByName(x).Title]

        TeamList.addItems(groups_to_insert,0)
        TeamList.getModel().SelectedItems = [group_ids.index(current_group)]



    def getHeight(self):
        return self.DialogContainer.Size.Height

    # --------- my code ---------------------
    # mri(self.LocalContext, self.DialogContainer)
    # xray(self.DialogContainer)

    def myFunction(self):
        # TODO: not implemented
        pass

    # --------- helpers ---------------------

    def messageBox(self, MsgText, MsgTitle, MsgType=MESSAGEBOX, MsgButtons=BUTTONS_OK):
        sm = self.LocalContext.ServiceManager
        si = sm.createInstanceWithContext("com.sun.star.awt.Toolkit", self.LocalContext)
        mBox = si.createMessageBox(self.Toolkit, MsgType, MsgButtons, MsgTitle, MsgText)
        mBox.execute()

    # -----------------------------------------------------------
    #               Execute dialog
    # -----------------------------------------------------------

    def showDialog(self):
        self.DialogContainer.setVisible(True)
        self.DialogContainer.createPeer(self.Toolkit, None)
        self.DialogContainer.execute()

    # -----------------------------------------------------------
    #               Action events
    # -----------------------------------------------------------


    def OKButton_OnClick(self):
        global sorted_by_title
        global current_group
        auto_list = self.child.getControl("SavedAutotext")
        selected_pos = auto_list.getSelectedItemPos()


        if selected_pos == -1:
            self.messageBox("No autotext is selected. Please select autotext and then press Insert", "Error", ERRORBOX)
            #MessageBox(parentwin, _("No autotext is selected. Please select autotext and then press Insert"), _('Error'),ERRORBOX)
            return

        psm = uno.getComponentContext().ServiceManager
        dps = psm.createInstance("com.sun.star.text.AutoTextContainer")

        oRange = dps.getByName(current_group)

        selected_autotext = oRange.getByIndex(sorted_by_title[selected_pos][1])
        ViewCursor = self.document.getCurrentController().getViewCursor()
        selected_autotext.applyTo(ViewCursor)

    def AddSelectionButton_OnClick(self):
        global groups_to_insert
        global group_ids
        global sorted_by_title
        global current_group

        oCurs = self.document.getCurrentSelection()
        psm = uno.getComponentContext().ServiceManager
        dps = psm.createInstance("com.sun.star.text.AutoTextContainer")
        ViewCursor = self.document.getCurrentController().getViewCursor()
        if ViewCursor.getString() == "":
            self.messageBox("No content is selected. Please select content and then add to autotext list", "Error", ERRORBOX)
            #MessageBox(parentwin, _("No content is selected. Please select content and then add to autotext list"), _('Error'),ERRORBOX)
            return
        oRange = dps.getByName(current_group)
        

        dp = psm.createInstance("com.sun.star.awt.DialogProvider")
        dlg = dp.createDialog("vnd.sun.star.extension://com.addon.autotextaddon/dialogs_autotext/Dialog2.xdl")
        
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
            self.messageBox("Cannot add selection to category", "Error", ERRORBOX)
            #MessageBox(parentwin, _("Cannot add selection to category") +" "+ current_group, _('Error'),ERRORBOX)
        

        #refresh entries of main listbox
        oRange = dps.getByName(current_group)
        #xray(smgr, ctx, oRange)
        autotext_listbox = self.child.getControl("SavedAutotext")
        current_autotexts = autotext_listbox.getItemCount()
        autotext_listbox.removeItems(0,current_autotexts) 
        autotext_listbox.addItems(update_auto_list(oRange),0)


    def MoreButton_OnClick(self):
        ctx = uno.getComponentContext()
        smgr = ctx.ServiceManager
        dispatcher = smgr.createInstanceWithContext( "com.sun.star.frame.DispatchHelper", ctx)
        doc = self.document.getCurrentController()
        dispatcher.executeDispatch(doc, ".uno:EditGlossary", "", 0, tuple())

    def HelpButton_OnClick(self):
        


def update_auto_list(oRange):
    global sorted_by_title
    indexes = range(oRange.getCount())
    combined_col = list(zip(oRange.Titles,indexes))
    combined_col.sort(key=lambda tup: tup[0])  # sorts in place
    sorted_by_title = combined_col
    sorted_to_listbox = [i[0] for i in sorted_by_title]
    return sorted_to_listbox



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

        global sorted_by_title 
        global current_group
        global groups_to_insert
        global group_ids

        psm = uno.getComponentContext().ServiceManager
        dps = psm.createInstance("com.sun.star.text.AutoTextContainer")

        current_group = group_ids[groups_to_insert.index(action_command)]


        autotext_listbox = dialog.getControl("SavedAutotext")

        oRange = dps.getByName(current_group)
        #xray(smgr, ctx, oRange)

        autotext_listbox = dialog.getControl("SavedAutotext")


        current_autotexts = autotext_listbox.getItemCount()
        autotext_listbox.removeItems(0,current_autotexts) 
        xray(autotext_listbox)
        autotext_listbox.addItems(update_auto_list(oRange),0)


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




def Run_Panel1(*args):
    """
    Intended to be used in a development environment only
    Copy this file in src dir and run with (Tools - Macros - MyMacros)
    After development copy this file back
    """
    ctx = uno.getComponentContext()
    sm = ctx.ServiceManager
    dialog = sm.createInstanceWithContext("com.sun.star.awt.UnoControlDialog", ctx)

    app = Panel1(dialog)
    app.showDialog()

g_exportedScripts = Run_Panel1,

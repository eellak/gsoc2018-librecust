# -*- coding: utf-8 -*-
#!/usr/bin/env python

import uno
from com.sun.star.awt.MessageBoxButtons import (BUTTONS_OK,
                                                BUTTONS_OK_CANCEL,
                                                BUTTONS_YES_NO,
                                                BUTTONS_YES_NO_CANCEL,
                                                BUTTONS_RETRY_CANCEL,
                                                BUTTONS_ABORT_IGNORE_RETRY)

from com.sun.star.awt.MessageBoxButtons import (DEFAULT_BUTTON_OK,
                                                DEFAULT_BUTTON_CANCEL,
                                                DEFAULT_BUTTON_RETRY,
                                                DEFAULT_BUTTON_YES,
                                                DEFAULT_BUTTON_NO,
                                                DEFAULT_BUTTON_IGNORE)

from com.sun.star.awt.MessageBoxType import (MESSAGEBOX,
                                             INFOBOX,
                                             WARNINGBOX,
                                             ERRORBOX,
                                             QUERYBOX)

from com.sun.star.awt import XActionListener
from com.sun.star.awt import XMouseListener
import unohelper
from urllib.parse import urlparse
from ui.Panel1_UI import Panel1_UI
from com.sun.star.beans import PropertyValue

# l10n
from com.sun.star.lang import (XSingleComponentFactory,
                               XServiceInfo)


import gettext
_ = gettext.gettext

sorted_by_title = []
current_group = "mytexts"
groups_to_insert = []
group_ids = []
ui_locale = None

# Localization functions


def get_main_directory(module_name):  # com.addon.pagenumbering
    ctx = uno.getComponentContext()
    srv = ctx.getByName(
        "/singletons/com.sun.star.deployment.PackageInformationProvider")
    return urlparse(srv.getPackageLocation(module_name)).path + "/"


'''Inspired by @sng at 
https://forum.openoffice.org/en/forum/viewtopic.php?f=45&t=81457
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
    """ gets a service from Uno """
    sm = uno.getComponentContext()
    ctx = sm.getServiceManager()
    try:
        service = ctx.createInstance(service_name)
    except:
        service = NONE
    return service


from com.sun.star.uno import RuntimeException as _rtex


class Panel1(Panel1_UI):
    '''
    Sidebar Panel AutoText Addon 
    '''

    def __init__(self, panelWin):
        Panel1_UI.__init__(self, panelWin)

        self.ctx = uno.getComponentContext()
        self.smgr = self.ctx.ServiceManager
        self.desktop = self.smgr.createInstanceWithContext(
            "com.sun.star.frame.Desktop", self.ctx)
        self.document = self.desktop.getCurrentComponent()

        global sorted_by_title
        global current_group
        global groups_to_insert
        global group_ids

        self.child = self.DialogContainer

        global ui_locale
        # Get current UI language
        try:
            ui_locale = gettext.translation('base',
                                            localedir=urllib.request.url2pathname(
                                                get_main_directory("com.addon.autotextaddon") +
                                            'locales'),
                                            languages=[getLanguage()])
        except Exception as e:
            ui_locale = gettext.translation('base',
                                            localedir=urllib.request.url2pathname(
                                                get_main_directory("com.addon.autotextaddon") +
                                            'locales'),
                                            languages=["en"])

        ui_locale.install()
        _ = ui_locale.gettext

        psm = uno.getComponentContext().ServiceManager
        dps = psm.createInstance("com.sun.star.text.AutoTextContainer")
        oRange = dps.getByName(current_group)

        # Update listbox entries for the first time
        Autotext_ListBox = self.child.getControl("SavedAutotext")
        Autotext_ListBox.addItems(update_auto_list(oRange), 0)

        # Mouse listener for preview label
        mouse_listener = MouseListener(self.ctx)
        Autotext_ListBox.addMouseListener(mouse_listener)

        TeamList = self.child.getControl("GroupListBox")
        TeamList.addActionListener(ListBoxActionListener(self.ctx, self.child))

        # Collect Autotext groups for dropdown Category
        # Define as selected the My Texts group getting its index
        group_ids = dps.getElementNames()
        groups_to_insert = []

        for x in group_ids:
            groups_to_insert[len(groups_to_insert):] = [dps.getByName(x).Title]

        TeamList.addItems(groups_to_insert, 0)
        TeamList.getModel().SelectedItems = [group_ids.index(current_group)]

        # Localize every dialog aspect
        Autotext_Label = self.child.getControl("LabelListbox")
        Autotext_Label.Text = _("Auto Texts")

        GroupLabel = self.child.getControl("GroupLabel")
        GroupLabel.Text = _("Group")

        Preview_Label = self.child.getControl("LabelPreview")
        Preview_Label.Text = _("Preview")

        OK_Button = self.child.getControl("OKButton")
        OK_Button.Label = _("Insert")

        AddSelection_Button = self.child.getControl("AddSelectionButton")
        AddSelection_Button.Label = _("Add Selection")

        More_Button = self.child.getControl("MoreButton")
        More_Button.Label = _("More...")

    def getHeight(self):
        return self.DialogContainer.Size.Height

    def messageBox(self,
                   MsgText,
                   MsgTitle,
                   MsgType=MESSAGEBOX,
                   MsgButtons=BUTTONS_OK):
        """
        Fire MessageBox execution defining MsgType (com.sun.star.awt.MessageBoxType) 
        with MsgBox types (com.sun.star.awt.MessageBoxButtons)
        """
        sm = self.LocalContext.ServiceManager
        si = sm.createInstanceWithContext(
            "com.sun.star.awt.Toolkit", self.LocalContext)
        mBox = si.createMessageBox(
            self.Toolkit, MsgType, MsgButtons, MsgTitle, MsgText)
        mBox.execute()

    def showDialog(self):
        self.DialogContainer.setVisible(True)
        self.DialogContainer.createPeer(self.Toolkit, None)
        self.DialogContainer.execute()

    # Action listeners

    def OKButton_OnClick(self):
        """
        Insert to current cursor position given by the ViewCursor
        """
        global sorted_by_title
        global current_group
        global ui_locale
        auto_list = self.child.getControl("SavedAutotext")
        selected_pos = auto_list.getSelectedItemPos()

        _ = ui_locale.gettext

        if selected_pos == -1:
            self.messageBox(_("No autotext is selected. Please select autotext and then press Insert"),
                            _("Error"),
                            ERRORBOX)
            return

        psm = uno.getComponentContext().ServiceManager
        dps = psm.createInstance("com.sun.star.text.AutoTextContainer")

        oRange = dps.getByName(current_group)

        selected_autotext = oRange.getByIndex(sorted_by_title[selected_pos][1])
        ViewCursor = self.document.getCurrentController().getViewCursor()
        selected_autotext.applyTo(ViewCursor)

    def AddSelectionButton_OnClick(self):
        """
        Get current selection from view cursor and add to current group
        shown from category dropdown
        """
        global groups_to_insert
        global group_ids
        global sorted_by_title
        global current_group
        global ui_locale

        _ = ui_locale.gettext

        oCurs = self.document.getCurrentSelection()
        psm = uno.getComponentContext().ServiceManager
        dps = psm.createInstance("com.sun.star.text.AutoTextContainer")
        ViewCursor = self.document.getCurrentController().getViewCursor()
        if ViewCursor.getString() == "":
            self.messageBox(_("No content is selected. Please select content and then add to autotext list"),
                            _("Error"),
                            ERRORBOX)
            return
        oRange = dps.getByName(current_group)

        dp = psm.createInstance("com.sun.star.awt.DialogProvider")
        dlg = dp.createDialog(
            "vnd.sun.star.extension://com.addon.autotextaddon/dialogs_autotext/Dialog2.xdl")

        dlg.Title = _("Add to category") + " " + \
            groups_to_insert[group_ids.index(current_group)]

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
            oRange.insertNewByName(new_autotext_shortcut,
                                   new_autotext_name, oCurs.getByIndex(0))
        except Exception as e:
            self.messageBox(
                _("Cannot add selection to category"), _("Error"), ERRORBOX)

        # refresh entries of main listbox
        oRange = dps.getByName(current_group)

        autotext_listbox = self.child.getControl("SavedAutotext")
        current_autotexts = autotext_listbox.getItemCount()
        autotext_listbox.removeItems(0, current_autotexts)
        autotext_listbox.addItems(update_auto_list(oRange), 0)

    def MoreButton_OnClick(self):
        """
        Access to the default AutoText window
        """
        ctx = uno.getComponentContext()
        smgr = ctx.ServiceManager
        dispatcher = smgr.createInstanceWithContext(
            "com.sun.star.frame.DispatchHelper", ctx)
        doc = self.document.getCurrentController()
        dispatcher.executeDispatch(doc, ".uno:EditGlossary", "", 0, tuple())


def update_auto_list(oRange):
    """
    Update list that holds names of Autotext entries for the range oRange
    """
    global sorted_by_title
    indexes = range(oRange.getCount())
    combined_col = list(zip(oRange.Titles, indexes))
    combined_col.sort(key=lambda tup: tup[0])  # sorts in place
    sorted_by_title = combined_col
    sorted_to_listbox = [i[0] for i in sorted_by_title]
    return sorted_to_listbox


class ListBoxActionListener(unohelper.Base, XActionListener):
    """
    Update AutoTexts list when Categiry dropdown is changing 
    """

    def __init__(self, ctx, child):
        self.ctx = ctx
        self.child = child  # Pass child to get access to sub-window elements

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

        autotext_listbox = dialog.getControl("SavedAutotext")

        current_autotexts = autotext_listbox.getItemCount()
        autotext_listbox.removeItems(0, current_autotexts)

        autotext_listbox.addItems(update_auto_list(oRange), 0)


class MouseListener(unohelper.Base, XMouseListener):
    """
    XMouseListener implementation for Preview Field updating
    """

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
        selected_pos = auto_list.getSelectedItemPos()
        psm = uno.getComponentContext().ServiceManager
        dps = psm.createInstance("com.sun.star.text.AutoTextContainer")

        oRange = dps.getByName(current_group)

        selected_autotext = oRange.getByIndex(sorted_by_title[selected_pos][1])
        # getString

        preview_label = dialog.getControl("PreviewLabel")

        preview_label.setText(selected_autotext.getString())

    def mouseReleased():
        pass

    def mouseEntered():
        dialog = ev.Source.getContext()
        global sorted_by_title
        autotext_listbox = dialog.getControl("SavedAutotext")
        current_autotexts = autotext_listbox.getItemCount()
        autotext_listbox.removeItems(0, current_autotexts)
        autotext_listbox.addItems(update_auto_list(oRange), 0)
        psm = uno.getComponentContext().ServiceManager
        dps = psm.createInstance("com.sun.star.text.AutoTextContainer")
        oRange = dps.getByName(current_group)

        pass

    def mouseExited():
        pass


def Run_Panel1(*args):
    ctx = uno.getComponentContext()
    sm = ctx.ServiceManager
    dialog = sm.createInstanceWithContext(
        "com.sun.star.awt.UnoControlDialog", ctx)

    app = Panel1(dialog)
    app.showDialog()


g_exportedScripts = Run_Panel1,

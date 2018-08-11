# -*- coding: utf-8 -*-
#!/usr/bin/env python

# =============================================================================
#
# Dialog implementation generated from a XDL file.
#
# Created: Mon Jul 30 19:49:02 2018
#      by: unodit 0.7.0
#
# WARNING! All changes made in this file will be overwritten
#          if the file is generated again!
#
# =============================================================================

import uno
import unohelper
from com.sun.star.awt import XActionListener
from com.sun.star.task import XJobExecutor


class Panel1_UI(unohelper.Base, XActionListener, XJobExecutor):
    """
    Class documentation...
    """

    def __init__(self, panelWin):
        self.LocalContext = uno.getComponentContext()
        self.ServiceManager = self.LocalContext.ServiceManager
        self.Toolkit = self.ServiceManager.createInstanceWithContext("com.sun.star.awt.ExtToolkit", self.LocalContext)

        # -----------------------------------------------------------
        #               Create dialog and insert controls
        # -----------------------------------------------------------

        # --------------create dialog container and set model and properties
        self.DialogContainer = panelWin
        self.DialogModel = self.ServiceManager.createInstance("com.sun.star.awt.UnoControlDialogModel")
        self.DialogContainer.setModel(self.DialogModel)
        self.DialogModel.Name = "Dialog1"
        self.DialogModel.PositionX = "0"
        self.DialogModel.PositionY = "0"
        self.DialogModel.Width = 151
        self.DialogModel.Height = 337
        self.DialogModel.Closeable = True
        self.DialogModel.Moveable = True
        self.DialogModel.DesktopAsParent = False


        # --------- create an instance of ListBox control, set properties ---
        self.SavedAutotext = self.DialogModel.createInstance("com.sun.star.awt.UnoControlListBoxModel")

        self.SavedAutotext.Name = "SavedAutotext"
        self.SavedAutotext.TabIndex = 1
        self.SavedAutotext.PositionX = "6"
        self.SavedAutotext.PositionY = "39"
        self.SavedAutotext.Width = 123
        self.SavedAutotext.Height = 136

        # inserts the control model into the dialog model
        self.DialogModel.insertByName("SavedAutotext", self.SavedAutotext)

        # --------- create an instance of ListBox control, set properties ---
        self.GroupListBox = self.DialogModel.createInstance("com.sun.star.awt.UnoControlListBoxModel")

        self.GroupListBox.Name = "GroupListBox"
        self.GroupListBox.TabIndex = 8
        self.GroupListBox.PositionX = "51"
        self.GroupListBox.PositionY = "6"
        self.GroupListBox.Width = 72
        self.GroupListBox.Height = 17
        self.GroupListBox.Dropdown = True

        # inserts the control model into the dialog model
        self.DialogModel.insertByName("GroupListBox", self.GroupListBox)

        # --------- create an instance of Button control, set properties ---
        self.OKButton = self.DialogModel.createInstance("com.sun.star.awt.UnoControlButtonModel")

        self.OKButton.Name = "OKButton"
        self.OKButton.TabIndex = 0
        self.OKButton.PositionX = "12"
        self.OKButton.PositionY = "313"
        self.OKButton.Width = 121
        self.OKButton.Height = 17
        self.OKButton.Label = "Insert"

        # inserts the control model into the dialog model
        self.DialogModel.insertByName("OKButton", self.OKButton)

        # add the action listener
        self.DialogContainer.getControl('OKButton').addActionListener(self)
        self.DialogContainer.getControl('OKButton').setActionCommand('OKButton_OnClick')

        # --------- create an instance of Button control, set properties ---
        self.AddSelectionButton = self.DialogModel.createInstance("com.sun.star.awt.UnoControlButtonModel")

        self.AddSelectionButton.Name = "AddSelectionButton"
        self.AddSelectionButton.TabIndex = 5
        self.AddSelectionButton.PositionX = "76"
        self.AddSelectionButton.PositionY = "291"
        self.AddSelectionButton.Width = 67
        self.AddSelectionButton.Height = 17
        self.AddSelectionButton.Label = "Add Selection"

        # inserts the control model into the dialog model
        self.DialogModel.insertByName("AddSelectionButton", self.AddSelectionButton)

        # add the action listener
        self.DialogContainer.getControl('AddSelectionButton').addActionListener(self)
        self.DialogContainer.getControl('AddSelectionButton').setActionCommand('AddSelectionButton_OnClick')

        # --------- create an instance of Button control, set properties ---
        self.MoreButton = self.DialogModel.createInstance("com.sun.star.awt.UnoControlButtonModel")

        self.MoreButton.Name = "MoreButton"
        self.MoreButton.TabIndex = 7
        self.MoreButton.PositionX = "4"
        self.MoreButton.PositionY = "291"
        self.MoreButton.Width = 59
        self.MoreButton.Height = 17
        self.MoreButton.Label = "More..."

        # inserts the control model into the dialog model
        self.DialogModel.insertByName("MoreButton", self.MoreButton)

        # add the action listener
        self.DialogContainer.getControl('MoreButton').addActionListener(self)
        self.DialogContainer.getControl('MoreButton').setActionCommand('MoreButton_OnClick')

        # --------- create an instance of Button control, set properties ---
        self.HelpButton = self.DialogModel.createInstance("com.sun.star.awt.UnoControlButtonModel")

        self.HelpButton.Name = "HelpButton"
        self.HelpButton.TabIndex = 10
        self.HelpButton.PositionX = "129"
        self.HelpButton.PositionY = "6"
        self.HelpButton.Width = 17
        self.HelpButton.Height = 15
        self.HelpButton.HelpText = "Page03"
        self.HelpButton.HelpURL = "com.addon.autotextaddon/Page03.xhp"
        self.HelpButton.Label = "?"
        self.HelpButton.PushButtonType = 3

        # inserts the control model into the dialog model
        self.DialogModel.insertByName("HelpButton", self.HelpButton)

        # --------- create an instance of FixedText control, set properties ---
        self.PreviewLabel = self.DialogModel.createInstance("com.sun.star.awt.UnoControlFixedTextModel")

        self.PreviewLabel.Name = "PreviewLabel"
        self.PreviewLabel.TabIndex = 2
        self.PreviewLabel.PositionX = "4"
        self.PreviewLabel.PositionY = "190"
        self.PreviewLabel.Width = 138
        self.PreviewLabel.Height = 93
        self.PreviewLabel.MultiLine = True
        self.PreviewLabel.Border = 1

        # inserts the control model into the dialog model
        self.DialogModel.insertByName("PreviewLabel", self.PreviewLabel)

        # --------- create an instance of FixedText control, set properties ---
        self.LabelPreview = self.DialogModel.createInstance("com.sun.star.awt.UnoControlFixedTextModel")

        self.LabelPreview.Name = "LabelPreview"
        self.LabelPreview.TabIndex = 3
        self.LabelPreview.PositionX = "6"
        self.LabelPreview.PositionY = "179"
        self.LabelPreview.Width = 66
        self.LabelPreview.Height = 11
        self.LabelPreview.Label = "Preview"

        # inserts the control model into the dialog model
        self.DialogModel.insertByName("LabelPreview", self.LabelPreview)

        # --------- create an instance of FixedText control, set properties ---
        self.LabelListbox = self.DialogModel.createInstance("com.sun.star.awt.UnoControlFixedTextModel")

        self.LabelListbox.Name = "LabelListbox"
        self.LabelListbox.TabIndex = 4
        self.LabelListbox.PositionX = "6"
        self.LabelListbox.PositionY = "28"
        self.LabelListbox.Width = 72
        self.LabelListbox.Height = 10
        self.LabelListbox.Label = "Auto texts"

        # inserts the control model into the dialog model
        self.DialogModel.insertByName("LabelListbox", self.LabelListbox)

        # --------- create an instance of FixedText control, set properties ---
        self.GroupLabel = self.DialogModel.createInstance("com.sun.star.awt.UnoControlFixedTextModel")

        self.GroupLabel.Name = "GroupLabel"
        self.GroupLabel.TabIndex = 9
        self.GroupLabel.PositionX = "0"
        self.GroupLabel.PositionY = "11"
        self.GroupLabel.Width = 51
        self.GroupLabel.Height = 10
        self.GroupLabel.Label = "Group:"

        # inserts the control model into the dialog model
        self.DialogModel.insertByName("GroupLabel", self.GroupLabel)

        # --------- create an instance of FixedLine control, set properties ---
        self.FixedLine1 = self.DialogModel.createInstance("com.sun.star.awt.UnoControlFixedLineModel")

        self.FixedLine1.Name = "FixedLine1"
        self.FixedLine1.TabIndex = 6
        self.FixedLine1.PositionX = "13"
        self.FixedLine1.PositionY = "171"
        self.FixedLine1.Width = 151
        self.FixedLine1.Height = 0

        # inserts the control model into the dialog model
        self.DialogModel.insertByName("FixedLine1", self.FixedLine1)

    # -----------------------------------------------------------
    #               Action events
    # -----------------------------------------------------------

    def actionPerformed(self, oActionEvent):

        if oActionEvent.ActionCommand == 'OKButton_OnClick':
            self.OKButton_OnClick()

        if oActionEvent.ActionCommand == 'AddSelectionButton_OnClick':
            self.AddSelectionButton_OnClick()

        if oActionEvent.ActionCommand == 'MoreButton_OnClick':
            self.MoreButton_OnClick()


# ----------------- END GENERATED CODE ----------------------------------------
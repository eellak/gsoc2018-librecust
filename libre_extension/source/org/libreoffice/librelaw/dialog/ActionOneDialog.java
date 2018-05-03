package org.libreoffice.librelaw.dialog;

import org.libreoffice.librelaw.helper.DialogHelper;
import org.libreoffice.librelaw.helper.Lo;
import org.libreoffice.librelaw.helper.FileHelper;


import com.sun.star.awt.XDialog;
import com.sun.star.awt.XDialogEventHandler;
import com.sun.star.lang.WrappedTargetException;
import com.sun.star.uno.XComponentContext;

import com.sun.star.awt.XListBox;

public class ActionOneDialog implements XDialogEventHandler {

	private XDialog dialog;
	private static final String actionOk = "actionOk";
	private static final String actionOpenFile = "actionOpenFile";
	private String[] supportedActions = new String[] { actionOk, actionOpenFile };
	private final XComponentContext m_xContext; //Needed for functions that need XComponentContext

	public ActionOneDialog(XComponentContext xContext) {
		m_xContext = xContext;
		this.dialog = DialogHelper.createDialog("ActionOneDialog.xdl", xContext, this);
		DialogHelper.addListelement(this.dialog,"ListBox1","TEST 1",0);
		DialogHelper.addListelement(this.dialog,"ListBox1","TEST 2",1);
		DialogHelper.addListmass(this.dialog,"ListBox1","/home/arvchristos/Pictures/", 2);
	}

	public void show() {
		dialog.execute();

	}

	private void onOkButtonPressed() {
		dialog.endExecute();
	}

	@Override
	public boolean callHandlerMethod(XDialog dialog, Object eventObject, String methodName) throws WrappedTargetException {
		if (methodName.equals(actionOk)) {
			onOkButtonPressed();
			return true; // Event was handled
		}
		if (methodName.equals(actionOpenFile)) {
			//FileHelper.openFile(m_xContext,"/home/arvchristos/Documents/project.odt");
			XListBox lister = DialogHelper.getListBox(this.dialog,"ListBox1");

			System.out.println(lister.getSelectedItem());
			lister.removeItems((short)0,(short)1);
			DialogHelper.addListelement(this.dialog,"ListBox1","TEST 555",0);
			return true; // Event was handled
		}
		return false; // Event was not handled
	}

	@Override
	public String[] getSupportedMethodNames() {
		return supportedActions;
	}

}

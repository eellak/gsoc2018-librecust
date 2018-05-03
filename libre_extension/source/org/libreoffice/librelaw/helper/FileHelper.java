package org.libreoffice.librelaw.helper;

import java.io.File;
import java.net.MalformedURLException;
import java.net.URISyntaxException;
import java.net.URL;

import com.sun.star.io.IOException;
import com.sun.star.beans.PropertyValue;
import com.sun.star.deployment.PackageInformationProvider;
import com.sun.star.deployment.XPackageInformationProvider;
import com.sun.star.comp.helper.BootstrapException;

import com.sun.star.beans.*;
import com.sun.star.uno.*;
import com.sun.star.awt.*;
import com.sun.star.util.*;
import com.sun.star.document.*;
import com.sun.star.container.*;
import com.sun.star.ui.*;
import com.sun.star.lang.*;
import com.sun.star.frame.*;

import org.libreoffice.librelaw.helper.Lo;
import org.libreoffice.librelaw.dialog.ActionOneDialog;
import org.libreoffice.librelaw.helper.DialogHelper;
import org.libreoffice.librelaw.helper.DocumentHelper;
import org.libreoffice.librelaw.helper.Props;

import com.sun.star.uno.Exception;
import com.sun.star.io.IOException;


public class FileHelper {

	final static String DIALOG_RESOURCES = "dialog/";

	/**
	 * Returns a path to a dialog file
	 */
	public static File getDialogFilePath(String xdlFile, XComponentContext xContext) {
		return getFilePath(DIALOG_RESOURCES + xdlFile, xContext);
	}

	/**
	 * Returns a file path for a file in the installed extension, or null on failure.
	 */
	public static File getFilePath(String file, XComponentContext xContext) {
		XPackageInformationProvider xPackageInformationProvider = PackageInformationProvider.get(xContext);
        String location = xPackageInformationProvider.getPackageLocation("org.libreoffice.librelaw.librelaw");
        Object oTransformer;
		try {
			oTransformer = xContext.getServiceManager().createInstanceWithContext("com.sun.star.util.URLTransformer", xContext);
		} catch (Exception e) {
			e.printStackTrace();
			return null;
		}
        XURLTransformer xTransformer = (XURLTransformer)UnoRuntime.queryInterface(XURLTransformer.class, oTransformer);
        com.sun.star.util.URL[] oURL = new com.sun.star.util.URL[1];
        oURL[0] = new com.sun.star.util.URL();
        oURL[0].Complete = location + "/" + file;
        xTransformer.parseStrict(oURL);
        URL url;
        try {
			url = new URL(oURL[0].Complete);
		} catch (MalformedURLException e1) {
			return null;
		}
        File f;
		try {
			f = new File(url.toURI());
		} catch (URISyntaxException e1) {
			return null;
		}
        return f;
	}

	public static void openFile(XComponentContext xContext,String filepath){
		try {
				// get the remote office component context


				System.out.println("Connected to a running office ...");

				System.out.println(
								"Reached url point" );
				// get the remote office service manager
				com.sun.star.lang.XMultiComponentFactory xMCF =
						xContext.getServiceManager();

				Object oDesktop = xMCF.createInstanceWithContext(
						"com.sun.star.frame.Desktop", xContext);

				com.sun.star.frame.XComponentLoader xCompLoader =
						UnoRuntime.queryInterface(
						 com.sun.star.frame.XComponentLoader.class, oDesktop);

				String sUrl = filepath;
				if ( sUrl.indexOf("private:") != 0) {
						java.io.File sourceFile = new java.io.File(filepath);
						StringBuffer sbTmp = new StringBuffer("file:///");
						sbTmp.append(sourceFile.getCanonicalPath().replace('\\', '/'));
						sUrl = sbTmp.toString();
				}
				PropertyValue[] properties = Props.makeProps("AsTemplate",true); //Open as template, more properties will be added dynamically
				// Load a Writer document, which will be automatically displayed
				com.sun.star.lang.XComponent xComp = xCompLoader.loadComponentFromURL(sUrl, "_default", 0, properties);


		}
		catch( Exception | java.io.IOException e ) {

				e.printStackTrace(System.err);
				System.exit(1);
		}
	}

}

package org.libreoffice.librelaw.comp;

import com.sun.star.uno.XComponentContext;

import com.sun.star.lib.uno.helper.Factory;


import com.sun.star.awt.*;
import com.sun.star.comp.helper.BootstrapException;
import com.sun.star.uno.*;
import com.sun.star.lang.*;
import com.sun.star.frame.*;

import com.sun.star.uno.Exception;

import java.io.IOException;

import org.libreoffice.librelaw.dialog.ActionOneDialog;
import org.libreoffice.librelaw.helper.DialogHelper;
import org.libreoffice.librelaw.helper.DocumentHelper;
import org.libreoffice.librelaw.helper.FileHelper;

import org.libreoffice.librelaw.helper.Lo;
import org.libreoffice.librelaw.helper.Props;

import com.sun.star.lang.XSingleComponentFactory;
import com.sun.star.registry.XRegistryKey;
import com.sun.star.lib.uno.helper.WeakBase;

import java.io.*;
import java.util.*;

import com.sun.star.beans.*;
import com.sun.star.uno.*;
import com.sun.star.awt.*;
import com.sun.star.util.*;
import com.sun.star.document.*;
import com.sun.star.container.*;
import com.sun.star.ui.*;

import com.sun.star.uno.Exception;
import com.sun.star.io.IOException;


public final class LibreLawImpl extends WeakBase
   implements com.sun.star.lang.XServiceInfo,
              com.sun.star.task.XJobExecutor
{
    private final XComponentContext m_xContext;
    private static final String m_implementationName = LibreLawImpl.class.getName();
    private static final String[] m_serviceNames = {
        "org.libreoffice.librelaw.LibreLaw" };


    public LibreLawImpl( XComponentContext context )
    {
        m_xContext = context;
    };

    public static XSingleComponentFactory __getComponentFactory( String sImplementationName ) {
        XSingleComponentFactory xFactory = null;

        if ( sImplementationName.equals( m_implementationName ) )
            xFactory = Factory.createComponentFactory(LibreLawImpl.class, m_serviceNames);
        return xFactory;
    }

    public static boolean __writeRegistryServiceInfo( XRegistryKey xRegistryKey ) {
        return Factory.writeRegistryServiceInfo(m_implementationName,
                                                m_serviceNames,
                                                xRegistryKey);
    }

    // com.sun.star.lang.XServiceInfo:
    public String getImplementationName() {
         return m_implementationName;
    }

    public boolean supportsService( String sService ) {
        int len = m_serviceNames.length;

        for( int i=0; i < len; i++) {
            if (sService.equals(m_serviceNames[i]))
                return true;
        }
        return false;
    }

    public String[] getSupportedServiceNames() {
        return m_serviceNames;
    }

    // com.sun.star.task.XJobExecutor:
    public void trigger(String action)
    {
    	switch (action) {
    	case "actionOne":
    		ActionOneDialog actionOneDialog = new ActionOneDialog(m_xContext);
    		actionOneDialog.show();
        FileHelper.openFile(m_xContext,"/home/arvchristos/Documents/project.odt");
    		break;
    	default:
    		DialogHelper.showErrorMessage(m_xContext, null, "Unknown action: " + action);
    	}

    }

}

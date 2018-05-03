
// Lo.java
// Andrew Davison, ad@fivedots.coe.psu.ac.th, February 2015

/* A growing collection of utility functions to make Office
   easier to use. They are currently divided into the following
   groups:

     * interface object creation (uses generics)

     * office starting
     * office shutdown

     * document opening
     * document creation
     * document saving
     * document closing

     * initialization via Addon-supplied context
     * initialization via script context

     * dispatch
     * UNO cmds

     * use Inspectors extension

     * color methods
     * other utils

     * container manipulation
*/
package org.libreoffice.librelaw.helper;

import java.io.*;
import java.util.*;
import java.net.URLClassLoader;


import com.sun.star.beans.*;
import com.sun.star.comp.helper.*;
import com.sun.star.frame.*;
import com.sun.star.connection.*;
import com.sun.star.bridge.*;
import com.sun.star.lang.*;
import com.sun.star.uno.*;
import com.sun.star.awt.*;
import com.sun.star.util.*;
import com.sun.star.document.*;

import com.sun.star.view.*;
import com.sun.star.container.*;
import com.sun.star.linguistic2.*;

import com.sun.star.uno.Exception;
import com.sun.star.io.IOException;

import com.sun.star.script.provider.XScriptContext;
import com.sun.star.reflection.*;

import com.sun.star.comp.beans.*;




public class Lo
{
  // docType ints
  public static final int UNKNOWN = 0;
  public static final int WRITER = 1;
  public static final int BASE = 2;
  public static final int CALC = 3;
  public static final int DRAW = 4;
  public static final int IMPRESS = 5;
  public static final int MATH = 6;

  // docType strings
  public static final String UNKNOWN_STR = "unknown";
  public static final String WRITER_STR = "swriter";
  public static final String BASE_STR = "sbase";
  public static final String CALC_STR = "scalc";
  public static final String DRAW_STR = "sdraw";
  public static final String IMPRESS_STR = "simpress";
  public static final String MATH_STR = "smath";

  // docType service names
  public static final String UNKNOWN_SERVICE = "com.sun.frame.XModel";
  public static final String WRITER_SERVICE = "com.sun.star.text.TextDocument";
  public static final String BASE_SERVICE = "com.sun.star.sdb.OfficeDatabaseDocument";
  public static final String CALC_SERVICE = "com.sun.star.sheet.SpreadsheetDocument";
  public static final String DRAW_SERVICE = "com.sun.star.drawing.DrawingDocument";
  public static final String IMPRESS_SERVICE = "com.sun.star.presentation.PresentationDocument";
  public static final String MATH_SERVICE = "com.sun.star.formula.FormulaProperties";

  // connect to locally running Office via port 8100
  private static final int SOCKET_PORT = 8100;


  // CLSIDs for Office documents
  // defined in <OFFICE>\officecfg\registry\data\org\openoffice\Office\Embedding.xcu
  public static final String WRITER_CLSID = "8BC6B165-B1B2-4EDD-aa47-dae2ee689dd6";
  public static final String CALC_CLSID = "47BBB4CB-CE4C-4E80-a591-42d9ae74950f";
  public static final String DRAW_CLSID = "4BAB8970-8A3B-45B3-991c-cbeeac6bd5e3";
  public static final String IMPRESS_CLSID = "9176E48A-637A-4D1F-803b-99d9bfac1047";
  public static final String MATH_CLSID = "078B7ABA-54FC-457F-8551-6147e776a997";
  public static final String CHART_CLSID = "12DCAE26-281F-416F-a234-c3086127382e";

/* unsure about these:
     chart2 "80243D39-6741-46C5-926E-069164FF87BB"
          service: com.sun.star.chart2.ChartDocument

     applet "970B1E81-CF2D-11CF-89CA-008029E4B0B1"
          service: com.sun.star.comp.sfx2.AppletObject

     plug-in "4CAA7761-6B8B-11CF-89CA-008029E4B0B1"
           service: com.sun.star.comp.sfx2.PluginObject

     frame "1A8A6701-DE58-11CF-89CA-008029E4B0B1"
           service: com.sun.star.comp.sfx2.IFrameObject

     XML report chart "D7896D52-B7AF-4820-9DFE-D404D015960F"
           service: com.sun.star.report.ReportDefinition

*/


  // remote component context
  private static XComponentContext xcc = null;

  // remote desktop UNO service
  private static XDesktop xDesktop = null;

  // remote service managers
  private static XMultiComponentFactory mcFactory = null;
                                   // has replaced XMultiServiceFactory
  private static XMultiServiceFactory msFactory = null;

  private static XComponent bridgeComponent = null;
      // this is only set if office is opened via a socket

  private static boolean isOfficeTerminated = false;



  public static XComponentContext getContext()
  {  return xcc;  }

  public static XDesktop getDesktop()
  {  return xDesktop;  }

  public static XMultiComponentFactory getComponentFactory()
  {  return mcFactory;  }

  public static XMultiServiceFactory getServiceFactory()
  {  return msFactory;  }

  public static XComponent getBridge()
  {  return bridgeComponent;  }



  @SuppressWarnings("deprecation")
  public static void setOOoBean(OOoBean oob)
  // use OOoBean to initialize Lo globals
  {
    try {
      OfficeConnection conn = oob.getOOoConnection();   // OfficeConnection is deprecated
      if (conn == null)
        System.out.println("No office connection found in OOoBean");
      else {
        xcc = conn.getComponentContext();
        if (xcc == null)
          System.out.println("No component context found in OOoBean");
        else
          mcFactory = xcc.getServiceManager();

        xDesktop = oob.getOOoDesktop();
        msFactory = oob.getMultiServiceFactory();
      }
    }
    catch (java.lang.Exception e) {
      System.out.println("Couldn't initialize LO using OOoBean: " + e);
    }
  }  // end of setOOoBean()



  // ====== interface object creation (uses generics) ===========

  public static <T> T qi(Class<T> aType, Object o)
  // the "Loki" function -- reduces typing
  {  return UnoRuntime.queryInterface(aType, o);  }



  public static <T> T createInstanceMSF(Class<T> aType, String serviceName)
  /* create an interface object of class aType from the named service;
     uses 'old' XMultiServiceFactory, so a document must have already been loaded/created
  */
  {
    if (msFactory == null) {
      System.out.println("No document found");
      return null;
    }

    T interfaceObj = null;
    try {
      Object o = msFactory.createInstance(serviceName);     // create service component
      interfaceObj = Lo.qi(aType, o);
           // uses bridge to obtain proxy to remote interface inside service;
           // implements casting across process boundaries
    }
    catch (Exception e) {
      System.out.println("Couldn't create interface for \"" + serviceName + "\": " + e);
    }
    return interfaceObj;
  }  // end of createInstanceMSF()



  public static <T> T createInstanceMSF(Class<T> aType, String serviceName,
                                                             XMultiServiceFactory msf)
  /* create an interface object of class aType from the named service;
     uses 'old' XMultiServiceFactory, so a document must have been already loaded/created
  */
  {
    if (msf == null) {
      System.out.println("No document found");
      return null;
    }

    T interfaceObj = null;
    try {
      Object o = msf.createInstance(serviceName);   // create service component
      interfaceObj = Lo.qi(aType, o);
           // uses bridge to obtain proxy to remote interface inside service;
           // implements casting across process boundaries
    }
    catch (Exception e) {
      System.out.println("Couldn't create interface for \"" + serviceName + "\":\n  " + e);
    }
    return interfaceObj;
  }  // end of createInstanceMSF()



  public static <T> T createInstanceMCF(Class<T> aType, String serviceName)
  /* create an interface object of class aType from the named service;
     uses XComponentContext and 'new' XMultiComponentFactory
     so only a bridge to office is needed
  */
  {
    if ((xcc == null) || (mcFactory == null)) {
      System.out.println("No office connection found");
      return null;
    }

    T interfaceObj = null;
    try {
      Object o = mcFactory.createInstanceWithContext(serviceName, xcc);
           // create service component using the specified component context
      interfaceObj = Lo.qi(aType, o);
           // uses bridge to obtain proxy to remote interface inside service;
           // implements casting across process boundaries
    }
    catch (Exception e) {
      System.out.println("Couldn't create interface for \"" + serviceName + "\": " + e);
    }
    return interfaceObj;
  }  // end of createInstanceMCF()



  public static <T> T createInstanceMCF(Class<T> aType, String serviceName, Object[] args)
  /* create an interface object of class aType from the named service and arguments;
     uses XComponentContext and 'new' XMultiComponentFactory
     so only a bridge to office is needed
  */
  {
    if ((xcc == null) || (mcFactory == null)) {
      System.out.println("No office connection found");
      return null;
    }

    T interfaceObj = null;
    try {
      Object o = mcFactory.createInstanceWithArgumentsAndContext(serviceName, args, xcc);
           // create service component using the specified args and component context
      interfaceObj = Lo.qi(aType, o);
           // uses bridge to obtain proxy to remote interface inside service;
           // implements casting across process boundaries
    }
    catch (Exception e) {
      System.out.println("Couldn't create interface for \"" + serviceName + "\": " + e);
    }
    return interfaceObj;
  }  // end of createInstanceMCF()





  public static <T> T getParent(Object aComponent, Class<T> aType)
  // retrieves the parent of the given object
  {
    XChild xAsChild = Lo.qi(XChild.class, aComponent);
    return Lo.qi(aType, xAsChild.getParent());
  }




  // ======================== start office ==============


  public static XComponentLoader loadOffice()
  {  return loadOffice(true);  }    // default is to using office via pipes


  public static XComponentLoader loadSocketOffice()
  {  return loadOffice(false);  }


  public static XComponentLoader loadOffice(boolean usingPipes)
  /* Creation sequence: remote component content (xcc) -->
                        remote service manager (mcFactory) -->
                        remote desktop (xDesktop) -->
                        component loader (XComponentLoader)
    Once we have a component loader, we can load a document.
    xcc, mcFactory, and xDesktop are stored as static globals.
  */
  {
    System.out.println("Loading Office...");
    if (usingPipes)
      xcc = bootstrapContext(); // connects to office via pipes
    else
      xcc = socketContext();    // connects to office via a socket
    if (xcc == null) {
      System.out.println("Office context could not be created");
      System.exit(1);
    }

    // get the remote office service manager
    mcFactory = xcc.getServiceManager();
    if (mcFactory == null) {
      System.out.println("Office Service Manager is unavailable");
      System.exit(1);
    }

    // desktop service handles application windows and documents
    xDesktop = createInstanceMCF(XDesktop.class, "com.sun.star.frame.Desktop");
    if (xDesktop == null) {
      System.out.println("Could not create a desktop service");
      System.exit(1);
    }

    // XComponentLoader provides ability to load components
    return Lo.qi(XComponentLoader.class, xDesktop);
  }  // end of loadOffice()



  private static XComponentContext bootstrapContext()
  // connect pipes to office using the Bootstrap class
  // i.e. see code at http://svn.apache.org/repos/asf/openoffice/symphony/trunk/main/
  //                    javaunohelper/com/sun/star/comp/helper/Bootstrap.java
  {
    XComponentContext xcc = null;   // the remote office component context
    try {
      xcc = Bootstrap.bootstrap();  //  get remote office component context
        // Connect to office, if office is not running then it's started
    }
    catch (BootstrapException e) {
      System.out.println("Unable to bootstrap Office");
    }
    return xcc;
  }  // end of bootstrapContext()



  private static XComponentContext socketContext()
  // use socket connection to Office
  // https://forum.openoffice.org/en/forum/viewtopic.php?f=44&t=1014
  {
    XComponentContext xcc = null;   // the remote office component context
    try {
      String[] cmdArray = new String[3];
      cmdArray[0] = "soffice";
                // requires soffice to be in Windows PATH env var.
      cmdArray[1] = "-headless";
      cmdArray[2] = "-accept=socket,host=localhost,port=" +
                                               SOCKET_PORT + ";urp;";
      Process p = Runtime.getRuntime().exec(cmdArray);
      if (p != null)
        System.out.println("Office process created");
      delay(5000);
             // Wait 5 seconds, until office is in listening mode

      // Create a local Component Context
      XComponentContext localContext =
                        Bootstrap.createInitialComponentContext(null);

      // Get the local service manager
      XMultiComponentFactory localFactory = localContext.getServiceManager();

      // connect to Office via its socket
/*
      Object urlResolver = localFactory.createInstanceWithContext(
                                  "com.sun.star.bridge.UnoUrlResolver", localContext);
      XUnoUrlResolver xUrlResolver = Lo.qi(XUnoUrlResolver.class, urlResolver);
      Object initObject = xUrlResolver.resolve(
            "uno:socket,host=localhost,port=" + SOCKET_PORT +
                                          ";urp;StarOffice.ServiceManager");
*/
      XConnector connector = Lo.qi(XConnector.class,
              localFactory.createInstanceWithContext(
                          "com.sun.star.connection.Connector", localContext));

      XConnection connection = connector.connect(
                         "socket,host=localhost,port=" + SOCKET_PORT);

      // create a bridge to Office via the socket
      XBridgeFactory bridgeFactory = Lo.qi(XBridgeFactory.class,
                localFactory.createInstanceWithContext(
                         "com.sun.star.bridge.BridgeFactory", localContext));

      // create a nameless bridge with no instance provider
      XBridge bridge = bridgeFactory.createBridge("socketBridgeAD", "urp", connection, null);

      bridgeComponent = Lo.qi(XComponent.class, bridge);

      // get the remote service manager
      XMultiComponentFactory serviceManager = Lo.qi(XMultiComponentFactory.class,
                                     bridge.getInstance("StarOffice.ServiceManager"));

      // retrieve Office's remote component context as a property
      XPropertySet props = Lo.qi(XPropertySet.class, serviceManager);
                                                     // initObject);
      Object defaultContext = props.getPropertyValue("DefaultContext");

      // get the remote interface XComponentContext
      xcc = Lo.qi(XComponentContext.class, defaultContext);
    }
    catch (java.lang.Exception e) {
      System.out.println("Unable to socket connect to Office");
    }

    return xcc;
  }  // end of socketContext()



  // ================== office shutdown =========================


  public static void closeOffice()
  // tell office to terminate
  {
    System.out.println("Closing Office");
    if (xDesktop == null) {
      System.out.println("No office connection found");
      return;
    }

    if(isOfficeTerminated) {
      System.out.println("Office has already been requested to terminate");
      return;
    }

    int numTries = 1;
    while (!isOfficeTerminated && (numTries < 4)) {
      delay(200);
      isOfficeTerminated = tryToTerminate(numTries);
      numTries++;
    }
  }  // end of closeOffice()



  public static boolean tryToTerminate(int numTries)
  {
    try {
      boolean isDead = xDesktop.terminate();
      if (isDead) {
        if (numTries > 1)
          System.out.println(numTries + ". Office terminated");
        else
          System.out.println("Office terminated");
      }
      else
        System.out.println(numTries + ". Office failed to terminate");
      return isDead;
    }
    catch(com.sun.star.lang.DisposedException e)
    {  System.out.println("Office link disposed");
       return true;
    }
    catch(java.lang.Exception e)
    {  System.out.println("Termination exception: " + e);
       return false;
    }
  }  // end of tryToTerminate()



  public static void killOffice()
  // kill office processes using a batch file
  // or use JNAUtils.killOffice()
  {
    try {
    	//this would work if we only implemented windows extnesions
    	//got to find a linux way to kill the associated office document
      // Runtime.getRuntime().exec("cmd /c lokill.bat");

    	JNAUtils.killOffice();
      System.out.println("Killed Office");
    }
    catch (java.lang.Exception e) {
      System.out.println("Unable to kill Office: " + e);
    }
  }  // end of killOffice()



  // ======================== document opening ==============


  public static XComponent openFlatDoc(String fnm, String docType,
                                       XComponentLoader loader)
  { String nm = XML.getFlatFilterName(docType);
    System.out.println("Flat filter Name: " + nm);
    return openDoc(fnm, loader, Props.makeProps("FilterName", nm));
  }


  public static XComponent openDoc(String fnm, XComponentLoader loader)
  {  return openDoc(fnm, loader, Props.makeProps("Hidden", true) );  }


  public static XComponent openReadOnlyDoc(String fnm, XComponentLoader loader)
  {  return openDoc(fnm, loader, Props.makeProps("Hidden", true, "ReadOnly", true) );  }



  public static XComponent openDoc(String fnm, XComponentLoader loader,
                                                           PropertyValue[] props)
  // open the specified document
  // the possibly props for a document are listed in the MediaDescriptor service
  {
    if (fnm == null) {
      System.out.println("Filename is null");
      return null;
    }

    String openFileURL = null;
    if (!FileIO.isOpenable(fnm)) {
      if (isURL(fnm)) {
        System.out.println("Will treat filename as a URL: \"" + fnm + "\"");
        openFileURL = fnm;
      }
      else
        return null;
    }
    else {
      System.out.println("Opening " + fnm);
      openFileURL = FileIO.fnmToURL(fnm);
      if (openFileURL == null)
       return null;
    }


    XComponent doc = null;
    try {
      doc = loader.loadComponentFromURL(openFileURL, "_blank", 0, props);
      msFactory =  Lo.qi(XMultiServiceFactory.class, doc);
    }
    catch (Exception e) {
      System.out.println("Unable to open the document");
    }
    return doc;
  }  // end of openDoc()




  public static boolean isURL(String fnm)
  {
    try {
      java.net.URL u = new java.net.URL(fnm);   // check for the protocol
      u.toURI();                                // check validation of URI
      return true;
    }
    catch (java.net.MalformedURLException e)
    {  return false;  }
    catch (java.net.URISyntaxException e)
    {  return false;  }
  }  // end of isURL()




  // ======================== document creation ==============


  public static String ext2DocType(String ext)
  {
    switch (ext) {
      case "odt": return WRITER_STR;
      case "odp": return IMPRESS_STR;
      case "odg": return DRAW_STR;
      case "ods": return CALC_STR;
      case "odb": return BASE_STR;
      case "odf": return MATH_STR;
      default:
        System.out.println("Do not recognize extension \"" + ext + "\"; using writer");
        return WRITER_STR;    // could use UNKNOWN_STR
    }
  }  // end of ext2DocType()


/* docType (without the ""private:factory/") is:
    "private:factory/swriter"       Writer document
    "private:factory/simpress"      Impress presentation document
    "private:factory/sdraw"         Draw document
    "private:factory/scalc"         Calc document
    "private:factory/sdatabase"     Base document
    "private:factory/smath"         Math formula document

  These are not handled:
    "private:factory/schart"                    Chart
    "private:factory/swriter/web"               Writer HTML Web document
    "private:factory/swriter/GlobalDocument"    Master document

    ".component:Bibliography/View1"       Bibliography-Edit the bibliography entries

    ".component:DB/QueryDesign"           Database comp
    ".component:DB/TableDesign"
    ".component:DB/RelationDesign"
    ".component:DB/DataSourceBrowser"
    ".component:DB/FormGridView"
*/


  public static String docTypeStr(int docTypeVal)
  {
    switch (docTypeVal) {
      case WRITER: return WRITER_STR;
      case IMPRESS: return IMPRESS_STR;
      case DRAW: return DRAW_STR;
      case CALC: return CALC_STR;
      case BASE: return BASE_STR;
      case MATH: return MATH_STR;
      default:
        System.out.println("Do not recognize extension \"" + docTypeVal + "\"; using writer");
        return WRITER_STR;    // could use UNKNOWN_STR
    }
  }  // end of docTypeStr()



  public static XComponent createDoc(String docType, XComponentLoader loader)
  {  return createDoc(docType, loader, Props.makeProps("Hidden", true) );  }


  public static XComponent createMacroDoc(String docType, XComponentLoader loader)
  {  return createDoc(docType, loader, Props.makeProps("Hidden", false,
             //"MacroExecutionMode", MacroExecMode.ALWAYS_EXECUTE) );  }
        "MacroExecutionMode", MacroExecMode.ALWAYS_EXECUTE_NO_WARN) );  }




  public static XComponent createDoc(String docType, XComponentLoader loader,
                                                             PropertyValue[] props)
  // create a new document of the specified type
  {
    System.out.println("Creating Office document " + docType);
    // PropertyValue[] props = Props.makeProps("Hidden", true);
          // if Hidden == true, office will not terminate properly
    XComponent doc = null;
    try {
      doc = loader.loadComponentFromURL("private:factory/"+docType, "_blank", 0, props);
      msFactory =  Lo.qi(XMultiServiceFactory.class, doc);
    }
    catch (Exception e) {
       System.out.println("Could not create a document");
    }
    return doc;
  }  // end of createDoc()



  public static XComponent createDocFromTemplate(String templatePath,
                                                 XComponentLoader loader)
  // create a new document using the specified template
  {
    if (!FileIO.isOpenable(templatePath))
      return null;
    System.out.println("Opening template " + templatePath);
    String templateURL = FileIO.fnmToURL(templatePath);
    if (templateURL == null)
      return null;

    PropertyValue[] props = Props.makeProps("Hidden", true, "AsTemplate", true);
    XComponent doc = null;
    try {
      doc = loader.loadComponentFromURL(templateURL, "_blank", 0, props);
      msFactory =  Lo.qi(XMultiServiceFactory.class, doc);
    }
    catch (Exception e) {
       System.out.println("Could not create document from template: " + e);
    }
    return doc;
  }  // end of createDocFromTemplate()



  // ======================== document saving ==============


  public static void save(Object odoc)
  // was XComponent
  {
    XStorable store = Lo.qi(XStorable.class, odoc);
    try {
      store.store();
      System.out.println("Saved the document by overwriting");
    }
    catch (IOException e) {
       System.out.println("Could not save the document");
    }
  }  // end of save()


  public static void saveDoc(Object odoc, String fnm)
  // was XComponent
  {
    XStorable store = Lo.qi(XStorable.class, odoc);
    XComponent doc = Lo.qi(XComponent.class, odoc);
    int docType = Info.reportDocType(doc);
    storeDoc(store, docType, fnm, null);   // no password
  }


  public static void saveDoc(Object odoc, String fnm, String password)
  // was XComponent
  {
    XStorable store = Lo.qi(XStorable.class, odoc);
    XComponent doc = Lo.qi(XComponent.class, odoc);
    int docType = Info.reportDocType(doc);
    storeDoc(store, docType, fnm, password);
  }


  public static void saveDoc(Object odoc, String fnm, String format, String password)
  // was XComponent
  { XStorable store = Lo.qi(XStorable.class, odoc);
    storeDocFormat(store, fnm, format, password);
  }



  //public static void storeDoc(XStorable store, int docType, String fnm)
  //{  saveDoc(store, docType, fnm, null);  }     // no password


  public static void storeDoc(XStorable store, int docType, String fnm, String password)
  // Save the document using the file's extension as a guide.
  {
    String ext = Info.getExt(fnm);
    String format = "Text";
    if (ext == null)
      System.out.println("Assuming a text format");
    else
      format = ext2Format(docType, ext);
    storeDocFormat(store, fnm, format, password);
  }  // end of storeDoc()



  public static String ext2Format(String ext)
  {  return ext2Format(Lo.UNKNOWN, ext);  }


  public static String ext2Format(int docType, String ext)
  /* convert the extension string into a suitable office format string.
     The formats were chosen based on the fact that they
     are being used to save (or export) a document.

     The names were obtained from
     http://www.oooforum.org/forum/viewtopic.phtml?t=71294
     and by running my DocInfo application on files.

     I use the docType to distinguish between the various meanings of the PDF ext.

     This could be a lot more extensive.

     Use Info.getFilterNames() to get the filter names for your Office
     (the last time I tried it, I got back 246 names!)
  */
  {
    switch (ext) {
      case "doc": return "MS Word 97";
      case "docx": return "Office Open XML Text";   // "MS Word 2007 XML"
      case "rtf":
        if (docType == Lo.CALC)
          return "Rich Text Format (StarCalc)";
        else
          return "Rich Text Format";   // assume writer

      case "odt": return "writer8";
      case "ott": return "writer8_template";

      case "pdf":
        if (docType == Lo.WRITER)
          return "writer_pdf_Export";
        else if (docType == Lo.IMPRESS)
          return "impress_pdf_Export";
        else if (docType == Lo.DRAW)
          return "draw_pdf_Export";
        else if (docType == Lo.CALC)
          return "calc_pdf_Export";
        else if (docType == Lo.MATH)
          return "math_pdf_Export";
        else
          return "writer_pdf_Export";    // assume we are saving a writer doc

      case "txt": return "Text";

      case "ppt": return "MS PowerPoint 97";
      case "pptx": return "Impress MS PowerPoint 2007 XML";
      case "odp": return "impress8";
      case "odg": return "draw8";

      case "jpg":
        if (docType == Lo.IMPRESS)
           return "impress_jpg_Export";
        else
          return "draw_jpg_Export";    // assume Draw doc

      case "png":
        if (docType == Lo.IMPRESS)
           return "impress_png_Export";
        else
          return "draw_png_Export";    // assume Draw doc

      case "xls": return "MS Excel 97";
      case "xlsx": return "Calc MS Excel 2007 XML";
      case "csv": return "Text - txt - csv (StarCalc)";   // "Text CSV";
      case "ods": return "calc8";
      case "odb": return "StarOffice XML (Base)";

      case "htm":
      case "html":
        if (docType == Lo.WRITER)
          return "HTML (StarWriter)";  // "writerglobal8_HTML";
        else if (docType == Lo.IMPRESS)
          return "impress_html_Export";
        else if (docType == Lo.DRAW)
          return "draw_html_Export";
        else if (docType == Lo.CALC)
           return "HTML (StarCalc)";
        else
          return "HTML";

      case "xhtml":
        if (docType == Lo.WRITER)
          return "XHTML Writer File";
        else if (docType == Lo.IMPRESS)
          return "XHTML Impress File";
        else if (docType == Lo.DRAW)
          return "XHTML Draw File";
        else if (docType == Lo.CALC)
          return "XHTML Calc File";
        else
          return "XHTML Writer File";    // assume we are saving a writer doc

      case "xml":
        if (docType == Lo.WRITER)
          return "OpenDocument Text Flat XML";
        else if (docType == Lo.IMPRESS)
          return "OpenDocument Presentation Flat XML";
        else if (docType == Lo.DRAW)
          return "OpenDocument Drawing Flat XML";
        else if (docType == Lo.CALC)
          return "OpenDocument Spreadsheet Flat XML";
        else
          return "OpenDocument Text Flat XML";    // assume we are saving a writer doc


      default:   // assume user means text
        System.out.println("Do not recognize extension \"" + ext + "\"; using text");
        return "Text";
    }
  }  // end of ext2Format()




  public static void storeDocFormat(XStorable store, String fnm, String format, String password)
  // save the document in the specified file using the supplied office format
  {
    System.out.println("Saving the document in " + fnm);
    System.out.println("Using format: " + format);
    try {
      String saveFileURL = FileIO.fnmToURL(fnm);
      if (saveFileURL == null)
        return;

      PropertyValue[] storeProps;
      if (password == null)  // no password supplied
        storeProps = Props.makeProps("Overwrite", true, "FilterName", format);
      else {
        String[] nms = new String[] {"Overwrite", "FilterName", "Password"};
        Object[] vals = new Object[] { true, format, password};
        storeProps = Props.makeProps(nms, vals);
      }
      store.storeToURL(saveFileURL, storeProps);
    }
    catch (IOException e) {
       System.out.println("Could not save " + fnm + ": " + e);
    }
  } // end of storeDocFormat()



  // ======================== document closing ==============


  public static void closeDoc(Object doc)
  // was XComponent
  {
    try {
      XCloseable closeable = Lo.qi(XCloseable.class, doc);
      close(closeable);
    }
    catch (com.sun.star.lang.DisposedException e) {
       System.out.println("Document close failed since Office link disposed");
    }
  }


  public static void close(XCloseable closeable)
  {
    if (closeable == null)
      return;
    System.out.println("Closing the document");
    try {
      closeable.close(false);   // true to force a close
      // set modifiable to false to close a modified doc without complaint setModified(False)
    }
    catch (CloseVetoException e) {
       System.out.println("Close was vetoed");
    }
  }  // end of close()



  // ================= initialization via Addon-supplied context ====================


  public static XComponent addonInitialize(XComponentContext addonXcc)
  {
    xcc = addonXcc;
    if (xcc == null)  {
      System.out.println("Could not access component context");
      return null;
    }

    mcFactory = xcc.getServiceManager();
    if (mcFactory == null) {
      System.out.println("Office Service Manager is unavailable");
      return null;
    }

    try {
      Object oDesktop = mcFactory.createInstanceWithContext(
                                       "com.sun.star.frame.Desktop", xcc);
      xDesktop = Lo.qi(XDesktop.class, oDesktop);
    }
    catch (Exception e) {
      System.out.println("Could not access desktop");
      return null;
    }

    XComponent doc = xDesktop.getCurrentComponent();
    if (doc == null)  {
      System.out.println("Could not access document");
      return null;
    }

    msFactory =  Lo.qi(XMultiServiceFactory.class, doc);
    return doc;
  }  // end of addonInitialize()



  // ============= initialization via script context ======================


  public static XComponent scriptInitialize(XScriptContext sc)
  {
    if (sc == null) {
      System.out.println("Script Context is null");
      return null;
    }

    xcc = sc.getComponentContext();
    if (xcc == null)  {
      System.out.println("Could not access component context");
      return null;
    }
    mcFactory = xcc.getServiceManager();
    if (mcFactory == null) {
      System.out.println("Office Service Manager is unavailable");
      return null;
    }

    xDesktop = sc.getDesktop();
    if (xDesktop == null)  {
      System.out.println("Could not access desktop");
      return null;
    }

    XComponent doc = xDesktop.getCurrentComponent();
    if (doc == null)  {
      System.out.println("Could not access document");
      return null;
    }

    msFactory =  Lo.qi(XMultiServiceFactory.class, doc);
    return doc;
  }  // end of scriptInitialize()




  // ==================== dispatch ===============================
  // see https://wiki.documentfoundation.org/Development/DispatchCommands


  public static boolean dispatchCmd(String cmd)
  {  return dispatchCmd(xDesktop.getCurrentFrame(), cmd, null);   }


  public static boolean dispatchCmd(String cmd, PropertyValue[] props)
  {  return dispatchCmd(xDesktop.getCurrentFrame(), cmd, props);   }


  public static boolean dispatchCmd(XFrame frame, String cmd, PropertyValue[] props)
  // cmd does not include the ".uno:" substring; e.g. pass "Zoom" not ".uno:Zoom"
  {
    XDispatchHelper helper =
         createInstanceMCF(XDispatchHelper.class, "com.sun.star.frame.DispatchHelper");
    if (helper == null) {
      System.out.println("Could not create dispatch helper for command " + cmd);
      return false;
    }

    try {
      XDispatchProvider provider = Lo.qi(XDispatchProvider.class, frame);

      /* returns failure even when the event works (?), and an illegal value
         when the dispatch actually does fail */
      /*
      DispatchResultEvent res =  (DispatchResultEvent)
                  helper.executeDispatch(provider, (".uno:" + cmd), "", 0, props);
      if (res.State == DispatchResultState.FAILURE)
        System.out.println("Dispatch failed for \"" + cmd + "\"");
      else if (res.State == DispatchResultState.DONTKNOW)
        System.out.println("Dispatch result unknown for \"" + cmd + "\"");
      */
      helper.executeDispatch(provider, (".uno:" + cmd), "", 0, props);
      return true;
    }
    catch(java.lang.Exception e)
    {  System.out.println("Could not dispatch \"" + cmd + "\":\n  " + e); }
    return false;
  }  // end of dispatchCmd()



  // ================= Uno cmds =========================


  public static String makeUnoCmd(String itemName)
  // use a dummy Java class name, Foo
  {  return "vnd.sun.star.script:Foo/Foo." + itemName +
                           "?language=Java&location=share";  }



  public static String extractItemName(String unoCmd)
  /* format is:
       "vnd.sun.star.script:Foo/Foo." + itemName +
                                  "?language=Java&location=share";
  */
  {
    int fooPos = unoCmd.indexOf("Foo.");
    if (fooPos == -1) {
      System.out.println("Could not find Foo header in command: \"" + unoCmd + "\"");
      return null;
    }

    int langPos = unoCmd.indexOf("?language");
    if (langPos == -1) {
      System.out.println("Could not find language header in command: \"" + unoCmd + "\"");
      return null;
    }

    return unoCmd.substring(fooPos+4, langPos);
  }  // end of extractItemName()




  // ======================== use Inspector extensions ====================


  public static void inspect(Object obj)
  /* call XInspector.inspect() in the Inspector.oxt extension
     Available from https://wiki.openoffice.org/wiki/Object_Inspector
  */
  {
    if ((xcc == null) || (mcFactory == null)) {
      System.out.println("No office connection found");
      return;
    }

    try {
      Type[] ts = Info.getInterfaceTypes(obj);   // get class name for title
      String title = "Object";
      if ((ts != null) && (ts.length > 0))
        title = ts[0].getTypeName() + " " + title;

      Object inspector = mcFactory.createInstanceWithContext(
                                  "org.openoffice.InstanceInspector", xcc);
               // hangs on second use
      if (inspector == null) {
        System.out.println("Inspector Service could not be instantiated");
        return;
      }

      System.out.println("Inspector Service instantiated");
/*
      // report on inspector
      XServiceInfo si = Lo.qi(XServiceInfo.class, inspector);
      System.out.println("Implementation name: " + si.getImplementationName());
      String[] serviceNames = si.getSupportedServiceNames();
      for(String nm : serviceNames)
         System.out.println("Service name: " + nm);
*/
      XIntrospection intro = createInstanceMCF(XIntrospection.class,
                                               "com.sun.star.beans.Introspection");
      XIntrospectionAccess introAcc = intro.inspect(inspector);
      XIdlMethod method = introAcc.getMethod("inspect", -1);   // get ref to XInspector.inspect()
/*
      // alternative, low-level way of getting the method
      Object coreReflect = mcFactory.createInstanceWithContext(
                                     "com.sun.star.reflection.CoreReflection", xcc);
      XIdlReflection idlReflect = Lo.qi(XIdlReflection.class, coreReflect);
      XIdlClass idlClass = idlReflect.forName("org.openoffice.XInstanceInspector");
      XIdlMethod[] methods = idlClass.getMethods();
      System.out.println("No of methods: " + methods.length);
      for(XIdlMethod m : methods)
         System.out.println("  " + m.getName());

      XIdlMethod method = idlClass.getMethod("inspect");
*/
      System.out.println("inspect() method was found: " + (method != null));

      Object[][] params =  new Object[][]{new Object[]{obj, title}};
      method.invoke(inspector, params);
    }
    catch(Exception e)
    { System.out.println("Could not access Inspector: " + e); }
  }  // end of accessInspector()





  public static void mriInspect(Object obj)
  /* call MRI's inspect()
     Available from http://extensions.libreoffice.org/extension-center/mri-uno-object-inspection-tool
                  or http://extensions.services.openoffice.org/en/project/MRI
     Docs: https://github.com/hanya/MRI/wiki
     Forum tutorial: https://forum.openoffice.org/en/forum/viewtopic.php?f=74&t=49294
  */
  {
    XIntrospection xi = createInstanceMCF(XIntrospection.class, "mytools.Mri");
    if (xi == null) {
      System.out.println("MRI Inspector Service could not be instantiated");
      return;
    }

    System.out.println("MRI Inspector Service instantiated");
    xi.inspect(obj);
  }  // end of mriInspect()




  // ------------------ color methods ---------------------


  public static int getColorInt(java.awt.Color color)
  // return the color as an integer, ignoring the alpha channel
  {
    if (color == null) {
      System.out.println("No color supplied");
      return 0;
    }
    else
      return (color.getRGB() & 0xffffff);
  } // end of getColorInt()



  public static int hexString2ColorInt(String colStr)
  // e.g. "#FF0000", "0xFF0000"
  {
    java.awt.Color color = java.awt.Color.decode(colStr);
    return getColorInt(color);
  }


  public static String getColorHexString(java.awt.Color color)
  {
    if (color == null) {
      System.out.println("No color supplied");
      return "#000000";
    }
    else
      return int2HexString(color.getRGB() & 0xffffff);
  }  // end of getColorHexString()



  public static String int2HexString(int val)
  {
    String hex = Integer.toHexString(val);
    if (hex.length() < 6)
      hex = "000000".substring(0, 6 - hex.length()) + hex;
    return "#" + hex;
  }  // end of int2HexString()



  // ================== other utils =============================


  public static void wait(int ms)    // I can never remember the name :)
  {  delay(ms);  }


  public static void delay(int ms)
  { try {
      Thread.sleep(ms);
    }
    catch(InterruptedException e){}
  }


  public static boolean isNullOrEmpty(String s)
  {  return ((s == null) || (s.length() == 0));  }


  public static void waitEnter()
  {
    System.out.println("Press Enter to continue...");
    try {
      System.in.read();
    }
    catch(java.io.IOException e){}
  }  // end of waitEnter()



  public static String getTimeStamp()
  { java.text.SimpleDateFormat sdf = new java.text.SimpleDateFormat("yyyy-MM-dd HH:mm:ss");
    return sdf.format(new java.util.Date());
  }



  public static void printNames(String[] names)
  {  printNames(names, 4);  }


  public static void printNames(String[] names, int numPerLine)
  // print a large array with <numPerLine> strings/line, indented by 2 spaces
  {
    if (names == null)
      System.out.println("  No names found");
    else {
      Arrays.sort(names, String.CASE_INSENSITIVE_ORDER);
      int nlCounter = 0;
      System.out.println("No. of names: " + names.length);
      for (String name : names) {
        System.out.print("  \"" + name + "\"");
        nlCounter++;
        if (nlCounter % numPerLine == 0) {
          System.out.println();
          nlCounter = 0;
        }
      }
      System.out.println("\n\n");
    }
  }  // end of printNames()



  public static void printTable(String name, Object[][] table)
  {
    System.out.println("-- " + name + " ----------------");
    for (int i=0; i < table.length; i++) {
      for(int j=0; j < table[i].length; j++)
        System.out.print("  " + table[i][j]);
      System.out.println();
    }
    System.out.println("-----------------------------\n");
  } // end of printTable()


  public static String capitalize(String s)
  {
    if ((s == null) || (s.length() == 0))
      return null;
    else if (s.length() == 1)
      return s.toUpperCase();
    else
      return Character.toUpperCase(s.charAt(0)) + s.substring(1);
  }  // end of capitalize()


  public static int parseInt(String s)
  {
    if (s == null)
      return 0;
    try {
      return Integer.parseInt(s);
    }
    catch (NumberFormatException ex){
      System.out.println(s + " could not be parsed as an int; using 0");
      return 0;
    }
  }  // end of parseInt()


  public static void addJar(String jarPath)
  // load this JAR into the classloader at run time
  // from http://stackoverflow.com/questions/60764/how-should-i-load-jars-dynamically-at-runtime
  {
    try {
      URLClassLoader classLoader =
                  (URLClassLoader)ClassLoader.getSystemClassLoader();
      java.lang.reflect.Method m =
            URLClassLoader.class.getDeclaredMethod("addURL", java.net.URL.class);
      m.setAccessible(true);
      m.invoke(classLoader, new java.net.URL(jarPath));
    }
    catch(java.lang.Exception e)
    {  System.out.println(e);  }
  }  // end of addJar()



  // ------------------- container manipulation --------------------



  public static String[] getContainerNames(XIndexAccess con)
  // extract the names of the elements in the indexed container
  {
    if (con == null) {
      System.out.println("Container is null");
      return null;
    }

    int numElems = con.getCount();
    if (numElems == 0) {
      System.out.println("No elements in the container");
      return null;
    }

    ArrayList<String> namesList = new ArrayList<String>();
    for (int i=0; i < numElems; i++) {
      try {
        XNamed named = Lo.qi(XNamed.class, con.getByIndex(i));
        namesList.add(named.getName());
      }
      catch(Exception e)
      {  System.out.println("Could not access name of element " + i);  }
    }

    int sz = namesList.size();
    if (sz == 0) {
      System.out.println("No element names found in the container");
      return null;
    }

    String[] names = new String[sz];
    for (int i=0; i < sz; i++)
      names[i] = namesList.get(i);

    return names;
  }  // end of getContainerNames()





  public static XPropertySet findContainerProps(XIndexAccess con, String nm)
  {
    if (con == null) {
      System.out.println("Container is null");
      return null;
    }

    for (int i=0; i < con.getCount(); i++) {
      try {
        Object oElem = con.getByIndex(i);
        XNamed named = Lo.qi(XNamed.class, oElem);
        if (named.getName().equals(nm)) {
          return (XPropertySet) Lo.qi(XPropertySet.class, oElem);
        }
      }
      catch(Exception e)
      {  System.out.println("Could not access element " + i);  }
    }

    System.out.println("Could not find a \"" + nm + "\" property set in the container");
    return null;
  }  // end of findContainerProps()




}  // end of Lo class

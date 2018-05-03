
// Props.java
// Andrew Davison, ad@fivedots.coe.psu.ac.th, March 2015

/* A growing collection of utility functions to make Office
   easier to use. They are currently divided into the following
   groups:
     - make/get/set properties in an array
     - set property in an existing array
     - set property in XPropertySet
     - get property value from XPropertySet
     - show properties array
     - show properties of an Object
*/
package org.libreoffice.librelaw.helper;

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


public class Props
{

  // -------------- make/get/set properties in an array --------------------


  public static PropertyValue[] makeBarItem(String cmd, String itemName)
  // propertiees for a toolbar item using a name and an image
  // problem: image does not appear next to text on toolbar
  {
    PropertyValue[] props = new PropertyValue[5];

    props[0] = new PropertyValue();
    props[0].Name = "CommandURL";
    props[0].Value = cmd;

    props[1] = new PropertyValue();
    props[1].Name = "Label";
    props[1].Value = itemName;

    props[2] = new PropertyValue();
    props[2].Name = "Type";
    props[2].Value = ItemType.DEFAULT;  // 0;

    props[3] = new PropertyValue();
    props[3].Name = "Visible";
    props[3].Value = true;

    props[4] = new PropertyValue();
    props[4].Name = "Style";
    props[4].Value = ItemStyle.DRAW_FLAT + ItemStyle.ALIGN_LEFT +
                     ItemStyle.AUTO_SIZE + ItemStyle.ICON  +
                     ItemStyle.TEXT;

    return props;
  }  // end of makeProps()




  public static PropertyValue[] makeProps(String oName, Object oValue)
  {
    PropertyValue[] props = new PropertyValue[1];
    props[0] = new PropertyValue();
    props[0].Name = oName;
    props[0].Value = oValue;
    return props;
  }  // end of makeProps()



  public static PropertyValue[] makeProps(String oName1, Object oValue1,
                                          String oName2, Object oValue2)
  { PropertyValue[] props = new PropertyValue[2];
    props[0] = new PropertyValue();
    props[0].Name = oName1;
    props[0].Value = oValue1;

    props[1] = new PropertyValue();
    props[1].Name = oName2;
    props[1].Value = oValue2;
    return props;
  }  // end of makeProps()


  public static PropertyValue[] makeProps(String oName1, Object oValue1,
                                          String oName2, Object oValue2,
                                          String oName3, Object oValue3)
  { PropertyValue[] props = new PropertyValue[3];
    props[0] = new PropertyValue();
    props[0].Name = oName1;
    props[0].Value = oValue1;

    props[1] = new PropertyValue();
    props[1].Name = oName2;
    props[1].Value = oValue2;

    props[2] = new PropertyValue();
    props[2].Name = oName3;
    props[2].Value = oValue3;
    return props;
  }  // end of makeProps()



  public static PropertyValue[] makeProps(String[] nms, Object[] vals)
  {
    if (nms.length != vals.length) {
      System.out.println("Mismatch in lengths of names and values");
      return null;
    }

    int numElems = nms.length;
    PropertyValue[] props = new PropertyValue[numElems];
    for (int i=0; i < numElems; i++) {
      props[i] = new PropertyValue();
      props[i].Name = nms[i];
      props[i].Value = vals[i];
    }
    return props;
  }  // end of makeProps()



  public static void setProp(PropertyValue[] props, String propName, Object value)
  {
    if (props == null) {
      System.out.println("Property array is null; cannot set " + propName);
      return;
    }
    for (PropertyValue prop : props) {
      if (prop.Name.equals(propName)) {
        // System.out.println("Changing " + propName + " to " + value);
        prop.Value = value;
        return;
      }
    }
    System.out.println(propName + " not found");
  }  // end of setProp()



  public static Object getProp(PropertyValue[] props, String propName)
  {
    if (props == null) {
      System.out.println("Property array is null; cannot get " + propName);
      return null;
    }
    for (PropertyValue prop : props) {
      if (prop.Name.equals(propName))
        return prop.Value;
    }
    System.out.println(propName + " not found");
    return null;
  }  // end of getProp()



  // ---------------------- set property in XPropertySet ----------------------

  public static void setProperty(Object obj, String propName, Object value)
  { XPropertySet propSet = Lo.qi(XPropertySet.class, obj);
    setProperty(propSet, propName, value);
  }


  public static void setProperty(XPropertySet propSet, String propName, Object value)
  {
    if (propSet == null) {
      System.out.println("Property set is null; cannot set \"" + propName + "\"");
      return;
    }
    try {
      propSet.setPropertyValue(propName, value);
    }
    catch(com.sun.star.lang.IllegalArgumentException e)
    {  System.out.println("Property \"" + propName + "\" argument is illegal");  }
    catch(Exception e)
    {  System.out.println("Could not set property \"" + propName + "\": " + e);  }
  }  // end of setProperty()



  public static void setProperties(Object obj, String[] nms, Object[] vals)
  { XPropertySet propSet = Lo.qi(XPropertySet.class, obj);
    setProperties(propSet, nms, vals);
  }


  public static void setProperties(XPropertySet propSet, String[] nms, Object[] vals)
  {
    if (propSet == null) {
      System.out.println("Property set is null; cannot set properties");
      return;
    }
    for (int i=0; i < nms.length; i++) {
      try {
        propSet.setPropertyValue(nms[i], vals[i]);
      }
      catch(com.sun.star.beans.PropertyVetoException e)
      {  System.out.println("Could not set read-only property \"" +
                                                        nms[i] + "\": " + e);  }
      catch(Exception e)
      {  System.out.println("Could not set property \"" + nms[i] + "\": " + e);  }
    }
  }  // end of setProperties()



  public static void setProperties(Object obj, Object fromObj)
  {
    XPropertySet propSet = Lo.qi(XPropertySet.class, obj);
    XPropertySet fromProps = Lo.qi(XPropertySet.class, fromObj);
    setProperties(propSet, fromProps);
  }


  public static void setProperties(XPropertySet propSet, XPropertySet fromProps)
  {
    if (propSet == null) {
      System.out.println("Property set is null; cannot set properties");
      return;
    }
    if (fromProps == null) {
      System.out.println("Source property set is null; cannot set properties");
      return;
    }

    String[] nms = getPropNames(fromProps);
    for (int i=0; i < nms.length; i++) {
      try {
        propSet.setPropertyValue(nms[i], getProperty(fromProps, nms[i]));
      }
      catch(Exception e)
      {  System.out.println("Could not set property \"" + nms[i] + "\": " + e);  }
    }
  }  // end of setProperties()


  // ----------- get property value from XPropertySet -----------------


  public static Object getProperty(Object obj, String propName)
  { XPropertySet propSet =  Lo.qi(XPropertySet.class, obj);
    return getProperty(propSet, propName);
  }



  public static Object getProperty(XPropertySet xProps, String propName)
  {
    Object value = null;
    try {
      value = xProps.getPropertyValue(propName);
    }
    catch (Exception e) {
      System.out.println("Could not get property " + propName);
    }
    catch (com.sun.star.uno.RuntimeException e) {
      System.out.println("Could not get runtime property " + propName);
    }
    return value;
  }  // end of getProperty()




  public static Property[] getProperties(Object obj)
  {
    XPropertySet propSet = Lo.qi(XPropertySet.class, obj);
    if (propSet == null)
      return null;

    Property[] props = propSet.getPropertySetInfo().getProperties();
    Arrays.sort(props,  new Comparator<Property>() {
      public int compare(Property p1, Property p2)
      {  return (p1.Name).compareTo(p2.Name); }
    });
    return props;
  }  // end of getProperties()




  public static String[] getPropNames(Object obj)
  {
    XPropertySet propSet = Lo.qi(XPropertySet.class, obj);
    if (propSet == null)
      return null;

    Property[] props = propSet.getPropertySetInfo().getProperties();
    String[] nms = new String[props.length];
    for (int i=0; i < props.length; i++)
       nms[i] = props[i].Name;
    return nms;
  }  // end of getProperties()




  public static boolean hasProperty(Object obj, String propName)
  {
    XPropertySet propSet = Lo.qi(XPropertySet.class, obj);
    return propSet.getPropertySetInfo().hasPropertyByName(propName);
  }  // end of hasProperty()



  public static Object getValue(String propName, PropertyValue[] props)
  {
    for (PropertyValue prop : props) {
      if (prop.Name.equals(propName))
        return prop.Value;
    }
    System.out.println(propName + " not found");
    return null;
  }  // end of getValue()




  // ------------------ show properties array ------------------------------


  public static void showIndexedProps(String title, Object obj)
  /* Try to convert object to an indexed container, with each element
     containing a properties array. Show all the data.
  */
  {
    System.out.println("Indexed Properties for \"" + title + "\":");

    XIndexAccess inAcc = Lo.qi(XIndexAccess.class, obj);
    if (inAcc == null) {
      System.out.println("Could not convert object to an IndexAccess container");
      return;
    }

    int numElems = inAcc.getCount();
    System.out.println("No. of elements: " + numElems);
    for(int i=0; i < numElems; i++) {
      try {
        PropertyValue[] props = Lo.qi(PropertyValue[].class, inAcc.getByIndex(i));
        Props.showProps("Elem " + i, props);
        System.out.println("----");
      }
      catch(Exception e)
      {  System.out.println("Could not get elem " + i + ": " + e);  }
    }
  }  // end of showIndexedProps()



  public static void showProps(String title, PropertyValue[] props)
  /* print out the properties as name = value pairs, one per line.
     If the value is a string array or a PropertyValue array, then cycle
     through the values in the array.
  */
  {
    System.out.println("Properties for \"" + title + "\":");
    if (props == null)
      System.out.println("  none found");
    else {
      for (PropertyValue prop : props)
        System.out.println("  " + prop.Name + ": " + propValueToString(prop.Value));
      System.out.println();
    }
  }  // end of showProps()



  public static String propValueToString(Object val)
  {
    if (val == null)
      return null;

    if (val instanceof String[])
      return Arrays.toString((String[])val);
    else if (val instanceof PropertyValue[]) {
      PropertyValue[] ps = (PropertyValue[])val;
      StringBuilder sb = new StringBuilder("[");
      for (PropertyValue p : ps)
        sb.append("    " + p.Name + " = " + p.Value);
      sb.append("  ]");
      return sb.toString();
    }
    else
      return val.toString();
  }  // end of propValueToString()




  public static void showValue(String propName, PropertyValue[] props)
  {
    for (PropertyValue prop : props) {
      if (prop.Name.equals(propName)) {
        System.out.println(prop.Name + ": " + propValueToString(prop.Value));
        return;
      }
    }
    System.out.println(propName + " not found");
  }  // end of showValue()




  // ------------------- show properties of an Object ----------------


  public static void showObjProps(String propKind, Object obj)
  {
    XPropertySet propSet = Lo.qi(XPropertySet.class, obj);
    if (propSet == null)
      System.out.println("No properties found for " + propKind);
    else
      showProps(propKind, propSet);
  }  // end of showObjProps()



  public static void showProps(String propKind, XPropertySet propsSet)
  {
    Property[] props = Props.propsSetToArray(propsSet);
    if (props == null)
      System.out.println("No " + propKind + " properties found");
    else {
      // sort the properties into alphabetical order by name
      Arrays.sort(props, new Comparator<Property>() {
        public int compare(Property p1, Property p2)
        {  return (p1.Name).compareTo(p2.Name);  }
      });

      System.out.println(propKind + " Properties");
      for (Property prop : props) {
        Object propValue = Props.getProperty(propsSet, prop.Name);
        System.out.println("  " + prop.Name + // ": " + prop.Type +
                                              " == " + propValue);
      }
      System.out.println();
    }
  }  // end of showProps()




  public static Property[] propsSetToArray(XPropertySet xProps)
  // convert property set to an array
  {
    if (xProps == null)
      return null;
    else {
      // get the property info interface of this XPropertySet
      XPropertySetInfo xPropsInfo = xProps.getPropertySetInfo();

      // get all properties (NOT the values) from XPropertySetInfo
      return xPropsInfo.getProperties();
    }
  }  // end of propsSetToArray()



  public static String showProperty(Property p)
  {  return p.Name + ": " + p.Type.getTypeName();  }



  // --------------------------- others ------------------------------


  public static void showDocTypeProps(String type)
  // show the properties associated with the file type name
  {
    if (type == null) {
      System.out.println("type is null");
      return;
    }

    XTypeDetection xTypeDetect =
         Lo.createInstanceMCF(XTypeDetection.class, "com.sun.star.document.TypeDetection");
    if (xTypeDetect == null) {
      System.out.println("No type detector reference");
      return;
    }

    XNameAccess xNameAccess = Lo.qi(XNameAccess.class, xTypeDetect);
    try {
      PropertyValue[] props = (PropertyValue[]) xNameAccess.getByName(type);
      showProps(type, props);
    }
    catch(Exception e)
    {  System.out.println("No properties for \"" + type + "\"");  }
  }  // end of showDocTypeProps()





  public static String[] getBoundProps(XMultiPropertySet propsSet)
  {
    Property[] props = propsSet.getPropertySetInfo().getProperties();

    ArrayList<String> names = new ArrayList<String>();
    for (Property p : props) {
      String name = p.Name;
      boolean isWritable = ((p.Attributes & PropertyAttribute.READONLY) == 0);
      boolean isNotNull = ((p.Attributes & PropertyAttribute.MAYBEVOID) == 0);
      boolean isBound = ((p.Attributes & PropertyAttribute.BOUND) != 0);
      if (isWritable && isNotNull && isBound)
        names.add(name);
    }

    if (names.size() == 0) {
      System.out.println("No suitable properties were found");
      return null;
    }
    else
      System.out.println("No. of suitable properties:" + names.size());

    String[] propNames = new String[names.size()];
    names.toArray(propNames);
    return propNames;
  }  // end of getBoundProps()


}  // end of Props class

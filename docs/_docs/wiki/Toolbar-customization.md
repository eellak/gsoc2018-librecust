---
title: Toolbar customization
permalink: /docs/Toolbar-customization/
---

## What is a toolbar
![toolbar_libre](https://i.imgur.com/5r5MZEE.png)
With the term toolbar we refer to the menu located on top of the main editor view, right under the [menubar](https://github.com/eellak/gsoc2018-librecust/wiki/Menubar-customization). Toolbars consist of specific menu elements including buttons and dropdown menus as shown above.

## The LibreOffice toolbar implementation
LibreOffice implements toolbars in a flexible form. More than one of them can be visible at the same window. They can span in full width vertically and horizontally being in docked or floating state. Users can move and rearrange toolbars using drag and drop events. Depending on the LibreOffice version, there are predefined toolbars with their configuration defined, once again, in .xml files located at the installation directory.

## Customizing toolbars
It is highly recommended to avoid fiddling with installation default configuration files, so the same customization mechanism as with the menubars is followed. A [User Profile](https://wiki.documentfoundation.org/UserProfile) directory holds the configuration files for each customized toolbar. These `.xml` files are located at the following path:
```bash
/home/<username>/.config/libreoffice/4/user/config/soffice.cfg/modules/swriter/toolbar
```
In this folder, every different `.xml` file represents toolbars that differ somehow from the predefined ones at the installation directory. 

Surely one can directly edit those xml files, however a more stable and recommended tactic is the use of the LO included customization tool located at Tools->Customize... 

![toolbar_cust_menu](https://i.imgur.com/DNsLY3i.png)

More info on Customize dialog on the TDF [wiki](https://wiki.documentfoundation.org/images/7/7f/0114GS34-CustomizingLibO.odt)
Using this tool, one can either edit predefined toolbars or create new ones. Either case is followed by the creation of a new `.xml` file in the User Profile directory. The former creates a `.xml` with the same name as the one in the installation directory, ovverriding default configuration while the latter creates a new file named `custom_toolbar_*.xml`. Each of these files have the following format:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE toolbar:toolbar PUBLIC "-//OpenOffice.org//DTD OfficeDocument 1.0//EN" "toolbar.dtd">
<toolbar:toolbar xmlns:toolbar="http://openoffice.org/2001/toolbar" xmlns:xlink="http://www.w3.org/1999/xlink" toolbar:uiname="testing">
 <!-- Toolbar items here. Examples: -->
 <toolbar:toolbaritem xlink:href=".uno:*"/>
 <toolbar:toolbarseparator/>
 <!-- More toolbar items here -->
</toolbar:toolbar>
```
New toolbars include the `toolbar:uiname` attribute at the `toolbar:toolbar` tag. All toolbars are enabled through View->Toolbars menubar option.
Regarding functionality, toolbars consist of shortcuts to implemented functions ([Dispatch commands](https://wiki.documentfoundation.org/Development/DispatchCommands)), or macro functions, similarly to menubar structure.

## Defining toolbars through addons
Every extension that implements a GUI part, i.e. an Addon, includes a file named `Addons.xcu`.This is the configuration file for every graphic, being a menubar or toolbar, element that will be added following the extension installation. Toolbar addons are defined using this tag:

```xml
<node oor:name="Images">
  <node oor:name="org.libreoffice.librelaw.LibreLaw.imageActionOne" oor:op="replace">
      <prop oor:name="URL" oor:type="xs:string">
	<value>service:org.libreoffice.librelaw.LibreLaw?openTemplate</value>
      </prop>

    <node oor:name="UserDefinedImages">
      <prop oor:name="ImageSmallURL">
	<value>vnd.sun.star.extension://org.libreoffice.librelaw.librelaw/images/actionOne_16.png</value>
      </prop>
      <prop oor:name="ImageBigURL">
	<value>vnd.sun.star.extension://org.libreoffice.librelaw.librelaw/images/actionOne_26.png</value>
      </prop>
    </node>
  </node>
</node>

<node oor:name="OfficeToolBar">
  <node oor:name="org.libreoffice.librelaw.LibreLaw.toolbar" oor:op="replace">
    <node oor:name="t02" oor:op="replace">
      <prop oor:name="URL" oor:type="xs:string">
	<value>service:org.libreoffice.librelaw.LibreLaw?openTemplate</value>
      </prop>
      <prop oor:name="Target" oor:type="xs:string">
	<value>_self</value>
      </prop>
      <prop oor:name="Context" oor:type="xs:string">
	<value>com.sun.star.text.TextDocument</value>
      </prop>
      <prop oor:name="Title" oor:type="xs:string">
	<value xml:lang="en">Law Templates</value>
	<value xml:lang="el">Υποδείγματα</value>
      </prop>
    </node>
  </node>
</node>
```
The images section defines the icons used for each of the toolbar items while the OfficeToolBar include definitions of these items. More information about Addon development as well as a walkthrough example are included in Chapter 46 of [Java LibreOffice Programming](http://fivedots.coe.psu.ac.th/~ad/jlop/) by Andrew Davison.  

### Attention
While most of the properties regarding the content of toolbar instances is configured using the above procedure, settings regarding design properties of the editor itself such as icon size or icon theme are set through registry sentries at the registrymodifications.xcu file or through extensions as described in the [Configuration extension](https://github.com/eellak/gsoc2018-librecust/wiki/Configuration-extension) wiki page.
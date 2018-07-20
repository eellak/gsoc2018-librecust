# Menubar customization

### What is a menubar
![menubar](https://i.imgur.com/GGMgWPA.png)

One of the most useful tool in every office software suite is the menubar. By definition, a menubar consists of a strip of drop-down menus that provide access to all functions. Users are quite familiar with this form of interface mainly because of its simplicity and inclusion in the majority of modern desktop applications. 

### Configuring menubar
For LibreOffice, menubar properties are defined at the following path:
```bash
/usr/lib/libreoffice/share/config/soffice.cfg/modules/swriter/menubar/menubar.xml
```
However this file is the default menubar structure definition. This means that in every update it is likely that this will be overwritten, thus it is frowned upon to customize this directory's menubar.xml.
That problem arises with numerous LibreOffice .xml customization documents. For this reason, corresponding files that can be modified also exist in a user directory as stated at the User Profile [wiki page](https://wiki.documentfoundation.org/UserProfile). 
For our setup this directory is used:
```bash
/home/<username>/.config/libreoffice/4/user/config/soffice.cfg/modules/swriter/menubar
```
Next, we will walk through the required steps for menubar customizations. For this, during this project, we are going to customize the menu to make it friendlier for a MS Office 2003 user.

Some differences can be easily pointed out from the previous comparison images. The model of the menu is the same so any differences have to do either with the name of each drop-down menu or with its sub-menus. Almost all functions of MS office 2003 menubar are implemented in LibreOffice. The main tool for menu bar customization is provided by LibreOffice, with the alternative of editing manually xml files, and found in Tools->Customize->Menus:

![customize_menubar](https://i.imgur.com/knW3txA.png)

More info on Customize dialog on the TDF [wiki](https://wiki.documentfoundation.org/images/7/7f/0114GS34-CustomizingLibO.odt)
As we can see, for every Menu entry, there can be a number of subentries. Each entry is a shortcut for an implemented function, or an installed macro from the macro Library (default/user implemented). Implemented Libreoffice functions are called "Dispatch commands". You can check out a list of them in the TDF [wiki](https://wiki.documentfoundation.org/Development/DispatchCommands).

We are going to select commands through the interface.
First, lets change a component of the menu Files and see what happens to the corresponding .config directory xml files. For this example we are going to delete the "Open Remote directory" option. The moment we save changes, a new menubar.xml is created at the user directory. 

As the following result shows, the new menubar.xml includes all of the xml entries for the current menubar setup.

Default menubar.xml
```xml
      <menu:menuitem menu:id=".uno:AddDirect"/>
      <menu:menuitem menu:id=".uno:OpenFromWriter"/>
      <menu:menuitem menu:id=".uno:OpenRemote"/>
      <menu:menuitem menu:id=".uno:RecentFileList"/>
      <menu:menuitem menu:id=".uno:CloseDoc"/>
```
User modified menubar.xml after "Open Remote" option deletion
```xml
      <menu:menuitem menu:id=".uno:AddDirect"/>
      <menu:menuitem menu:id=".uno:OpenFromWriter"/>
      <menu:menuitem menu:id=".uno:RecentFileList"/>
      <menu:menuitem menu:id=".uno:CloseDoc"/>
```
The previous behaviour provides the option to either, considering the Dispatch Command list, customize programmaticaly the menubar using xml parser or use the given interface and save configurations for future use. 
All menubar entries are customizable, with some of them referring to Dispatch commands that alter dynamically the contents of the menu, such as Tools->Add-ons that includes a list of Addon specific entries defined in the extension specific `Addons.xcu` file.


At the current state of LibreOffice core, only one defined menubar can exist with the default name menubar.xml.


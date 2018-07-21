---
title: Configuration Extension
permalink: /docs/Configuration-extension/
---

Multiple LibreOffice properties have to be edited for the project to succeed. An important aspect of the project is the deployment of configuration, so as to avoid editing settings manually for each installation. We deploy almost all needed settings (enable toolbars and document styling properties are excluded) using an `.oxt` extension package, namely a renamed `.zip` archive of the following structure:

```bash
settings_loader.oxt
├── META-INF
│   ├── manifest.xml
├── description.xml
├── description-el-GR.txt
└── *.xcu
```
## Contents
- [manifest.xml](#manifestxml)
- [description.xml](#descriptionxml)
- [XCU files](#xcu-files)
- [Building .oxt extension](#building-oxt-extension)

### manifest.xml
The manifest.xml file contains a list of all the .xcu configuration files we are going to add:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<!DOCTYPE manifest:manifest PUBLIC "-//OpenOffice.org//DTD Manifest 1.0//EN" "Manifest.dtd">
<manifest:manifest xmlns:manifest="http://openoffice.org/2001/manifest">
  <manifest:file-entry manifest:media-type="application/vnd.sun.star.configuration-data" manifest:full-path="*.xcu"/>
  <!-- more manifest files, one per registry section -->
</manifest:manifest>
```
Notice that we are not allowed to use one `.xcu` file for all configuration additions. In fact, a new file is needed for each different section of the registry.

### description.xml
Provide useful info such as versioning and contact info:
```xml
<?xml version="1.0" encoding="UTF-8"?>
<description xmlns="http://openoffice.org/extensions/description/2006" xmlns:xlink="http://www.w3.org/1999/xlink" xmlns:lo="http://libreoffice.org/extensions/description/2011">
  <version value="0.0.1"/>
  <identifier value="org.libreoffice.settings_loader"/>

  <publisher>
    <name xlink:href="" lang="en-US">GFOSS</name>
  </publisher>

  <display-name>
    <name lang="en-US">LibreOffice Automatic Configuration Extension</name>
  </display-name>

  <extension-description>
    <src xlink:href="description-en-US.txt" lang="en-US"/>
    <src xlink:href="description-el-GR.txt" lang="el-GR"/>
  </extension-description>
</description>
```
Notice that we can have one description file per locale.

### XCU files
A typical `.xcu` file is associated with a unique LibreOffice setting as shown below:

```xml
<?xml version="1.0" encoding="UTF-8"?>
<oor:component-data xmlns:oor="http://openoffice.org/2001/registry" xmlns:xs="http://www.w3.org/2001/XMLSchema" oor:name="Common" oor:package="org.openoffice.Office">
<node oor:name="Misc">
   <prop oor:name="SymbolSet" oor:finalized="true">
      <value>0</value>
   </prop>
</node>
</oor:component-data>
```
This file refers to the toolbar icon size setting, changing its value to 0 and finalizing the field so it cannot be changed by the user unless the extension is uninstalled. The steps for identifying and setting the configuration parameters are thoroughly analyzed on [TDF Wiki](https://wiki.documentfoundation.org/images/b/b0/LibreOffice_config_extension_writing.pdf). A straightforward view of the configuration registry is given by changing the setting manually, then checking registrymodifications.xcu file using any diff script that works well with XML files and searching the `oor:path` for the desired item at [libreoffice/core git](https://cgit.freedesktop.org/libreoffice/core/tree/officecfg/registry/schema/org/openoffice).

We choose, until figuring out a better way, to set the desired toolbar settings not using embedded `.xcu` files but by writing directly to the `registrymodifications.xcu` which is by default located to specific [paths](https://wiki.documentfoundation.org/UserProfile). This is a fairly large XML document depending on saved settings that holds each and every user profile detail. Specific `<item>` entries have to be added for a number toolbar settings, arising the need for XML editing. However, there is a noticeable overhead in using DOM parsing software for this big files, mainly because the whole XML document has to be loaded in memory before constructing the parsing struct. 
LibreOfice developers surely faced this problem that led them to use SAX parsing for their operations. We can take advantage of this and add desired entries at the start of the document, avoiding loading it to memory. An example script in this contect is the following:

```Python
import os
import sys
import argparse

parser = argparse.ArgumentParser(description='Process config file')
parser.add_argument('--inp', help="Path of current LO configuration file (registrymodifications.xcu)", required=True)
parser.add_argument('--out', help="Path of output (Caution if path of registrymodifications.xcu it will be ovewritten)", required=True)
args = parser.parse_args()

with open('./inp', 'r') as f_in:
    with open('./args.out','w') as f_out:
        for line_no, line in enumerate(f_in, 1):
            if line_no == 3:
                f_out.write('<item oor:path="/org.openoffice.Office.UI.WriterWindowState/UIElements/States/org.openoffice.Office.UI.WindowState:WindowStateType['private:resource/toolbar/classificationbar']"><prop oor:name="ContextActive" oor:op="fuse"><value>true</value></prop></item>\n')
            f_out.write(line)
```   
### Building .oxt extension
As we have already stated, an `.oxt` file is just a zip archive, so all we have to do is compress the aforementioned directories and files. We use a bash script (dir_to_oxt.sh) tailored for our file structure that mainly executes the following command:
```bash
zip -r ../settings_loader.oxt ./*
``` 
Finally, we can install/remove the extension either from the LibreOffice menu or by using `unopkg`:
```bash
unopkg add –shared my_config_extension.oxt
unopkg remove –shared my_config_extension.oxt
```
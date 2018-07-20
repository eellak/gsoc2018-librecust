---
title: Coding Workflow
permalink: /docs//Coding-workflow/
---

# Coding workflow
In this page, the setup of the environment used to develop a LibreOffice extension is outlined 

## Choosing a language
This is the most important part of th development process. LibreOffice, as well as other suites of the same parent branch such as OpenOffice, provide an integrated environment to build and debug macros and/or extensions. However, in order to use this environment, one has to follow the path of macro development using a language called LO Basic. This language has its syntax roots to VBA so high-level compatibility between Microsoft and Apache suites is achieved.
It's archaic syntax as well as the absence of modern programming goodies such as list containers or object oriented principles turn developers in the quest of finding a different language to use.

This is the main reason why, communicating with LO, is done using a multi language [API](https://api.libreoffice.org/). Well known languages can be used for LibreOffice programming with some among them to be Java, C++ or Python. In this GSOC project, Python is used as the language for the final extension implementations. However, some prototyping steps such as inspecting a Page style property set are executed using Basic macro commands.

The interface elements used, such as dialogs containing buttons and dropdown lists, are implemented in specific XML files of `.xdl` extension. Those can be manually written following the required LO XML schemas or compiled using the LO Dialog editor. This editor can be found at `Tools->Macros->Organize dialogs->Edit`

## Python
In order to execute python macros there are some dependencies and extensions that must be installed. The following is mandatory while the next extension is not, however we suggest using it for easing the whole testing process: 
Packages
* libreoffice-script-provider-python
Extensions
* [APSO - Alternative Script organizer for Python](https://extensions.libreoffice.org/extensions/apso-alternative-script-organizer-for-python): This extension fills the gap between Basic and Python development, emulating a script organizer for Python that offers similar functionality to the one of Basic IDE.

APSO can be accessed through `Tools->Macros->Organize python scripts`:
![APSO Start screen](https://i.imgur.com/hlC7HNP.png)

Using its menu a user can directly edit extension's python scripts. 

**Important:** Every change done through `Menu->Edit` of APSO is written directly to extension's files, so it will be overwritten with a new install of the same extension `.oxt`.

After coding the Python script, we should pack it in a format distributable to other users. This format is the well known `.oxt` for OpenOffice and LibreOffice. We should point out that `.oxt`, as well as other OpenOffice extensions (`.odt`,`.ott` and others) are just `.zip` archives that can be normally extracted. 

## Packaging the extension code
There are many approaches relevant to compiling an LibreOffice extension from script files. In this project, we use macros embedded in a specific for this purpose document named [Extension Compiler](https://wiki.openoffice.org/wiki/Extensions_Packager#Extension_Compiler). The reader is referred to the document's content for more info regarding compiler usage. 

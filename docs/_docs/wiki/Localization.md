---
title: Localization
permalink: /docs/Localization/
---

# Localization - l10n
Extensions should be available to as much users as possible, without assuming that a user can use English to navigate through an extension or access documentation. This is the reason why localization(l10n) is considered an essential in extension development. Along this section, we are going to document the l10n relevant to several extension elements process.

## l10n for string elements
An important aspect, and the welcoming part of almost every extension (that should include one) is its user interface. In terms of LibreOffice/OpenOffice, this interface is called a dialog and these suites have implemented a dedicated editor for such interfaces, the so called Dialog Editor. Among other l10n approaches, developers seem to follow two:
* Using l10n toolset as described in the [wiki](https://help.libreoffice.org/Basic/Translation_of_Controls_in_the_Dialog_Editor). Following this approach requires most elements to be statically included in the `.xdl` dialog description file.
* Describing dialog elements giving them specific IDs and then defining details in main script. Following this approach allows for more flexibility mainly because elements are finally generated dynamically and sophisticated l10n libraries can be used.

During this project, we first followed the former approach. However, as the extensions started to scale, an approach with greater scalability and maintainability was essential so the latter was chosen. 

The project extensions are developed in Python so the well known localization and iternationalization library called [gettext](https://www.gnu.org/software/gettext/) is used. This module is bundled with Python and consists of an API and a toolset to help extract strings and create l10n catalogs. A brief introduction as well as a descriptive tutorial can be found at the PhraseApp [blog](https://phraseapp.com/blog/posts/translate-Python-gnu-gettext/).

Outlining the l10n process using gettext:
1. Mark all those strings to be translated.
2. Based on the marked strings, create localization templates that are plain text files filled by the developer (`.pot` files).
3. Use those templates to create specific translation files.
4. Organize those translation files in specific directories per locale.
5. Refer to those translations from the main extension code.

### Marking translatable strings

Initially, the gettext module for the Python script is included, and the marking function is defined:
```python
import gettext
_ = gettext.gettext 
```

Next, all translatable strings are marked using this marking function:

```python
	Doc = XSCRIPTCONTEXT.getDocument()
    psm = uno.getComponentContext().ServiceManager
    dp = psm.createInstance("com.sun.star.awt.DialogProvider")
    dlg = dp.createDialog(
        "vnd.sun.star.script:dialogs.PageNumberingDialog?location=application")

    # Initialize the required fields
    oDialog1Model = dlg.Model

    oDialog1Model.Title = _("Page Numbering Title")
```

Previously, we mentioned that most of dialog control elements will be dynamically set during extension execution. The previous code segment represents that choice, by setting the dialog title during execution. More dialog control properties that are of `string` type are defined in such way:

```python
	#Cancel and OK button Labels
    CancelButton = oDialog1Model.getByName("CancelButton")
    CancelButton.Label = _("Cancel")

    OKButton = oDialog1Model.getByName("OKButton")
    OKButton.Label = _("OK")

    PositionLabel = oDialog1Model.getByName("PositionLabel")
    PositionLabel.Label = _("Position")
    PositionListBox = oDialog1Model.getByName("Position")
    PositionListBox.StringItemList = [_("Header"), _("Footer")]
    
    
    AlignmentLabel = oDialog1Model.getByName("AlignmentLabel")
    AlignmentLabel.Label = _("Alignment")
    AlignmentListBox = oDialog1Model.getByName("Alignment")
    AlignmentListBox.StringItemList = [_("Left"), _("RightS"), _("Centered")]
    
    #...#

    FirstPageLabel = oDialog1Model.getByName("FirstPageLabel")
    FirstPageLabel.Label = _("First Page")
   
    #...#

    PageOffsetLabel = oDialog1Model.getByName("PageOffsetLabel")
    PageOffsetLabel.Label = _("Page Offset")
 
 	#...#

    TypeLabel = oDialog1Model.getByName("TypeLabel")
    TypeLabel.Label = _("Numbering Type")
 
    #...#
 
    DecorLabel = oDialog1Model.getByName("DecorLabel")
    DecorLabel.Label = _("Decor")
    #...#    
```

### Creating templates
In order to create template l10n files for the previous marked strings, the `pygettext` tool is used:

```bash
pygettext.py -d base -o locales/base.pot Python/main_Python_script.py
```
This will create one template in the base domain for the main Python script. Strings inside `_()` functions are used as id's for replaceable text. More info about domains can be found in GNU gawk [manual](https://www.gnu.org/software/gawk/manual/html_node/Explaining-gettext.html). 

The result template has the following format:

```
# SOME DESCRIPTIVE TITLE.
# Copyright (C) YEAR ORGANIZATION
# FIRST AUTHOR <EMAIL@ADDRESS>, YEAR.
#
msgid ""
msgstr ""
"Project-Id-Version: PACKAGE VERSION\n"
"POT-Creation-Date: 2018-06-22 19:53+0300\n"
"PO-Revision-Date: YEAR-MO-DA HO:MI+ZONE\n"
"Last-Translator: FULL NAME <EMAIL@ADDRESS>\n"
"Language-Team: LANGUAGE <LL@li.org>\n"
"MIME-Version: 1.0\n"
"Content-Type: text/plain; charset=UTF-8\n"
"Content-Transfer-Encoding: 8bit\n"
"Generated-By: pygettext.py 1.5\n"


#: main.py:85
msgid "Page Numbering Title"
msgstr ""

#: main.py:89
msgid "Cancel"
msgstr ""

#: main.py:92
msgid "OK"
msgstr ""

#: main.py:95
msgid "Position"
msgstr ""

#: main.py:97
msgid "Footer"
msgstr ""

#: main.py:97
msgid "Header"
msgstr ""

#... Rest of translateable strings go here
```

More about the meta-data located at the start of template files can be found in gnu.org [wiki](https://www.gnu.org/software/gettext/manual/html_node/PO-Files.html)

### Creating directory tree for multiple locales
After acquiring the template, the l10n developer must create a specific directory structure that will host specific translations. We created two translations, one for Greek (el) and one for English (en)

```.
├── locales
│   ├── el
│   │   └── LC_MESSAGES
│   │       └── base.po
│   ├── en
│   │   └── LC_MESSAGES
│   │       └── base.po
│   └── base.pot
└── main.py
```

Each of the `LC_MESSAGES` includes a file named `base.po`. This file is just a copy of the `base.pot` template after filling each one of the translation strings (`msgstr` field) and saving with `.po` extension.

### Generating machine catalogs
Although `.po` files are human readable, they cannot be direct;y used by gettext. The `msgfmt` tool is used to create gettext compatible catalogs (`.mo` files):
```bash
cd locales/en/LC_MESSAGES
msgfmt.py -o base.mo base
```
After executing the previous commands for each locale the catalogs are created:
```.
├── locales
│   ├── el
│   │   └── LC_MESSAGES
│   │       ├── base.mo
│   │       └── base.po
│   ├── en
│   │   └── LC_MESSAGES
│   │       ├── base.mo
│   │       └── base.po
│   └── base.pot
└── main.py
```

### Choosing the right locale catalog during execution
Although we have created the required catalogs, we still have to select the right one depending on the running locale. Generally, selecting a locale in Python requires the following:

```python
import gettext
 
locale = gettext.translation('base', localedir='locales', languages=['locale_string']) #locale_string = en, el, ...
locale.install()
_ = locale.gettext # Greek 
```

To implement full l10n features, we have to decide which is the right locale to use. This is done by getting the right property info from the LO PropertySet:

```python
def getLanguage():
    oProvider = "com.sun.star.configuration.ConfigurationProvider"
    oAccess   = "com.sun.star.configuration.ConfigurationAccess"
    oConfigProvider = get_instance(oProvider)
    oProp = PropertyValue()
    oProp.Name = "nodepath"
    oProp.Value = "org.openoffice.Office.Linguistic/General"
    properties = (oProp,)
    key = "UILocale"
    oSet = oConfigProvider.createInstanceWithArguments(oAccess, properties)
    if oSet and (oSet.hasByName(key)):
        ooLang = oSet.getPropertyValue(key)

    if not (ooLang and not ooLang.isspace()):
        oProp.Value = "/org.openoffice.Setup/L10N"
        properties = (oProp,)
        key = "ooLocale"
        oSet = oConfigProvider.createInstanceWithArguments(oAccess, properties)
        if oSet and (oSet.hasByName(key)):
            ooLang = oSet.getPropertyValue(key)
    return ooLang

def get_instance(service_name):
        """ gets a service from Uno """
        sm = uno.getComponentContext()
        ctx = sm.getServiceManager()
        try:
            service = ctx.createInstance(service_name)
        except:
            service = NONE
        return service
```

`getLanguage()` returns the string value of the currently used locale in LibreOffice. Then, setting the correct locale and catalog is based on this string value:

```python
from urllib.parse import urlparse

def get_main_directory(module_name): #com.addon.pagenumbering
    ctx = uno.getComponentContext()
    srv = ctx.getByName("/singletons/com.sun.star.deployment.PackageInformationProvider")
    return urlparse(srv.getPackageLocation(module_name)).path + "/"

def main(*args):
	try:
        ui_locale = gettext.translation('base', localedir=get_main_directory("com.addon.pagenumbering")+'Python/locales', languages=[getLanguage()])
    except Exception as e:
        ui_locale = gettext.translation('base', localedir=get_main_directory("com.addon.pagenumbering")+'Python/locales', languages=["en"])

    ui_locale.install()
    _ = ui_locale.gettext
```

Although dialog controls include the majority of translatable strings, the previous methodology applies to other elements:

```python
def main(*args):

    try:
        ui_locale = gettext.translation('base', localedir=get_main_directory("com.addon.pagenumbering")+'Python/locales', languages=[getLanguage()])
    except Exception as e:
        ui_locale = gettext.translation('base', localedir=get_main_directory("com.addon.pagenumbering")+'Python/locales', languages=["en"])

    ui_locale.install()
    _ = ui_locale.gettext

    # get the doc from the scripting context which is made available to all scripts

    Doc = XSCRIPTCONTEXT.getDocument()
    UndoManager = Doc.getUndoManager()


    UndoManager.enterUndoContext(_("Page Numbering"))	#There should be included all those changing operations that should be put in undo stack

    # Operations for undomanagergo here

	UndoManager.leaveUndoContext()    
```

## Help pages l10n
Generating help pages is described extensively in [Extension Compiler](https://wiki.openoffice.org/wiki/Extensions_Packager#Extension_Compiler) during extension packaging. LibreOffice/OpenOffice handles the display of the correct locale help pages provided that these pages are included in the Extension Compiler `.odt` file.

## How to localize librecust extensions 
The steps required to create a new localization catalog for librecust extensions is outlined in the following steps:
1. Choose extension to l10n.
2. Generate most recent `.pot` template:
    ```bash
    pygettext.py -d base -o locales/base.pot Python/main_Python_script.py
    ```
3. Create new folder for the locale in the directory tree:
	
    ```bash
    mkdir locales/new_locale/LC_MESSAGES
    ```
    ```.
    ├── locales
    │   ├── el
    │   │   └── LC_MESSAGES
    │   │       ├── base.mo
    │   │       └── base.po
    │   ├── en
    │   │   └── LC_MESSAGES
    │   │       ├── base.mo
    │   │       └── base.po
    │   ├── new_locale
    │   │   └── LC_MESSAGES
    │   └── base.pot
    └── main.py
    ```
4. Fill template and create `.po` file:
    Based on the `.pot` template, the `msgstr` fields are filled and the `.po` file is saved in the `locales/new_locale/LC_MESSAGES` 
5. Generate locale catalog file:
    ```bash
    cd locales/new_locale/LC_MESSAGES
    msgfmt.py -o base.mo base
    ```

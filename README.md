# LibreOffice customization and creation of legal Templates

Adding open source software in employee's workflow.

# Brief description

## Project outline
This GSOC project, **Librecust**, includes the following substeps:
- Development of specific menu, UI customizations and extensions(add-ons) to achieve MS Office familiar interface without undermining LO functionality.
- Creation of extensions to automate editing and creation of Greek legal documents as an alternative to template usage in services that do not follow a standardized document format, in order to introduce LO mechanisms as a tool for Greek Public Services.
- Documentation of LO customization and extension development as well as deployment approaches for real case scenarios (testing on Specific Court Department with multiple workstations)

This project was suggested by [GFOSS - Open Technologies Alliance](https://gfoss.eu/home-posts/) in the context of [Google Summer of Code 2018](https://www.google.com).

## UI customization
- ### Menubar
Users have developed MS Office related muscle memory while using this struct. LO includes a superset of MS Office functionality so we reorder all menubar options while including each additional in another submenu. [Done]
- ### Toolbar
Small icon size is defined as default (MS Office 2003) with similar icons while leaving space for additional buttons relative to the extension development [Done]

Simple basic macros to inspect and access certain submenus (eg Page Setup Dialog) that are not accessible through [Dispatch Commands](https://wiki.documentfoundation.org/Development/DispatchCommands) (.uno:*) [Code](https://github.com/eellak/gsoc2018-librecust/tree/master/menu_customization/macros/LibreCustLib) [Done].

## Extension development
Extension elements are prototyped in LO Basic for API abstraction, then ported and finalized to Python to access a more active and populated developer community.
- ### Page Numbering Addon
Page numbering Addon, providing interface for page offsets, starting pages, and different numbering types in the same documents, avoiding manual insertion of Page Styles and Breaks.[Code](https://github.com/eellak/gsoc2018-librecust/tree/master/page_numbering_addon)

#### Notes
Page style nesting is not developed so a new approach of style inheritance through cloning style property set is implemented ([XPropertySet](https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1beans_1_1PropertySet.html) service).

[Our approach](https://github.com/eellak/gsoc2018-librecust/blob/master/page_numbering_addon/Python%20version/python/main.py#L299)

- ### Legal paper assisting toolbar (LawAddon)
Use of legal document indexing API for typing and editing shortcuts. All template related extension modules will be compatible with existing management software used in certain departments. While more info is included in the corresponding [readme](https://github.com/eellak/gsoc2018-librecust/tree/master/law_addon), the elements compiling LawAddon are the following:
* Insert Law: Extension that fetches Greek law text body to current cursor position. The API used for law fetching is provided by another GSOC project from GFOSS. [gsoc2018-3gm](https://github.com/eellak/gsoc2018-3gm). [Code](https://github.com/eellak/gsoc2018-librecust/blob/master/law_addon/Python%20Version/python/main.py#L118)
* Insert external document: Extension that inserts an external document as reference link to current cursor position using relative parts for document portability. [Code](https://github.com/eellak/gsoc2018-librecust/blob/master/law_addon/Python%20Version/python/main.py#L290)
* Insert contents table: Insert contents table simulating the corresponding tool from menubar. [Code]()
* Update contents table: Update all content tables without leaving current cursor position, speeding up the default process for long documents. [Code]()

## Template creation
While there are few public departments that use standardized law documents (and have already implemented them), most services and court departments produce and use non-standardized documents. This is the reason why we decided to engineer a different approach for automation of document creation. The base of this approach is the AutoText functionality that is implemented in LibreOffice/OpenOffice.

Utilizing feedback from employees, we developed an AutoText addon that allows simultaneous usage of autotexts and editing of document. AutoTexts can save not only plain text but also tables and format data so repeating parts of documnts are saved as documents, optimizing the whole relevant to Law document editing. [Code](https://github.com/eellak/gsoc2018-librecust/tree/master/autotext_addon)  

## Deployment
In every possible service the deployment part is a crucial process. Some of our customizations are distributed through extensions while others (menu customizations) require editing user directory configuration files (.xml). Achieving a unified installation interface includes the development of an interactive bash script giving options for partial or complete installation of Librecust. Regarding certain settings application (eg default toolbar size) we took advantage of the LO SAX xml parsing and just add certain xml elements to the file head, letting LO to reconstruct the xml on application startup.
The whole project requires continuous testing and feedback so deployment was our first concern and the installation approach is already implemented. See [installation script](https://github.com/eellak/gsoc2018-librecust/tree/master/install_script)

The previous approach can be used in almost any Linux distribution. However, in order to massively install our customizations in public service workstations (that use Debian based distributions), we packaged the whole librecust process in a `deb` package. The package elements are included in the corresponding [directory](https://github.com/eellak/gsoc2018-librecust/tree/master/project_packages/deb).

## Documentation
Throughout this GSOC project, documentation for each part will be compiled. We follow an example centric approach, describing each step related to our project, creating a [wiki](https://github.com/eellak/gsoc2018-librecust/wiki) that can be the base for great number of different LO customization projects.

### Developer documentation
The [wiki](https://github.com/eellak/gsoc2018-librecust/wiki) includes documentation pages for developers.

### End User documentation
End user man pages are included as metadata in LibreOffice Help at install. An [example](https://github.com/eellak/gsoc2018-librecust/tree/master/page_numbering_addon/Addon%20metadata) of this inclusion for reference can be observed at each extension's metadata.

However, it is not mandatory to install the extensions or he whole project to read those manpages. They are also part of our [Github page](https://eellak.github.io/gsoc2018-librecust/).

### Challenges
While LO Basic is the most documented language, mainly because of its abstraction, developers keen on using modern languages (eg Python, Java). LibreOffice Python UNO bridge is poorly documented with helping topics spread across multiple forum posts, so our documentation will be of much help for new developers.

# Installing and building librecust
## Installation
The installation process is described in the corresponding [wiki page]()

## Building librecust
Building and packaging instructions for developers are provided in the corresponding [wiki page](https://github.com/eellak/gsoc2018-librecust/wiki/Build-Project).

## Implementation
Menu customizations are implemented by editing user configuration `.xml` files and adding UI functionality through predefined [dispatch commands](https://wiki.documentfoundation.org/Development/DispatchCommands) and macro scripts.
The must-see reference for LibreOffice Macro development that is of great use throughout this project is Andrew Pitonyak's [OpenOffice Macro Information](http://www.pitonyak.org/AndrewMacro.odt).

Modules and partially mockups will be implemented in `.ui` format mainly using [Glade](https://glade.gnome.org/). In the event of a feature that is not already implemented in LibreOffice (`.uno` files), we are going to use  [Libreoffice Software Development Kit 6.0](https://api.libreoffice.org/).

Then, we need to harvest Greek legal documents for template creation. Some relevant sources are websites of associations such as [EANDA](http://www.eanda.gr/) and [DSA](http://www.dsa.gr/). Those sources provide templates that do not have any specific format. Most of them are created by employees or lawyers thus their undefined structure.

Templates include "User defined fields" for static information (e.g. date and members of court) and "Bookmarks" for case specific info (e.g. description of law case) as well as properties for classification. Those can be tracked and used through the Java or Basic API as shown in LibreOffice [examples](https://api.libreoffice.org/examples/DevelopersGuide/Text/).

Finally, after observing template details, we engineered addons that automate their creation taking into account their non-standard nature across different services. 

We started with the intention to build a LibreOffice extension providing an interface for template selection and filling. However, most public services already used such an interface, so we decided to build a different approach of document filling automation through AutoTexts.

A large part of the project and its composing functions is implemented (or inspired) by the following sources:
- Andrew Davison work on documenting Java Libreoffice Programming Concepts on [Java LibreOffice Programming](http://fivedots.coe.psu.ac.th/~ad/jlop/#contents)
- Samuel Mehrbrodt's repository for a basic Eclipse LibreOffice extension project [libreoffice-starter-extension](https://github.com/smehrbrodt/libreoffice-starter-extension)
- Andrew D. Pitonyak's OpenOffice.org Macros Explained - [OOME Third Edition](http://www.pitonyak.org/OOME_3_0.pdf)

# Timeline
The timeline followed throughout librecust development is included in the corresponding [timeline gist](https://gist.github.com/arvchristos/a579323d320b288dbbc50ad547e859ec) 

# Final Report
The final report for GSOC 2018, as written by Arvanitis Christos, and in the form of a gist file can be found [here](https://gist.github.com/arvchristos/64a4c37bc9060e27ad82fb6258ad9dbf). 

# Future Work
The following future work can be done to improve the state of Librecust project:

1. Add more sources to `Insert Law` functionality for uneventful access to the vast majority of law documents (Only access to [gsoc2018-3gm](https://github.com/eellak/gsoc2018-3gm) database)
2. Merge current document with external elements: By the end of the project, for every external document a bookmark is provided to give access to external element positions to future developers that attempt to implement this functionality. Complete merging requires canvas writing to external document elements (e.g. png, pdf...) in order for page numbering to be included. The exported document can be a pdf including all documents referenced in the main editing one.
3. Page Numbering addon: Add further functionality to page numbering addon (even/odd pages numbered). The LIbreOffice API already includes functions that lead to such additions.
4. Completely open source template management software.
5. Solution for distribution of AutoTexts among workstations of same departments.
6. Automatic extraction of AutoText elements from a huge number of documents for each public service.
7. Packaging for multiple other distributions   

# The team
## Student 
- Arvanitis Christos (@arvchristos) [link to github page].

## Mentors
Mentors overseeing the development process:
- Kostas Papadimas
- Theodoros Karounos
# LibreOffice customization and creation of legal Templates - librecust

Welcome to Google Summer of Code 2018 project *LibreOffice customization and creation of legal Templates* (or librecust). The project is adding open source software in employee's workflow, applying currently on Greek legal services (mainly on *The Council of State* and extending to other services such "Administrative Court of Appeal" departments).

# Overview
* [Description](#brief-description)
* [Installation](#installing-and-building-librecust)
* [Timeline](#timeline)
* [Final report](#final-report)
* [Future work](#future-work)
* [The team](#the-team)

# Brief description

## Project outline
This GSOC project, **librecust**, includes the following substeps:
- Development of specific menu, UI customizations and extensions(add-ons) to achieve MS Office familiar interface without undermining LO functionality.
- Creation of extensions to automate editing and creation of Greek legal documents as an alternative to template usage in services that do not follow a standardized document format, in order to introduce LO mechanisms as a tool for Greek Public Services.
- Documentation of LO customization and extension development as well as development of deployment approaches for real case scenarios (testing on Specific Court Department (*The Council of State*) with multiple active workstations)

This project was suggested by [GFOSS - Open Technologies Alliance](https://gfoss.eu/home-posts/) in the context of [Google Summer of Code 2018](https://www.google.com).

## UI customization
- ### Menubar
Users have developed MS Office related muscle memory while using this tool. LO includes a superset of MS Office functionality so we reorder all menubar options while including each additional in another submenu.
- ### Toolbar
The corresponding, in terms of MS Office functionality, toolbar items are included with similar appearance (small icon size is defined as default (MS Office 2003) with similar icons) while leaving space for additional buttons relative to the extension development. The icon set included in the set of modifications is created by [@charliecnr](https://www.deviantart.com/charliecnr). 

Simple basic macros to inspect and access certain sub-menus (e.g. Page Setup Dialog) that are not accessible through default [dispatch Commands](https://wiki.documentfoundation.org/Development/DispatchCommands) (`.uno:*`) [Code](https://github.com/eellak/gsoc2018-librecust/tree/master/menu_customization/macros/).

## Extension development
Extension elements are prototyped in LO Basic for API abstraction, then ported and finalized to Python to access a more active and populated developer community.
- ### Page Numbering Addon
Page numbering Addon, providing interface for page offsets, starting pages, and different numbering types in the same documents, avoiding manual insertion of Page Styles and Breaks.[Code](https://github.com/eellak/gsoc2018-librecust/tree/master/page_numbering_addon)

- #### Notes
Page style nesting is not developed so an approach of style inheritance through cloning style property set is implemented ([XPropertySet](https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1beans_1_1PropertySet.html) service).

[Approach followed in librecust](https://github.com/eellak/gsoc2018-librecust/blob/7abb56c11406746ab8d9bb694df3a68062a15ee8/page_numbering_addon/LibreOffice/python/build_files/python/main.py#L344)

- ### Legal paper assisting toolbar (LawAddon)
All template related extension modules are compatible with existing management software used in certain departments. While more info is included in the corresponding [readme](https://github.com/eellak/gsoc2018-librecust/tree/master/law_addon), the elements compiling LawAddon are the following:
* Insert Law: Extension that fetches Greek law text body to current cursor position. The API used for law fetching is provided by another GSOC project from GFOSS. [gsoc2018-3gm](https://github.com/eellak/gsoc2018-3gm).
* Insert external document: Extension that inserts an external document as reference link to current cursor position using relative parts for document portability.
* Insert contents table: Insert contents table simulating the corresponding tool from menubar.
* Update contents table: Update all content tables without leaving current cursor position, speeding up the default process for long documents.

All the aforementioned utilities are implemented in the [LawAddon python script](https://github.com/eellak/gsoc2018-librecust/blob/master/law_addon/LibreOffice/build_files/python/main.py).

## Template creation
While there are few public departments that use standardized law documents (and have already implemented them), most services and court departments produce and use non-standardized documents. This is the reason why we decided to engineer a different approach for automation of document creation. The base of this approach is the AutoText functionality that is implemented in LibreOffice/OpenOffice.

Utilizing feedback from employees, we developed an AutoText addon that allows simultaneous usage of autotexts and editing of document. AutoTexts can save not only plain text but also tables and format data so repeating parts of documnts are saved as documents, optimizing the whole relevant to Law document editing. [Code](https://github.com/eellak/gsoc2018-librecust/tree/master/autotext_addon)

Additionally, AutoTexts provide the ability to distribute certain text segments across a local network, so an AutoText database can be created for each department.   

## Deployment
In every possible service the deployment part is a crucial process. Some of our customizations are distributed through extensions while others (menu customizations) require editing user directory configuration files (.xml). Achieving a unified installation interface includes the development of an interactive bash script giving options for partial or complete installation of librecust. Regarding certain settings application (e.g. default toolbar size) we took advantage of the LO SAX XML parsing and just add certain xml elements to the file head, letting LO to reconstruct the XML on application startup.
The whole project requires continuous testing and feedback so deployment was our first concern and the installation approach is already implemented. See [installation script](https://github.com/eellak/gsoc2018-librecust/tree/master/install_script)

The previous approach can be used in almost any Linux distribution. However, in order to massively install our customizations in public service workstations (that use Debian based distributions), we packaged the whole librecust process in a `deb` package. The package elements are included in the corresponding [directory](https://github.com/eellak/gsoc2018-librecust/tree/master/project_packages/deb).

## Documentation
Throughout this GSOC project, documentation for each part will be compiled. We follow an example centric approach, describing each step related to our project, creating a [wiki](https://github.com/eellak/gsoc2018-librecust/wiki) that can be the base for great number of different LO customization/extension projects.

### Developer documentation
The [wiki](https://github.com/eellak/gsoc2018-librecust/wiki) includes documentation pages for developers.

### End User documentation
End user man pages are included as meta-data in LibreOffice Help at install. An [example](https://github.com/eellak/gsoc2018-librecust/tree/master/autotext_addon/LibreOffice/sidebar_version/oxt_metadata) of this inclusion for reference can be observed at each extension's meta-data.

However, it is not mandatory to install extensions or the whole project to access those man-pages. They are also part of the project's [Github page](https://eellak.github.io/gsoc2018-librecust/).

### Challenges
While LO Basic is the most documented language, mainly because of its abstraction, developers keen on using modern languages (e.g. Python, Java). LibreOffice Python UNO bridge is poorly documented with helping topics spread across multiple forum posts, so our documentation will be of much help for new developers.

# Installing and building librecust
## Installation
The installation process is described in the corresponding [wiki page](https://github.com/eellak/gsoc2018-librecust/wiki/Installation)

## Building librecust
Building and packaging instructions for developers are provided in the corresponding [wiki page](https://github.com/eellak/gsoc2018-librecust/wiki/Build-Project).

# Implementation
Menu customizations are implemented by editing user configuration `.xml` files and adding UI functionality through predefined [dispatch commands](https://wiki.documentfoundation.org/Development/DispatchCommands) and macro scripts. Any unimplemented feature is developed using macro scripts and inspecting tools for access to different menu items (e.g. tabs, radio buttons...) simulating the corresponding menu items of MS Office.
The must-see reference for LibreOffice Macro development that is of great use throughout this project is Andrew Pitonyak's [OpenOffice Macro Information](http://www.pitonyak.org/AndrewMacro.odt).

Then, we need to harvest Greek legal documents for template creation. Some relevant sources are websites of associations such as [EANDA](http://www.eanda.gr/) and [DSA](http://www.dsa.gr/). Those sources provide templates that do not have any specific format. Most of them are created by employees or lawyers thus their undefined structure.

Templates include "User defined fields" for static information (e.g. date and members of court) and "Bookmarks" for case specific info (e.g. description of law case) as well as properties for classification. Those can be tracked and used through the Java or Basic API as shown in LibreOffice [examples](https://api.libreoffice.org/examples/DevelopersGuide/Text/).

Finally, after observing template details, we engineered addons that automate their creation taking into account their non-standard nature across different services. 

We started with the intention to build a LibreOffice extension providing an interface for template selection and filling. However, most public services already used such an interface, so we decided to build a different approach of document filling automation through AutoTexts.

A large part of the project and its composing functions is implemented (or inspired) by the following sources:
- Andrew Davison work on documenting Java Libreoffice Programming Concepts on [Java LibreOffice Programming](http://fivedots.coe.psu.ac.th/~ad/jlop/#contents)
- Samuel Mehrbrodt's repository for a basic Eclipse LibreOffice extension project [libreoffice-starter-extension](https://github.com/smehrbrodt/libreoffice-starter-extension)
- Andrew D. Pitonyak's OpenOffice.org Macros Explained - [OOME Third Edition](http://www.pitonyak.org/OOME_3_0.pdf)
- [@kelsa-pi](https://github.com/kelsa-pi) UNO Dialog Tools [unodit](https://github.com/kelsa-pi/unodit) project.

# Timeline
The timeline followed throughout librecust development is included in the corresponding [timeline gist](https://gist.github.com/arvchristos/a579323d320b288dbbc50ad547e859ec) 

# Final Report
The final report for GSOC 2018, as written by Arvanitis Christos, and in the form of a gist file, can be found [here](https://gist.github.com/arvchristos/64a4c37bc9060e27ad82fb6258ad9dbf). 

# Future Work
The following future work can be done to improve the state of librecust project:

1. Add more sources to `Insert Law` functionality for uneventful access to the vast majority of law documents (Only access to [gsoc2018-3gm](https://github.com/eellak/gsoc2018-3gm) database)
2. Merge current document with external elements: By the end of the project, for every external document a bookmark is provided to give access to external element positions to future developers that attempt to implement this functionality. Complete merging requires canvas writing to external document elements (e.g. `png`, `pdf`...) in order for page numbering to be included. The exported document can be a pdf including all documents referenced in the main editing one.
3. Page Numbering add-on: Add further functionality to page numbering add on (even/odd pages numbered). The LIbreOffice API already includes functions that lead to such additions.
4. Completely open source template management software.
5. Solution for distribution of AutoTexts among workstations of same departments (replacing proprietary/outdated management software in such services).
6. Automatic extraction of AutoText elements from a huge number of documents for each public service.
7. Packaging for multiple other distributions   

# The team
## Student 
- Arvanitis Christos [@arvchristos](https://github.com/arvchristos).

## Mentors
Mentors overseeing the development process:
- Kostas Papadimas
- Theodoros Karounos

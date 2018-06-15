# LibreOffice customization and creation of legal Templates

Adding open source software in employee's workflow.

## Project outline
This GSOC project, Librecust[1], includes the following substeps:
- Development of specific menu, UI customizations and extensions(add-ons) to achieve MS Office familiar interface without undermining LO functionality.
- Creation of Greek legal system templates to introduce LO mechanisms as a tool for Greek Public Services
- Documentation of LO customization and extension development as well as deployment approaches for real case scenarios (testing on Specific Court Department with multiple workstations)

This project was suggested by [GFOSS - Open Technologies Alliance](https://gfoss.eu/home-posts/) in the context of [Google Summer of Code 2018](https://www.google.com).

## UI customization
- ### Menubar
Users have developed MS Office related muscle memory while using this struct. LO includes a superset of MS Office functionality so we reorder all menubar options while including each additional in another submenu. [Done]
- ### Toolbar
Small icon size is defined as default (MS Office 2003) with similar icons while leaving space for additional buttons relative to the extension development [Done]
Simple basic macros to inspect and access certain submenus (eg Page Setup Dialog) that are not accessible through [Dispatch Commands](https://wiki.documentfoundation.org/Development/DispatchCommands) (.uno:*) [Done]

## Extension development
All extensions are first developed using LO Basic language for API abstraction, then ported to Python to access a much active and populated developer community.
- ### Page Numbering Addon
Page numbering addon, providing interface for page offsets, starting pages, and different numbering types in the same documents, avoiding manual insertion of Page Styles and Breaks. LO Basic implementation is done while localization and Python porting is pending.
#### Notes
Page style nesting is not developed so a new approach of style inheritance through cloning style property set ([XPropertySet](https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1beans_1_1PropertySet.html) service).

- ### Legal paper assisting toolbar
Use of legal document indexing API for typing and editing shortcuts. All template related extension modules will be compatible with existing management software used in certain departments [Process pending until further communication with Legal employees and judges].

## Template creation
Proof of concept templates will be engineered according to end user needs and implemented using variable fields LO functionality [User Fields and Bookmarks] respecting existing software conventions. [Pending until second evaluation]

## Deployment
In every possible service the deployment part is a crucial process. Some of our customizations are distributed through extensions while others (menu customizations) require editing user directory configuration files (.xml). Achieving a unified installation interface includes the development of an interactive bash script giving options for partial or complete installation of Librecust. Regarding certain settings application (eg default toolbar size) we took advantage of the LO SAX xml parsing and just add certain xml elements to the file head, letting LO to reconstruct the xml on application startup.
The whole project requires continuous testing and feedback so deployment was our first concern and the installation approach is already implemented. See [installation script](https://github.com/eellak/gsoc2018-librecust/tree/master/install_script)

## Documentation
Throughout this GSOC project, documentation for each part will be compiled. We follow an example centric approach, describing each step related to our project, creating a wiki that can be the base for great number of different LO customization projects. UI customization is already documented while extension and template creation are still pending.
### Challenges
While LO Basic is the most documented language, mainly because of its abstraction, developers keen on using modern languages (eg Python, Java). LibreOffice Python UNO bridge is poorly documented with helping topics spread across multiple forum posts, so our documentation will be of much help for new developers.


## Implementation
Menu customizations are implemented by editing user configuration `.xml` files and adding UI functionality through predefined [dispatch commands](https://wiki.documentfoundation.org/Development/DispatchCommands) and macro scripts.
The must-see reference for LibreOffice Macro development that is of great use throughout this project is Andrew Pitonyak's [OpenOffice Macro Information](http://www.pitonyak.org/AndrewMacro.odt).

Modules and partially mockups will be implemented in `.ui` format mainly using [Glade](https://glade.gnome.org/). In the event of a feature that is not already implemented in LibreOffice (`.uno` files), we are going to use  [Libreoffice Software Development Kit 6.0](https://api.libreoffice.org/).

Then, we need to harvest Greek legal documents for template creation. Some relevant sources are websites of associations such as [EANDA](http://www.eanda.gr/) and [DSA](http://www.dsa.gr/). Those sources provide templates that do not have any specific format. Most of them are created by employees or lawyers thus their undefined structure.

Through this project, we will also create a "proof of concept" archive of templates using data and documents from several Greek court divisions as well as document the creation procedure of those templates and developed addons.

Templates will include "User defined fields" for static information (e.g. date and members of court) and "Bookmarks" for case specific info (e.g. description of law case) as well as properties for classification. Those can be tracked and used through the Java or Basic API as shown in LibreOffice [examples](https://api.libreoffice.org/examples/DevelopersGuide/Text/).

Finally, when the required "proof of concept" document archive is built, we will create templates for each one of them.

The document directory will be available for use through a LibreOffice extension. This extension will be an add-on (in the context of having a GUI built with LibreOffice Basic dialog editor).

The extension code acts as the backend part of our extension implementing functions that ease the access to LibreOffice Java API.

A large number of those functions are implemented (or inspired) by the following sources:
- Andrew Davison work on documenting Java Libreoffice Programming Concepts on [Java LibreOffice Programming](http://fivedots.coe.psu.ac.th/~ad/jlop/#contents)
- Samuel Mehrbrodt's repository for a basic Eclipse LibreOffice extension project [libreoffice-starter-extension](https://github.com/smehrbrodt/libreoffice-starter-extension)
-  Andrew D. Pitonyak's OpenOffice.org Macros Explained - [OOME Third Edition](http://www.pitonyak.org/OOME_3_0.pdf)

## Installing
During the development period of the project the installation procedure will be rather long. When sub-goals are implemented all steps will be included in an .oxt installation.

Installation requires running the installation bash script located at install_script/installer.sh

```bash
cd install_script
bash installer.sh
```
An interactive script asks the user for installation of required sub-modules of the project. Superuser permissions are required in some steps.

## Mentors
Mentors overseeing the development process:
- Kostas Papadimas
- Theodoros Karounos

## Timeline
- [x] April 23 – May 14
* Building development environment while updating README and documentation for installation and packaging details.
* Harvesting of Greek legal documents and design of automation tools for template creation.
- [x] May 14 – May 20
* Creation of mockups and prototypes for specific MS Office details that are going to be implemented while getting feedback from users.
- [x] May 20 – June 15
* Implementation and testing of UI customizations.
* Development of Page Numbering extension in the context of easing UI workflow.
- [ ] June 15 – July 20
* Template development for a number of the harvested legal documents.
* Port page_numbering_addon to python while documenting.
- [ ] July 20 – August 8
* Testing, adjustments and further documentation.

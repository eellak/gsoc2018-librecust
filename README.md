# LibreOffice customization and creation of legal Templates

Adding open source software in employee's workflow.

## Description

A set of modules and templates for LibreOffice Suite that ease the transition from Microsoft Office as well as ready to use templates that automate the creation of Greek Legal Documents. Those templates aim to encounter time consuming tasks by removing the formatting and layout procedures from employee workflow. Furthermore, an interface to access all those templates will be developed. All steps will be documented during the process and afterwards for future reference and development.

This project was suggested by [GFOSS - Open Technologies Alliance](https://gfoss.eu/home-posts/) in the context of [Google Summer of Code 2018](https://www.google.com).

## Implementation
Modules and partially mockups will be implemented in `.ui` format mainly using [Glade](https://glade.gnome.org/). In the event of a feature that is not already implemented in LibreOffice (`.uno` files), we are going to use  [Libreoffice Software Development Kit 6.0](https://api.libreoffice.org/).

Then, we need to harvest Greek legal documents for template creation. Some relevant sources are websites of associations such as [EANDA](http://www.eanda.gr/) and [DSA](http://www.dsa.gr/). THose sources provide templates that do not have any specific format. Most of them are created by employees or lawyers thus their undefined structure.

Through this project, we will also create a "proof of concept" archive of templates as well as document the creation procedure and provide a user interface dialog to ease the template creation.

Templates will include "User defined fields" for static information (e.g. date and members of court) and "Bookmarks" for case specific info (e.g. description of law case) as well as properties for classification. Those can be tracked and used through the Java API as shown in LibreOffice [examples](https://api.libreoffice.org/examples/DevelopersGuide/Text/).

Finally, when the required "proof of concept" document archive is built, we will create templates for each one of them.

The document directory will be available for use through a LibreOffice extension. This extension will be an add-on (in the context of having a GUI built with LibreOffice Basic dialog editor).

The extension code acts as the backend part of our extension implementing functions that ease the access to LibreOffice Java API.

A large number of those functions are implemented (or inspired) by the following sources:
- Andrew Davison work on documenting Java Libreoffice Programming Concepts on [Java LibreOffice Programming](http://fivedots.coe.psu.ac.th/~ad/jlop/#contents)
- Samuel Mehrbrodt's repository for a basic Eclipse LibreOffice extension project [libreoffice-starter-extension](https://github.com/smehrbrodt/libreoffice-starter-extension)

## Mentors
Mentors overseeing the development process:
- Kostas Papadimas
- Theodoros Karounos

## Timeline
- [ ] April 23 – May 14
* Building development environment while updating README and documentation for installation and packaging details.
* Harvesting of Greek legal documents and design of automation tools for template creation.
- [ ] May 14 – May 20
* Creation of mockups and prototypes for specific MS Office details that are going to be implemented while getting feedback from users.
- [ ] May 20 – June 15
* Implementation and testing of UI customizations.
- [ ] June 15 – July 20
* Template development for a number of the harvested legal documents.
- [ ] July 20 – August 8
* Testing, adjustments and further documentation.

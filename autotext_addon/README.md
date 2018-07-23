# AutoText Addon
During the GSOC librecust project, we faced an implementation problem for one of the main goals. Templates, while they are simple to engineer, are not the optimal solution for all Greek public services. There are services that have standardized document formats, making it easy to implement template documents. However, there are other services that do not follow a specific pattern for every document.

We had to construct a plan to automate and help the editing process of such service's document. This is where [LibreOffice/OpenOffice autotexts](https://help.libreoffice.org/Writer/AutoText) come to hand. 

The main idea behind this addon is the question why try to standardize the whole document when one can make modular sub-templates for different parts that are common such as the table that includes members of the court or the header that provides info about the court responsible for this ruling.

## Installation
AutoText can be installed using the `.oxt` file at the Python subdirectory and the LibreOffice Extension Manager.
The option of `.deb` install is also given, however this was implemented mainly for easier deployment of the whole librecust project, thus this approach is not recommended for standalone AutoText installations.

## More info about usage
More info about the usage of this addon is included in the extension help pages, accessible either through the help icon of the main dialog or through the following menu:

`Help->LibreOffice Help`

## Implementation
The extension is developed in Python, in the same manner as other librecust extensions (Page Numbering, Law addon...). The localization process followed is described in the corresponding [wiki page](https://github.com/eellak/gsoc2018-librecust/wiki/Localization). 

# Page Numbering Addon

During this project, we decided, after getting feedback from common users (law department employees), to implement a plugin that eases the process of adding page numbering to a document.

This plugin, or by LO/OO terminology add-on(an extension that includes any kind of UI implementation/customization), includes the following features:

## Features

* Add page numbering without taking page-break system into account

  Although Page Breaks are an intuitive and effective approach for document layout and styling, users migrating from Microsoft Office suites find it more than difficult to understand)

* Configure styling options such as Font, Character height, Αlignment and page position (Header/Footer)
* Page offset and First page options
* Numbering type selection such as Roman, Arabic or Greek
* Multiple Page numbering setups per document

## Implementation
In order to get familiar with LO API we first implemented a version of the plugin in LO Basic language. Although this is the most documented among LO/OO compatible languages, it follows an archaic programming principle with little to none moder features. That is the reason that led us to port the official version in Python, using [UNO:API](https://api.libreoffice.org/) as the connection with LibreOffice.

During the porting process, we still tested all of our next steps in the Basic module for faster communication with LO, exploiting the abstraction of Basic over Python.

All facts and drawbacks that we came through during this implementation are documented in the Wiki, as well as the whole process of building the workflow used for a common Python add-on implementation.

Page Numbering Addon will be released in version 0.0.1 during/after GSOC period. Source code will, surely, be available and suggestions, improvements or bug reports will be more than welcome. Any updates will be distributed through the official extension manager.

## Installation
Each implementation (Python/LO Basic) is packaged as en extension in `.oxt` format. The LO Basic version has no dependencies. For the suggested Python version the following are applied:

### Python Dependencies
* libreoffice-script-provider-python package or even better [uno-tools](https://pypi.org/project/unotools/)

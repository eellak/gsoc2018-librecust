---
title: Installation
permalink: /docs/Installation/
---

Info about the repo for each distribution will go here

## Requirements

### Debian

#### LibreOffice 6

* libreoffice-script-provider-python
From this LO version, help is not included with the main installation package. On the contrary, help is installed as a seperate package, and is required in order to include additional help pages (through Help->LibreOffice Help) for off-line access. 
* libreoffice-help-el
* libreoffice-help-en-us

For full Greek support (e.g. Dialogs, localization, UI locale...) the following package is required:
* libreoffice-l10n-el

#### LibreOffice 5 and earlier
* libreoffice-script-provider-python

For full Greek support (e.g. Dialogs, localization, UI locale...) the following package is required:
* libreoffice-l10n-el

## Installation

### Debian 
Add the package repository to apt:

```bash
echo "deb https://eellak.github.io/gsoc2018-librecust/repos/apt/debian/ precise main" | sudo tee -a /etc/apt/sources.list
```
Update
```bash
sudo apt update
```

Install librecust package
```bash
sudo apt install librecust
```

### Arch and others
Execute the interactive install.sh found at [install_script](https://github.com/eellak/gsoc2018-librecust/tree/master/install_script) directory:

```bash
cd install_script
bash installer.sh
```
An interactive script asks the user for installation of required sub-modules of the project. Superuser permissions are required in some steps.


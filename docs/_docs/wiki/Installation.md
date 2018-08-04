---
title: Installation
permalink: /docs/Installation/
---

Info about the repo for each distribution will go here

## Debian 
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

## Arch
Execute the interactive install.sh found at [install_script](https://github.com/eellak/gsoc2018-librecust/tree/master/install_script) directory:

```bash
cd install_script
bash installer.sh
```
An interactive script asks the user for installation of required sub-modules of the project. Superuser permissions are required in some steps.


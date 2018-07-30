---
title: Build project
permalink: /docs/Build_Project/
---

## Clone repo
First of all, clone the latest version of the librecust project from the [Github repo](https://github.com/eellak/gsoc2018-librecust/tree/master/)

```bash
git clone https://github.com/eellak/gsoc2018-librecust.git
```

## Edit code
Improve (or maybe destroy) any part of the project.

## Partial building of composing parts
### Extensions
For the following extensions, a rebuild of the `.oxt` is recommended after any change using Extension compiler `.odt` document as described in the corresponding [wiki page](Coding/workflow/link/):
* Page Numbering Addon
* LibreLaw Toolbar
* AutoText Addon

For the settings loader extension, a simple bash script is included in the `settings_loader` directory named `dir_to_oxt.sh` that rebuilds the `.oxt` extension using the files in the `settings_loader/extension` directory. For reference regarding this simple bash script [here](path/to/dir_to_oxt.sh).

### UI customization
Edit the required files as described in the following wiki pages:
* Toolbar customization
* Menubar customization
* Icon Set configuration

These files have just to be copied in the right directory, either from the installation script or from the `.deb` package. Package creation is described in the next documentation chapter.

## Prepare installation script resources
As seen in the `install_script` directory, the `installer.sh` script installs every part using the files built in the main directory folders. No changes should be made to the naming convention of the files without changing accordingly this bash script. If no new extension is used, run the `installer.sh` script after building new files.

## Build .deb package
In order to build the package using the project code the following packages need to be installed:
* build-essential
* devscripts
* debhelper

The basic idea is that a directory is used to build the `.deb` package. This is the reason why we need to copy each of the project's part in the following directory:

`project_packages/deb/librecust-x.x.x/`

Inside this directory the next tree is seen:

```
librecust-x.x.x
├── DEBIAN
│   ├── files_for_debian_packaging
├── temp
│   └── libreoffice
│       └── files that need to either be installed(extensions) or copied to user directory(UI xml customizations) 
└── usr
    └── lib
        └── libreoffice
            └── share
                └── config
                    └── icon set zip file
```

Copy the edited extensions or `.xml` files to the right directory as pointed out in the previous tree diagram. Be careful when copying, you need to delete any previous version of the same file in order to install the latest version. 

If you are interested in the way this package works, feel free to check the DEBIAN/ directory that contains every implementation info that leads to the final package as seen during `dpkg -i extension.deb` or `apt` usage.

When all customized files are put in position, execute `rebuild.sh` to create the updated `.deb` package. Be careful that this script overwrites the previously created `.deb` file. In order to avoid this please edit the version of the `librecust-x.x.x` parent directory (x.x.x).

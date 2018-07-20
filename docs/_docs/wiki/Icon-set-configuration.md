---
title: Icon set configuration
permalink: /docs/Icon-set-configuration/
---

#Icon set configuration

Icon sets/themes come in specific `.zip` format, with certain naming. An icon theme named **Foo** will be archived in a `.zip` file named `images_Foo.zip`. The reader is referred to the included [images_office2013.zip](https://github.com/eellak/gsoc2018-librecust/blob/master/menu_customization/toolbar/icon_theme/images_office2013.zip) example icon theme for a starting template. THis is the suggested way to create an icon theme at this point mainly because there is not any interface or tool to ease this procedure.  

Regarding icon sets in LibreOffice there are two ways to deploy changes in a new installation, depending on the LO version.

## LibreOffice 5 and earlier
Icon sets can be installed by copying the `.zip` file in the local installation directory under `/share/config/`. That is the reason why in the [installer.sh](https://github.com/eellak/gsoc2018-librecust/blob/master/install_script/installer.sh) script we are using the following command to install the desired icon theme:

```bash
LIBRE_LIB_CONFIG_PATH="/usr/lib/libreoffice/share/config/"
cp "$ICON_THEME_PATH"/*.zip $LIBRE_LIB_CONFIG_PATH
``` 
Following the previous approach, we may install an icon theme, but a corresponding uninstallation script must be used to remove any changes. This script should include an remove command like the following one:
```bash
rm $LIBRE_LIB_CONFIG_PATH/images_Foo.zip
```
## LibreOffice 6
The [MUFFIN concept](https://blog.documentfoundation.org/blog/2016/12/21/the-document-foundation-announces-the-muffin-a-new-tasty-user-interface-concept-for-libreoffice/) added a variety of flexibility options for LO developers, including the ability to bundle icon themes in extension format.
The procedure includes creating a typical extension and adding the `.zip` archive, thoroughly described at the [TDF wiki](https://design.blog.documentfoundation.org/2017/10/23/how-to-bundle-icon-themes/).

Using this approach, there is no need to implement uninstall scripts because the built-in Extension Manager handles such operations. Additionally, more than one icon themes can be included in a single extension and using .oxt format makes the customizations ready to be shared through the official [Extensions website](http://extensions.libreoffice.org/).

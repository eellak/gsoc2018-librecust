#!/bin/bash

#[ "$UID" -eq 0 ] || exec sudo bash "$0" "$@" #if we decide superuser execution

# Define a timestamp function
timestamp() {
  date +"%d%m%y_%H%M" #FORMAT DayMonthYear_HoursMinutes
}

WORKING_DIR="$(pwd)"
UNOPKG_PATH="$(which unopkg)"
LIBRECUST_MACRO_PATH="$(realpath ../)/menu_customization/macros/LibreCustLib.oxt"
SETTINGS_LOADER_PATH="$(realpath ../)/settings_loader/settings_loader.oxt"
PAGE_NUMBERING_PATH="$(realpath ../)/page_numbering_addon/LibreOffice/python/build_files/PageNumberingAddonPython-0.0.1.oxt"
AUTOTEXT_PATH="$(realpath ../)/autotext_addon/LibreOffice/sidebar_version/build_files/AutotextAddon-0.0.1.oxt"
LAWADDON_PATH="$(realpath ../)/law_addon/LibreOffice/build_files/LawAddon-0.0.1.oxt"
MENUBAR_PATH="$(realpath ../)/menu_customization/menubar/menubar.xml"
TOOLBAR_PATH="$(realpath ../)/menu_customization/toolbar"
USER_HOME_PATH="$(eval echo "~$different_user")"
USER_PROFILE_PATH="$USER_HOME_PATH/.config/libreoffice/4/user/config/"
ICON_THEME_PATH="$TOOLBAR_PATH/icon_theme"
LIBRE_LIB_CONFIG_PATH="/usr/lib/libreoffice/share/config/"
INSTALLATION_TIMESTAMP="$(timestamp)"

echo "▌  ▗ ▌        ▌
▌  ▄ ▛▀▖▙▀▖▞▀▖▌  ▝▀▖▌  ▌
▌  ▐ ▌ ▌▌  ▛▀ ▌  ▞▀▌▐▐▐
▀▀▘▀▘▀▀ ▘  ▝▀▘▀▀▘▝▀▘ ▘▘"
echo "LibreLaw project install client"

echo "In order to install LibreLaw, all instances of Libreoffice should be terminated"
echo "Please save your active documents before proceeding with the LibreOffice process termination"

read -p "Terminate LibreOffice? [y/n] " -n 1 -r
echo    # (optional) move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "Installation Failed: exiting"
    exit 1
fi

killall soffice.bin

#--------------------------------------------------------------------------------
# Librecust macro library
#--------------------------------------------------------------------------------
read -p "Install macro library (Librecust.oxt)? [y/n] " -n 1 -r
echo    # (optional) move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "Installation Failed: exiting"
    exit 1
fi

eval $UNOPKG_PATH gui $LIBRECUST_MACRO_PATH 

#--------------------------------------------------------------------------------
# Settings Loader
#--------------------------------------------------------------------------------
read -p "Install Settings Loader (settings_loader.oxt)? [y/n] " -n 1 -r
echo    # (optional) move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "Installation Failed: exiting"
    exit 1
fi

eval $UNOPKG_PATH gui $SETTINGS_LOADER_PATH 

#--------------------------------------------------------------------------------
# Page Numbering
#--------------------------------------------------------------------------------
read -p "Install Page Numbering Addon (PageNumberingAddon.oxt)? [y/n] " -n 1 -r
echo    # (optional) move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "Installation Failed: exiting"
    exit 1
fi

eval $UNOPKG_PATH gui $PAGE_NUMBERING_PATH

#--------------------------------------------------------------------------------
# AutoText Addon
#--------------------------------------------------------------------------------
read -p "Install AutoText Addon (AutoTextAddon.oxt)? [y/n] " -n 1 -r
echo    # (optional) move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "Installation Failed: exiting"
    exit 1
fi

eval $UNOPKG_PATH gui $AUTOTEXT_PATH #unopkg gui because it is licensed and unopkg crashes when used with such extensions

#--------------------------------------------------------------------------------
# Law Addon
#--------------------------------------------------------------------------------
read -p "Install Law Toolbar (LawAddon.oxt)? [y/n] " -n 1 -r
echo    # (optional) move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "Installation Failed: exiting"
    exit 1
fi

eval $UNOPKG_PATH gui $LAWADDON_PATH #unopkg gui because it is licensed and unopkg crashes when used with such extensions

#--------------------------------------------------------------------------------
# Menu Bar
#--------------------------------------------------------------------------------

#Then we have to copy menubar after we backup previous menubar configuration with timestamp

read -p "Install Modified menubar (menubar.xml)? [y/n] " -n 1 -r
echo    # (optional) move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "Installation Failed: exiting"
    exit 1
fi

# Backup current configuration and name it using timestamp for future reference
cd "$USER_PROFILE_PATH/soffice.cfg/modules/swriter/menubar/"
cp ./menubar.xml "./menubar.xml.bak_$INSTALLATION_TIMESTAMP"

# Copy customized menubar.xml
cp $MENUBAR_PATH ./menubar.xml

cd $WORKING_DIR #return to installer.sh path

#--------------------------------------------------------------------------------
# Toolbar
#--------------------------------------------------------------------------------

#Then we have to copy toolbars while backing up previous config
read -p "Install Modified toolbars (toolbar/*.xml)? [y/n] " -n 1 -r
echo    # (optional) move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "Installation Failed: exiting"
    exit 1
fi

# Backup current configuration and name it using timestamp for future reference
cd "$USER_PROFILE_PATH/soffice.cfg/modules/swriter/toolbar/"
mkdir "toolbar_bak_$INSTALLATION_TIMESTAMP"

cp ./*.xml "./toolbar_bak_$INSTALLATION_TIMESTAMP/"

# Copy customized toolbars to User Profile
cp "$TOOLBAR_PATH"/*.xml ./

#--------------------------------------------------------------------------------
# Icon theme
#--------------------------------------------------------------------------------

#Install icon theme (LibreOffice 5 needs the .zip file copied to install_dir. Version 6 allows bundling an icon theme in extension format)
read -p "Install Office 2013 icon theme by charliecnr (toolbar/icon_theme/)? [y/n] " -n 1 -r
echo    # (optional) move to a new line
if [[ ! $REPLY =~ ^[Yy]$ ]]
then
    echo "Installation Failed: exiting"
    exit 1
fi

# Copy icon theme
sudo cp "$ICON_THEME_PATH"/*.zip $LIBRE_LIB_CONFIG_PATH


#Then we have to create desired file structure and copy templates

#Finaly we have to install the main Librelaw oxt extension


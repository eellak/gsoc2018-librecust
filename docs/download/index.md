---
layout: default
title: Download
---



<div class="container">
    <h2 class="header-light regular-pad">Download Librecust</h2>
    <hr>
<div markdown="1">
Before downloading any of the extensions, please consider the [requirements]({{ "/docs/Installation/#requirements" | prepend: site.baseurl }}).

Download and install the complete Librecust package (either way is interactive giving the ability to choose the modules to be installed):
</div>
    <div class="row">
    <div class="col-md-6">
        <div class="panel panel-primary">
            <div class="panel-heading">Latest release</div>
            <div class="panel-body">                
<div markdown="1">
Download latest release from Github repository.
```bash
git clone https://github.com/eellak/gsoc2018-librecust.git
```
For Installation instructions visit the [docs]({{ "/docs/Installation" | prepend: site.baseurl }}).
</div>

            </div>
        </div>
    </div>
    <div class="col-md-6">
        <div class="panel panel-info">
            <div class="panel-heading">Through apt repo</div>
            <div class="panel-body">
<div markdown="1">
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
</div>
            </div>
        </div>
    </div>
    </div>

    <h3 class="header-light regular-pad">Standalone Extensions</h3>
    <hr>
<div markdown="1">
Before downloading any of the extensions, please consider the [requirements]({{ "/docs/Installation/#requirements" | prepend: site.baseurl }}).
</div>

    <div class="row">
    <div class="col-md-4">
        <div class="panel panel-primary">
            <div class="panel-heading">Page Numbering Addon</div>
            <div class="panel-body">                
<div markdown="1">
Download latest release from Github repository.
* [0.0.1](https://github.com/eellak/gsoc2018-librecust/raw/master/page_numbering_addon/LibreOffice/python/build_files/PageNumberingAddonPython-0.0.1.oxt) (LibreOffice)
* [0.0.1](https://github.com/eellak/gsoc2018-librecust/raw/master/page_numbering_addon/OpenOffice/python/build_files/PageNumberingAddonPython-A-0.0.1.oxt) (Apache OpenOffice)
</div>

            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="panel panel-info">
            <div class="panel-heading">AutoText Addon</div>
            <div class="panel-body">
<div markdown="1">
Download latest release from Github repository.
* [0.0.1](https://github.com/eellak/gsoc2018-librecust/raw/master/autotext_addon/LibreOffice/sidebar_version/build_files/AutotextAddon-0.0.1.oxt) (LibreOffice | Sidebar version)
* [0.0.1](https://github.com/eellak/gsoc2018-librecust/raw/master/autotext_addon/LibreOffice/toolbar_version/build_files/AutotextAddon-0.0.1.oxt) (LibreOffice | Toolbar version)
</div>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="panel panel-success">
            <div class="panel-heading">Law Toolbar</div>
            <div class="panel-body">
<div markdown="1">
Download latest release from Github repository.
* [0.0.1](https://github.com/eellak/gsoc2018-librecust/raw/master/law_addon/LibreOffice/build_files/LawAddon-0.0.1.oxt) (LibreOffice)
* [0.0.1](https://github.com/eellak/gsoc2018-librecust/raw/master/law_addon/LibreOffice/build_files/LawAddon-A-0.0.1.oxt) (Apache OpenOffice)
</div>
            </div>
        </div>
    </div>
    </div>

    <h3 class="header-light regular-pad">UI customizations</h3>
        <div class="row">
    <div class="col-md-4">
        <div class="panel panel-primary">
            <div class="panel-heading">Menu Bar</div>
            <div class="panel-body">                
<div markdown="1">
Download latest xml from Github repository:
* [menubar.xml](https://github.com/eellak/gsoc2018-librecust/raw/master/menu_customization/menubar/menubar.xml)

Then copy to User directory:

```bash
cp ./menubar.xml "$USER_PROFILE_PATH/soffice.cfg/modules/swriter/menubar/"
```

<span class="label label-warning">Warning</span> Currently, only EL locale modifications available.
</div>

            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="panel panel-info">
            <div class="panel-heading">Tool Bar</div>
            <div class="panel-body">
<div markdown="1">
Download latest release from Github repository.
* [singlemode.xml](https://github.com/eellak/gsoc2018-librecust/raw/master/menu_customization/toolbar/singlemode.xml)
* [textobjectbar.xml](https://github.com/eellak/gsoc2018-librecust/raw/master/menu_customization/toolbar/textobjectbar.xml)

Then copy to User directory:

```bash
cp ./*.xml "$USER_PROFILE_PATH/soffice.cfg/modules/swriter/toolbar/"
```

</div>
            </div>
        </div>
    </div>
    <div class="col-md-4">
        <div class="panel panel-success">
            <div class="panel-heading">Icon set</div>
            <div class="panel-body">
<div markdown="1">
Download latest release from [@charliecnr](https://www.deviantart.com/charliecnr) deviantart [page](https://www.deviantart.com/charliecnr/art/Office-2013-theme-for-LibreOffice-512127527).
</div>
            </div>
        </div>
    </div>
    </div>

</div>

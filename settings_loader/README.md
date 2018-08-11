# Settings Loader

This extension is a way to deploy certain configurations to LibreOffice. Such configurations, otherwise options, are usually enabled by the user (e.g. UI Locale, icon theme and others).
Documentation regarding the structure of such extension can be found at the following sources:
1. [Thorsten Behrens slides](http://www.linuxtag.org/2012/fileadmin/www.linuxtag.org/slides/Thorsten%20Behrens%20-%20LibreOffice%20configuration%20management%20-%20Tools_%20approaches%20and%20best%20practices.p331.pdf)
2. [TDF wiki](https://wiki.documentfoundation.org/images/b/b0/LibreOffice_config_extension_writing.pdf)
3. [Librecust wiki](https://github.com/eellak/gsoc2018-librecust/wiki/Configuration-extension) page for configuration extension development.

Following the previous guides, configure the files included in the extension directory. When ready, execute the following:

```bash
bash ./dir_to_oxt.sh 
```

The settings_loader.oxt file is the extension to be installed for configuration deployment.

---
title: Debugging
permalink: /docs/Debugging/
---

In this page, the steps relevant to debugging that where followed during the project are included. 

## Inspecting
Developing LibreOffice extensions is pretty difficult with all those terms like interfaces, services, contexts and others. This is why many developers where concerned and finally developed extensions that provide info about the state of document and API elements. Currently, the two most famous and feature complete extensions are the following:
* [MRI](https://extensions.libreoffice.org/extensions/mri-uno-object-inspection-tool)
* [Xray](http://berma.pagesperso-orange.fr/index2.html)

While most of developers prefer the MRI inspection tool, we weren't able to setup it properly so we used and afterwards documented the alternative Xray tool.

### Installing 
In order to use Xray for either implementation (Basic, Python), installing the Xray extension is required following the next steps:
* Download the appropriate language `.odt`. The installation macros are embedded in this document
* Make sure that macro safety is set to minimum from LibreOffice Options
* Press `Install Xray`

## Xray on Basic
While developing a macro, in order to inspect an object, a call to xray with this object as argument is required:
```vb
Sub Main

Doc = ThisComponent
ParagraphStyles = Doc.StyleFamilies.getByName("ParagraphStyles")
OldStyle = ParagraphStyles.getByName("Heading 1")
' get current cursor style name / set with the same 
ThisComponent.CurrentController.ViewCursor.ParaStyleName = "Heading 1"
xray OldStyle
End Sub

sub insert_hd1()
    Doc = ThisComponent
    UndoManager = Doc.getUndoManager()
    
    ParagraphStyles = Doc.StyleFamilies.getByName("ParagraphStyles")
    
REM get current cursor position
    ViewCursor = Doc.CurrentController.getViewCursor()
    

    UndoManager.enterUndoContext("Change Paragraph style")
    
    ViewCursor.ParaStyleName = "Heading 1"

    UndoManager.leaveUndoContext()

end sub
```
In the previous example, we inspect the current cursor paragraph style for methods and documents with the following result.  

![XrayStyle](https://i.imgur.com/4IQiAOD.png)   

## Xray on Python
On Python, the steps required to inspect an element with Xray are more or less the same with the Basic implementation. However, there are some differences that we should point out. 
```python
import uno
import unohelper

def xray(smgr, ctx, target):
    mspf = smgr.createInstanceWithContext(
        "com.sun.star.script.provider.MasterScriptProviderFactory", ctx)
    script_provider = mspf.createScriptProvider("")
    script = script_provider.getScript(
        "vnd.sun.star.script:XrayTool._Main.Xray?language=Basic&location=application")
    script.invoke((target,), (), ())

def main(*args):
    ctx = uno.getComponentContext()
    smgr = ctx.ServiceManager

    Doc = XSCRIPTCONTEXT.getDocument()
    ParagraphStyles = Doc.StyleFamilies.getByName("ParagraphStyles")
    OldStyle = ParagraphStyles.getByName("Heading 1")
    xray(smgr, ctx, OldStyle)
```

The same window as before is produced.
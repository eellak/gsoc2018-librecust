---
title: Page Numbering Addon
permalink: /docs/Page-Numbering-Addon/
---

During this project, among other extensions, we created an addon to simplify the process of page numbering in LIbreOffice and OpenOffice. With the term addon, we refer to an extension that includes a Graphic User Interface end. 

## Motivation
A reasonable question would be why such an addon is needed, considering the fact that LibreOffice has already implemented a superset of other editor's functionality, including page numbering.


In order to add simple page numbering to a document in LibreOffice, you have to understand the whole page styling mechanism, when footers are enabled and for how many pages dows a page style range extend. In addition to this, a whole and complete understanding of page breaks and page offsets is required in order to achieve something seemingly straightforward, numbering that starts from a following of the first page with counting initiating from a greater than "1" value. 
## Introduction
At this point we should take a look at the final dialog, and consider the functionality that must be included in our extension:

![Dialog](https://i.imgur.com/mKqsgTs.png)   

Aformentioned properties and functionality is shown above, while maintaining a simple user interface.

## Implementation
During the first period of our GSOC project, we decided to implement this addon in two languages, LO Basic and Python. We should now justify this choice. 
### LO Basic
This is one of the first languages that supported OpenOffice and LibreOffice API communication through macro scripts. The majority of documentation sources are Basic specific and this is by no means something inexplicable. OpenOffice and LibreOffice suites include a Basic IDE for editing and debugging macros. Additionally, LibreOffice eases the distribution of such basic macros, giving the option to either attach macros to specific documents or install them globally to the suite.

However, the main advantage of Basic macros that leads to their popularity over other implementations is the fact that the whole API is manipulated with an abstract model. When other languages use interfaces that have to be implemented in order to use API methods, Basic macros have services that directly include all of those methods. Moreover, accessing open instances of LibreOffice is straightforward comparing to other languages that have to develop complex code in order to acquire a remote component context.
### Python and others
While Basic macros are easier to construct, this level of abstraction comes with some disadvantages a programmer has to take into account while deciding the final implementation language. Basic is by no means a full featured language. Scaling a Basic macro can be difficult and debugging is not as simple as in other modern languages.
 
Basic was firstly introduced to support inter-compatibility across OpenOffice and Microsoft Office macro scripts attached to documents. This means that VBA coding principles characterize Basic macros. 

Using Basic leads to many "reinventing-the-wheel" situations. Sorting algorithms, optimized dictionaries and other structs have to be written from scratch, sacrificing performance and stability of large scale LibreOffice extensions. 
In addition to these, Basic coding standards do not appeal to new programmers. This means that documentation is fairly old and supported only by those people that managed to get familiar with Basic's standards. Trying to get help for a Basic implementation clearly reveals the aforementioned drawback. At this point we should mention that there is a great amount of people willing to help with macro coding mainly at the following forums:
* [OpenOffice Forum](https://forum.openoffice.org/en/forum/)      
* [Ask LibreOffice](https://ask.libreoffice.org/en/questions/)     

Taking into consideration all of the following points, we decided to prototype our addons using Basic macro scripting and then port the implementation to Python for the finalized version.

## Algorithm description
Hereupon, we will outline the algorithm that is followed to insert page numbering in current document. In order to better explain the whole procedure we should state the steps that should be followed by a user to insert page numbering starting from the n-th page with offset of p.
The first pages that will not have numbering should follow a page style different than the page style followed by the numbered pages. A page style extends to the next page break inserted by the user. The offset is defined while inserting a manual page break.
1. The user decides what page style will be followed by each of the two ranges (numbered - not numbered). 
2. The unnumbered range starts from the first page so this will be defined by clicking on the first page and assigning the correct page style (assuming this is the Standard Page Style).
3. Creation of numbered range page style. Frequently, the user just wants a standard page style with a footer enabled. This requires the support for copying and cloning page styles or style inheritance that is not, at the time of wiki compiling, an implemented feature. We tackle this particular problem by creating a new style and copying the whole property set(more on this including later).
4. Then a manual break is inserted by Insert->Manual Break menu option. As style in the dropdown we define the newly created one.
5. On the same dialog the "Change page number" option is enabled and p is inserted as value.
6. THe user should edit the footer and add a "Page Number" field.

It is often for documents to require two or more page numbering ranges. This procedure is followed for every numbered range and a new page style is created for every range.

As we can see, inserting page numbering in LibreOffice Writer is not as simple as it should be.

## Connection between user steps and code
### Access current document
This addon adds page numbering on the current document. In order to access the current document, we use the following code:

**Basic**
```vba
Doc = ThisComponent
```
**Python**
```Python
Doc = XSCRIPTCONTEXT.getDocument()
```
Then we get access to the Undo Manager interface. This struct allows multiple edit actions to be included in one undo step in the undo stack giving the illusion that the whole page numbering process is just one step.

**Basic**
```vba
UndoManager = Doc.getUndoManager()
```
**Python**
```Python
UndoManager = Doc.getUndoManager()
```
### Creating dialogs
Now is the time to initialize the graphical end of the addon, so as to get input for the numbering. We choose to edit and create a new dialog using the included dialog editor (Tools->Macros->Organize Dialogs...). Available dialog elements are documented in the OpenOffice [wiki](https://wiki.openoffice.org/wiki/Documentation/BASIC_Guide/Control_Elements). 
Our dialog consists of: 
* Eight labels, one for each component
* Two Buttons (OK and Cancel)
* Two Combo Box elements (Decor and Type)
* Three List Box elements (Alignment, Position and Font)
* Three Numeric Fields (Size, First Page and Page Offset)

The dialog is saved and/or exported in `.xdl` format. This file will be included and installed with the final extension.

In order to fill components with data, one should first access the dialog. This is done using the following code:

**Basic**
```vba
	DialogLibraries.LoadLibrary("PageNumberingAddon")
	oLib = DialogLibraries.GetByName("PageNumberingAddon")
	myDlg = oLib.GetByName("PageNumberingDialog")
	oDlg = CreateUnoDialog(myDlg)
```
**Python**
```Python
    psm = uno.getComponentContext().ServiceManager
    dp = psm.createInstance("com.sun.star.awt.DialogProvider")
    dlg = dp.createDialog("vnd.sun.star.script:dialogs.PageNumberingDialog?location=application")
```
Notice that in Basic code, we include the dialog in the PageNumberingAddon library while in Python we use the dialogs, library. This is just a choice of ours, the user can choose to save dialogs in the desired library. In any case, accessing and editing components requires the use of dialog model.

**Basic**
```vba
oDialog1Model = oDlg.Model
```
**Python**
```Python
oDialog1Model = dlg.Model
```
During prototyping of the addon (Basic implementation), we initiated the dialog fields using a [top window listener](https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1awt_1_1XTopWindowListener.html). This fires the execution of certain methods when an event such as "window minimized" is traced. A flag is used to check whether the dialog was closed, canceled or the data is valid and further execution is mandatory. However, during Python porting, we choose to initialize all fields and respective data before executing the dialog.    

For the sake of completeness, the steps followed to create a top window listener are described in the according wiki [page](https://github.com/eellak/gsoc2018-librecust/wiki/Event-listeners#window-listeners).
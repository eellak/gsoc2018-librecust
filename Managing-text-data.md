# Managing and traversing text data
In order to apply text changes and traverse text data, the main iterators used by LibreOffice/OpenOffice are named cursors, in correspondence to the UI cursors in text editing.

For this addon, two kinds of cursors are used:
* [View Cursor](https://github.com/eellak/gsoc2018-librecust/wiki/Managing-text-data#view-cursors), [official wiki](https://wiki.openoffice.org/wiki/Writer/API/View_cursor)
* [Text Cursor](https://github.com/eellak/gsoc2018-librecust/wiki/Managing-text-data#text-cursors)


## View Cursors
A view cursor, in terms of LO/OO API, is used to move across the page layout. This cursor is equivalent to the cursor shown in the UI. For this purpose, only one View cursor is instantiated in scripts, as one cursor is show to the user while editing a document. In this extension, we use View cursors to change page properties, while moving across pages, adding manual page breaks and altering page styles. 

View cursor reference in Basic and Python:
### Basic
```Basic
    ViewCursor = Doc.CurrentController.getViewCursor()
```
### Python
```Python
    Doc = XSCRIPTCONTEXT.getDocument()
    ViewCursor = Doc.CurrentController.getViewCursor()
```
There is a variety of View cursors in LO API, which, mainly because of the abstraction layer of Basic and Python, provide methods accessible through the getViewCursor() method [1]


| Interface     | Description   |
| ------------- | ------------- |
| com.sun.star.view.XViewCursor | Simple cursor with basic movement methods that work in both text and tables |
| com.sun.star.text.XTextViewCursor | Derived from XTextCursor, this describes a cursor in a text document’s view. It supports only very simple movements |
| com.sun.star.view.XLineCursor | Defines line-related methods; this interface is not derived from a text range. |
| com.sun.star.text.XPageCursor | Defines page-related methods; this interface is not derived from a text range. |
| com.sun.star.view.XScreenCursor | Defines methods to move up and down one screen at a time. |

In order to add manual page breaks, we need to move across pages using XPageCursor methods:

### Basic
```Basic
    ViewCursor.jumpToPage(int Arg1) 
```

### Python
```Python
     ViewCursor.jumpToPage(int Arg1)
```

## Changing Page Style

### Accessing Page Style
Accessing the current page style requires getting the [style](https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1style_1_1PageStyle.html) from the current View cursor with identical approach in Basic and Python

`CurrentStyleName = ViewCursor.PageStyleName`

## Creating Manual Page Break
In order to create a manual page break, one has to change the PageDescName property of the first page following the break. Additionally, as shown in the dialog generated when inserting a manual break, one can define a new page number for the following page range.
A page range is defined as the number of pages between two page breaks or a page break and start/end of document. A page style is a property of a range. 
Adding a manual page break at the n-th page:
```Python
# Set index of first numbered page
# We cannot use PageNumber.Offset property because we may need bigger than total page number indexing
ViewCursor.jumpToPage(n)
ViewCursor.PageNumberOffset = n

# Every numbered page will be of Standard Page style for now
ViewCursor.PageDescName = “Standard”
```

Page style names can be accessed using the following method calls:
`PageStyles = Doc.StyleFamilies.getByName("PageStyles")`

PageStyle is of type [StyleFamily](https://api.libreoffice.org/docs/idl/ref/servicecom_1_1sun_1_1star_1_1style_1_1StyleFamilies.html). Using the documentation, we spot a method called .getElementNames(). 

After we get the string name of a PageStyle we can get its object and property set using the following call:
`NewStyle = PageStyles.getByName(“StyleName”)`

The process of cloning page styles is described in Page Style Cloning(link) wiki page

While inserting content using a view cursor is possible, for non trivial operations using Text cursors is advised 

## Text cursors
As far as data is concerned, view cursors have minimum interaction in comparison to Text cursors. The latter can only move within specific text ranges, but is not restricted to viewable content like the former. Multiple text cursors are allowed for one document. XTextCursor interface is implemented from a set of interfaces including[1]:

| Interface     | Description   |
| ------------- | ------------- |
| com.sun.star.text.XTextCursor | The primary text cursor that defines simple movement methods |
| com.sun.star.text.XWordCursor | Provides word-related movement and testing methods |
| com.sun.star.text.XSentenceCursor | Provides sentence-related movement and testing methods |
| com.sun.star.text.XParagraphCursor | Provides paragraph-related movement and testing methods |
| com.sun.star.text.XTextViewCursor | Derived from XTextCursor, this describes a cursor in a text document’s view |

Getting a text cursor requires the acquisition of ViewCursor

`oCursor = ViewCursor.getText().createTextCursorByRange(ViewCursor)`

However, page styles provide specific text ranges for Header and Footer locations, a feature used in Page Numbering Addon:

```Python
#Header text
 Num_Position = NumberedPage.HeaderText

#Footer text
Num_Position = NumberedPage.FooterText
```
After getting the required text range, a text cursor for data interaction is acquired:
`NumCursor = Num_Position.Text.createTextCursor()`

## Inserting content
Num_Position object implements the [XText](https://api.libreoffice.org/docs/idl/ref/interfacecom_1_1sun_1_1star_1_1text_1_1XText.html)  interface, allowing for text content insertion/deletion using specific methods. As far as Page Numbering Addon is concerned, these methods are used as following:

### Basic
```Basic
‘ NumberingDecorationComboBox is a dialog element that provides a decoration string value.
‘ PageNumber is a specific field that represents page numbering LO struct. 

    Select Case NumberingDecorationComboBox.Text
        Case "#"
            Num_Position.insertTextContent(NumCursor, PageNumber, False)
        Case "-#-"
            Num_Position.insertString(NumCursor, "-", False)
            Num_Position.insertTextContent(NumCursor, PageNumber, False)
            Num_Position.insertString(NumCursor, "-", False)
        Case "[#]"
            Num_Position.insertString(NumCursor, "[", False)
            Num_Position.insertTextContent(NumCursor, PageNumber, False)
            Num_Position.insertString(NumCursor, "]", False)
        Case "(#)"
            Num_Position.insertString(NumCursor, "(", False)
            Num_Position.insertTextContent(NumCursor, PageNumber, False)
            Num_Position.insertString(NumCursor, ")", False)
        Case Else
            Print "Custom decoration unimplemented feature"
    End Select
```
### Python
```Python
# NumberingDecorationComboBoxText object is a dialog control that provides decoration option
NumberingDecorationComboBoxText = oDialog1Model.getByName(
        "NumberingDecoration").Text

    if NumberingDecorationComboBoxText == "#":
        Num_Position.insertTextContent(NumCursor, PageNumber, False)
    elif NumberingDecorationComboBoxText == "-#-":
        Num_Position.insertString(NumCursor, "-", False)
        Num_Position.insertTextContent(NumCursor, PageNumber, False)
        Num_Position.insertString(NumCursor, "-", False)
    elif NumberingDecorationComboBoxText == "[#]":
        Num_Position.insertString(NumCursor, "[", False)
        Num_Position.insertTextContent(NumCursor, PageNumber, False)
        Num_Position.insertString(NumCursor, "]", False)
    elif NumberingDecorationComboBoxText == "(#)":
        Num_Position.insertString(NumCursor, "(", False)
        Num_Position.insertTextContent(NumCursor, PageNumber, False)
        Num_Position.insertString(NumCursor, ")", False)
    else:
        raise Exception("Custom decoration unimplemented feature")
```

More on Cursors on Andrew Pitonyak ’s [OpenOffice.org Macros Explained](http://www.pitonyak.org/book/) book 

[1] Andrew Pitonyak ’s [OpenOffice.org Macros Explained](http://www.pitonyak.org/book/) book
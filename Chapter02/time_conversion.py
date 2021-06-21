"""Small example of changes to QDateTime in PyQt6 
Similar changes can also be found in QDate and QTime

PyQt QDateTime documentation:
https://www.riverbankcomputing.com/static/Docs/PyQt6/api/qtcore/qdatetime.html
Qt QDateTime documentation:
https://doc.qt.io/qt-6/qdatetime.html

Building Custom UIs with PyQt with Packt Publishing
Chapter 2 - Building the Foundation for GUIs
Created by: Joshua Willman
"""

from PyQt6.QtCore import Qt, QDateTime, QLocale

# Get your current date and time
date_time = QDateTime.currentDateTime()

# To return the current date and time as a string, use 
# toString() and pass a format parameter (either a Qt.DateFormat 
# enum or a format string.)

# Print the ISO time format using Qt.DateFormat enums
print("ISO Date:")
print(date_time.toString(Qt.DateFormat.ISODate) + "\n")
# Output:
# 2021-06-21T14:35:01

# Support of localized dates using the enum Qt.DateFormat, 
# such as SystemLocaleDate, LocaleDate, DefaultLocaleLongDate, etc.,
# have been removed in PyQt6 and replaced with QLocale methods. The 
# following lines demonstrate how to print out short and long time formats.
# QLocale.system() is a QLocale object initialized by the system locale
print("QLocale.FormatType.ShortFormat:")
print(QLocale.system().toString(date_time, QLocale.FormatType.ShortFormat))

print("QLocale.FormatType.LongFormat:")
print(QLocale.system().toString(date_time, QLocale.FormatType.LongFormat) + "\n")

# Of course, the same formatting can also be achieved using format strings
print("Format string, Short:")
print(date_time.toString("M/dd/yy h:mm AP"))

print("Format string, Long:")
print(date_time.toString("MMMM dd, yyyy h:mm:ss AP t") + "\n")

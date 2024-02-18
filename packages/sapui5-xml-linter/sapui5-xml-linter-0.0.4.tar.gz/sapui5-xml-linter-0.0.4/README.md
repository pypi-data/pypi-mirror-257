# SAP UI5 View XML Linter

This is a Python script that checks your view XML files and removes attributes
that have the default value set. This can happen when your view files come out
of a design platform like SAP Build.

Usage:

Do this once to download the API files for SAPUI5:

```
./sapui5-xml-linter -u
```

Thene, everytime you want to check yout files, run this command:

```
./sapui5-xml-linter /path-to-project/webapp/view
```

(substitute the path with the folder where your xml view files reside)

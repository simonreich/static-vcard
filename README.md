# Program

This program reads 
    template/header.html
    template/footer.html
    pages/*/*.n
    static/*

where n is an integer >=0. 
The example page out/name-of-page.html will be formatted as
    template/header.html
    pages/name-of-page.html/*.0
    pages/name-of-page.html/*.1
    pages/name-of-page.html/*.2
    ...
    template/footer.html

The resulting files will be placed in folder out/.

# License

Copyright (C) 2018 Simon Reich. Licensed under the GPL (see the license file).

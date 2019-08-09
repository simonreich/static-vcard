# Program

This program reads 
    template/header.html
    template/footer.html
    pages/*.n1/*.n2
    static/*

where `n1` and `n2` are integers `>=0`. 
The example page `out/name-of-page.html` will contain the following parts
    template/header.html
    pages/name-of-page.html.1/*.0
    pages/name-of-page.html.1/*.1
    pages/name-of-page.html.1/*.2
    ...
    template/footer.html

All files from the `static/` folder will be copied to `out/. All generated html files will also be placed in the folder `out/`.

## Page navigation bar

If there are more than 2 pages in total, a page navigation bar will be created. This bar will be sorted according to `n1` (the integer following the page name). A page called either `index.html`, `index.htm`, or `index.php` will always be renamed to `Home`. Pages named `impressum.html`, `impressum.htm`, or `impressum.php` will always be omitted (I usually place a link to this page in the footer - hence it is not shown in the navigation bar).

## Section navigation bar

If there is more than 1 section on a page, a section navigation bar will be created. This bar will be sorted according to `n2` (the integer following the section name).

# License

Copyright (C) 2018-2019 Simon Reich. Licensed under the GPL (see the license file).

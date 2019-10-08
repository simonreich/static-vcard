# Program

This script is a bare bone content management system (cms) and a static site generator. It glues pieces of html code together to form a web page.

# File Structure

This program reads the following files:

1. `template/header.html`
2. `template/footer.html`
3. `pages/*.n1/*.n2`
4. `static/*`

where `n1` and `n2` are integers `>=0`. 

# Site Generation

First, let's look at an example. Assume the following files:

1. `template/header.html`
2. `template/footer.html`
3. `pages/index.html.0/Section 1.1`
4. `pages/index.html.0/Example 2.2`
5. `pages/index.html.0/Results.3`
6. `pages/Test & Simulation.html.1/Reading.1`
7. `pages/Test & Simulation.html.1/Simulation 1.2`
8. `pages/Test & Simulation.html.1/Simulation 2.3`
9. `static/empty.css`

The output will be placed into the `out` folder. The above example will create three files:

1. `out/index.html`
  1. `template/header.html`
  2. `pages/index.html.0/Section 1.1`
  3. `pages/index.html.0/Example 2.2`
  4. `pages/index.html.0/Results.3`
  5. `template/footer.html`
2. `out/Test & Simulation.html`
  1. `template/header.html`
  2. `pages/Test & Simulation.html.1/Reading.1`
  3. `pages/Test & Simulation.html.1/Simulation 1.2`
  4. `pages/Test & Simulation.html.1/Simulation 2.3`
  5. `template/footer.html`
3. `out/empty.css`

Files from the `pages` folder will consist of three parts. First, the html code from `template/header.html` is copied. Second, html code from the sections of each page is appended. Last, the file `template/footer.html` is added. Additionally, a navigation bar is created for each page and each section.

Pages from the `static` folder will be copied into the `out` folder (after html creation).

## Page navigation bar

If there are more than 2 pages in total, a page navigation bar will be created. This bar will be sorted according to `n1` (the integer following the page name). A page called either `index.html`, `index.htm`, or `index.php` will always be renamed to `Home`. Pages named `impressum.html`, `impressum.htm`, or `impressum.php` will always be omitted (I usually place a link to this page in the footer - hence it is not shown in the navigation bar).

## Section navigation bar

If there is more than 1 section on a page, a section navigation bar will be created. This bar will be sorted according to `n2` (the integer following the section name).

# License

Copyright (C) 2018-2019 Simon Reich. Licensed under the GPL (see the license file).

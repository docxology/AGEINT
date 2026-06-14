```latex
% AGEINT preamble: compact dense atlas — smaller font, smaller margins, red links.
\usepackage{booktabs}
\usepackage{longtable}
\usepackage{xcolor}
\usepackage{scrextend}
\changefontsizes[8.9pt]{7.8pt}
\setlength{\parskip}{0.15em}
\renewcommand{\arraystretch}{0.88}
\setlength{\LTpre}{2pt}
\setlength{\LTpost}{2pt}
\geometry{margin=0.5in}
\setcounter{tocdepth}{2}
\makeatletter
\renewcommand*\l@section{\@dottedtocline{1}{1.5em}{3.4em}}
\renewcommand*\l@subsection{\@dottedtocline{2}{3.8em}{5.2em}}
\renewcommand*\l@subsubsection{\@dottedtocline{3}{7.2em}{6.2em}}
\makeatother
\definecolor{ageintred}{HTML}{C00000}
\hypersetup{colorlinks=true, linkcolor=ageintred, urlcolor=ageintred, citecolor=ageintred, anchorcolor=ageintred, filecolor=ageintred, menucolor=ageintred}
```

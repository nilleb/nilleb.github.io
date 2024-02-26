---
title: "Lingua Italiana, LaTeX e UTF-8"
date: "2006-01-26"
categories: 
  - "computer-science"
  - "thoughts"
tags: 
  - "everydays"
---

Era tutto ieri e tutta stamattina che impazzivo alla ricerca di una soluzione per quelle strane lettere accentate che comparivano nella versione DVI della mia tesi.. Sintomo molto strano, dato che aprendo il file con qualsiasi editor, compreso vi, riuscivo invece a vedere le lettere corrette. Ciò che mi ha aperto gli occhi è stato _cat_, con la sua semplicità. C'è voluto un attimo, poi, a capire che si trattava della codifica del file. Tutti gli editor riconoscevano il formato come utf8, e lo formattano come richiesto. Invece, il misero cat non riconosceva le indicazioni di formato.. E neppure LaTeX, nel suo vano tentativo di compilare i miei comandi. In giro sulla rete in tanti si prodigano di consigli e istruzoni su come risolvere il problema, ma Gentoo l'ha risolto brillantemente e con pochissimo sforzo da parte mia. Un `emerge latex-unicode` è bastato ad installare le librerie corrette. Ed un `\usepackage[utf8x]{inputenc} \usepackage[italian,english]{babel}` sistemato nel preambolo del mio file hanno fatto il resto. Ora posso smettere di usare le sequenze di escape (\\'e == é) e scrivere le bellissime lettere accentate della lingua italiana! :-)

**Riferimenti**

- Gentoo Wiki a proposito della configurazione di Unicode [§](http://gentoo-wiki.com/HOWTO_Make_your_system_use_unicode/utf-8)
- Pagina del CTAN a proposito del modulo Unicode [§](http://ctan.org/info?id=unicode)
- Unicode FAQ [§](http://www.cl.cam.ac.uk/~mgk25/unicode.html)

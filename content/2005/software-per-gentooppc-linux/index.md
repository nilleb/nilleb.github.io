---
title: "Software per Gentoo/PPC Linux"
date: 2005-12-31
categories: 
  - "computer-science"
  - "thoughts"
tags: 
  - "everydays"
---

Il sistema operativo che uso è Linux, e l'architettura del mio portatile è PowerPC. In parole povere, ho un iBook con su installato Linux. Quale Linux? Gentoo, ovviamente. Questa distribuzione offre tali e tanti vantaggi da renderla irrinunciabile. I programmi vengono costruiti a partire dalle preferenze dell'utente, e se è difficile configurarla la prima volta che la si installa poi tutto scorre liscio come l'olio. In questi ultimi tempi poi la stabilità è migliorata e non ho più problemi di sorta. Tornando ai difetti, il più grave è quello di dover compilare tutti i programmi. Questo implica che prima di poter usare OpenOffice o KDE si debbano spendere parecchie ore per la loro compilazione. A volte esistono repository (significa grossomodo "archivi") di programmi già compilati per questa o quella architettura con queste o quelle USE flag. Per svelare il significato di questi tecnicismi rimando ai manuali e ai wiki di Gentoo. Per essere chiari, posso solo dire che ciascuno di questi archivi contengono programmi molto particolari, compilati in base alle preferenze del gestore dell'archivio. Su questo sito è disponibile per il download il binario di OpenOffice-2.0.0 per PowerPC, in lingua italiana, inglese, francese, tedesca e spagnola. Le USE flag usate sono le seguenti (prese dall'output del mio emerge): `[ebuild R ] app-office/openoffice-2.0.0 +curl +eds +gnome +gtk +java -kde -ldap -mozilla -nas +xml2 +zlib`

**Riferimenti**

- Gentoo GNU/Linux [§](http://www.gentoo.org)
- Documentazione di Gentoo GNU/Linux [§](http://www.gentoo.org/doc/it/index.xml)
- Handbook per Gentoo GNU/Linux PPC [§](http://www.gentoo.org/doc/it/handbook/handbook-ppc.xml)
- Il Manuale di Gentoo GNU/Linux [§](http://www.gentoo.org/doc/it/handbook/)
- Pacchetto binario di OpenOffice-2.0.0 [§](http://www.glare.it/Software/gentoo-ppc-packages/openoffice-2.0.0.tbz2)

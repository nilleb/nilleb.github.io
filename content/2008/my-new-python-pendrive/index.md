---
title: "my new python pendrive"
date: 2008-01-23
categories: 
  - "thoughts"
---

questa mattina, nell'attesa che una installazione si completasse, ho creato la mia pennina USB con su Python&IronPython. Riprendendo un thread ([http://portableapps.com/node/1105](http://portableapps.com/node/1105)) su un qualche gruppo/sito, ho installato Python2.5 e le librerie Win32 sul mio PC windows, poi ho spostato tutto (ivi comprese python25.dll, msvcr71.dll, pythoncom25.dll, pywintypes25.dll, che sono andate a finire da system32 alla directory in cui si trova python.exe) verso la pennina. Ho creato un file batch (idle.bat) nella stessa cartella di pythonw.exe, contenente le righe seguenti:

```
@echo off start pythonw.exe Lib/idlelib/idle.pyw %1 %2 %3 %4 %5 %6 %7 %8 %9
```

Per IronPython è bastato scompattare l'archivio scaricabile da internet e cambiare un pochetto il file site.py che si trova in Lib\\, aggiungendo le due linee seguenti:

```
sys.path.append(sys.prefix+r"\..\Python25\Lib") sys.path.append(sys.prefix[0]+r":\Sources\Python\Lib")
```

Voila, la pennina è pronta! (90MB circa sono richiesti...)

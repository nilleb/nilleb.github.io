---
title: "what about a[n expensive] double screen?"
date: "2008-04-17"
categories: 
  - "computers"
tags: 
  - "double-screen"
  - "everydays"
  - "multi-os"
  - "productivity"
  - "synergy"
  - "vnc"
  - "win2vnc"
  - "work"
---

In most modern offices you can find developers and engineers working on two machines at a time. Well, they're obliged to use two mouses and two keyboards unless their chief doesn't buy a specific double screen video card.

Otherwise, you've two laptops, and you would like to work on both them without the need to switch mouse and keyboard.

Well, until Tuesday I didn't know any software capable to do the trick. Then, a friend posted a message on a miling list, and that was the most valuable and performance-improving discovery of the week :-)

At that moment I started to use [Win2VNC](http://fredrik.hubbe.net/win2vnc.html) and [Synergy](http://synergy2.sourceforge.net/). I'm using them on Windows, as required by my work. But they can be executed, or a similar product exists, also on other operating systems.

Win2VNC and X2VNC require a [VNC](http://en.wikipedia.org/wiki/Vnc) server mounted on the secondary host. In that case, let me recommend you [RealVNC](http://www.realvnc.com/). All these softwares are licensed under the GPL. But let me say that Win2VNC has a number of _limitations_ which shrink drastically your productivity when you haven't an US keyboard. OK, it's GPL and thus I could change it, but I haven't the time to do so.

Synergy is the software I'm currently using. It's easy to configure, even if its conf file is really complex and full of fine grain options. It wasn't however necessary to edit it to obtain an acceptable behavior. I love the presence of a Test mode, which pops you up a console with the significant events. It hasn't the greatest part of limitations of Win2VNC, even if I required something to take screenshots. I should only change the configuration file, but I'm lazy or I haven't the time to.. Synergy doesn't require a VNC server, and the Synergy devs care to security problems. That's not an assurance for life, but it will wipe out your colleague attempts to pwn your machine :-)

Well, let me recommend you Synergy. :-)

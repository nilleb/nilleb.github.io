---
title: "OpenVideoCrawler"
date: 2005-12-15
categories: 
  - "computer-science"
  - "thoughts"
tags: 
  - "everydays"
---

I've completed a crawler for [open-video.org](http://open-video.org/) video repository. It's written in Python, and it works. It generates descriptors for [H-DOSE](http://dose.sourceforge.net/) semantic search engine, or a less complicated, non-xml-style information file. Then it computes some keyword statistics about the movies in the collection, tells you whether you indexed fictitious movies and which where the fictitious ones. It has good performances, but they largely depend on your connection to the internet. I publish this info here and in english for laziness sake. This is a subproject for my degree [thesis](http://elite.polito.it/tesista.php?id=76) in computer science. **Related files:**

- [crawler (Python)](http://www.glare.it/Software/OVCrawler/crawler.py)
- [first execution output](http://www.glare.it/Software/OVCrawler/crawler_run.tar.gz)
- [crawler(Java-not complete)](http://www.glare.it/Software/OVCrawler/OlderStuff/openVideoCrawler.jar)

- [python script that extracts some statistics about the java-generated descriptors (BAD!)](http://www.glare.it/Software/OVCrawler/OlderStuff/pystats-0.1.py)

_All the above code is released under the terms of [GPL](http://www.gnu.org/licenses/gpl.txt)._

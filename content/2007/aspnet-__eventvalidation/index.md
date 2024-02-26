---
title: "asp.net: __eventvalidation"
date: "2007-11-30"
categories: 
  - "thoughts"
---

a mechanism has been added in [asp.net](http://asp.net) to avoid injection on sensible page contents: the event validation.  
simple as registering, server side, all the possible values of all the variables in your web page.  
something like:  
HASH(DropDownList1.UniqueID) XOR HASH(Valeur de l'article)  
the result is then serialized to the \_\_eventvalidation hidden field.  
  
more on VIEWSTATE, a strict friend to \_\_EVENTVALIDATION \[excerpt from a pdf published in the follow-up\]  
\_\_VIEWSTATE is an application state container.  
Maintain state between multiple postback requests.  
"Holds all your variables"  
Serialized base64 encoded data.  
Viewstate contents can be encrypted.  
  
to understand what this is used for, here are the following pages  
[http://msdn2.microsoft.com/en-us/library/7kh55542.aspx](http://msdn2.microsoft.com/en-us/library/7kh55542.aspx)  
[http://blogs.msdn.com/amitsh/archive/2007/07/31/why-i-get-invalid-postback-or-callback-argument-errors.aspx](http://blogs.msdn.com/amitsh/archive/2007/07/31/why-i-get-invalid-postback-or-callback-argument-errors.aspx)  
[http://odetocode.com/Blogs/scott/archive/2006/03/21/3153.aspx](http://odetocode.com/Blogs/scott/archive/2006/03/21/3153.aspx)  
[http://weblogs.asp.net/bleroy/archive/2004/08/18/216861.aspx](http://weblogs.asp.net/bleroy/archive/2004/08/18/216861.aspx)  
[http://msdn.microsoft.com/msdnmag/issues/06/12/CuttingEdge/](http://msdn.microsoft.com/msdnmag/issues/06/12/CuttingEdge/)  
  
now on more precise explications  
[http://www.security-assessment.com/files/presentations/Syscan%20-%20Next%20Generation%20.NET%20Vulnerabilities.pdf](http://www.security-assessment.com/files/presentations/Syscan%2520-%2520Next%2520Generation%2520.NET%2520Vulnerabilities.pdf)  
  
tools  
[http://www.windowsecurity.com/articles/SPIKE-BURP-real-world-computer-security-usage-Part4.html](http://www.windowsecurity.com/articles/SPIKE-BURP-real-world-computer-security-usage-Part4.html)  
[http://www.portswigger.net/proxy/](http://www.portswigger.net/proxy/)  
  
all this is fun.

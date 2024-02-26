---
title: "Exchange 2010 and Organizational Forms Libraries"
date: "2010-02-26"
tags: 
  - "2010"
  - "exchange"
  - "exchange-2010"
  - "organizational-forms-library"
  - "outlook"
  - "public-folder-database"
---

With Exchange 2010 you've the possibility to create a Public Folder Database (PFDB), in order to keep the backward compatibility with Outlook 2003 and Entourage clients. You can create such PFDB answering yes to a question during the setup, or with a specific procedure through the Exchange Management Console. Once such a PFDB is available, you can create an Organizational Forms Library.

Concerning this Organizational Forms Libraries (used to store the Outlook Forms since at least Exchange 2000) an official procedure existed for Exchange 2007: [http://support.microsoft.com/kb/933358](http://support.microsoft.com/kb/933358)

Trying to complete this procedure, you'll find out that the **PR\_URL\_NAME** property is not available for an Exchange 2010 Organizational Forms Library. So, here you the missing steps, that you shall execute right after the **2.g** step in the official Microsoft procedure:

- On the **Property Pane** menu, click on **Modify "Extra" Properties**
- Click **Add**, then type in the **Property Tag** textbox the value 0x6707001E
- In the **Property Type** textbox the value **PT\_STRING8** appears. In the **Property Name** box the **PR\_URL\_NAME** string appears along with some other characters
- Click **OK** twice
- Double click on the **PR\_URL\_NAME** property.
- Type in the **Ansi String** textbox the value **/NOM\_IPM\_SUBTREE/EFORMS REGISTRY/\[The Name Of Your Organizational Forms Library\]**
- Click **OK**
- Now you can complete the official procedure starting on the step **2.h**

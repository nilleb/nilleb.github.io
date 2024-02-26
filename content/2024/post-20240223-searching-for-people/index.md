---
title: "Searching for people is not the same as searching for articles and concepts"
date: 2024-02-23
tags: 
  - "search"
  - "people"
---

The aim of this post is to share my experience in implementing [a people search engine](https://www.youtube.com/watch?v=pgWgT89l-e8&pp=ygUtcGVvcGxlIGZpbmRlciBoYWNrYXRvbiBhc2lhbiBkZXZlbG9wbWVudCBiYW5r) for a multicultural environment such as the Asian Development Bank. In this post, I will focus on “searching a person” only - the part “search for an expert” will be the subject of the next post.

<br/>

Cultural differences make that searching for a person is often hard. In Asia, you can’t even imagine counting all the existing cultures. Even if your workplace assumes that every employee uses English for their everyday job, differences in prononciation and context transform a simple task in a nightmare. Usually this ends up calling a Friend of a Friend who still remembers that person that you need to call.

<br/>

In terms of off-the-shelf solutions you may find some relief in your default digital workplace (what a chance to be able to browse the profile pictures all your colleagues!) but…

- chances are that this tool has been implemented by a company immersed in a culture very different from yours

- chances are that you will have to test many different solutions before finding one suitable to your needs

- last, if such a solution exists, you shall struggle with internal policies (because people data is sensitive! because of many little interoperability issues that could arise, when your digital landscape is thirty years old..)

<br/>

## Why searching for people is so difficult?

Because of typos, misspellings, phonetics, incompatible vocabulary, incomplete or incorrect contextual information. At least! 😊

<br/>

My personal list to solve this problem is this one:

- considering just the name

	- tolerance to typos and misspellings (fuzzy string matching)

	- phonetics (metaphones)

- considering the organizational structure (department, division, job title) and the location

	- acronyms (data preparation)

	- dividing roots from suffixes (data preparation)

	- different weights for different fields (first and last name, then job title, then department, then division, then location; data preparation)

	- trigrams

<br/>

Technically speaking, solving these problems requires the use of several techniques at the same time - phonetical matching along with trigrams and string distances for example.

Every technique will be producing results for a specific use case (ie. searching for a phoneme vs searching for a trigram), hence it will be paramount to research the best weights to blend the results of different techniques.

Always speaking of weights, the contextual information about a person should concur in finding her - just not all the context information is equivalent (the system identifier of the person has negligeable importance compared to the first name; the department acronym could be more important than the department long name; is it easy, in your context, to define whether the division or the department is more important?).

## How can you determine if you are doing this right?

Good knowledge of the data you are leveraging will help - a lot. Spend a fair amount of time just inspecting it, checking for outliers, describing it.

Feedback is a gift, so you should not be counting on it. A corporate search engine has also the defect of a low query volume. Nevertheless, in the modern landscape you can easily collect KPIs about your solution behavior, and analyze its trends. The intensive use of Structured Logging and tags can not only help you monitor the state of your application, but also build governance dashboards that will help you visualize how the search engine is doing.

 In Search Engines theory you will find a few techniques about how to assess whether a search engine is returning the right results. We recommend organizing beta test sessions with users from across all the organization, to make sure that their use cases are addressed. Then prepare a collection of integration tests, to be played against every new release of the search engine AND iteration of the indexer.


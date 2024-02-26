---
title: "The devil's in the details"
date: 2017-08-08
---

You know, I always start a new BigQuery query copying and pasting an existing one, and modifying it.

`SELECT record.attribute, target.kind, target.uid, target.subType, target.className context.contextType, context.contextId, context.contextSubType, context.contextClassName, context.parent.uid FROM TABLE_DATE_RANGE([dataset.raw_data_], TIMESTAMP("2017-08-08"), TIMESTAMP("2017-08-08")) WHERE record.attribute == 'value' AND context.parent.uid is not null order by createdAt desc LIMIT 1000`

Then, you execute it.

And you realize that the result types don't match what you expect. In the above query, all the fields with a uid look like integers. But, in my case, there's no integer at all. Worse than that: I have the impression that the contextId and the contextKind have been switched. Since my code is responsible for collecting this data, I get the unit tests. I check them, their expected results, and I stop at a breakpoint, just to check. Everything's fine. I start telling myself that I must have screwed the function calls in come cases. You know, Python isn't strongly typed, and you could easily pass through. My code is pretty tolerant, and at last all the data is being stored as strings. So, breakpoints, logging instructions everywhere, part 2. I even discover that deferred.defer doesn't trace anything when you're on a queue which is not the default one. Wow. At last, I find myself logging the HTTP requests. Everything's fine on my side. OK.

Let's exclude a bug in BigQuery itself. What have I done wrong? That must be my select. Let's select everything. Looks fine, my fields have the good type AFAICS. Then, Let's have a look at the initial query. I start browsing the columns. record, OK. target, ... Well, where has passed the target.className? OK, I get it now. It's not a matter of switching columns. It's just a matter of what BigQuery allows as a valid query, and what its UI is able to parse.

One hour later, I'm happy. That was just a question of a missing comma.

**Subject:** Quick Data Quality Update & Questions

Hi Matt,

Hope you're having a good day! I wanted to reach out and share some of the data quality findings we’ve uncovered in our recent analysis. Nothing urgent, but some items definitely need clarificatioin.

We ran checks for missing values, duplicates, and possible reference issues between receipts and users. Turns out, we found over **1,100 receipts** that reference user IDs we couldn’t find in the user table. There’s also some big spending outliers: a handful of receipts show over **\$1,000** in totalSpend, going as high as \$4,300. That might be correct, but we'd want to confirm if that’s normal or a sign of a data entry glitch.

Another interesting point is the **duplicate user IDs**—about **283** of them. Could be test data or maybe multiple accounts associated with the same person. Also, about **600 brand records** are missing the `topBrand` flag. We’re not sure whether that should default to “False” or if we need to gather more info from the brand partners. We’d love your insight on this.

### Key Questions:

1. Are large totalSpent values expected (especially above \$1,000)?  
2. Should we handle those 1,119 “orphan” receipts referencing nonexistent users, or can we remove them altogether?  
3. If `topBrand` is missing, should we treat it as “False,” or is there a differnet default?  
4. What’s your preference on merging duplicate users: do we keep them separate or unify them under the same ID?

### Performance Concerns:

We’re also looking at how this dataset will grow over time. If we keep ingesting more receipts and users, queries may start to slow down. We can explore indexing strategies or partitioning based on date or user ID. But it’d help to know the expected volume and usage patterns—are we expecting real-time queries, or is it more for monthly reporting?

### Next Steps:

If you can share some background on how these data sets are generated (especially what’s considered “test” vs. “live” data), that would be super helpful. Also, if you have any guidelines for what “normal” spend and brand usage look like, we can refine our validations. Once we have these clarifications, we’ll update the data pipeline to handle anomalies more seamlessly and ensure that we can trust the analytics going forward.

Let me know if you have any immediate thoughts or if there's any further detail you’d like. Thanks for your time!

**Best,**  
Cheng  
Analytics Engineer

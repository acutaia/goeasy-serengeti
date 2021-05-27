This *SERENGETI* endpoint provides ways to let external users and applications to request for information
collected on the platform. 

This interface enables external organization to gather aggregated meta-data on
citizens' mobility. 

Within the API boundaries, it is possible to parametrize requests by selecting timeframes,
area of interests, mobility types and other details. To preserve user’s privacy, it has been defined a lower
threshold for the area selected. 

In addition, it has been enabled the possibility to extract, with other requests,
the list of positions for the collected journeys.

The design process of the data extraction API is the result of the collaboration
between project partners and stakeholders. 

The following diagram shows the final software design of the data
extraction service from the *SERENGETI* perspective.

---

![image](/img/get_statistics.png)

---

In principle, the main role of *SERENGETI*, concerning the extraction API, is to behave as a secure application
proxy between external requesters, and the Private Database of the GOEASY Platform.

This *SERENGETI* endpoint provides ways to let external users and applications to request for mobility
behaviour detection information with respect to a given track id. After the security framework approval, it parses
and sanitize the provided input, forward the request within the Federated API provided by the Privacy Aware
DBMS system. 

The quoted system asynchronously oversees the update of the latest entries collected on the
Public Database with the features provided by the Dependable LBS components and the mobility behaviour
detection system.

The values returned by the Data Access Manager are given back to the user through the
https response within the timeout threshold of the standard.

The following diagram shows the final software design of the Mobility Behaviour Detection service 
from the *SERENGETI* perspective.

---

![image](https://acutaia.github.io/goeasy-serengeti/img/get_mobility.png)

---

In conclusion, the first step of *SERENGETI* is managed by the Access Worker, by exploiting a specific security
configuration for the credentials applied on the API. It later exploits a forwarding logic by acting as an
application proxy that interconnects the other cloud services. 

In the background, the accounting worker still collects resource usage and other information to be 
encrypted and stored on the IOTA network.

This *SERENGETI* endpoint provides ways to let users and applications to request for position data
authentication services without the exploitation of other GEP features, such as the persistent collection.

The following diagram shows the final software design of the authentication service from the *SERENGETI* perspective. It
shows the main steps performed by the deployed software running on the cloud platform.

---

![image](/img/user_feed_authenticate_test.png)

---

The first step of *SERENGETI*, for all the endpoints developed, is to verify with the Security Framework policy
if the bearer token, OAuth2 compliant, provided in the request is granted by all the authorization rules applied
on the client requesting the service. 

In addition, the json payload injected is verified and sanitized within the schema allowed boundaries 
of the specific service.

The activities quoted are an essential step to guarantee security requirements on the cloud platform.

To increase feature modularity, these steps are performed by a sub-component called Access worker. 

In case of unauthorized users or data inconsistency, the data is dropped, and it will be returned to the requester an 
error message. In the background, a dedicated worker collects resource usage and other information such as requests 
sources and data consistency to enable both monitoring and maintenance of the platform. 

In the meanwhile, the given positions are analysed to properly select the reference system of interest.

To safely interact with the remote system, managed by the U-Blox API, *SERENGETI* punctually obtain a valid token from Keycloak. 

These credentials are used to retrieve authenticated reference values to be used by the cloud algorithms to verify
position trustiness.

The position Alteration Library triggers the authentication process for each position received and set the
authenticity flag accordingly. At the end of the process the overall results are given to the requester.

This *SERENGETI* endpoint provides a unique point of access to let external users and applications to send
standardized data through a JSON payload via https POST requests. 

After the security framework approval, it responds by embedding a unique, random, and anonymous id, 
generated on the cloud, for the specific track provided. 

Finally, the content of the message received is parsed and sanitized.

The logic developed enables the reception of a set of locations embedding Galileo raw data. It requires the 
presence of the entire Galileo navigation messages received while the external devices were computing their positions.

The latitude and longitude of the list of positions received are extracted by the 
Reference System Manager library and exploited for the proper selection of the U-Blox Reference System instance.

This necessity is due to the different visibility
of Galileo satellites over the deployments considered on the project. Consequently, one or multiple reference
system cloned instances must be considered at country level to provide the proper information to the position
authentication algorithm for a given list of positions.

After the selection of the remote U-Blox reference platform
of interest, it triggers a set of requests collecting the necessary reference data to be exploited for the
identification of the attacks.

Accumulated data are then given to the End-to-End Position Authentication (E2EA) 
worker to finalize the process in charge on the e-Security infrastructure.

The track id is stored on the Private Database, but the GOEASY Platform, by exploiting Keycloak, and the
anonymization process is not able to link it with a specific user.

Because of the quoted approaches, only the
specific client, through an authorized application collects the list of tracks belonged to him, for future
exploitations.

---

![image](https://acutaia.github.io/goeasy-serengeti/img/user_feed_authenticate.png)

---
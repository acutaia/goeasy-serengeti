![image](https://raw.githubusercontent.com/acutaia/goeasy-serengeti/main/static/logo_full.png)

[![Test](https://github.com/acutaia/goeasy-serengeti/actions/workflows/test.yml/badge.svg)](https://github.com/acutaia/goeasy-serengeti/actions/workflows/test.yml)
[![Deploy on Docker Hub](https://github.com/acutaia/goeasy-serengeti/actions/workflows/docker_deployment.yml/badge.svg)](https://github.com/acutaia/goeasy-serengeti/actions/workflows/docker_deployment.yml)
[![codecov](https://codecov.io/gh/acutaia/goeasy-serengeti/branch/main/graph/badge.svg?token=AD4AS9A8MV)](https://codecov.io/gh/acutaia/goeasy-serengeti)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Python 3.8+](https://img.shields.io/badge/python-3.8_|_3.9-blue.svg)](https://www.python.org/downloads/release)

---

**OpenAPI**: https://galileocloud.goeasyproject.eu/serengeti/api/v1/docs

**Documentation**: 

---
## **The project**

The GOEASY project will provide the technical and business foundations to enable a new generation of trusted and dependable mass-market Location Based Services and Applications to engage, stimulate and reward citizens for more sustainable behaviours and healthier choices.

This three-years project contributes to the consolidation of an environmentally aware and engaged public community in the EU, while delivering added value innovative solutions for Location Based Services and opening new scenarios and opportunities for Smart  City solutions (by enabling innovative LBS and IoT services). The research outputs are relevant for EU citizens lives, promoting a healthier environment, increasing sustainability in cities, creating employment opportunities and improving existing technologies.

GNSS user technology is now widely available in mass market devices including personal devices, connected vehicles, Internet of Things (IoT) objects, etc. The widespread availability of GNSS receivers, joint with ubiquitous communication capabilities of devices and the ability of cloud-based ICT platforms to federate with each other through open standards and APIs, is enabling a new generation of Location Based Services (LBS) able to support highly-scalable pervasive applications where large number of geographically-distributed users are engaged e.g. in immersive games and commercial services.

While GNSS proves to be able to support such applications successfully, a major drawback prevents such approach to be used in more serious (and potentially highly rewarding) mass market applications i.e. the lack of authentication features, resulting in high difficulties in preventing users from spoofing position information to gain advantages or damage other users.

GOEASY will be evaluated by means of two concrete use cases, namely the ApesMobility and the AsthmaWatch, both evaluated engaging real users in a medium-scale pilot in Torino (Italy) and Stockholm (Sweden).

## **SEcure tRusted collEction aNd exchanGE of posiTion Information (SERENGETI)**

The SERENGETI software component is the main point of access of the GOEASY platform. It provides REST
based OAuth2 secured endpoints to enable authorized users and software to interact with the GEP features.
In addition to the application proxy features, it allows to feed the platform with personal tracking data collected
by the Trusted GOEASY Devices (such as the Smartphones running the ApesMobility application), to be
authenticated, anonymize, and stored on a Private Database. 

The overall endpoints offered by the current software are mainly divided as follows:
- Data Feeding API
- Data Authentication API
- Data Inspection API
- Data Extraction API
- Administration API

### **Data Feeding API**

This SERENGETI endpoint provides a unique point of access to let external users and applications to send
standardized data through a JSON payload via https POST requests. 

After the security framework approval, it responds by embedding a unique, random, and anonymous id, 
generated on the cloud, for the specific track provided. 

Finally, the content of the message received is parsed and sanitized.

The logic developed enables the reception of a set of locations embedding Galileo raw data. It requires the presence of the entire Galileo
navigation messages received while the external devices were computing their positions.

The latitude and longitude of the list of positions received are extracted by the Reference System Manager library and exploited
for the proper selection of the U-Blox Reference System instance.

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
exploitations. The responsibility to collect the anonymize id in an encrypted way is demanded to the final
application.

![image](https://raw.githubusercontent.com/acutaia/goeasy-serengeti/main/static/user_feed_authenticate.png)

### **Data Authentication API**

This SERENGETI endpoint provides ways to let users and applications to request for position data
authentication services without the exploitation of other GEP features, such as the persistent collection.

Thecurrent feature is enabled for testing purposes and for those scenarios where data is already stored on the
cloud, and the main interests are linked on providing additional information for data trustiness. 

The following diagram shows the final software design of the authentication service from the SERENGETI perspective. It
shows the main steps performed by the deployed software running on the cloud platform.

![image](https://raw.githubusercontent.com/acutaia/goeasy-serengeti/main/static/user_feed_authenticate_test.png)


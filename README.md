
![NIBE Logo](https://www.nibeuplink.com/Content/Images/Nibe/Logo_footer.png)


# NibeUplink
This Python library extracts data from NIBE Uplink™ site or its API.


# Authors
NibeUplink was written by [István Szirtes](https://github.com/W00D00/NIBEUplink)


# Requirements
Python 3.x
Recommended Python 3.6


# NIBE Uplink™
The internet and NIBE Uplink gives you a quick overview and the present status of your system. 
You get a good overall view and good information for monitoring and controlling your heating and hot water. 
If your system is affected by a malfunction, you receive an alert via e-mail that allows you to react quickly.
NIBE Uplink also gives you the opportunity to control comfort, no matter where you are.

[Documentation](https://www.nibeuplink.com/FAQ)


# NIBE Uplink™ API
NIBE Uplink API enables your app, service or product to utilize the power of NIBE Uplink. 
This website provides you with the documentation you need to get started coding and integrating with the NIBE Uplink API.

[Services Agreement](https://api.nibeuplink.com/Home/ApiAgreement)

[Documentation](https://api.nibeuplink.com/docs/v1)


# Prerequisites
## NIBE Uplink™ registrations
* Verify that your NIBE module is supported by NIBE Uplink™. [FAQ](https://www.nibeuplink.com/FAQ)
* Verify that your NIBE module is connected to the internet. [FAQ](https://www.nibeuplink.com/FAQ)
* You should have a registered account in NIBE Uplink™. [NIBE web page](https://www.nibeuplink.com)
* Your heatpump should be registered in NIBE Uplink™. [FAQ](https://www.nibeuplink.com https://www.nibeuplink.com/FAQ)
* You should have registered application in NIBE Uplink™ API. [About](https://api.nibeuplink.com/Home/About)

## Collect authentication data
### NIBE Uplink™ Login details
You will need to get and store the authentication data of the NIBE Uplink™ Login to use this library and fetch data from NIBE.
The "config.py" file is dedicated to store all of your authentication data.
* username:
	Your NIBE Uplink account's E-mail.
* password:
	Your NIBE Uplink account's password.
* system ID(s):
	Get your <systemid> from NIBE Uplink™ web site. 
	Open one of your heatpumps on [NIBE web page](https://www.nibeuplink.com) and the given system's ID will be in your address bar:
	"https://www.nibeuplink.com/System/<systemid>/Status/Overview"
	More system can be stored with system descriptor and its ID in a dictionary.

### NIBE Uplink™ API Application details
* Callback URL
** Good reading to set the url: [marshflattsfarm.org.uk](https://www.marshflattsfarm.org.uk/wordpress/?page_id=3480)
* Identifier
* Secret

## Create a token
...


# Install
...


# Usage examples
## Get XY data
...

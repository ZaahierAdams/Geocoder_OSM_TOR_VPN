# Geocoder OSM TOR VPN
<div align="center">
  <img alt="Logos" src="https://i.imgur.com/OVi97Jv.png"></img>
</div>
Converts street addresses into geographical coordinates *(latitude and longitude)* using OpenStreetMap (OSM) API service via Tor VPN. 
Prior to geocoding the application data scrubs addresses.

## Reason for application 
### Data Scrubber
Parsing poor quality address data through most geocoders yields poor results. This problem can be mitigated through data cleansing of addresses. 

### VPN 
OSM offers a free geocoding service. However, you are given a limited number of requests per period. This makes bulk geocoding difficult. This limitation can be overcome by regularly changing the IP address of the request. 

## How it works
1. The application extracts the bulk addresses from ```Input.csv```. This file is in the same directory as the application.

2. Addresses are scrubbed using reference suburb data in ```Suburbs_PostalCodes.csv```. The image below demonstrates how the application identifies spelling errors in the scrubbing process:

<div align="center">
  <img alt="ScrubberBestFit" src="https://i.imgur.com/zWenpHt.jpg"></img>
</div>

3. Initiates a *Tor* session 
4. Makes a request to *OSM* geocoding API using the street address components as query string parameters via an IP address provided by *Tor*
5. After every 100 requests a new IP address is used for subsequent requests 
6. Successfully geocoded addresses are saved to ```'Foward Geocode Output 1.csv```
7. Addresses that have failed to geocode are saved to a separate file. 
8. The application will re-attempt to geocode the failed addresses by widening the geographical scope of the search. Demonstrated in this rudimentary example:

<div align="center">
  <img alt="WidenScope" src="https://i.imgur.com/crmqcQH.png"></img>
</div>

**Note:** The expectation is that the bulk addresses fall within a specific geographical scope, i.e. a city/ state etc… 

## Setting up 
### Python Libraries 
[Requests](https://pypi.org/project/requests/), [Stem](https://pypi.org/project/stem/)

### Tor password
*Line 29* in ```main.py``` :
```
controller.authenticate(password="TOR_PASSWORD_HERE")
```

### Geographical scope 
*Line 104-105* in ```main.py```:
```
cityName = 'Cape Town'
countryName = 'South Africa'
```
**Note** The expectation is that the street addresses are within the scope of ```cityName```

### Reference data
```Suburbs_PostalCodes.csv``` contains the names and corresponding postal codes of suburbs with the specified ```cityName```. Replace this file’s contents to those corresponding with the ```cityName``` that you have provided. 

## Acknowledgements
[Tor](https://www.torproject.org/), [OSM](https://www.openstreetmap.org/about)
 

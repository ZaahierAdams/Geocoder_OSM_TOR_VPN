## VPN
import requests
from stem import Signal
from stem.control import Controller

## Scrubber 
from Dict_Create import Dict_Create
from difflib import SequenceMatcher, get_close_matches

## Other
import csv
import json
from json import JSONDecodeError



'''
TOR VPN methods
'''
def get_tor_session():
    session = requests.session()
    session.proxies = {'http':  'socks5://127.0.0.1:9050',
                       'https': 'socks5://127.0.0.1:9050'}
    return session


def renew_connection():
    with Controller.from_port(port = 9051) as controller:
        controller.authenticate(password="TOR_PASSWORD_HERE")
        controller.signal(Signal.NEWNYM)


def VPN():
    renew_connection()
    session = get_tor_session()
    
    new_ip_text     = session.get("http://httpbin.org/ip").text
    new_ip_json     = json.loads(new_ip_text)
    print(new_ip_json["origin"])
    


'''
Best-fit Scrubber
'''
def Best_Match(Suburb, DPC, DPC_keys):
    if Suburb in DPC: 
        try:
            post_code   = DPC[Suburb]['Post Code']
            street_code = DPC[Suburb]['Street Code']
            area        = DPC[Suburb]['Area']
                        
            return Suburb, post_code, street_code, area
        
        except IndexError:
            return Suburb, '', '', ''
            
    else:
        try:
            best_fit_1  = get_close_matches(Suburb, DPC_keys)[0]
#            best_fit_2  = get_close_matches(Suburb, DPC_keys)[1]
#            best_fit_3  = get_close_matches(Suburb, DPC_keys)[2]

            
            metric_1    = SequenceMatcher(None, Suburb, best_fit_1).ratio()
                       
            if metric_1 >= 0.8:
                
                Suburb          = best_fit_1
                
                try:
                    post_code   = DPC[best_fit_1]['Post Code']
                except IndexError:
                    post_code   = ''
                    
                try:
                    street_code = DPC[best_fit_1]['Street Code']
                except IndexError:
                    street_code = ''
                    
                try:
                    area        = DPC[best_fit_1]['Area']
                except IndexError:
                    area        = ''
                    
                return Suburb, post_code, street_code, area
                 
            else:
                ## run through geocoder anyway
                return Suburb, '', '', '' 
            
        except IndexError:
            ## No best fit found
            return Suburb, '', '', ''
    
    

'''
Geocodes addresses at suburb level
    
'''
def VPN_OSM_Suburb_Geocoder(method, DPC, DPC_keys, CPT_keys):
    
    cityName = 'Cape Town'
    countryName = 'South Africa'
    
    VPN()
    
    if method == 1:
        input_file  = open('Input.csv', 'r')
        fail_file   = 'FAILED 1.csv'
    elif method == 2:
        input_file  = open('FAILED 1.csv', 'r')
        fail_file   = 'FAILED 2.csv'
    elif  method == 3:
        input_file  = open('FAILED 2.csv', 'r')
        fail_file   = 'FAILED 3.csv'
    elif method == 4:
        input_file  = open('FAILED 3.csv', 'r')
        fail_file   = 'FAILED 4.csv'
    elif method == 5:
        input_file  = open('FAILED 4.csv', 'r')
        fail_file   = 'FAILED 5.csv'
    elif method == 6:
        input_file  = open('FAILED 5.csv', 'r')
        fail_file   = 'FAILED 6.csv'    
    else:
        pass
        
    output_file = 'Foward Geocode Output 1.csv'
    
    failed = []
    iteration = 0
    
    
    
    with open(output_file, mode='a+') as output:
        writer = csv.writer(output, delimiter=',', lineterminator = '\n')
        
        ## output column headings
        
        if method == 1:
            writer.writerow(['Input_Street',
                             'Input_Suburb 1',
                             'Input_Suburb 2',
                             'Output_Suburb',
                             'Output_Town',
                             'Output_City',
                             'Output_County',
                             'Output_State',
                             'Output_Country',
                             'Output_Latitude',
                             'Output_Longitude',
                             ])
        else:
            pass
        
        
        for row in input_file:
            Street      = row.strip().split(',')[0].replace('\n','').title()
            Suburb_1    = row.strip().split(',')[1].replace('\n','').title()
            Suburb_2    = row.strip().split(',')[2].replace('\n','').title()
            iteration   += 1
            
            address_string = ''
            
            
            
            '''
            Address string constructor
            '''
            
            if method == 1:
                '''
                Use Address + Suburb 1 + Suburb 2 + /cityName + countryName
                '''
                
                
                if Suburb_1         == Suburb_2:
                    address_string  = Street + ', ' + Suburb_1
                else:
                    address_string  = Street + ', ' + Suburb_1 + ', ' + Suburb_2
                    
                if Suburb_1 in CPT_keys or Suburb_2 in CPT_keys:
                    if Suburb_1 != cityName and Suburb_2 != cityName:
                        address_string = address_string + ', ' + cityName + ', ' + countryName
                    else:
                        pass
                else:
                    address_string = address_string + ', ' + countryName

            
            
            elif method == 2:
                '''
                Use Address + Suburb 1 + /cityName + countryName
                '''
                
                address_string  = Street + ', ' + Suburb_1
                                    
                if Suburb_1 in CPT_keys or Suburb_2 in CPT_keys:
                    if Suburb_1 != cityName:
                        address_string = address_string + ', ' + cityName + ', ' + countryName
                    else:
                        pass
                else:
                    address_string = address_string + ', ' + countryName
            
    
            
            elif method == 3:
                '''
                Scrub Suburbs using DPC
                '''
                ## Pass heading
                if Suburb_1 == 'Suburb 1':
                    pass
                
                else:
                    Suburb_1_new,   Suburb_1_post_code,     Suburb_1_street_code,   Suburb_1_area   = Best_Match(Suburb_1, DPC, DPC_keys)
                    Suburb_2_new,   Suburb_2_post_code,     Suburb_2_street_code,   Suburb_2_area   = Best_Match(Suburb_2, DPC, DPC_keys)
                    
                    if Suburb_1_area == Suburb_2_area:
                        if Suburb_1_new == Suburb_2_new:
                            ## Use Suburb_1_new name only 
                            ## Too risky to use rest of Suburb_1_new information
                            address_string = address_string + Suburb_1_new #+ ', ' + Suburb_1_area + ', ' + Suburb_1_street_code
                            
                        else:
                            if Suburb_2_new == Suburb_1_area:
                                ## Use Suburb_1_new name only 
                                address_string = address_string + Suburb_1_new + ', ' + Suburb_1_area + ', ' + Suburb_1_street_code
                            else:
                                ## Use Suburb_1_new info. + Suburb_2_new name
                                address_string = address_string + Suburb_1_new + ', ' + Suburb_2_new + ', ' + Suburb_1_area + ', ' + Suburb_1_street_code      
                    else:
                        ## Use cleansed Suburb names only
                        address_string = address_string + Suburb_1_new + ', ' + Suburb_2_new
                        
                    if Suburb_1_new in CPT_keys or Suburb_2_new in CPT_keys or Suburb_1_area in CPT_keys or Suburb_2_area in CPT_keys:
                        if cityName in address_string:
                            pass
                        else:
                            address_string = address_string + + ', ' + cityName + ', ' + countryName
                    else:
                        ## append countryName
                        address_string = address_string + ', ' + countryName
                
                
            elif method == 4:
                '''
                Use Address + Suburb 1 + Suburb 2
                '''
                if Suburb_1         == Suburb_2:
                    address_string  = Street + ', ' + Suburb_1
                else:
                    address_string  = Street + ', ' + Suburb_1 + ', ' + Suburb_2
            
            
            elif method == 5:
                '''
                Use Address + Suburb 1 
                '''
                address_string  = Street + ', ' + Suburb_1
                
            
            elif method == 6:
                '''
                Use Address + countryName
                '''
                address_string  = Street + ', ' + countryName


            else:
                pass
            
            
            address_parse = address_string.replace(' ','+')
            address_parse = address_parse.replace('+,+','+')
            if address_parse.startswith(',+'):
                address_parse = address_parse[2:]
            else:
                pass
            
            
            
            '''
            Change IP Address every 100th query
            
            '''
            if iteration % 100 != 0:
                pass  
            else:
    #            pass
                VPN()
            
            
            
            '''
            Parse string through API URL using VPN
            '''
            
            if Suburb_1 == 'Suburb 1':
                pass
            else:
                url = 'https://nominatim.openstreetmap.org/?addressdetails=1&q={}&format=json&limit=1'.format(address_parse)
                
                session = get_tor_session()
                json_string     = session.get(url).text[1:-1]
                
                try:
                    json_dict       = json.loads(json_string)  
                    
                    
                    try:
                        output_latitude     = float(json_dict['lat'])
                    except KeyError:
                        output_latitude     = ' '
                    
                    try:
                        output_longitude    = float(json_dict['lon'])
                    except KeyError:
                        output_longitude    = ' '
                    
                    try:
                        output_suburb       = json_dict['address']['suburb']
                    except KeyError:
                        output_suburb       = ' '
                    
                    try:
                        output_town         = json_dict['address']['town']
                    except KeyError:
                        output_town         = ' '
                        
                    try:
                        output_city         = json_dict['address']['city']
                    except KeyError:
                        output_city         = ' '
                        
                    try:
                        output_county       = json_dict['address']['county']
                    except KeyError:
                        output_county       = ' '
                        
                    try:
                        output_state        = json_dict['address']['state']
                    except KeyError:
                        output_state        =' '
                        
                    try:
                        output_country      = json_dict['address']['country']
                    except KeyError:
                        output_country      =' '
                        
                    
        #            print()
        #            print(output_latitude, output_longitude)
        #            print(output_suburb)
        #            print(output_town)
        #            print(output_city)
        #            print(output_county)
        #            print(output_state)
        #            print(output_country)
                    
                    if output_latitude < -22 and output_latitude > -35 and output_longitude > 15 and output_longitude < 35 :
                        print()
                        print('_________________________________________')
                        print('PASSED')
                        print('Input Parameters:\t', Suburb_1, Suburb_2)
                        print()
                        print('Final Parameters:\t',output_suburb, output_town, output_city)
                        print('Final coords:\t',output_latitude,';',output_longitude)
        
        
                        writer.writerow([Street, 
                                         Suburb_1, 
                                         Suburb_2, 
                                         output_suburb, 
                                         output_town, 
                                         output_city, 
                                         output_county, 
                                         output_state, 
                                         output_country,
                                         output_latitude,
                                         output_longitude])
            
                    else:
                        failed.append([Street, Suburb_1, Suburb_2]) # would be useful to append scrubbed data
                        print()
                        print('_________________________________________')
                        print('FAILED')
                        print('Input Parameters:\t', Suburb_1, Suburb_2)
                        print()
                        print('Final Parameters:\t',output_suburb, output_town, output_city)
                        print('Final coords:\t',output_latitude,';',output_longitude)
                        
                except JSONDecodeError:
                    failed.append([Street, Suburb_1, Suburb_2]) 
                    print()
                    print('_________________________________________')
                    print('FAILED')
                    print('Input Parameters:\t', Suburb_1, Suburb_2)

            
        #        except AttributeError:
        #            print('\nAttribute ERROR', type(json_string)) 
        
        #        except Exception as e:
        #            print(e)
                    
    
            
    with open(fail_file, mode='w') as output:
            writer = csv.writer(output, delimiter=',', lineterminator = '\n')
            writer.writerow(['Street', 'Suburb 1', 'Suburb 2'])
            
            for fail in failed: 
                writer.writerow([fail[0], fail[1], fail[2], fail[3]])    
                
    input_file.close()
    
    
    passed_output = iteration - len(failed)
    failed_output = len(failed)
    print()
    print('______________________________')
    print('Method #'+str(method))
    print()
    print('Number of iteration:\t', iteration)
    print('Passed:\t\t\t', passed_output)
    print('Failed:\t\t\t', failed_output)
    print('______________________________')
    
    return iteration, passed_output, failed_output


def main():
        
    DPC = Dict_Create('Domestic_Postal_Codes.csv') # SOME ERRORS HAVE BEEN PICKED UP IN DPC !!!
    CPT = Dict_Create('Suburbs_PostalCodes.csv')
    DPC_keys = []
    CPT_keys = []
    for key in DPC:
        DPC_keys.append(key)
    for key in CPT:
        CPT_keys.append(key)
        
    iter1, passed1, failed1 = VPN_OSM_Suburb_Geocoder(1, DPC, DPC_keys, CPT_keys)
    iter2, passed2, failed2 = VPN_OSM_Suburb_Geocoder(2, DPC, DPC_keys, CPT_keys)
    iter3, passed3, failed3 = VPN_OSM_Suburb_Geocoder(3, DPC, DPC_keys, CPT_keys)
    iter4, passed4, failed4 = VPN_OSM_Suburb_Geocoder(4, DPC, DPC_keys, CPT_keys)
    iter5, passed5, failed5 = VPN_OSM_Suburb_Geocoder(5, DPC, DPC_keys, CPT_keys)
    iter6, passed6, failed6 = VPN_OSM_Suburb_Geocoder(6, DPC, DPC_keys, CPT_keys)
    
    print()
    print('Method\t\tIterations\t\tPassed\t\tFailed')
    print('__________________________________________________________________')
    print(1,'\t\t', iter1,'\t\t\t', passed1,'\t\t', failed1)
    print(2,'\t\t', iter2,'\t\t\t', passed2,'\t\t', failed2)
    print(3,'\t\t', iter3,'\t\t\t', passed3,'\t\t', failed3)
    print(4,'\t\t', iter4,'\t\t\t', passed4,'\t\t', failed4)
    print(5,'\t\t', iter5,'\t\t\t', passed5,'\t\t', failed5)
    print(6,'\t\t', iter6,'\t\t\t', passed6,'\t\t', failed6)
    print('__________________________________________________________________')
    

if __name__ == '__main__':
    main()
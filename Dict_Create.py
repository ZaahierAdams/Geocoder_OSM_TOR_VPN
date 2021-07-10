   
def Dict_Create(file_path):  
    file    = open(file_path,'r')
    itrn    = 0
    keys    = []
    dic     = {}
    
    for sub in file:
        suburb_name     = sub.split(',')[0].replace('\n','').title()
        post_code       = sub.split(',')[1].replace('\n','').title()
        street_code     = sub.split(',')[2].replace('\n','').title()
        area            = sub.split(',')[3].replace('\n','').title()

        if itrn == 0:
            keys.extend([suburb_name, post_code, street_code, area])
        else:
            dic.update(
                    {
                    suburb_name : 
                        {
                            keys[1] : post_code,
                            keys[2] : street_code,
                            keys[3] : area
                            }
                    }
                    )
        itrn += 1
    
    file.close()
    return dic

#CPT_suburbs = Dict_Create('CPT_Suburbs.csv')
#DPC         = Dict_Create('Domestic_Postal_Codes.csv')
#
#print(DPC)



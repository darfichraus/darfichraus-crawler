import requests
import json
import database as database
import re
import concurrent.futures

url = 'https://services7.arcgis.com/mOBPykOjAyBO2ZKk/arcgis/rest/services/RKI_Landkreisdaten/FeatureServer/0/query?where=1%3D1&outFields=*&outSR=4326&f=json'

source_type = "RKI"
disease = "CORONA"

resp = requests.get(url=url)

data = resp.json()
landkreise = data['features']

geoDB = database.client["darfichraus"]

def searchCountyInDatabase(county, search_type):
        regex = re.compile("^" + county + ".*", re.IGNORECASE)

        matches = geoDB['geodata'].find(
                {
                        "properties.NAME_3": regex
                }
        ).count()

        if matches > 1:
                if matches == 2:
                        geoDataId = geoDB['geodata'].find(
                                {
                                        "properties.NAME_3": regex
                                }
                        )

                        for res in geoDataId:
                                if res['properties']['ENGTYPE_3'] == search_type:
                                        # print(county, "with search_type", search_type, "was found")
                                        return str(res["_id"])

                regex = re.compile("^" + county + "$", re.IGNORECASE)
                rematch = geoDB['geodata'].find(
                        {
                                "properties.NAME_3": regex
                        }
                )
                for res in rematch:
                        if res['properties']['ENGTYPE_3'] == search_type:
                                # print(county, "with search_type", search_type, "was found with new search pattern")
                                return str(res["_id"])

                return ""
        else:
                geoDataId = geoDB['geodata'].find(
                        {
                                "properties.NAME_3": regex
                        }
                )

                for res in geoDataId:
                        return str(res["_id"])

                return ""

        # for item in allItems:
                
                # else:
                #         print(item['properties']['NAME_3'])

def create_landkreis_info(item):
        info = item['attributes']
        gen = info['GEN']
        county = info['county']
        search_mode = 'Rural district'
        district_type = "Landkreis"
        if county.startswith('SK'):
                search_mode = 'Urban district'
                district_type = "Stadt"
        res = searchCountyInDatabase(gen, search_mode)
        info['geometry'] = res
        info['districtType'] =  district_type
        info['source'] = source_type
        info['disease'] = disease
        return info

insertInfo = []

with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        future_to_info = {executor.submit(create_landkreis_info, landkreis): landkreis for landkreis in landkreise}
        for future in concurrent.futures.as_completed(future_to_info):                                
                try:
                        insertInfo.append(future.result())
                except Exception as exc:
                        print('%r generated an Exception: %s' % (future.result(), exc))        

class InformationItem:

        def asDocument(self, item):

                newDocument = {}
                for key in self.__dir__():
                        if key in item.keys():
                                newDocument[key] = item[key]

                return newDocument
                

        def __dir__(self):
                return ['GEN', 'BEZ', 'EWZ', 'death_rate', 'cases', 'deaths', 'cases_per_100k', 'cases_per_population', 'BL', 'county', 'last_update', 'cases7_per_100k', 'districtType', 'geometry', 'source', 'disease']

for item in insertInfo:
        try:
                info_to_insert = InformationItem().asDocument(item)
                insert_result = geoDB["healthCountyInformation"].insert_one(info_to_insert)                
        except Exception as inst:
                print(inst)
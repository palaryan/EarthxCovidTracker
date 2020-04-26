import time
from spotchain.Spotchain import Spotchain
import math
import requests
class Interface():
    
    def __init__(self):
        self.api_url = "https://api.geospark.co/v1/api"
        self.headers = {'Content-Type':'application/json',
                'Api-Key': '9b92e9804d3d4991989b85ca2ba07d90'}
        self.max_intensity = 100
        self.f = open("generate", "r")
        self.matched_coords = eval(self.f.readline().strip("\n"))
    def grab_user_location(self, uid=None, all_users=False):
        if (not all_users):
            req = requests.get(self.api_url + "/user/?user_id={}".format(uid), headers=self.headers).json()
            return req['data'][0]['last_location_update']['coordinates']['coordinates'][::-1]
        req = requests.get(self.api_url + '/user/', headers=self.headers).json()
        coords = [user['last_location_update']['coordinates']['coordinates'][::-1] for user in req['data']['users']]
        return coords
    def grab_nearby_users(self, h, k, radius):
        radius  /= 4800
        radius /= 60
        coords = self.grab_user_location(all_users=True)
        matched_coords = []
        for coord in coords:
            if ((coord[0] - h) ** 2 + (coord[1] - k) ** 2 <= radius ** 2):
                distance = math.sqrt((coord[1] - k) ** 2 + (coord[0] - h) ** 2)
                matched_coords.append({'latitude':coord[0], 'longitude':coord[1]})
        if (len(matched_coords) != 0):
            return matched_coords
        else:
            return "Not Found"
    def get_score(self, h, k, radius):
        radius /= 4800
        radius /= 60
        #matched_coords = self.grab_nearby_users(h, k, radius)
        '''
        Due to the fact that our team is unable to move around due to current restrictions, we used
        a set of generated test data that we loaded in our backend. Since this normally isn't
        persistent data, it has not been integrated within our blockchain
        '''
        matched_coords = self.matched_coords
        if (matched_coords != "Not Found"):
            coord_area = (((6 / 4800 / 60) ** 2)* math.pi)
            return {'latitude':h, 'longitude':k, 'percentage':((len(matched_coords) - 1)/((math.pi * (radius ** 2)) / coord_area)) * 100}
        else:
            return "Not Found"
  
        

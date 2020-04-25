import math
import requests
class Interface():
    
    def __init__(self):
        self.api_url = "https://api.geospark.co/v1/api"
        self.headers = {'Content-Type':'application/json',
                'Api-Key': '9b92e9804d3d4991989b85ca2ba07d90'}
        self.max_intensity = 100
    def grab_user_location(self, uid=None, all_users=False):
        if (not all_users):
            req = requests.get(self.api_url + "/user/?user_id={}".format(uid), headers=self.headers).json()
            return req['data'][0]['last_location_update']['coordinates']['coordinates']
        req = requests.get(self.api_url + '/user/', headers=self.headers).json()
        coords = [user['last_location_update']['coordinates']['coordinates'] for user in req['data']['users']]
        return coords
    def grab_nearby_users(self, h, k, radius):
        radius  /= 4800
        radius /= 60
        coords = self.grab_user_location(all_users=True)
        matched_coords = []
        for coord in coords:
            if ((coord[0] - h) ** 2 + (coord[1] - k) ** 2 <= radius ** 2):
                distance = math.sqrt((coord[1] - k) ** 2 + (coord[0] - h) ** 2)
                matched_coords.append({str(coords):str(self.max_intensity - distance)})
        return matched_coords
  
        


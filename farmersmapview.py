from kivy.garden.mapview import MapView
from  kivy.lang.builder import Builder
from kivy.clock import Clock
Builder.load_string("""
#:import MapView kivy.garden.mapview.MapView
<FarmersMapView>:
    lat: 24.245943 
    lon: 120.531460
    zoom: 13
    on_zoom:
        self.zoom = 10 if self.zoom < 10 else self.zoom
""", filename="farmersmapview.kv")

class FarmersMapView(MapView):
    getting_markets_timer = None
    
    # def start_getting_markets_in_fov(self):
    #     try:
    #         self.getting_markets_timer.cancle()
    #     except:
    #         pass
    #     self.getting_markets_timer = Clock.schedule_once(self.get_markets_in_fov, 1)
    
    # def get_markets_in_fov(self, *args):
    #     print(self.get_bbox())
    #     
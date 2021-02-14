import kivy
from kivy.modules import inspector
from kivy.core.window import Window
from kivy.app import App 
from kivy.lang import Builder
from kivy.uix.widget import Widget
from kivy.uix.gridlayout import GridLayout
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.widget import Widget 
from kivy.uix.textinput import TextInput 
from kivy.uix.relativelayout import RelativeLayout 
from kivy.uix.label import Label
from kivy.uix.checkbox import CheckBox
from kivy.uix.button import Button
from kivy.metrics import sp
from kivy.uix.popup import Popup
from kivy.uix.image import Image
from kivy.uix.popup import Popup
from kivy.uix.progressbar import ProgressBar 
from kivy.clock import Clock
from kivy.uix.behaviors import ButtonBehavior
from kivy.uix.floatlayout import FloatLayout
from kivy.uix.image import Image


from kivymd.uix.list import TwoLineIconListItem
from kivymd.uix.list import ThreeLineIconListItem
from kivymd.app import MDApp
from kivymd.uix.label import MDLabel
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.floatlayout import MDFloatLayout
from kivy.uix.behaviors.drag import DragBehavior
from kivymd.uix.button import MDRaisedButton
from kivymd.uix.button import MDFlatButton
from kivymd.uix.button import MDTextButton
from kivymd.uix.button import MDRectangleFlatIconButton
from kivymd.uix.dialog import MDDialog
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.textfield import MDTextFieldRect
from kivymd.uix.card import MDCardSwipe
from kivymd.uix.list import ThreeLineListItem
from kivymd.uix.progressbar import MDProgressBar
from kivymd.uix.card import MDCard

from farmersmapview import FarmersMapView
from kivy.lang import Builder
from kivy.metrics import dp
from kivy.properties import (
    BooleanProperty,
    ListProperty,
    NumericProperty,
    OptionProperty,
    StringProperty,
    ObjectProperty,
)
import kivymd.material_resources as m_res
from kivymd.theming import ThemableBehavior
from kivymd.uix.behaviors import RectangularRippleBehavior
from kivymd.uix.button import MDIconButton
from kivymd.uix.gridlayout import MDGridLayout
from kivymd.uix.selectioncontrol import MDCheckbox
from kivymd.uix.list import BaseListItem
from kivymd.uix.list import ContainerSupport
from kivymd.uix.list import IconLeftWidget
from kivymd.uix.list import ILeftBodyTouch
from kivymd.uix.button import MDIconButton

import final_combiner
import get_data as gd
import webbrowser
from functools import partial
from kivy.graphics import *
from kivy_garden.mapview import MapView, MapMarkerPopup
from kivy_garden.mapview.geojson import GeoJsonMapLayer
import os, sys



class Test(MDGridLayout, MDApp, Widget):

    '''這是螢幕主畫面(不包含一開始進去tutorial，tutorial在650多行那邊的on_start()'''

    '''這邊到300行出頭是一開始進去後會難到的配置，300多行後會是按完Run之後會秀出來的畫面'''

    progress_bar = ObjectProperty()
    def __init__(self, **kwargs):
        super(Test, self).__init__(**kwargs)

        self.click = 0

        # ---以下定義點擊前三名按鈕時的次數---
        self.add1 = 0
        self.add1_shop_list = []
        self.add1_temp_list = []
        self.add1_rent_list = []
        self.add1_bound = []
        self.bound1 = GeoJsonMapLayer()

        self.add2 = 0
        self.add2_shop_list = []
        self.add2_temp_list = []
        self.add2_rent_list = []
        self.add2_bound = []
        self.bound2 = GeoJsonMapLayer()

        self.add3 = 0
        self.add3_shop_list = []
        self.add3_temp_list = []
        self.add3_rent_list = []
        self.add3_bound = []
        self.bound3 = GeoJsonMapLayer()

        # from geopy.geocoders import Nominatim
        # self.geolocator = Nominatim(user_agent="Brian_map")

        # self.wid = Widget()
        self.progress_bar = MDProgressBar()
        self.popup = MDDialog(
            title ='數據加載中，請稍後！',
            
            #content = self.progress_bar
        )
        self.popup.auto_dismiss =False
        self.popup.add_widget(self.progress_bar)
        self.popup.children[1].size_hint = [1, 1]
        self.popup.children[1].children[5].font_size = 40
        self.popup.children[1].children[5].font_name = 'msjhbd.ttc'
        self.popup.size_hint = [0.5, 0.5]
        self.popup.background_color = [0.5,0.5,0.5,0.75]
        self.progress_bar.value = 1
        self.popup.bind(on_open = self.puopen)


        # 主畫面切成左右兩欄
        self.cols = 3

        # 左欄是一個Gridlayout,有四列
        self.left = MDGridLayout(rows=6, size_hint=[0.4, 1], spacing=[0,3])
        # 創建地圖
        self.map = FarmersMapView()
        
        # 左欄最上方要來做店租範圍
        self.left.one = MDGridLayout(size=[590,657], rows=2,
                                     size_hint=[1, 0.2], md_bg_color=[0.39, 0.4, 0.72, 1],
                                     padding=[35,-20, 35, -20], spacing=[0,-30])
        # 把標籤裝進去最上層
        self.left.one.add_widget(Label(text='選擇月租範圍', font_size='20sp', font_name='msjhbd.ttc', size_hint_y=0.18))
        # 新增一層容器準備裝三個東西
        self.left.one.box = BoxLayout(spacing=8, size_hint_y=0.15)
        # 盒子裝進一個下限input、一上限input、一個'-'tag
        self.lower_bound = MDTextFieldRect(x=275, hint_text="$下限", font_name='msjhbd.ttc', pos_hint={'y':0.45}, size_hint=[1.5,0.5], use_bubble=True, use_handles=True)
        self.upper_bound = MDTextFieldRect(hint_text="$上限", font_name='msjhbd.ttc', pos_hint={'y':0.45}, center_x=275.76, center_y=508.20, size_hint=[1.5,0.5], use_bubble=True, use_handles=True)
        self.dash_sign = MDFlatButton(text='-', font_size=30, size_hint=[1, 0.49], pos_hint={'y':0.45})
        self.dash_sign.md_bg_color = [1, 1, 1, 1]
        self.left.one.box.add_widget(self.lower_bound)
        self.left.one.box.add_widget(self.dash_sign)
        self.left.one.box.add_widget(self.upper_bound)
        # 盒子裝回上層
        self.left.one.add_widget(self.left.one.box)

        # 新增行政區選單
        self.left.six = MDGridLayout(size=[590,657], rows=2,
                                     size_hint=[1, 0.25], md_bg_color=[0.39, 0.4, 0.72, 1],
                                     padding=[35,-5, 35, 5], spacing=[0,-10])
        self.left.six.add_widget(Label(text='行政區選擇', font_size='20sp', font_name='msjhbd.ttc', height=32, size_hint=[1,0.1]))
        self.left.six.box = BoxLayout(size_hint_y=0.15, center_y=390)
        from kivy.uix.spinner import Spinner
        district = ["中區", "東區", "西區", "南區", "北區", "西屯區", "南屯區", "北屯區", "豐原區", "大里區", "太平區", "清水區", "沙鹿區", "大甲區", "東勢區", "梧棲區", "烏日區", "神岡區", "大肚區", "大雅區", "后里區", "霧峰區", "潭子區", "龍井區", "外埔區", "和平區", "石岡區", "大安區", "新社區"]
        self.spinner = Spinner(
            text='行政區',
            values=[n for n in district],
            size_hint=(None, None),
            size=(95, 44),
            #pos_hint = {'right':0.2},
            font_name='msjhbd.ttc',
            background_color=[1,0,0,1])
        self.spinner.option_cls.font_name = 'msjhbd.ttc'
        self.spinner.option_cls.background_color = [1,0,0,1]
        #self.spinner.values[0].font_name = 'msjhbd.ttc'
        self.spinner.dropdown_cls.max_height = self.spinner.height* 7 + 7 * 4
        #self.spinner.center_x = 160
        #self.left.six.box.add_widget(BoxLayout(size_hint_y=0.5, size_hint_x=0.5, width=100))
        self.left.six.box.add_widget(MDGridLayout(md_bg_color=[0.39, 0.4, 0.72, 1], size_hint=[None,0.5]))
        self.left.six.box.add_widget(self.spinner)
        self.left.six.add_widget(self.left.six.box)
        #self.left.six.box.children[0].center = (160, 522.1339285)
        #self.spinner.pos_hint = {'right':0.9}
        #self.spinner.center_x = 150
        
        
        # 這裡是畫面左欄第二格
        self.left.two = MDGridLayout(rows=2, size_hint=[1,None], size=[365,170], md_bg_color=[0.39, 0.4, 0.72, 1])
        #self.left.two.center_y = 400
        # 把"指標排序"標籤裝進第二格子的上方
        self.left.two.add_widget(Label(text='指標排序', font_size='20sp', font_name='msjhbd.ttc', height=32, size_hint=[1,0.1]))
        # 左欄第二格下方增加一個grid容器
        self.left.two.grid = MDGridLayout(rows=3, size_hint=[1,0.26], padding=[30,0,20,0])
        self.left.two.grid.size_hint = [1,0.26]
        self.left.two.add_widget(self.left.two.grid)
        # 準備三個box放入此grid
        self.left.two.box1 = BoxLayout(size_hint=[1,None], size=[365,40], spacing=13) 
        self.left.two.box2 = BoxLayout(size_hint=[1,None], size=[365,40], spacing=13)        
        self.left.two.box3 = BoxLayout(size_hint=[1,None], size=[365,40], spacing=13)
        self.left.two.grid.add_widget(self.left.two.box1)
        self.left.two.grid.add_widget(self.left.two.box2)
        self.left.two.grid.add_widget(self.left.two.box3)
        # 處理第一個box的標籤(全用按鈕取代)、輸入
        self.left.two.btn1 = MDRaisedButton(text='      人口特性      ', font_name='msjhbd.ttc', font_size='16sp')
        self.left.two.btn1.md_bg_color =  [0.55, 0.63, 0.99, 1]
        self.left.two.input1 = MDTextFieldRect(hint_text='請輸入1、2、3：', size_hint=[1,None], size=[94,37], font_name='msjhbd.ttc')
        self.left.two.input1.size_hint_x = None
        self.left.two.input1.width = 120
        self.left.two.box1.add_widget(self.left.two.btn1)
        self.left.two.box1.add_widget(self.left.two.input1)

        self.left.two.btn3 = MDRaisedButton(text='      薪資所得      ', font_name='msjhbd.ttc', font_size='16sp')
        self.left.two.btn3.md_bg_color =  [0.68, 0.82, 0.96, 1]
        self.left.two.input3 = MDTextFieldRect(hint_text='請輸入1、2、3：', size_hint=[1,None], size=[94,37], font_name='msjhbd.ttc')
        self.left.two.input3.size_hint_x = None
        self.left.two.input3.width = 120
        self.left.two.box2.add_widget(self.left.two.btn3)
        self.left.two.box2.add_widget(self.left.two.input3)

        self.left.two.btn5 = MDRaisedButton(text='      人口消長      ', font_name='msjhbd.ttc', font_size='16sp')
        self.left.two.btn5.md_bg_color =  [0.5, 0.87, 0.98, 1]
        self.left.two.input5 = MDTextFieldRect(hint_text='請輸入1、2、3：', size_hint=[1,None], size=[94,37], font_name='msjhbd.ttc')
        self.left.two.input5.size_hint_x = None
        self.left.two.input5.width = 120
        self.left.two.box3.add_widget(self.left.two.btn5)
        self.left.two.box3.add_widget(self.left.two.input5)


        # 這裡是畫面左欄第三格
        self.left.three = MDGridLayout(rows=2, md_bg_color=[0.39, 0.4, 0.72, 1], size_hint=[1, 0.57])
        # 把"指標排序"標籤裝進第二格子的上方
        self.left.three.add_widget(Label(text='選擇競爭對手', font_size='20sp', font_name='msjhbd.ttc', height=32, size_hint=[1,0.06]))
        
        # 左欄第三格下方增加一個grid容器
        self.left.three.grid = MDGridLayout(rows=5, size_hint=[1,0.26], spacing=3, padding=[30,0,40,0])
        self.left.three.add_widget(self.left.three.grid)
        # 準備五個box放入此grid
        self.left.three.box1 = BoxLayout(size_hint=[1, 0.05])
        self.left.three.box2 = BoxLayout(size_hint=[1, 0.05])        
        self.left.three.box3 = BoxLayout(size_hint=[1, 0.05])
        self.left.three.box4 = BoxLayout(size_hint=[1, 0.05])
        #self.left.three.box5 = BoxLayout(size_hint=[1, 0.4])
        self.left.three.box6 = BoxLayout()
        self.left.three.grid.add_widget(self.left.three.box1)
        self.left.three.grid.add_widget(self.left.three.box2)
        self.left.three.grid.add_widget(self.left.three.box3)
        self.left.three.grid.add_widget(self.left.three.box4)

        
        # 處理第一個box的標籤(全用按鈕取代)、勾選
        self.left.three.btn1 = MDRaisedButton(text='       早餐店         ', font_name='msjhbd.ttc', size_hint=[None, 0.9], font_size='16sp')
        self.left.three.btn1.md_bg_color = [0.55, 0.63, 0.99, 1]
        self.left.three.input1 = MDCheckbox()
        self.left.three.input1.x = 140
        self.left.three.input1.selected_color = (1,1,1,1)
        self.left.three.input1.unselected_color = (1,1,1,1)
        self.left.three.box1.add_widget(self.left.three.btn1)
        self.left.three.box1.add_widget(self.left.three.input1)
        # 處理第二個box的標籤(全用按鈕取代)、勾選
        self.left.three.btn2 = MDRaisedButton(text='便當、自助餐店', font_name='msjhbd.ttc', size_hint=[None, 0.9], font_size='16sp')
        self.left.three.btn2.md_bg_color = [0.48, 0.81, 0.78, 1]
        self.left.three.input2 = MDCheckbox()
        self.left.three.input2.x = 140
        self.left.three.input2.selected_color = (1,1,1,1)
        self.left.three.input2.unselected_color = (1,1,1,1)
        self.left.three.box2.add_widget(self.left.three.btn2)
        self.left.three.box2.add_widget(self.left.three.input2)
        # 處理第三個box的標籤(全用按鈕取代)、勾選
        self.left.three.btn3 = MDRaisedButton(text='麵店、小吃店    ', font_name='msjhbd.ttc', size_hint=[None, 0.9], font_size='16sp')
        self.left.three.btn3.md_bg_color = [0.68, 0.82, 0.96, 1]
        self.left.three.input3 = MDCheckbox()
        self.left.three.input3.x = 140
        self.left.three.input3.selected_color = (1,1,1,1)
        self.left.three.input3.unselected_color = (1,1,1,1)
        self.left.three.box3.add_widget(self.left.three.btn3)
        self.left.three.box3.add_widget(self.left.three.input3)
        # 處理第四個box的標籤(全用按鈕取代)、勾選  
        self.left.three.btn4 = MDRaisedButton(text='      餐館餐廳      ', font_name='msjhbd.ttc', size_hint=[None, 0.9], font_size='16sp')
        self.left.three.btn4.md_bg_color = [0.62, 0.84, 0.51, 1]
        self.left.three.input4 = MDCheckbox()
        self.left.three.input4.x = 140
        #self.left.three.input4.color = [1,1,1,2]
        self.left.three.input4.selected_color = (1,1,1,1)
        self.left.three.input4.unselected_color = (1,1,1,1)
        self.left.three.box4.add_widget(self.left.three.btn4)
        self.left.three.box4.add_widget(self.left.three.input4)

        self.run_button = MDRaisedButton(text='Run')

        # 製作廟宇按鈕
        self.left.four = MDGridLayout(rows=2, size_hint=[1,None], size=[365,90], md_bg_color=[0.39, 0.4, 0.72, 1])
        self.left.four.add_widget(Label(text='廟宇出現與否', font_size='20sp', font_name='msjhbd.ttc', height=32, size_hint=[1,0.025]))
        self.left.four.box = BoxLayout(size_hint=[1, 0.025], padding=[30,-20,40,5])
        self.left.four.add_widget(self.left.four.box)
        self.left.four.btn = MDRaisedButton(text='          廟宇          ', font_name='msjhbd.ttc', size_hint=[None, 0.8], font_size='16sp')
        self.left.four.input = MDCheckbox()
        self.left.four.input.selected_color = (1,1,1,1)
        self.left.four.input.unselected_color = (1,1,1,1)
        self.left.four.box.add_widget(self.left.four.btn)
        self.left.four.box.add_widget(self.left.four.input)

        # 把每一層加回去
        self.left.add_widget(self.left.one)
        self.left.add_widget(self.left.six)
        self.left.add_widget(self.left.two)
        self.left.add_widget(self.left.three)
        self.left.add_widget(self.left.four)
        self.add_widget(self.left)
        self.add_widget(self.map)

        

        # 測試用的按鈕 
        #self.run_button = MDRaisedButton(text='Run')
        self.left.five = MDGridLayout(size_hint=[1,0.1], md_bg_color=[0.39, 0.4, 0.72, 1])
        self.left.five.add_widget(self.run_button)
        self.run_button.bind(on_release=self.popup.open)
        self.left.add_widget(self.left.five)
        self.run_button.right = 270
        self.run_button.ripple_alpha = 0.7
        self.run_button.radius = [10,10,10,10]
        self.run_button.md_bg_color = [1,1,1,1]
        self.run_button.text_color = [0,0,0,1]
        #self.left.six.box.children[0].right = 150
        #self.left.six.box.right = 390
        #self.left.six.box.children[0].pos_hint = {'right':0.001, 'left':0.9}
        

        
        #self.left.four.box.pos_hint = {'top':0.5}

    def add_shop(self, neigh, clist, password):
        shop_list = gd.get_shop_codata(neigh, clist)
        # print(shop_list)
        #self.add1 += 1
        #print(self.add1)
        print('###add_shop_func###')
        if shop_list == ['no data']:
            print('')
        else:
            for shop in shop_list:
                lon = float(shop['coor'][1])
                lat = float(shop['coor'][0])
                marker = MapMarkerPopup(lat = lat, lon = lon, source = "競爭對手_標點.png")
                marker.add_widget(Button(text=neigh+ '\n' +shop['name']+ '\n' + shop['class'], font_name='msjhbd.ttc', 
                    font_size = 15, size_hint= [None, None], size = [150,150]))
                self.map.add_marker(marker)
                if(password == 1):
                    self.add1_shop_list.append(marker)
                elif(password == 2):
                    self.add2_shop_list.append(marker)
                elif(password == 3):
                    self.add3_shop_list.append(marker)
            #print(self.add1)
        # else:
        #     for marker in self.add1_shop_list:
        #         self.map.remove_marker(marker)
                #print('sucess')
    def clear_shop(self, password):

        print('###clear_shop_func###')

        if(password == 1):
            print("clear1!")
            for marker in self.add1_shop_list:
                self.map.remove_marker(marker)
            self.add1_shop_list.clear()
        elif(password == 2):
            print("clear2!")
            for marker in self.add2_shop_list:
                self.map.remove_marker(marker)
            self.add2_shop_list.clear()
        elif(password == 3):
            for marker in self.add3_shop_list:
                self.map.remove_marker(marker)
            self.add3_shop_list.clear()


    def add_temp(self, neigh, boolt, password):
        print('###add_temp_func###')

        temp_list = gd.get_temp_codata(neigh)
        # print(temp_list)
        if boolt == True:
            if temp_list == ['no data']:
                print('')
            else:
                for temp in temp_list:
                    lon = float(temp['coor'][1])
                    lat = float(temp['coor'][0])
                    marker = MapMarkerPopup(lat = lat, lon = lon, source = "廟_標點.png")
                    marker.add_widget(Button(text=neigh+ '\n' +temp['name'], font_name='msjhbd.ttc', 
                        font_size = 15, size_hint= [None, None], size = [100,100]))
                    self.map.add_widget(marker)
                    if(password == 1):
                        self.add1_temp_list.append(marker)
                    elif(password == 2):
                        self.add2_temp_list.append(marker)
                        print('hoooooo')
                    elif(password == 3):
                        self.add3_temp_list.append(marker)
        else:
            print("")
    
    def clear_temp(self, password):
        print('###clear_temp_func###')
        
        if(password == 1):
            print("clear1!")
            for marker in self.add1_temp_list:
                print(marker)
                self.map.remove_marker(marker)
            self.add1_temp_list.clear() 
        elif(password == 2):
            print("clear2!")
            for marker in self.add2_temp_list:
                print(marker)
                self.map.remove_marker(marker)
            self.add2_temp_list.clear()
        elif(password == 3):
            for marker in self.add3_temp_list:
                print(marker)
                self.map.remove_marker(marker)
            self.add3_temp_list.clear()
        
        

    def add_rent(self,password, neigh, Min_price = 0, Max_price = 100000000):
        print('###add_rent_func###')
        
        # print(Min_price, Max_price)
        rent_list = gd.get_rent_codata(neigh)
        # print(rent_list)
        if rent_list == ['no data']:
            print('')
        else:
            cou = 1
            for rent in rent_list:
                if (int(rent['price']) >= Min_price) & (int(rent['price']) <= Max_price):
                    lon = float(rent['coor'][1])
                    lat = float(rent['coor'][0])
                    marker = MapMarkerPopup(lat = lat, lon = lon, source = "店面_標點.png")
                    rent_button = Button(text=neigh+ '\n' +'店面' + str(cou)+ '\n' +rent['size']+ '\n' + '$'+rent['price']+'/月', font_name='msjhbd.ttc', 
                        font_size = 15, size_hint= [None, None], size = [100,100])
                    rent_button.bind(on_press = partial(webbrowser.open, rent['web']))
                    marker.add_widget(rent_button)
                    self.map.add_widget(marker)
                    cou += 1 
                    if(password == 1):
                        self.add1_rent_list.append(marker)
                    elif(password == 2):
                        self.add2_rent_list.append(marker)
                    elif(password == 3):
                        self.add3_rent_list.append(marker)
    
    def clear_rent(self, password):
        print('###clear_rent_func###')

        
        if(password == 1):
            print("clear1!")
            for marker in self.add1_rent_list:
                self.map.remove_marker(marker)
            self.add1_rent_list.clear()
        elif(password == 2):
            print("clear2!")
            for marker in self.add2_rent_list:
                self.map.remove_marker(marker)
            self.add2_rent_list.clear()
        elif(password == 3):
            for marker in self.add3_rent_list:
                self.map.remove_marker(marker)
            self.add3_rent_list.clear()


    
    # def add_border(self, filename):
    #     import os, sys
    #     import json
    #     with open(os.path.realpath(sys.argv[0]).strip(sys.argv[0])+"data\\"+"鄰里邊界\\"+filename, 'r', encoding = 'utf-8') as f:
    #         data = json.load(f)
    #     for i in data['features'][0]['geometry']['coordinates'][0]:
    #         lon = i[0]
    #         lat = i[1]
    #         marker = MapMarkerPopup(lon=lon, lat=lat, source='邊界.png')
    #         self.map.add_widget(marker)
    

    def add_boundary(self, password):
        print('###add_boundary_func###')

        print('我要密碼')
        print(password)
        # if(self.add1 == 1 and password == 1):
        #     self.bound1 = GeoJsonMapLayer()
        # elif(self.add2 == 1 and password == 2):
        #     self.bound2 = GeoJsonMapLayer()
        # if(self.add3 == 1 and password == 3):
        #     self.bound3 = GeoJsonMapLayer()
        #self.bound3 = GeoJsonMapLayer()

        # if(password == 1):
        #     print('1號邊界成功')
        #     #print("梧棲區\\" + self.rank1.text + ".json")
            
        #     self.bound1.source = os.path.realpath(sys.argv[0]).strip(sys.argv[0]) + "梧棲區\\" + self.rank1.text + ".json"
        #     self.add1_bound.append(self.bound1)
        #     self.map.add_layer(self.bound1)
        if(password == 1):
            
            self.bound1.source = os.path.realpath(sys.argv[0]).strip(sys.argv[0]) + "data\\" + "鄰里邊界\\" + self.spinner.text + "\\" + self.rank1.text + ".json"
           
            self.add1_bound.append(self.bound1)
            self.map.add_layer(self.bound1)
        elif(password == 2):
            
            self.bound2.source = os.path.realpath(sys.argv[0]).strip(sys.argv[0]) + "data\\" + "鄰里邊界\\" + self.spinner.text + "\\" + self.rank2.text + ".json"
            self.add2_bound.append(self.bound2)
            self.map.add_layer(self.bound2)
        elif(password == 3):
            
            self.bound3.source = os.path.realpath(sys.argv[0]).strip(sys.argv[0]) + "data\\" + "鄰里邊界\\" + self.spinner.text + "\\" + self.rank3.text + ".json"
           
            self.add3_bound.append(self.bound3)
            self.map.add_layer(self.bound3)
        # elif(password == 3):
        #     print(password)
            
        #     self.bound3.source = os.path.realpath(sys.argv[0]).strip(sys.argv[0]) + "梧棲區\\" + self.rank3.text + ".json"
        #     self.add3_bound.append(self.bound3)
        #     self.map.add_layer(self.bound3)
        # if(password == 1):
        #     self.bound1.source = os.path.realpath(sys.argv[0]).strip(sys.argv[0]) + "梧棲區\\" + self.rank1.text + ".json"
        #     #print(bound1.source)
        #     self.add1_bound.append(self.bound1)
        #     print("我是密碼" + str(password))
        #     print(self.rank1.text)
        # elif(password == 2):
        #     self.bound2.source = os.path.realpath(sys.argv[0]).strip(sys.argv[0]) + "梧棲區\\" + self.rank2.text + ".json"
        #     #print(self.bound2.source)
        #     self.add2_bound.append(self.bound2)
        #     print("我是密碼" + str(password))
        #     print(self.rank2.text)
        # elif(password == 3):
        #     self.bound3.source = os.path.realpath(sys.argv[0]).strip(sys.argv[0]) + "梧棲區\\" + self.rank3.text + ".json"
        #     self.add3_bound.append(self.bound3)
        #     print("我是密碼" + str(password))
        
        # if(password == 1):
        #     self.map.add_layer(self.bound1)
        # elif(password == 2):
        #     self.map.add_layer(self.bound2)
        # elif(password == 3):
        #     self.map.add_layer(self.bound3)

    def remove_boundary(self, password):
        print('###remove_boundary_func###')

        #target = None
        # if(password == 1):
        #     for a in self.add1_bound:
        #         self.map.remove_layer(a)
        #         self.add1_bound.clear()
        if(password == 1):
            for b in self.add1_bound:
                self.map.remove_layer(b)
                self.add1_bound.clear()
        elif(password == 2):
            for b in self.add2_bound:
                self.map.remove_layer(b)
                self.add2_bound.clear()
        elif(password == 3):
            for b in self.add3_bound:
                self.map.remove_layer(b)
                self.add3_bound.clear()
        # elif(password == 3):
        #     for c in self.add3_bound:
        #         self.map.remove_layer(c)
        #         self.add3_bound.clear()
        #print(target, end=',,')
        #self.map.remove_layer(target[0])
        #target.clear()
        #print(target, end=',,')


    '''pressed定義Run之後處理數據並放到資訊卡上的事件'''

    acard = None
    def pressed(self, instance):
        print(self.spinner.text)
        #print(self.spinner.text)
        top3_rank = final_combiner.final_rank([int(self.left.two.input1.text),int(self.left.two.input3.text),int(self.left.two.input5.text)])
        if not self.acard:
            self.rank1 = ThreeLineIconListItem(text=top3_rank[0][0], secondary_text='人口特性：' + str(top3_rank[0][1]), tertiary_text='新資所得：' + str(top3_rank[0][2]), text_color=[1,1,1,1])
            self.rank1.add_widget(IconLeftWidget(icon='numeric-1-box'))
            self.rank1.bg_color=[0,0,0,0]
            self.rank1.children[1].children[2].font_name = 'msjhbd.ttc'
            self.rank1.children[1].children[1].font_name = 'msjhbd.ttc'
            self.rank1.children[1].children[0].font_name = 'msjhbd.ttc'
            self.rank1.children[1].children[2].font_size = '18'
            
            more_rank1 = MDLabel(text='人口消長：' + str(top3_rank[0][3]))
            more_rank1.font_name = 'msjhbd.ttc'
            more_rank1.font_style = 'Body1'
            more_rank1.font_size = 16
            more_rank1.color = [0,0,0,0.7]
            self.rank1.children[1].add_widget(more_rank1)
            self.rank1.children[1].size_hint = [1, None]
            self.rank1.children[1].children[3].pos = [56, 280]

            self.rank1.children[0].children[0].children[0].color = [1,1,1,1]
            self.rank1.children[0].children[0].children[0].pos_hint = {'left':0.1}
            self.rank1.children[0].padding = [-10,0,0,0]
            self.rank1.children[1].children[3].theme_text_color = 'Custom'
            self.rank1.children[1].children[3].text_color = [1,1,1,1]
            self.rank1.children[1].children[2].theme_text_color = 'Custom'
            self.rank1.children[1].children[2].text_color = [1,1,1,1]
            self.rank1.children[1].children[1].theme_text_color = 'Custom'
            self.rank1.children[1].children[1].text_color = [1,1,1,1]
            self.rank1.children[1].children[0].theme_text_color = 'Custom'
            self.rank1.children[1].children[0].text_color = [1,1,1,1]
            # 從另一個預先寫好、計算各里指標分數的模組final_combiner引進final_rank函數，取得前三名的區域及其各項指標分數後用top3_rank變數紀錄起來
            # 接著改寫、擴充kivy套件內的工具(ThreeLineIconListItem)，做成資訊卡，同時使其擁有按鈕的特性讓使用者做點選


            self.rank2 = ThreeLineIconListItem(text=top3_rank[1][0], secondary_text='人口特性：' + str(top3_rank[1][1]), tertiary_text='新資所得：' + str(top3_rank[1][2]))
            self.rank2.add_widget(IconLeftWidget(icon='numeric-2-box'))
            self.rank2.bg_color=[0,0,0,0]

            self.rank2.children[1].children[2].font_size = '18'
            self.rank2.children[1].children[2].font_name = 'msjhbd.ttc'
            self.rank2.children[1].children[1].font_name = 'msjhbd.ttc'
            self.rank2.children[1].children[0].font_name = 'msjhbd.ttc'
            
            more_rank2 = MDLabel(text='人口消長：' + str(top3_rank[1][3]))
            more_rank2.font_name = 'msjhbd.ttc'
            more_rank2.font_style = 'Body1'
            more_rank2.font_size = 16
            more_rank2.color = [0,0,0,0.54]
            self.rank2.children[1].add_widget(more_rank2)
            self.rank2.children[1].size_hint = [1, None]

            self.rank2.children[0].children[0].children[0].color = [1,1,1,1]
            self.rank2.children[0].children[0].children[0].pos_hint = {'left':0.1}
            self.rank2.children[0].padding = [-10,0,0,0]
            self.rank2.children[1].children[3].theme_text_color = 'Custom'
            self.rank2.children[1].children[3].text_color = [1,1,1,1]
            self.rank2.children[1].children[2].theme_text_color = 'Custom'
            self.rank2.children[1].children[2].text_color = [1,1,1,1]
            self.rank2.children[1].children[1].theme_text_color = 'Custom'
            self.rank2.children[1].children[1].text_color = [1,1,1,1]
            self.rank2.children[1].children[0].theme_text_color = 'Custom'
            self.rank2.children[1].children[0].text_color = [1,1,1,1]

            self.rank3 = ThreeLineIconListItem(text=top3_rank[2][0], secondary_text='人口特性：' + str(top3_rank[2][1]), tertiary_text='新資所得：' + str(top3_rank[2][2]))
            self.rank3.add_widget(IconLeftWidget(icon='numeric-3-box'))
            self.rank3.bg_color=[0,0,0,0]

            self.rank3.children[1].children[2].font_size = '18'
            self.rank3.children[1].children[2].font_name = 'msjhbd.ttc'
            self.rank3.children[1].children[1].font_name = 'msjhbd.ttc'
            self.rank3.children[1].children[0].font_name = 'msjhbd.ttc'
            
            more_rank3 = MDLabel(text= '人口消長：' + str(top3_rank[2][3]))
            more_rank3.font_name = 'msjhbd.ttc'
            more_rank3.font_style = 'Body1'
            more_rank3.font_size = 16
            more_rank3.color = [0,0,0,0.54]
            self.rank3.children[1].add_widget(more_rank3)
            self.rank3.children[1].size_hint = [1, None]

            self.rank3.children[0].children[0].children[0].color = [1,1,1,1]
            self.rank3.children[0].children[0].children[0].pos_hint = {'left':0.1}
            self.rank3.children[0].padding = [-10,0,0,0]
            self.rank3.children[1].children[3].theme_text_color = 'Custom'
            self.rank3.children[1].children[3].text_color = [1,1,1,1]
            self.rank3.children[1].children[2].theme_text_color = 'Custom'
            self.rank3.children[1].children[2].text_color = [1,1,1,1]
            self.rank3.children[1].children[1].theme_text_color = 'Custom'
            self.rank3.children[1].children[1].text_color = [1,1,1,1]
            self.rank3.children[1].children[0].theme_text_color = 'Custom'
            self.rank3.children[1].children[0].text_color = [1,1,1,1]

            self.rank1.size = [352, 100]
            self.rank2.size = [352, 100]
            self.rank3.size = [352, 100]
            
            self.click += 1
            
      
            self.rank1.children[1].padding = [56, 16, 24, 7]
            self.rank2.children[1].padding = [56, 4, 24, 7]
            self.rank3.children[1].padding = [56, 4, 24, 7]

            self.rank1.children[1].children[0].adaptive_height = True
            self.rank1.children[1].pos = [0, 180]
            self.rank2.children[1].children[1].adaptive_height = True
            self.rank2.children[1].pos = [0, 130]
            self.rank3.children[1].children[1].adaptive_height = True
  
            self.add_widget(MDGridLayout(cols=1, size_hint=[0.285,1], md_bg_color=[0.39, 0.4, 0.72, 1]))
            self.children[0].add_widget(self.rank1)
            self.children[0].add_widget(self.rank2)
            self.children[0].add_widget(self.rank3)

            self.rank1.bind(on_release = self.add_renk1_marker)
            self.rank2.bind(on_release = self.add_renk2_marker)
            self.rank3.bind(on_release = self.add_renk3_marker)


    ''' 當初設計沒有想好架構，導致要再次定義pressed事件(第二次之後的Run)，如果是如果是第二次點擊Run之後要重新更新資訊卡的內容'''
    def second_pressed(self, instance):
        for i in range(1,4):
            self.clear_shop(i)
            self.clear_temp(i)
            self.clear_rent(i)
            self.remove_boundary(i)
        self.add1 = 0
        self.add2 = 0
        self.add3 = 0
        #self.map.children[0].unload()
        top3_rank = final_combiner.final_rank([int(self.left.two.input1.text),int(self.left.two.input3.text),int(self.left.two.input5.text)])
        self.rank1.children[1].children[3].text = top3_rank[0][0]
        self.rank1.children[1].children[2].text = "人口特性：" + str(top3_rank[0][1])
        self.rank1.children[1].children[1].text = "新資所得：" + str(top3_rank[0][2])
        self.rank1.children[1].children[0].text = "人口消長：" + str(top3_rank[0][3])

        self.rank2.children[1].children[3].text = top3_rank[1][0]
        self.rank2.children[1].children[2].text = "人口特性：" + str(top3_rank[1][1])
        self.rank2.children[1].children[1].text = "新資所得：" + str(top3_rank[1][2])
        self.rank2.children[1].children[0].text = "人口消長：" + str(top3_rank[1][3])

        self.rank3.children[1].children[3].text = top3_rank[2][0]
        self.rank3.children[1].children[2].text = "人口特性：" + str(top3_rank[2][1])
        self.rank3.children[1].children[1].text = "新資所得：" + str(top3_rank[2][2])
        self.rank3.children[1].children[0].text = "人口消長：" + str(top3_rank[2][3])
        self.rank1.bind(on_release = self.add_renk1_marker)
        self.rank2.bind(on_release = self.add_renk2_marker)
        self.rank3.bind(on_release = self.add_renk3_marker)
    
    def add_renk1_marker(self, instance):
        # print(len(self.map.children[2]))
        cla_list = [self.left.three.btn1.text.strip(), self.left.three.btn2.text.strip(), self.left.three.btn3.text.strip()
        , self.left.three.btn4.text.strip()]
        ch_list = [self.left.three.input1.active, self.left.three.input2.active, self.left.three.input3.active
        , self.left.three.input4.active]
        #print(cla_list, ch_list)
        act_list = []
        for cont in range(4):
            if ch_list[cont] == True:
                act_list.append(cla_list[cont])
        #print(self.rank1.text)
        self.add1 += 1
    
        if(self.add1 % 2 == 1):
            self.add_boundary(1)
            self.add_shop(self.rank1.text, act_list, 1)
            self.add_temp(self.rank1.text, self.left.four.input.active, 1)
            self.add_rent(1,self.rank1.text, int(self.lower_bound.text), int(self.upper_bound.text))
            
            # location = self.geolocator.geocode("梧棲區大庄里")
            # self.map.center_on(location.latitude , location.longitude)
            self.map.center_on(24.2454073 , 120.54976945174974)
        elif(self.add1 % 2 == 0):
            self.remove_boundary(1)
            self.clear_shop(1)
            self.clear_temp(1)
            self.clear_rent(1)
        
        
        # filename = self.rank1.text + ".json"
        # self.add_border(filename)
        
        self.map.zoom = 13
        # from geopy.geocoders import Nominatim
        # geolocator = Nominatim(user_agent="Brian_map")
        
        

    def add_renk2_marker(self, instance):
        cla_list = [self.left.three.btn1.text.strip(), self.left.three.btn2.text.strip(), self.left.three.btn3.text.strip()
        , self.left.three.btn4.text.strip()]
        ch_list = [self.left.three.input1.active, self.left.three.input2.active, self.left.three.input3.active
        , self.left.three.input4.active]

        act_list = []
        for cont in range(4):
            if ch_list[cont] == True:
                act_list.append(cla_list[cont])
        
        self.add2 += 1
        
        if(self.add2 % 2 == 1):
            self.add_boundary(2)
            self.add_shop(self.rank2.text, act_list, 2)
            self.add_temp(self.rank2.text, self.left.four.input.active, 2)
            self.add_rent(2,self.rank2.text, int(self.lower_bound.text), int(self.upper_bound.text))

            # location = self.geolocator.geocode("梧棲區大村里")
            # self.map.center_on(location.latitude , location.longitude)
            self.map.center_on(24.2549239 , 120.5316259)
        elif(self.add2 % 2 == 0):
            self.remove_boundary(2)
            self.clear_shop(2)
            self.clear_temp(2)
            self.clear_rent(2)
        
    def add_renk3_marker(self, instance):
        cla_list = [self.left.three.btn1.text.strip(), self.left.three.btn2.text.strip(), self.left.three.btn3.text.strip()
        , self.left.three.btn4.text.strip()]
        ch_list = [self.left.three.input1.active, self.left.three.input2.active, self.left.three.input3.active
        , self.left.three.input4.active]

        act_list = []
        for cont in range(4):
            if ch_list[cont] == True:
                act_list.append(cla_list[cont])

        self.add3 += 1
        
        if(self.add3 % 2 == 1):
            self.add_boundary(3)
            self.add_shop(self.rank3.text, act_list, 3)
            self.add_temp(self.rank3.text, self.left.four.input.active, 3)
            self.add_rent(3,self.rank3.text, int(self.lower_bound.text), int(self.upper_bound.text))

            # location = self.geolocator.geocode("梧棲區大村里")
            # self.map.center_on(location.latitude , location.longitude)
            self.map.center_on(24.2570033 , 120.53346300048884)
        elif(self.add3 % 2 == 0):
            self.remove_boundary(3)
            self.clear_shop(3)
            self.clear_temp(3)
            self.clear_rent(3)

 
    '''進度條跑到滿格時，要讓他reset變1'''
    def progress_reset(self, run):
        self.progress_bar.value = 1
        
    '''讓進度條要一直往右跑，如果滿了就要關掉進度條畫面'''
    def next(self, dt):
        self.progress_bar.value += 6
        if self.progress_bar.value >= 100:
            
            Clock.schedule_once(self.popup.dismiss, 0.5)
            if self.click == 0:
                Clock.schedule_once(self.pressed, 0.6)
            else:
                Clock.schedule_once(self.second_pressed, 0.6)
            #else:
            Clock.unschedule(self.new)
            Clock.schedule_once(self.progress_reset, 0.6)
            
    '''定義進度條跑的速率'''
    def puopen(self, instance):

        self.new = Clock.schedule_interval(self.next, 1/20)
        #if self.progress_bar.value >= 100:
            

'''這邊我拿來處理螢幕一開始進去要看到的tutorial，然後這邊算是程式運行的主體，就是說透過這個class，kivy會提供一個是窗給你去裝載你所有的畫面'''
class 商業選址App(MDApp):

    dialog = None

    def build(self):
        inspector.create_inspector(Window, Test())   
        return Test()

    def on_start(self):

    
        if not self.dialog:
            self.dialog = MDDialog(
                #text="Discard draft?",
                buttons=[
                    MDFlatButton(
                        text="     ", text_color=self.theme_cls.primary_color
                    ),
                    MDRectangleFlatIconButton(
                        text="I know！", text_color=self.theme_cls.primary_color, font_name='msjhbd.ttc', on_release=self.dialog_vanish
                    )
                
                ]
            )
            self.dialog.add_widget(Image(source='tutorial.png'))
            self.dialog.auto_dismiss = False
            self.dialog.size_hint = [0.74, 0.74]
            self.dialog.children[1].size_hint = [1,1]
            self.dialog.md_bg_color = [1,1,1,1]
            
        self.dialog.open()

    def dialog_vanish(self, obj):
        self.dialog.dismiss()

if __name__ == "__main__":
    商業選址App().run()
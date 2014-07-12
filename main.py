
#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4 nu

'''
SuperShape Editor
'''

__title__ = 'SuperShape'
__version__ = '0.4'
__author__ = 'julien@hautefeuille.eu'

import sys
import os

# If platform is android, turn-off log system
# Need to avoid SD card full
if sys.platform == 'android':
    os.environ['KIVY_NO_CONSOLELOG'] = '1'

# Main Kivy import
import kivy
kivy.require('1.8.1')
from kivy.config import Config
from kivy.app import App

# If platform different of android then fix the screen resolution
# Better view on Desktop
if sys.platform != 'android':
    Config.set('graphics', 'width', 960)
    Config.set('graphics', 'height', 540)
if sys.platform != 'linux':
    Config.set('graphics', 'width', 1280)
    Config.set('graphics', 'height', 720)

# Tools Kivy imports
from kivy.uix.button import Button
from kivy.uix.popup import Popup
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.label import Label
from kivy.uix.slider import Slider
from kivy.uix.colorpicker import ColorPicker
from kivy.uix.switch import Switch
from kivy.logger import Logger

# Supershape lib for Kivy
from supershape import Shape

# Transform path list
from tools import coupled

# Export to svg file
import svgwrite


class RightMenu(BoxLayout):
    '''
    RightMenu class
    '''
    pass


class MainBox(BoxLayout):
    '''
    Mainbox class
    '''

    def __init__(self, **kwargs):
        '''
        Init main class ui
        '''
        super(MainBox, self).__init__(**kwargs)
        self.f_size = '15sp'

        # Shape Widget
        self.shape = Shape(size_hint=(0.7, 1))
        self.add_widget(self.shape)

        # Right Menu
        self.panel = TabbedPanel(size_hint=(0.3, 1), do_default_tab=False)
        self.tab_param = TabbedPanelItem(text='Parameters')
        self.tab_color = TabbedPanelItem(text='Shape')
        self.tab_color_bg = TabbedPanelItem(text='Background')
        self.tab_export = TabbedPanelItem(text='Export')
        self.panel.add_widget(self.tab_param)
        self.panel.add_widget(self.tab_color)
        self.panel.add_widget(self.tab_color_bg)
        self.panel.add_widget(self.tab_export)

        self.menu_right = RightMenu(
            padding=15,
            orientation="vertical")

        # Switch mode line
        self.box_switch = BoxLayout(orientation='horizontal')
        self.mode_label = Label(
            text="Line mode",
            font_size=self.f_size,
            markup=True)
        self.box_switch.add_widget(self.mode_label)
        self.switch_mode = Switch(active=False)
        self.switch_mode.bind(active=self.on_switch)
        self.box_switch.add_widget(self.switch_mode)
        self.menu_right.add_widget(self.box_switch)

        # Size value
        self.box_size = BoxLayout(orientation='horizontal')
        self.size_label = Label(
            text="Shape size",
            font_size=self.f_size,
            markup=True)
        self.size_label_value = Label(
            text=str(self.shape.shape_size),
            font_size=self.f_size,
            markup=True)
        self.box_size.add_widget(self.size_label)
        self.box_size.add_widget(self.size_label_value)
        self.slider_shape_size = Slider(
            min=self.shape.property('shape_size').get_min(self.shape),
            max=self.shape.property('shape_size').get_max(self.shape),
            value=self.shape.shape_size, step=1)
        self.slider_shape_size.bind(value=self.change_shape_size)
        self.menu_right.add_widget(self.box_size)
        self.menu_right.add_widget(self.slider_shape_size)

        # Width point or line
        self.box_stroke = BoxLayout(orientation='horizontal')
        self.wdth_label = Label(
            text="Stroke width",
            font_size=self.f_size,
            markup=True)
        self.wdth_label_value = Label(
            text=str(self.shape.wdth),
            font_size=self.f_size,
            markup=True)
        self.box_stroke.add_widget(self.wdth_label)
        self.box_stroke.add_widget(self.wdth_label_value)
        self.slider_wdth = Slider(
            min=self.shape.property('wdth').get_min(self.shape),
            max=self.shape.property('wdth').get_max(self.shape),
            value=self.shape.wdth, step=1)
        self.slider_wdth.bind(value=self.change_wdth)
        self.menu_right.add_widget(self.box_stroke)
        self.menu_right.add_widget(self.slider_wdth)

        # a value
        self.box_a = BoxLayout(orientation='horizontal')
        self.a_label = Label(
            text="Param a ",
            font_size=self.f_size,
            markup=True)
        self.a_label_value = Label(
            text=str(self.shape.a),
            font_size=self.f_size,
            markup=True)
        self.box_a.add_widget(self.a_label)
        self.box_a.add_widget(self.a_label_value)
        self.slider_a = Slider(
            min=self.shape.property('a').get_min(self.shape),
            max=self.shape.property('a').get_max(self.shape),
            value=self.shape.a)
        self.slider_a.bind(value=self.change_a)
        self.menu_right.add_widget(self.box_a)
        self.menu_right.add_widget(self.slider_a)

        # b value
        self.box_b = BoxLayout(orientation='horizontal')
        self.b_label = Label(
            text="Param b ",
            font_size=self.f_size,
            markup=True)
        self.b_label_value = Label(
            text=str(self.shape.b),
            font_size=self.f_size,
            markup=True)
        self.box_b.add_widget(self.b_label)
        self.box_b.add_widget(self.b_label_value)
        self.slider_b = Slider(
            min=self.shape.property('b').get_min(self.shape),
            max=self.shape.property('b').get_max(self.shape),
            value=self.shape.b)
        self.slider_b.bind(value=self.change_b)
        self.menu_right.add_widget(self.box_b)
        self.menu_right.add_widget(self.slider_b)

        # m value
        self.box_m = BoxLayout(orientation='horizontal')
        self.m_label = Label(
            text="Param m ",
            font_size=self.f_size,
            markup=True)
        self.m_label_value = Label(
            text=str(self.shape.m),
            font_size=self.f_size,
            markup=True)
        self.box_m.add_widget(self.m_label)
        self.box_m.add_widget(self.m_label_value)
        self.slider_m = Slider(
            min=self.shape.property('m').get_min(self.shape),
            max=self.shape.property('m').get_max(self.shape),
            value=self.shape.m)
        self.slider_m.bind(value=self.change_m)
        self.menu_right.add_widget(self.box_m)
        self.menu_right.add_widget(self.slider_m)

        # n1 value
        self.box_n1 = BoxLayout(orientation='horizontal')
        self.n1_label = Label(
            text="Param n1 ",
            font_size=self.f_size,
            markup=True)
        self.n1_label_value = Label(
            text=str(self.shape.n1),
            font_size=self.f_size,
            markup=True)
        self.box_n1.add_widget(self.n1_label)
        self.box_n1.add_widget(self.n1_label_value)
        self.slider_n1 = Slider(
            min=self.shape.property('n1').get_min(self.shape),
            max=self.shape.property('n1').get_max(self.shape),
            value=self.shape.n1)
        self.slider_n1.bind(value=self.change_n1)
        self.menu_right.add_widget(self.box_n1)
        self.menu_right.add_widget(self.slider_n1)

        # n2 value
        self.box_n2 = BoxLayout(orientation='horizontal')
        self.n2_label = Label(
            text="Param n2 ",
            font_size=self.f_size,
            markup=True)
        self.n2_label_value = Label(
            text=str(self.shape.n2),
            font_size=self.f_size,
            markup=True)
        self.box_n2.add_widget(self.n2_label)
        self.box_n2.add_widget(self.n2_label_value)
        self.slider_n2 = Slider(
            min=self.shape.property('n2').get_min(self.shape),
            max=self.shape.property('n2').get_max(self.shape),
            value=self.shape.n2)
        self.slider_n2.bind(value=self.change_n2)
        self.menu_right.add_widget(self.box_n2)
        self.menu_right.add_widget(self.slider_n2)

        # n3 value
        self.box_n3 = BoxLayout(orientation='horizontal')
        self.n3_label = Label(
            text="Param n3 ",
            font_size=self.f_size,
            markup=True)
        self.n3_label_value = Label(
            text=str(self.shape.n3),
            font_size=self.f_size,
            markup=True)
        self.box_n3.add_widget(self.n3_label)
        self.box_n3.add_widget(self.n3_label_value)
        self.slider_n3 = Slider(
            min=self.shape.property('n3').get_min(self.shape),
            max=self.shape.property('n3').get_max(self.shape),
            value=self.shape.n3)
        self.slider_n3.bind(value=self.change_n3)
        self.menu_right.add_widget(self.box_n3)
        self.menu_right.add_widget(self.slider_n3)

        # Nb points
        self.box_nbp = BoxLayout(orientation='horizontal')
        self.nbp_label = Label(
            text="Points number ",
            font_size=self.f_size,
            markup=True)
        self.nbp_label_value = Label(
            text=str(self.shape.nbp),
            font_size=self.f_size,
            markup=True)
        self.box_nbp.add_widget(self.nbp_label)
        self.box_nbp.add_widget(self.nbp_label_value)
        self.slider_nbp = Slider(
            min=self.shape.property('nbp').get_min(self.shape),
            max=self.shape.property('nbp').get_max(self.shape),
            value=self.shape.nbp, step=2)
        self.slider_nbp.bind(value=self.change_nbp)
        self.menu_right.add_widget(self.box_nbp)
        self.menu_right.add_widget(self.slider_nbp)

        # Percent
        self.box_percent = BoxLayout(orientation='horizontal')
        self.percent_label = Label(
            text="Percent ",
            font_size=self.f_size,
            markup=True)
        self.percent_label_value = Label(
            text=str(self.shape.percent),
            font_size=self.f_size,
            markup=True)
        self.box_percent.add_widget(self.percent_label)
        self.box_percent.add_widget(self.percent_label_value)
        self.slider_percent = Slider(
            min=self.shape.property('percent').get_min(self.shape),
            max=self.shape.property('percent').get_max(self.shape),
            value=self.shape.percent, step=1)
        self.slider_percent.bind(value=self.change_percent)
        self.menu_right.add_widget(self.box_percent)
        self.menu_right.add_widget(self.slider_percent)

        # Travel
        self.box_travel = BoxLayout(orientation='horizontal')
        self.travel_label = Label(
            text="Travel ",
            font_size=self.f_size,
            markup=True)
        self.travel_label_value = Label(
            text=str(self.shape.travel),
            font_size=self.f_size,
            markup=True)
        self.box_travel.add_widget(self.travel_label)
        self.box_travel.add_widget(self.travel_label_value)
        self.slider_travel = Slider(
            min=self.shape.property('travel').get_min(self.shape),
            max=self.shape.property('travel').get_max(self.shape),
            value=self.shape.travel, step=2)
        self.slider_travel.bind(value=self.change_travel)
        self.menu_right.add_widget(self.box_travel)
        self.menu_right.add_widget(self.slider_travel)

        # ColorPicker for Shape
        self.picker = ColorPicker()
        self.picker.bind(color=self.on_color)

        # ColorPicker for background
        self.picker_bg = ColorPicker()
        self.picker_bg.bind(color=self.on_color_bg)

        # Export svg button
        self.export_button = Button(text='Export', size_hint=(1, 0.15))
        self.export_button.bind(on_press=self.export)

        # Tab packs
        self.tab_param.add_widget(self.menu_right)
        self.tab_color.add_widget(self.picker)
        self.tab_color_bg.add_widget(self.picker_bg)
        self.tab_export.add_widget(self.export_button)
        self.add_widget(self.panel)

        # Popups
        self.pop_export = Popup(
            title="Export file",
            content=Label(text="File exported"),
            size_hint=(None, None),
            size=(640, 240))

    def change_wdth(self, *args):
        '''
        Change stroke width
        '''
        self.shape.wdth = self.slider_wdth.value
        self.wdth_label_value.text = str(self.slider_wdth.value)

    def on_switch(self, *args):
        '''
        Switch mode line or point
        '''
        self.shape.line = self.switch_mode.active

    def on_color(self, *args):
        '''
        Shape color
        '''
        self.shape.color = self.picker.hex_color

    def on_color_bg(self, *args):
        '''
        Shape background color
        '''
        self.shape.bg_color = self.picker_bg.hex_color

    def change_shape_size(self, *args):
        '''
        Shape size
        '''
        self.shape.shape_size = self.slider_shape_size.value
        self.size_label_value.text = str(self.slider_shape_size.value)

    def change_a(self, *args):
        '''
        a value
        '''
        self.shape.a = self.slider_a.value
        self.a_label_value.text = str(self.slider_a.value)

    def change_b(self, *args):
        '''
        b value
        '''
        self.shape.b = self.slider_b.value
        self.b_label_value.text = str(self.slider_b.value)

    def change_m(self, *args):
        '''
        m value
        '''
        self.shape.m = self.slider_m.value
        self.m_label_value.text = str(self.slider_m.value)

    def change_n1(self, *args):
        '''
        n1 value
        '''
        self.shape.n1 = self.slider_n1.value
        self.n1_label_value.text = str(self.slider_n1.value)

    def change_n2(self, *args):
        '''
        n2 value
        '''
        self.shape.n2 = self.slider_n2.value
        self.n2_label_value.text = str(self.slider_n2.value)

    def change_n3(self, *args):
        '''
        n3 value
        '''
        self.shape.n3 = self.slider_n3.value
        self.n3_label_value.text = str(self.slider_n3.value)

    def change_nbp(self, *args):
        '''
        point number
        '''
        self.shape.nbp = self.slider_nbp.value
        self.nbp_label_value.text = str(self.slider_nbp.value)

    def change_percent(self, *args):
        '''
        Percent value
        '''
        self.shape.percent = self.slider_percent.value
        self.percent_label_value.text = str(self.slider_percent.value)

    def change_travel(self, *args):
        '''
        Travel number
        '''
        self.shape.travel = self.slider_travel.value
        self.travel_label_value.text = str(self.slider_travel.value)

    def export(self, *args):
        '''
        Export to svg file
        '''
        document = svgwrite.Drawing(filename='export.svg', debug=True)
        tmp = [(float("%.4g" % e)) for e in self.shape.path]
        # Export polygon
        if self.shape.line:
            svg_path = coupled(tmp)
            document.add(document.polygon(points=svg_path))
        else:  # Export points
            svg_path = coupled(coupled(tmp))
            for elem in svg_path:
                document.add(document.line(
                    start=elem[0],
                    end=elem[1]
                ))
        document.save()
        self.shape.export_to_png('export.png')
        self.pop_export.open()


class ShapeApp(App):
    '''
    Main application
    '''

    #icon = 'icon.png'
    title = "SuperShape Editor"

    def build(self):
        '''
        Main build method
        '''
        return MainBox()

    def on_pause(self):
        '''
        Hack Android pause mode
        Kivy function
        Manage pause Android mode
        '''
        return True

    def on_start(self):
        '''
        Logging Kivy function
        Logs on_start application
        '''
        Logger.info('Application starts')

    def on_stop(self):
        '''
        Loggin Kivy function
        Logs on_stop application
        '''
        Logger.critical('Application stops')


if __name__ in ('__android__', '__main__'):
    ShapeApp().run()

import datetime

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

DEG = u'\N{DEGREE SIGN}'

class WeatherWindow(Gtk.Window):
    font_sma = 8
    font_med1 = 12
    font_med2 = 16
    font_big = 24
    width = 500
    height = 200
    forecast = None
    current = None
    
    def __init__(self, title='hello', **kwargs):
        super().__init__(title=title)
        dims = Gdk.Display().get_default().get_monitor(0).get_geometry()
        if 'width' in kwargs.keys():
            self.width = kwargs['width']
        if 'height' in kwargs.keys():
            self.height = kwargs['height']
        self.set_default_size(width=self.width, height=self.height)
        self.move((dims.width / 2) - (self.width / 2), 40)
        self.set_has_resize_grip(False)
        self.set_decorated(False)
        self.connect('destroy', Gtk.main_quit)       

    # close the window with the escape key
    def do_key_press_event(self, event):
        if event.keyval == Gdk.KEY_Escape:
            Gtk.main_quit()

    # close the window when user clicks away from it
    def do_focus_out_event(self, event):
        Gtk.main_quit()

    def showWindow(self):
        self.show_all()
        self.set_type_hint(Gdk.WindowTypeHint.DIALOG)
        Gtk.Widget.set_opacity(self, 0.95)
        Gtk.main()

    def closeWindow(self):
        Gtk.main_quit()

    def drawGrid(self):
        s = self.font_sma
        m1 = self.font_med1
        m2 = self.font_med2
        b = self.font_big
        grid = Gtk.Grid()
        Gtk.Widget.set_halign(grid, Gtk.Align.FILL)
        Gtk.Widget.set_valign(grid, Gtk.Align.FILL)

        self.add(grid)

        # current weather
        city = Gtk.Label(self.current['city'], expand=True)
        city.set_justify(Gtk.Justification.LEFT)
        day = Gtk.Label(expand=True)
        day.set_markup(f"<span bgcolor='#003300'>{self.current['date']}</span>")
        Gtk.Widget.set_halign(day, Gtk.Align.FILL)
        day.set_justify(Gtk.Justification.RIGHT)
        temp = Gtk.Label(expand=True)
        Gtk.Widget.set_halign(temp, Gtk.Align.FILL)
        Gtk.Widget.set_valign(temp, Gtk.Align.FILL)
        temp.set_markup(f"<span bgcolor='#000021' font='{b}'>{self.current['temp']}</span>")
        Gtk.Widget.set_hexpand(temp, True)
        sun = Gtk.Label(expand=True)
        sun.set_markup(f"<span font='{m2}'>{self.current['sun']}</span>")

        grid.add(city)
        grid.attach(day, 1, 0, 1, 1)
        grid.attach(temp, 0, 1, 2, 1)
        grid.attach(sun, 0, 2, 2, 1)

        i = 0
        for d, day in self.forecast.items():
            forecast = Gtk.Label(expand=True, valign=Gtk.Align.CENTER)
            forecast.set_markup(f"<span bgcolor='#{i}{i}0000'>{self.forecastString(day)}</span><span font='{b}'>{day['icon']}</span>")
            forecast.set_justify(Gtk.Justification.LEFT)
            Gtk.Widget.set_halign(forecast, Gtk.Align.START)
            #Gtk.Widget.set_valign(forecast, Gtk.Align.BASELINE)
            grid.attach(forecast, 2, i, 1, 1) 
            i += 1


    def setData(self, current, forecast):
        self.current = current
        self.forecast = forecast

    def drawBox(self):
        box = Gtk.Box(spacing=5)
        wbox = Gtk.Box()
        wbox.set_homogeneous(False)
        fbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.pack_start(wbox, True, True, 0)
        box.pack_start(fbox, True, True, 0)

        label = Gtk.Label()
        label.set_markup(self.currentWeatherString(self.current))
        label.set_justify(Gtk.Justification.CENTER)
        wbox.pack_start(label, True, True, 0)

        for d,day in self.forecast.items():
            label = Gtk.Label()
            label.set_markup(self.forecastString(day))
            label.set_justify(Gtk.Justification.LEFT)
            fbox.pack_start(label, True, True, 0)

        self.add(box)

    def currentWeatherString(self, data):
        city = f"<span font='18'>{data['city']}</span>"
        date = f"<span font='18'>{data['date']}</span>"
        temps = f"<span font='{self.WSize}'>{data['temp']}</span>"
        sun = f"<span font='14'>{data['sun']}</span>"
        top = f"<span>{city}{date}</span>"
        bottom = f"<span>{temps}{sun}</span>"
        #return f"{city}\n{date}\n{temps}\n{sun}"
        return f"{top}\n\n{bottom}"

    def forecastString(self, data):
        temps = f"<span font='12'>{data['temps']}</span>"
        conditions = f"<span font='10'>{data['cond']}</span>"
        date = f"<span font='{self.font_sma}'>{data['date']}</span>"
        return f"{date}\n{temps}\n{conditions}\n"


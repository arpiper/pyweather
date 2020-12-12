import datetime

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

DEG = u'\N{DEGREE SIGN}'

class WeatherWindow(Gtk.Window):
    font_sma = 8
    font_med1 = 12
    font_med2 = 14
    font_big = 26
    width = 500
    height = 200
    forecast = None
    current = None
    
    def __init__(self, title='hello', **kwargs):
        print('before suer')
        super().__init__(title=title)
        dims = Gdk.Display().get_default().get_monitor(0).get_geometry()
        print('dims')
        print(dims)
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

    # close the window when user clicks it.
    def do_button_press_event(self, event):
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
        self.add(grid)

        # city and date
        info_string = f"<span font='{m2}'>{self.current['date']}</span>\n" \
            f"<span font='{m2}'>{self.current['city']}</span>"
        info = Gtk.Label(expand=True, xalign=0.1, margin_left=10)
        info.set_markup(info_string)

        # current weather conditionsa and  sunset/sunrise
        ws = f"<span font='{b}'>{self.current['temp']}</span>\n" \
            f"<span font='10'>{self.current['cond']}</span>\n" \
            f"<span font_family='Weather Icons' font='10'>\uf052</span>" \
            f"<span font='10'> {self.current['sun']}</span>"
        weather = Gtk.Label(expand=True, xalign=0.5, yalign=0.5)
        weather.set_markup(ws)

        grid.attach(info, 0, 0, 1, 4)
        grid.attach(weather, 1, 0, 1, 4)

        # 3 day forecast 
        i = 0
        for d, day in self.forecast.items():
            container = Gtk.Grid(expand=True, valign=Gtk.Align.CENTER, margin_top=5, margin_bottom=5)
            ic = Gtk.Label(valign=Gtk.Align.CENTER, expand=True) 
            ic.set_markup(f"<span font_family='Weather Icons' font='20'>{day['icon']}</span>")
            da = Gtk.Label(expand=True, halign=Gtk.Align.START)#, xalign=0)
            da.set_markup(f"<span font='8'>{day['date']}</span>")
            te = Gtk.Label(expand=True,halign=Gtk.Align.START)#  xalign=0)
            te.set_markup(f"<span font='12'>{day['temps']}</span>")
            co = Gtk.Label(expand=True,halign=Gtk.Align.START)# xalign=0)
            co.set_markup(f"<span font='10'>{day['cond']}</span>")
            container.attach(ic, 0, 0, 1, 3)
            container.attach(da, 1, 0, 2, 1)
            container.attach(te, 1, 1, 2, 1)
            container.attach(co, 1, 2, 2, 1)
            grid.attach(container, 2, i, 2, 1)
            i += 1

    def setData(self, current, forecast):
        print('setData', self)
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
        temps = f"<span font='{self.font_big}'>{data['temp']}</span>"
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


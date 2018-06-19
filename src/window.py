import datetime
from subprocess import run, Popen, check_output, PIPE, STDOUT

import tkinter as tk

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk, Gdk

DEG = u'\N{DEGREE SIGN}'

class WeatherWindow(Gtk.Window):
    FSize = 8
    WSize = 24
    
    def __init__(self, title='hello'):
        super().__init__(title=title)
        self.set_default_size(width=400, height=200)
        self.set_has_resize_grip(False)
        self.connect('destroy', Gtk.main_quit)       
        # Hide the title bar.
        #self.get_window().set_decorations(Gdk.WMDecoration.BORDER)

    def setData(self, current, forecast):
        box = Gtk.Box(spacing=5)
        wbox = Gtk.Box()
        wbox.set_homogeneous(False)
        fbox = Gtk.Box(orientation=Gtk.Orientation.VERTICAL)
        box.pack_start(wbox, True, True, 0)
        box.pack_start(fbox, True, True, 0)

        label = Gtk.Label()
        label.set_markup(self.currentWeatherString(current))
        label.set_justify(Gtk.Justification.CENTER)
        wbox.pack_start(label, True, True, 0)

        for d,day in forecast['days'].items():
            label = Gtk.Label()
            label.set_markup(self.forecastString(day))
            label.set_justify(Gtk.Justification.LEFT)
            fbox.pack_start(label, True, True, 0)

        self.add(box)

    def currentWeatherString(self, data):
        d = datetime.datetime.now()
        date = f"<span font='16'>{data['name']}\n{d.strftime('%A, %B %d')}</span>"
        temps = f"<span font='24'>{data['main']['temp']}{DEG} C</span>"
        return f"{date}\n{temps}\n"

    def forecastString(self, data):
        temps = f"<span font='{self.FSize}'>High: {data['high']}{DEG} - Low: {data['low']}{DEG}</span>"
        conditions = f"<span font='{self.FSize}'>{data['conditions']['description'].upper()}</span>"
        d = datetime.datetime.strptime(data['date'].split(' ')[0], '%Y-%m-%d')
        date = f"<span font='{self.FSize}'>{d.strftime('%A, %b %d')}</span>"
        return f"{date}\n{temps}\n{conditions}\n"


class TkWindow():
    root = None
    window = None
    width = 500
    height = 300
    title = "Tkinter Window"

    def __init__(self, root, **kwargs):
        self.root = root
        self.root.title(self.title)
        self.root.bind('<Key>', self.escapeKey)
        self.root.bind('<FocusOut>', self.focusOut)
        #self.root.wm_attributes('-type', 'splash')
        self.window = tk.Toplevel(self.root)
        self.window.overrideredirect(1)
        #self.root.overrideredirect(1)
        self.root.attributes('-alpha', 0.0)
        sw = int((root.winfo_screenwidth() / 2) - (self.width / 2))
        #self.root.geometry(f'{self.width}x{self.height}+{sw}+50')
        self.root.withdraw()
        self.window.geometry(f'{self.width}x{self.height}+{sw}+50')
        self.window.bind('<FocusOut>', self.focusOut)
        self.window.bind('<Key>', self.escapeKey)

    def show(self):
        self.window.mainloop()

    def weatherFrame(self, weather):
        frame = tk.Frame(self.window)
        label = tk.Label(frame, text=weather)
        label.pack()
        frame.pack(side=tk.LEFT)

    def forecastFrame(self, forecast):
        frame = tk.Frame(self.window)
        label = tk.Label(frame, text=forecast)
        label.pack()
        frame.pack(side=tk.RIGHT)

    def escapeKey(self, event):
        #if event.keysym == 'Escape' 
        if event.keycode == 9:
            self.root.destroy()

    def focusOut(self, event):
        self.root.destroy()


class WeatherPopup():
    font_size = 10 
    width = 500
    line_height = 400
    position = [710, 50]
    text = ''
    fg = '#fefefe'
    bg = '#424242'
    lines = 2
    title = ''

    def __init__(self, title, text, *args, **kwargs):
        self.title = title
        self.text = text
        self.lines = len(text.split('\n'))
        if 'width' in kwargs.keys():
            self.width = kwargs['width']
        if 'height' in kwargs.keys():
            self.height = kwargs['height']
        if 'font_size' in kwargs.keys():
            self.font_size = kwargs['font_size']

    def open(self):
        cmd = [
            'dzen2',
            '-fn', f'Titillium-Light:pixelsize={self.font_size}',
            '-x', f'{self.position[0]}',
            '-y', f'{self.position[1]}',
            '-w', f'{self.width}',
            '-h', f'{self.line_height}',
            '-e', 'button1=exit;onstart=uncollapse',
            '-p',
            '-l', '4',
            #'-fg', self.fg,
            #'-bg', self.bg,
        ]
        print(self.text)
        e = Popen(['echo', f'{self.title}', f'{self.text}'], stdout=PIPE, universal_newlines=True, encoding='utf-8')
        d = Popen(cmd, stdin=e.stdout, stderr=STDOUT)
        e.stdout.close()
        t = d.communicate()[0]
        #run(['echo', f'{self.text}'])


from tkinter import *
from tkinter import ttk
from tkcalendar import Calendar
from tktimepicker import AnalogPicker
from PIL import Image, ImageFont, ImageDraw
import datetime
import subprocess
import os

class TestToPng:

    def __init__(self, root):

        root.title("Text to PNG")

        mainframe = ttk.Frame(root, padding="3 3 12 12")
        mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)

        self.aspect_ratios = ((7, 9), (9, 7))
        aspect_ratios_strings = ('7x9', '9x7')
        a_ratios = StringVar(value=aspect_ratios_strings)
        self.hidden = BooleanVar(value=False)
        self.hidden_text_color = IntVar(value=5)
        entry = Entry(mainframe, textvariable=self.hidden_text_color)
        slider = Scale(mainframe, from_=0, to=255, orient='horizontal', variable=self.hidden_text_color)
        self.use_current_time = BooleanVar(value=True)
        self.flip_image = BooleanVar(value=False)

        self.lbox = Listbox(mainframe, listvariable=a_ratios, height=5, width=5)
        check1 = Checkbutton(mainframe, text='Hidden', variable=self.hidden)
        check2 = Checkbutton(mainframe, text='Use Current Time', variable=self.use_current_time)
        check3 = Checkbutton(mainframe, text='Flip Image', variable=self.flip_image)
        self.cal = Calendar(mainframe)
        self.clock = AnalogPicker(mainframe)
        self.textbox = Text(mainframe, wrap='word')
        self.lbox.grid(column=0, row=0)
        check1.grid(column=1, row=0)
        check2.grid(column=2, row=1)
        check3.grid(column=3, row=1)
        entry.grid(column=2, row=0)
        slider.grid(column=3, row=0, columnspan=2)
        self.cal.grid(column=0, row=1)
        self.clock.grid(column=1, row=1)
        self.textbox.grid(column=0, row=2, columnspan=2)

        # self.feet = StringVar()
        # feet_entry = ttk.Entry(mainframe, width=7, textvariable=self.feet)
        # feet_entry.grid(column=2, row=1, sticky=(W, E))
        # self.meters = StringVar()
        #
        # ttk.Label(mainframe, textvariable=self.meters).grid(column=2, row=2, sticky=(W, E))
        ttk.Button(mainframe, text="Clear", command=self.clear_text).grid(column=3, row=3, sticky=W)
        ttk.Button(mainframe, text="Generate", command=self.calculate).grid(column=3, row=4, sticky=W)
        #
        # ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
        # ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
        # ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

        for child in mainframe.winfo_children():
            child.grid_configure(padx=5, pady=5)

        # feet_entry.focus()
        # lbox.bind('<<ListboxSelect>>', lambda e: print(aspect_ratios[lbox.curselection()[0]]))
        # root.bind("<Return>", self.calculate)

        self.lbox.selection_set(0)
        self.clock.setMinutes(0)


    def clear_text(self):
        self.textbox.delete('1.0', END)

    def calculate(self, *args):
        date = self.cal.selection_get()
        hour, minute, period = self.clock.time()
        hour += 12 * (period == 'PM')
        time = datetime.time(hour, minute)
        dt = datetime.datetime.combine(date, time)
        text = self.textbox.get('1.0', END).strip()
        ratio = self.aspect_ratios[self.lbox.curselection()[0]] # Standard is portrait 7x9
        hidden = self.hidden.get()
        use_current_time = self.use_current_time.get()
        text_color = (255, 255, 255)
        image_width = 667  # Standard is 667
        margin = 0.05  # Standard is 0.05
        font_size = 100  # Standard is 100
        spacing = 4  # Standard is 4
        font_url = "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"  # Standard is "/System/Library/Fonts/Supplemental/Arial Unicode.ttf"

        # calculations
        if hidden:
            text_color = tuple([self.hidden_text_color.get()]*3)
        if use_current_time:
            dt = datetime.datetime.now()
        image_ratio = ratio[0] / ratio[1]
        image_height = int(image_width / image_ratio)
        margin_width = image_width * margin
        margin_height = image_height * margin
        text_width = image_width - (2 * margin_width)
        text_height = image_height - (2 * margin_height)
        center = (int(round(image_width / 2)), int(round(image_height / 2)))
        if len(text) > 20:
            filename = f'{dt.strftime("%Y.%m.%d_%H.%M.%S")}_{text[:20]}.png'
        else:
            filename = f'{dt.strftime("%Y.%m.%d_%H.%M.%S")}_{text}.png'
        # Sending to the desktop
        filepath = os.path.join(os.path.expanduser("~/Desktop"), filename)

        def get_wrapped_text(text: str, font: ImageFont.ImageFont,
                             line_length: int):
            lines = ['']
            paragraphs = text.split('\n')
            for paragraph in paragraphs:
                for word in paragraph.split(sep=' '):
                    line = f'{lines[-1]} {word}'.strip()
                    if font.getlength(line) <= line_length:
                        lines[-1] = line
                    else:
                        if font.getlength(word) <= line_length:
                            lines.append(word)
                        else:
                            return None
                lines.append('\n')
            return '\n'.join(lines[:-1])

        for text_size in range(font_size, 0, -1):
            font = ImageFont.truetype(font_url, text_size)
            wrapped = get_wrapped_text(text, font, text_width)
            if wrapped is None:
                continue
            image = Image.new('RGB', (image_width, image_height), color='black')
            draw = ImageDraw.Draw(image)
            left, top, right, bottom = draw.multiline_textbbox(center, wrapped, font=font, align='center',
                                                               spacing=spacing)
            instance_text_height = bottom - top
            if instance_text_height <= text_height:
                text_wrapped = wrapped
                instance_text_width = right - left
                break

        # Some fonts have an offset that really messes up the positioning
        font_box = font.getbbox(text_wrapped)
        # Moving the text half the text area size up and left
        text_top_left = (
        center[0] - (instance_text_width / 2) - font_box[0], center[1] - (instance_text_height / 2) - font_box[1])
        image = Image.new('RGB', (image_width, image_height), color='black')
        draw = ImageDraw.Draw(image)
        draw.multiline_text(text_top_left, text_wrapped, font=font, align='center', spacing=spacing, fill=text_color)

        if self.flip_image.get():
            image = image.transpose(Image.ROTATE_180)

        image.save(filepath)
        set_created_command = 'SetFile -d "{}" "{}"'.format(dt.strftime('%m/%d/%Y %H:%M:%S'), filepath)
        set_modified_command = 'SetFile -m "{}" "{}"'.format(dt.strftime('%m/%d/%Y %H:%M:%S'), filepath)
        subprocess.Popen(set_created_command, shell=True)
        subprocess.Popen(set_modified_command, shell=True)


root = Tk()
TestToPng(root)
root.mainloop()
import tkinter as tk
import tkinter.ttk as ttk
from ttkbootstrap import Style
from math import sin, cos, tan, radians, pi
import os


class MyLocalRoot(tk.Tk):
    def __init__(self):
        super().__init__()
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        self.title('Weld Bevel Designer')
        self.resizable(0, 0)
        self.iconbitmap('engineering_white.ico')

        w_width = 1000
        w_height = 550
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x_position = int((screen_width - w_width) / 2)
        y_position = int((screen_height - w_height) / 2)
        self.geometry(f'{w_width}x{w_height}+{x_position}+{y_position}')


class MessageBox(tk.Toplevel):
    """ Creates a message box with the same style as the main application """

    def __init__(self, parent, title, message):

        # Configuration
        if True:
            super().__init__()
            self.config(padx=10, pady=10)
            self.minsize(350, 150)
            self.columnconfigure(0, weight=1)
            self.columnconfigure(1, weight=1)
            self.rowconfigure(0, weight=0)
            self.rowconfigure(1, weight=1)
            self.rowconfigure(2, weight=0)
            self.iconbitmap(os.path.join(os.getcwd(), 'engineering_white.ico'))
            self.title(title)

        # Widgets
        if True:
            self.control_var = tk.IntVar(value=0)
            label = ttk.Label(self, text=message, anchor='center', justify='center')
            label.grid(row=0, column=0, columnspan=2, sticky='nsew', pady=10, padx=10)

            ok_button = ttk.Button(self, text="OK", command=lambda: self.adjust_var(1), width=10,
                                   style='danger.TButton')
            ok_button.grid(row=2, column=0, sticky='nsew', padx=30, pady=(0, 10))

            cancel_button = ttk.Button(self, text="Cancel", command=lambda: self.adjust_var(0), width=10,
                                       style='success.TButton')
            cancel_button.grid(row=2, column=1, sticky='nsew', padx=30, pady=(0, 10))

        # Determine relative position
        if True:
            position_x = parent.winfo_x()
            position_y = parent.winfo_y()
            height = parent.winfo_height()
            width = parent.winfo_width()

            local_height = self.minsize()[1]
            local_width = self.minsize()[0]

            final_position = (position_x + width / 2 - local_width / 2, position_y + height / 2 - local_height / 2)
            self.geometry('%dx%d+%d+%d' % (local_width, local_height, final_position[0], final_position[1]))
            self.grab_set()

    def adjust_var(self, option):
        self.control_var.set(option)
        self.destroy()

    def show(self):
        self.deiconify()
        self.wait_window()
        value = self.control_var.get()
        return value


class WeldBevelDesigner(ttk.Frame):

    def __init__(self, parent):

        # Parent Class Initialization and Configuration
        if True:
            super().__init__(parent)
            w_width = 1000
            w_height = 550
            self.parent = parent
            self.style = Style(theme='sandstone')
            self.fill_color = self.style.colors.get('secondary')
            self.border_color = self.style.colors.get('primary')

        # Main Frame Configuration
        if True:
            self.columnconfigure(0, weight=0, minsize=int(w_width*0.28))
            self.columnconfigure(1, weight=0, minsize=int(w_width*0.44))
            self.columnconfigure(2, weight=0, minsize=int(w_width*0.27))
            self.rowconfigure(0, weight=1)

        # Sub Frames Configuration
        if True:
            self.left_frame = ttk.Frame(self)
            self.left_frame.grid(row=0, column=0, sticky='nsew')
            self.left_frame.columnconfigure(0, weight=1)
            self.left_frame.rowconfigure(0, weight=1)
            self.left_frame.rowconfigure(1, weight=0)
            self.left_frame.rowconfigure(2, weight=0)
            self.left_frame.grid_propagate(0)

            self.canvas_frame = ttk.Frame(self)
            self.canvas_frame.grid(row=0, column=1, sticky='nsew', padx=5)
            self.canvas_frame.rowconfigure(0, weight=1)
            self.canvas_frame.columnconfigure(0, weight=1)
            self.canvas_frame.grid_propagate(0)

            self.right_frame = ttk.Frame(self)
            self.right_frame.grid(row=0, column=2, sticky='nsew')
            self.right_frame.columnconfigure(0, weight=1)
            self.right_frame.rowconfigure(0, weight=1)
            self.right_frame.rowconfigure(1, weight=0)
            self.right_frame.grid_propagate(0)

        # Local Canvas
        if True:
            self.canvas_size = (0.44*w_width-20, w_height-20)
            self.canvas = tk.Canvas(self.canvas_frame, bg='white', highlightthickness=0,
                                    width=self.canvas_size[0], height=self.canvas_size[1])
            self.canvas.grid(row=0, column=0, sticky='nsew')

        # LEFT FRAME 1: Frame With the Bevel Selection Options
        if True:
            local_frame = ttk.Frame(self.left_frame)
            local_frame.grid(row=0, column=0, sticky='nsew')
            local_frame.columnconfigure(0, weight=1)

            # Frame Title
            label = ttk.Label(local_frame, text='Bevel Selection', style='secondary.Inverse.TLabel')
            label.grid(row=0, column=0, sticky='nsew')

            # Standard Bevel Check Button
            self.standard_bevel_var = tk.IntVar(value=1)
            check_button = ttk.Checkbutton(local_frame, text='Standard Bevels', variable=self.standard_bevel_var,
                                           style='primary.Roundtoggle.Toolbutton',
                                           command=self.activate_non_standard_bevel)
            check_button.grid(row=1, column=0, sticky='ew', pady=10)

            # Standard bevel options and combobox
            bevel_options = ('Single Square', 'Single Bevel', 'Double Bevel',
                             'Single V', 'Single J', 'Single Compound', 'Single U',
                             'Double V', 'Double J', 'Double Compound', 'Double U')

            self.standard_bevel_label = ttk.Label(local_frame, text='Standard Bevel Selection')
            self.standard_bevel_label.grid(row=2, column=0, sticky='nsew', pady=5)
            self.bevel_var = tk.StringVar()
            self.combobox_1 = ttk.Combobox(local_frame, textvariable=self.bevel_var, justify='center', state='readonly',
                                           values=bevel_options)
            self.combobox_1.bind('<<ComboboxSelected>>', self.update_bevel_options)
            self.combobox_1.grid(row=3, column=0, sticky='nsew', pady=5)

            # Non standard bevel options and combo boxes
            self.single_bevel_options = ('Single Square',
                                         'Single V', 'Single J', 'Single Compound',
                                         'Double V', 'Double J', 'Double Compound')

            self.left_label = ttk.Label(local_frame, text='Left Bevel Selection')
            self.left_label.grid(row=4, column=0, sticky='nsew', pady=5)
            self.left_label.grid_remove()

            self.left_bevel_var = tk.StringVar()
            self.combobox_2 = ttk.Combobox(local_frame, textvariable=self.left_bevel_var, justify='center',
                                           state='readonly', values=self.single_bevel_options)
            self.combobox_2.bind('<<ComboboxSelected>>', self.update_bevel_options)
            self.combobox_2.grid(row=5, column=0, sticky='nsew', pady=5)
            self.combobox_2.grid_remove()

            self.right_label = ttk.Label(local_frame, text='Right Bevel Selection')
            self.right_label.grid(row=6, column=0, sticky='nsew', pady=5)
            self.right_label.grid_remove()

            self.right_bevel_var = tk.StringVar()
            self.combobox_3 = ttk.Combobox(local_frame, textvariable=self.right_bevel_var, justify='center',
                                           state='readonly', values=self.single_bevel_options)
            self.combobox_3.bind('<<ComboboxSelected>>', self.update_bevel_options)
            self.combobox_3.grid(row=7, column=0, sticky='nsew', pady=5)
            self.combobox_3.grid_remove()

        # LEFT FRAME 2: Frame With the Weld Reinforcement Settings
        if True:
            local_frame = ttk.Frame(self.left_frame)
            local_frame.grid(row=1, column=0, sticky='nsew')
            local_frame.columnconfigure(0, weight=1)
            local_frame.columnconfigure(1, weight=0)

            self.additional_options_vars_list = []

            additional_options = {'Reinforcement Face Up [mm]': {'value': 1, 'from': 0, 'to': 3, 'increment': 0.5},
                                  'Reinforcement Face Down [mm]': {'value': 1, 'from': 0, 'to': 3, 'increment': 0.5},
                                  'Root Gap [mm]': {'value': 2, 'from': 0, 'to': 5, 'increment': 0.5}}

            label = ttk.Label(local_frame, text='Weld Reinforcements and Root Gap', style='secondary.Inverse.TLabel')
            label.grid(row=0, column=0, columnspan=2, sticky='nsew')
            for i, item in enumerate(additional_options.keys()):
                options = additional_options[item]
                label = ttk.Label(local_frame, text=f'{item}:', anchor='e')
                label.grid(row=i+1, column=0, sticky='nsew', pady=4)

                _var = tk.DoubleVar(value=additional_options[item]['value'])
                self.additional_options_vars_list.append(_var)

                spinbox = ttk.Spinbox(local_frame, textvariable=_var, width=4, from_=options['from'],
                                      to_=options['to'], increment=options['increment'], command=self.update_plot)
                spinbox.grid(row=i+1, column=1, sticky='nsew', pady=4)
                spinbox.bind('<Return>', self.update_plot)
                spinbox.bind('<FocusOut>', self.update_plot)

        # LEFT FRAME 3: Frame With the Plot Adjustments
        if True:
            local_frame = ttk.Frame(self.left_frame)
            local_frame.grid(row=2, column=0, sticky='nsew')
            local_frame.columnconfigure(0, weight=1)
            local_frame.columnconfigure(1, weight=0)

            label = ttk.Label(local_frame, text='Plot Area Adjust', style='secondary.Inverse.TLabel')
            label.grid(row=0, column=0, columnspan=2, sticky='nsew', pady=(20, 10))

            # Plot Zoom
            label = ttk.Label(local_frame, text='Zoom [%]:', anchor='e')
            label.grid(row=1, column=0, sticky='nsew', pady=4)

            _var = tk.DoubleVar(value=30)
            self.additional_options_vars_list.append(_var)

            spinbox = ttk.Spinbox(local_frame, textvariable=_var, width=4, from_=25, to_=75,
                                  increment=5, command=self.adjust_drawing_area)
            spinbox.grid(row=1, column=1, sticky='nsew', pady=4)
            spinbox.bind('<Return>', self.adjust_drawing_area)
            spinbox.bind('<FocusOut>', self.adjust_drawing_area)

            # Show Area Check Button
            self.show_area_var = tk.IntVar(value=1)
            check_button = ttk.Checkbutton(local_frame, text='Show Weld Areas', variable=self.show_area_var,
                                           style='primary.Roundtoggle.Toolbutton', command=self.show_weld_area)
            check_button.grid(row=2, column=0, columnspan=2, sticky='e', pady=5)

            # Quit Button
            button = ttk.Checkbutton(local_frame, text='Quit Application',
                                     style='secondary.TButton', command=self.exit_application)
            button.grid(row=3, column=0, columnspan=2, sticky='ew', pady=5, padx=10)

        # RIGHT FRAME 1: First Frame with Bevel Setting
        if True:
            self.primary_bevel_frame = ttk.Frame(self.right_frame)
            self.primary_bevel_frame.grid(row=0, column=0, sticky='nsew')
            self.primary_bevel_frame.columnconfigure(0, weight=1)
            self.primary_bevel_frame.columnconfigure(1, weight=0)

            # Frame Title
            label = ttk.Label(self.primary_bevel_frame, text='Bevel Details', style='secondary.Inverse.TLabel')
            label.grid(row=0, column=0, sticky='nsew', pady=(0, 10))

        # RIGHT FRAME 2: Second Frame with Bevel Setting
        if True:
            self.secondary_bevel_frame = ttk.Frame(self.right_frame)
            self.secondary_bevel_frame.grid(row=1, column=0, sticky='nsew')
            self.secondary_bevel_frame.grid_remove()
            self.secondary_bevel_frame.columnconfigure(0, weight=1)
            self.secondary_bevel_frame.columnconfigure(1, weight=0)

            # Frame Title
            label = ttk.Label(self.secondary_bevel_frame, text='Right Bevel Details', style='secondary.Inverse.TLabel')
            label.grid(row=0, column=0, sticky='nsew', pady=(0, 10))

        # Attributes
        if True:
            # Bevel Parameters
            self.bevel_parameters = {
                'Single Square': ('Total Thickness [mm]',),
                'Single Bevel': ('Total Thickness [mm]', 'Root Land [mm]', 'Bevel Angle [°]'),
                'Single V': ('Total Thickness [mm]', 'Root Land [mm]', 'Bevel Angle [°]'),
                'Single J': ('Total Thickness [mm]', 'Root Land [mm]',
                             'Bevel Angle [°]', 'Bevel Radius [mm]'),
                'Single U': ('Total Thickness [mm]', 'Root Land [mm]',
                             'Bevel Angle [°]', 'Bevel Radius [mm]'),
                'Single Compound': ('Total Thickness [mm]', 'Root Land [mm]',
                                    'Transition Depth [mm]', 'Bevel Angle 1 [°]', 'Bevel Angle 2 [°]'),
                'Double Bevel': ('Total Thickness [mm]', 'Side 1 Depth [mm]', 'Root Land [mm]',
                                 'Bevel Angle Side 1 [°]', 'Bevel Angle Side 2 [°]'),
                'Double V': ('Total Thickness [mm]', 'Side 1 Depth [mm]', 'Root Land [mm]',
                             'Bevel Angle Side 1 [°]', 'Bevel Angle Side 2 [°]'),
                'Double J': ('Total Thickness [mm]', 'Side 1 Depth [mm]', 'Root Land [mm]',
                             'Bevel Angle Side 1 [°]', 'Bevel Radius Side 1 [mm]',
                             'Bevel Angle Side 2 [°]', 'Bevel Radius Side 2 [mm]'),
                'Double U': ('Total Thickness [mm]', 'Side 1 Depth [mm]', 'Root Land [mm]',
                             'Bevel Angle Side 1 [°]', 'Bevel Radius Side 1 [mm]',
                             'Bevel Angle Side 2 [°]', 'Bevel Radius Side 2 [mm]'),
                'Double Compound': ('Total Thickness [mm]', 'Side 1 Depth [mm]', 'Root Land [mm]',
                                    'Transition Depth 1 [mm]', 'Bevel Angle 1 - Side 1 [°]',
                                    'Bevel Angle 2 - Side 1 [°]', 'Transition Depth 2 [mm]',
                                    'Bevel Angle 1 - Side 2 [°]', 'Bevel Angle 2 - Side 2 [°]')
            }
            self.spin_box_parameters = {
                'Total Thickness [mm]': {'value': 20, 'from': 3, 'to': 200, 'increment': 1},
                'Root Gap [mm]': {'value': 2, 'from': 0, 'to': 10, 'increment': 0.5},
                'Root Land [mm]': {'value': 2, 'from': 0, 'to': 100, 'increment': 0.5},
                'Bevel Angle [°]': {'value': 37.5, 'from': 5, 'to': 50, 'increment': 0.5},
                'Bevel Radius [mm]': {'value': 5, 'from': 1, 'to': 50, 'increment': 0.5},
                'Transition Depth [mm]': {'value': 10, 'from': 2, 'to': 100, 'increment': 1},
                'Bevel Angle 1 [°]': {'value': 37.5, 'from': 5, 'to': 50, 'increment': 0.5},
                'Bevel Angle 2 [°]': {'value': 10, 'from': 5, 'to': 50, 'increment': 0.5},
                'Bevel Angle Side 1 [°]': {'value': 37.5, 'from': 5, 'to': 50, 'increment': 0.5},
                'Bevel Angle Side 2 [°]': {'value': 37.5, 'from': 5, 'to': 50, 'increment': 0.5},
                'Bevel Radius Side 1 [mm]': {'value': 5, 'from': 1, 'to': 50, 'increment': 0.5},
                'Bevel Radius Side 2 [mm]': {'value': 5, 'from': 1, 'to': 50, 'increment': 0.5},
                'Transition Depth 1 [mm]': {'value': 5, 'from': 3, 'to': 100, 'increment': 1},
                'Bevel Angle 1 - Side 1 [°]': {'value': 37.5, 'from': 5, 'to': 50, 'increment': 0.5},
                'Bevel Angle 2 - Side 1 [°]': {'value': 10, 'from': 5, 'to': 50, 'increment': 0.5},
                'Transition Depth 2 [mm]': {'value': 5, 'from': 3, 'to': 100, 'increment': 1},
                'Bevel Angle 1 - Side 2 [°]': {'value': 37.5, 'from': 5, 'to': 50, 'increment': 0.5},
                'Bevel Angle 2 - Side 2 [°]': {'value': 10, 'from': 5, 'to': 50, 'increment': 0.5},
                'Side 1 Depth [mm]': {'value': 10, 'from': 0, 'to': 100, 'increment': 1}
            }

            # Variables that control the widgets values and bevel options
            self.left_options_vars_list = []
            self.right_options_vars_list = []
            self.left_options = []
            self.right_options = []

            # Variables for calculating the weld area
            self.top_reinforcement = []
            self.bottom_reinforcement = []
            self.text_ids = []
            self.weld_area = {'Top Reinforcement Area': 0,
                              'Bottom Reinforcement': 0,
                              'Left Weld Area': 0,
                              'Right Weld Area': 0}

        # Initialization Methods
        if True:
            self.canvas_grid_items = []
            self.drawing_limits = {}
            self.adjust_drawing_area('@start')

    # Initialization Method --------------------------------------------------------------------------------------------
    def adjust_drawing_area(self, event=''):
        """ Draws the drawing limits for the base metal and bevel """

        # Deletes previous items
        self.canvas.delete('all')
        self.canvas_grid_items = []

        # Get the colors and the zoom
        line_color = self.style.colors.get('danger')
        zoom = self.additional_options_vars_list[3].get()

        # Initial Values
        base_metal_rel_thickness = (zoom / 100) * self.canvas_size[1]
        base_metal_center_line = 0.5 * self.canvas_size[1]
        lower_border = base_metal_center_line + base_metal_rel_thickness / 2
        upper_border = base_metal_center_line - base_metal_rel_thickness / 2
        v_center_line_position = self.canvas_size[0] / 2

        # Draws the Grid Lines
        if True:
            start = (v_center_line_position, 0)
            end = (v_center_line_position, self.canvas_size[1])
            line = self.canvas.create_line(*start, *end, fill=line_color, width=1, dash=(3, 2))
            self.canvas_grid_items.append(line)

            start = (0, base_metal_center_line)
            end = (self.canvas_size[0], base_metal_center_line)
            line = self.canvas.create_line(*start, *end, fill=line_color, width=1, dash=(3, 2))
            self.canvas_grid_items.append(line)

        # Draws the Base Metal Limits
        if True:
            start = (0, upper_border)
            end = (self.canvas_size[0], upper_border)
            line = self.canvas.create_line(*start, *end, fill=line_color, width=1, dash=(3, 2))
            self.canvas_grid_items.append(line)

            start = (0, lower_border)
            end = (self.canvas_size[0], lower_border)
            line = self.canvas.create_line(*start, *end, fill=line_color, width=1, dash=(3, 2))
            self.canvas_grid_items.append(line)

        self.drawing_limits['relative_thickness'] = base_metal_rel_thickness
        self.drawing_limits['mid_thickness'] = base_metal_center_line
        self.drawing_limits['mid_length'] = v_center_line_position
        self.drawing_limits['upper_border'] = upper_border
        self.drawing_limits['lower_border'] = lower_border

        if event != '@start':
            self.update_plot()

    # Widgets Related Methods ------------------------------------------------------------------------------------------
    def activate_non_standard_bevel(self):
        """ Enables the selection of different bevels for each side """

        # Erases the current drawing and applicable variables
        if True:
            self.bevel_var.set('')

            self.left_bevel_var.set('')
            self.left_options_vars_list = []
            self.left_options = []

            self.right_bevel_var.set('')
            self.right_options_vars_list = []
            self.right_options = []

            self.top_reinforcement = []
            self.bottom_reinforcement = []

            self.adjust_drawing_area('@start')

        # Removes all widgets from both bevel frames
        if True:
            for widget in self.primary_bevel_frame.winfo_children():
                widget.destroy()
            for widget in self.secondary_bevel_frame.winfo_children():
                widget.destroy()

        # Standard bevels selected
        if self.standard_bevel_var.get():

            # Removes the second bevel frame from screen
            self.secondary_bevel_frame.grid_remove()
            self.right_frame.rowconfigure(1, weight=0)

            # Adds title to the first frame
            label = ttk.Label(self.primary_bevel_frame, text='Bevel Details', style='secondary.Inverse.TLabel')
            label.grid(row=0, column=0, columnspan=2, sticky='nsew', pady=(0, 10))

            # Remove non-standard related widgets
            self.combobox_2.grid_remove()
            self.combobox_3.grid_remove()
            self.left_label.grid_remove()
            self.right_label.grid_remove()

            # Show standard related widgets
            self.combobox_1.grid()
            self.standard_bevel_label.grid()

        else:
            # Shows the second bevel frame on screen
            self.secondary_bevel_frame.grid()
            self.right_frame.rowconfigure(1, weight=1)

            # Adds a title to each frame
            label = ttk.Label(self.primary_bevel_frame, text='Left Bevel Details', style='secondary.Inverse.TLabel')
            label.grid(row=0, column=0, columnspan=2, sticky='nsew', pady=(0, 10))
            label = ttk.Label(self.secondary_bevel_frame, text='Right Bevel Details', style='secondary.Inverse.TLabel')
            label.grid(row=0, column=0, columnspan=2, sticky='nsew', pady=(0, 10))

            # Remove standard related widgets
            self.combobox_1.grid_remove()
            self.standard_bevel_label.grid_remove()

            # Show non-standard related widgets
            self.combobox_2.grid()
            self.combobox_3.grid()
            self.left_label.grid()
            self.right_label.grid()

            # Disables the 'right' bevel selection combobox, waiting for the 'left bevel' selection
            self.combobox_3.config(state='disabled')

    def update_bevel_options(self, event):
        """ Updates the spin boxes to be shown based on the bevel selected by the user """

        # Defines the origin of the event
        combo_box_list = (self.combobox_1, self.combobox_2, self.combobox_3)
        origin = combo_box_list.index(event.widget)

        # Gets the selected bevel and the applicable options
        if True:
            if origin == 0:
                selected_bevel = self.bevel_var.get()
                self.left_options = self.bevel_parameters[selected_bevel]
                self.right_options = self.bevel_parameters[selected_bevel]

            elif origin == 1:
                selected_bevel = self.left_bevel_var.get()
                self.left_options = self.bevel_parameters[selected_bevel]

                # Whenever left bevel is selected, erases the second bevel
                self.right_bevel_var.set('')
                for widget in self.secondary_bevel_frame.winfo_children():
                    widget.destroy()
                label = ttk.Label(self.secondary_bevel_frame, text='Right Bevel Details',
                                  style='secondary.Inverse.TLabel')
                label.grid(row=0, column=0, columnspan=2, sticky='nsew')

            else:
                selected_bevel = self.right_bevel_var.get()
                self.right_options = self.bevel_parameters[selected_bevel]

        # Clears the bevel frames from previous options
        if True:
            if origin in (0, 1):
                for widget in self.primary_bevel_frame.winfo_children():
                    widget.destroy()
            else:
                for widget in self.secondary_bevel_frame.winfo_children():
                    widget.destroy()

        # Adds title to the frames
        if True:
            if origin == 0:
                label = ttk.Label(self.primary_bevel_frame, text='Bevel Details', style='secondary.Inverse.TLabel')
                label.grid(row=0, column=0, columnspan=2, sticky='nsew', pady=(0, 10))
            elif origin == 1:
                label = ttk.Label(self.primary_bevel_frame, text='Left Bevel Details', style='secondary.Inverse.TLabel')
                label.grid(row=0, column=0, columnspan=2, sticky='nsew', pady=(0, 10))
            else:
                label = ttk.Label(self.secondary_bevel_frame, text='Right Bevel Details',
                                  style='secondary.Inverse.TLabel')
                label.grid(row=0, column=0, columnspan=2, sticky='nsew', pady=(0, 10))

        # Clears the variables, selects the options list and the frame
        if True:
            var_list = []
            if origin in (0, 1):
                options = self.left_options
                frame = self.primary_bevel_frame
            else:
                options = self.right_options
                frame = self.secondary_bevel_frame

        # Creates all the applicable options
        for i, item in enumerate(options):

            if origin == 2 and \
                    item in ('Total Thickness [mm]', 'Root Land [mm]', 'Side 1 Depth [mm]') and \
                    item in self.left_options:
                _var = tk.StringVar()
                var_list.append(_var)
                continue

            label = ttk.Label(frame, text=f'{item}:', anchor='e')
            label.grid(row=i+1, column=0, sticky='nsew', padx=2, pady=2)

            opt = self.spin_box_parameters[item]

            _var = tk.StringVar(value=opt['value'])
            var_list.append(_var)

            spinbox = ttk.Spinbox(frame, textvariable=_var, width=4, from_=opt['from'], to_=opt['to'],
                                  increment=opt['increment'], command=lambda: self.check_values(origin=origin))
            spinbox.grid(row=i+1, column=1, sticky='nsew', padx=2, pady=2)
            spinbox.bind('<Return>', lambda event: self.check_values(event, origin=origin))
            spinbox.bind('<FocusOut>', lambda event: self.check_values(event, origin=origin))

        if origin == 0:
            self.left_options_vars_list = var_list
            self.right_options_vars_list = var_list

        elif origin == 1:
            self.left_options_vars_list = var_list

            # Enables the right bevel combobox with the applicable values
            if self.combobox_3.cget('state') != 'readonly':

                if self.left_bevel_var.get() == 'Single Square':
                    bevel_list = self.single_bevel_options

                elif 'Single' in self.left_bevel_var.get():
                    bevel_list = [bevel for bevel in self.single_bevel_options if 'Single' in bevel]

                else:
                    bevel_list = [bevel for bevel in self.single_bevel_options if 'Double' in bevel]

                self.combobox_3.config(state='readonly', values=bevel_list)
            else:
                self.right_bevel_var.set('')
                self.combobox_3.event_generate('<<ComboboxSelected>>')
        else:
            self.right_options_vars_list = var_list

        self.check_values(origin=origin)
        self.update_plot()

    def check_values(self, event=None, origin=None):
        """ Checks for consistency in the user values """

        if origin == 0:
            selected_bevel = self.bevel_var.get()
            local_list = self.left_options_vars_list
            original_options = self.bevel_parameters[selected_bevel]
            current_options = [widget.cget('text').strip(':')
                               for widget in self.primary_bevel_frame.winfo_children() if '[' in widget.cget('text')]
        elif origin == 1:
            selected_bevel = self.left_bevel_var.get()
            local_list = self.left_options_vars_list
            original_options = self.bevel_parameters[selected_bevel]
            current_options = [widget.cget('text').strip(':')
                               for widget in self.primary_bevel_frame.winfo_children() if '[' in widget.cget('text')]
        else:
            selected_bevel = self.right_bevel_var.get()
            local_list = self.right_options_vars_list
            original_options = self.bevel_parameters[selected_bevel]
            current_options = [widget.cget('text').strip(':')
                               for widget in self.secondary_bevel_frame.winfo_children() if '[' in widget.cget('text')]

        # Grabs the relevant thickness, land and depth data
        if True:
            try:
                land = float(
                    self.left_options_vars_list[self.left_options.index('Root Land [mm]')].get())
            except ValueError:
                try:
                    land = float(
                        self.right_options_vars_list[self.right_options.index('Root Land [mm]')].get())
                except ValueError:
                    land = 0

            try:
                root_depth = float(
                    self.left_options_vars_list[self.left_options.index('Side 1 Depth [mm]')].get())
            except ValueError:
                try:
                    root_depth = float(
                        self.right_options_vars_list[self.right_options.index('Side 1 Depth [mm]')].get())
                except ValueError:
                    root_depth = 0

            try:
                total_thickness = float(
                    self.left_options_vars_list[self.left_options.index('Total Thickness [mm]')].get())
            except ValueError:
                total_thickness = 0

        # Thickness limits
        if 'Total Thickness [mm]' in current_options:
            total_thickness = max(3., min(200., total_thickness))
            local_list[original_options.index('Total Thickness [mm]')].set(total_thickness)

        # Side 1 depth limits
        if True:
            if 'Side 1 Depth [mm]' in current_options and selected_bevel == 'Double Compound':
                root_depth = max(land, min(root_depth, total_thickness-land))
                local_list[original_options.index('Side 1 Depth [mm]')].set(root_depth)

            if 'Side 1 Depth [mm]' in current_options:
                root_depth = max(land/2, min(root_depth, total_thickness-land/2))
                local_list[original_options.index('Side 1 Depth [mm]')].set(root_depth)

        # Root land limits
        if True:
            if 'Root Land [mm]' in current_options and 'Single' in selected_bevel:
                land = max(0., min(100., land, total_thickness))
                local_list[original_options.index('Root Land [mm]')].set(land)

            elif 'Root Land [mm]' in current_options and 'Single J' in selected_bevel:
                radius = float(local_list[original_options.index('Bevel Radius [mm]')].get())
                land = max(0., min(100., land, 2*root_depth, total_thickness-radius))
                local_list[original_options.index('Root Land [mm]')].set(land)

            elif 'Root Land [mm]' in current_options and 'Double J' in selected_bevel:
                radius = float(local_list[original_options.index('Bevel Radius Side 1 [mm]')].get())
                radius_2 = float(local_list[original_options.index('Bevel Radius Side 2 [mm]')].get())
                land = max(0., min(100., land, 2*root_depth, total_thickness-radius-radius_2))
                local_list[original_options.index('Root Land [mm]')].set(land)

            elif 'Root Land [mm]' in current_options:
                land = max(0., min(100., land, 2*root_depth, total_thickness))
                local_list[original_options.index('Root Land [mm]')].set(land)

        # Bevel radius limits
        if True:
            if 'Bevel Radius [mm]' in current_options:
                radius = float(local_list[original_options.index('Bevel Radius [mm]')].get())
                radius = max(1.0, min(100., radius, total_thickness-land))
                local_list[original_options.index('Bevel Radius [mm]')].set(radius)

            if 'Bevel Radius Side 1 [mm]' in current_options:
                radius = float(local_list[original_options.index('Bevel Radius Side 1 [mm]')].get())
                radius = max(1.0, min(100., radius, root_depth-land/2))
                local_list[original_options.index('Bevel Radius Side 1 [mm]')].set(radius)

            if 'Bevel Radius Side 2 [mm]' in current_options:
                radius = float(local_list[original_options.index('Bevel Radius Side 2 [mm]')].get())
                radius = max(1.0, min(100., radius, total_thickness-root_depth-land/2))
                local_list[original_options.index('Bevel Radius Side 2 [mm]')].set(radius)

        # Transition depth limits
        if True:
            if 'Transition Depth [mm]' in current_options:
                transition = float(local_list[original_options.index('Transition Depth [mm]')].get())
                transition = max(2.0, min(transition, total_thickness-land))
                local_list[original_options.index('Transition Depth [mm]')].set(transition)

            if 'Transition Depth 1 [mm]' in current_options:
                transition = float(local_list[original_options.index('Transition Depth 1 [mm]')].get())
                transition = max(2.0, min(transition, root_depth-land/2))
                local_list[original_options.index('Transition Depth 1 [mm]')].set(transition)

            if 'Transition Depth 2 [mm]' in current_options:
                transition = float(local_list[original_options.index('Transition Depth 2 [mm]')].get())
                transition = max(2.0, min(transition, total_thickness - root_depth - land/2))
                local_list[original_options.index('Transition Depth 2 [mm]')].set(transition)

        if origin == 1 and self.right_bevel_var.get():
            self.check_values(origin=2)
        else:
            self.update_plot()

    # Plot Related Methods ---------------------------------------------------------------------------------------------
    def update_plot(self, event=None):
        """
        Updates the plot area by choosing the bevel parts (left/right bevels) 
        and then calling the applicable drawing methods
        """

        # Dictionaries for bevel types
        if True:
            bevel_parts = {
                'Single Square': ('Single Square', 'Single Square'),
                'Single Bevel': ('Single Square', 'Single V'),
                'Single V': ('Single V', 'Single V'),
                'Single J': ('Single Square', 'Single J'),
                'Single U': ('Single J', 'Single J'),
                'Single Compound': ('Single Compound', 'Single Compound'),
                'Double Bevel': ('Single Square', 'Double V'),
                'Double V': ('Double V', 'Double V'),
                'Double J': ('Double J', 'Double J'),
                'Double Compound': ('Double Compound', 'Double Compound'),
                'Double U': ('Double J', 'Double J')
            }

            bevel_methods = {
                'Single Square': self.draw_square,
                'Single V': self.draw_v,
                'Single J': self.draw_j,
                'Single Compound': self.draw_compound,
                'Double V': self.draw_double_v,
                'Double J': self.draw_double_j,
                'Double Compound': self.draw_double_compound,
            }

        # Finds the left and right bevels
        standard_bevel = self.standard_bevel_var.get()

        if standard_bevel:
            left_bevel, right_bevel = bevel_parts.get(self.bevel_var.get(), (None, None))
        else:
            left_bevel = self.left_bevel_var.get()
            right_bevel = self.right_bevel_var.get()

        if not left_bevel and not right_bevel:
            return

        # Updates the additional plot data: proportion, weld_gap, weld_reinforcement_1, weld_reinforcement_2
        self.find_plot_data()

        # Removes previous drawings
        for _id in self.canvas.find_all():
            if _id not in self.canvas_grid_items:
                self.canvas.delete(_id)

        # Erases the lists to hold the weld coordinates
        if True:
            self.top_reinforcement = []
            self.bottom_reinforcement = []
            self.weld_area = {'Top Reinforcement Area': 0,
                              'Bottom Reinforcement Area': 0,
                              'Left Weld Area': 0,
                              'Right Weld Area': 0}

        # Draws the selected bevels
        if left_bevel:
            bevel_methods[left_bevel]('left')
        if right_bevel:
            bevel_methods[right_bevel]('right')

        if left_bevel and right_bevel:
            self.draw_weld_reinforcement()

    def find_plot_data(self):
        """ Additional plot data """

        weld_reinforcement_1 = self.additional_options_vars_list[0].get()
        weld_reinforcement_2 = self.additional_options_vars_list[1].get()
        weld_gap = self.additional_options_vars_list[2].get()
        base_metal_thickness = float(self.left_options_vars_list[0].get())

        proportion = self.drawing_limits['relative_thickness'] / base_metal_thickness

        self.drawing_limits['proportion'] = proportion
        self.drawing_limits['weld_reinforcement_1'] = weld_reinforcement_1 * proportion
        self.drawing_limits['weld_reinforcement_2'] = weld_reinforcement_2 * proportion
        self.drawing_limits['weld_gap'] = weld_gap * proportion

    # Bevel drawing methods --------------------------------------------------------------------------------------------
    @staticmethod
    def triangle_area(point_1, point_2, point_3):
        x1, y1 = point_1
        x2, y2 = point_2
        x3, y3 = point_3
        return abs(0.5 * (((x2 - x1) * (y3 - y1)) - ((x3 - x1) * (y2 - y1))))

    def draw_square(self, position):
        """ Method to draw a square bevel """

        if position == 'left':
            sign = -1
            edge = 0
        else:
            sign = 1
            edge = self.canvas_size[0]

        # General data
        gap = self.drawing_limits['weld_gap']
        lower_border = self.drawing_limits['lower_border']
        upper_border = self.drawing_limits['upper_border']

        # Drawing points
        i1 = ((self.canvas_size[0] + sign * gap) / 2, lower_border)
        i2 = ((self.canvas_size[0] + sign * gap) / 2, upper_border)
        i3 = (edge, upper_border)
        i4 = (edge, lower_border)
        self.canvas.create_line(*i1, *i2, *i3, *i4, *i1, fill=self.border_color, width=1)

        # Weld coordinates
        self.bottom_reinforcement.append(i1)
        self.top_reinforcement.append(i2)

    def draw_v(self, position):
        """ Method to draw a V bevel """

        if position == 'left':
            sign = -1
            edge = 0
            key = 'Left Weld Area'
            vars_list = self.left_options_vars_list
            options = self.left_options
        else:
            sign = 1
            edge = self.canvas_size[0]
            key = 'Right Weld Area'
            vars_list = self.right_options_vars_list
            options = self.right_options

        # General data
        thickness_in_drawing = self.drawing_limits['relative_thickness']
        gap = self.drawing_limits['weld_gap']
        lower_border = self.drawing_limits['lower_border']
        upper_border = self.drawing_limits['upper_border']
        proportion = self.drawing_limits['proportion']

        # Bevel specific data
        angle = float(vars_list[options.index('Bevel Angle [°]')].get())
        try:
            land = float(self.left_options_vars_list[self.left_options.index('Root Land [mm]')].get()) * proportion
        except ValueError:
            land = float(self.right_options_vars_list[self.right_options.index('Root Land [mm]')].get()) * proportion
        aperture = tan(radians(angle)) * (thickness_in_drawing - land)

        # Drawing points
        i1 = ((self.canvas_size[0] + sign * gap) / 2, lower_border)
        i2 = ((self.canvas_size[0] + sign * gap) / 2, lower_border - land)
        i3 = ((self.canvas_size[0] + sign * gap) / 2 + sign * aperture, upper_border)
        i4 = (edge, upper_border)
        i5 = (edge, lower_border)
        weld_line = ((self.canvas_size[0] + sign * gap) / 2, upper_border)
        self.canvas.create_polygon(*i2, *i3, *weld_line, *i2, fill=self.fill_color, outline='red')
        self.canvas.create_line(*i1, *i2, *i3, *i4, *i5, *i1, fill=self.border_color, width=1)

        # Weld area
        area = self.triangle_area(i2, i3, weld_line) / proportion ** 2
        self.weld_area[key] += area

        # Weld coordinates
        self.bottom_reinforcement.append(i1)
        self.top_reinforcement.append(i3)

    def draw_j(self, position):
        """ Method to draw a J bevel """

        if position == 'left':
            sign = -1
            edge = 0
            key = 'Left Weld Area'
            vars_list = self.left_options_vars_list
            options = self.left_options
        else:
            sign = 1
            edge = self.canvas_size[0]
            key = 'Right Weld Area'
            vars_list = self.right_options_vars_list
            options = self.right_options

        # General data
        thickness_in_drawing = self.drawing_limits['relative_thickness']
        gap = self.drawing_limits['weld_gap']
        lower_border = self.drawing_limits['lower_border']
        upper_border = self.drawing_limits['upper_border']
        proportion = self.drawing_limits['proportion']

        # Bevel specific data
        angle = float(vars_list[options.index('Bevel Angle [°]')].get())
        radius = float(vars_list[options.index('Bevel Radius [mm]')].get()) * proportion
        try:
            land = float(self.left_options_vars_list[self.left_options.index('Root Land [mm]')].get()) * proportion
        except ValueError:
            land = float(self.right_options_vars_list[self.right_options.index('Root Land [mm]')].get()) * proportion
        height = radius * (1 - sin(radians(angle)))
        width = radius * cos(radians(angle))
        aperture = tan(radians(angle)) * (thickness_in_drawing - land - height)

        # Drawing Points
        i1 = ((self.canvas_size[0] + sign * gap) / 2, lower_border)
        i2 = ((self.canvas_size[0] + sign * gap) / 2, lower_border - land)
        self.canvas.create_line(*i1, *i2, fill=self.border_color, width=1)

        arc_initial_pos = ((self.canvas_size[0] + sign * gap) / 2 - radius, lower_border - land - 2 * radius)
        arc_final_pos = ((self.canvas_size[0] + sign * gap) / 2 + radius, lower_border - land)

        self.canvas.create_arc(*arc_initial_pos, *arc_final_pos, start=-90, extent=sign * (90 - angle),
                               style='pieslice', fill=self.fill_color, outline='red')
        self.canvas.create_arc(*arc_initial_pos, *arc_final_pos, start=-90, extent=sign * (90 - angle),
                               outline=self.border_color, style='arc', width=1)

        i3 = ((self.canvas_size[0] + sign * gap) / 2 + sign * width, lower_border - land - height)
        i4 = ((self.canvas_size[0] + sign * gap) / 2 + sign * aperture + sign * width, upper_border)
        i5 = (edge, upper_border)
        i6 = (edge, lower_border)
        weld_line_1 = ((self.canvas_size[0] + sign * gap) / 2, lower_border - land - radius)
        weld_line_2 = ((self.canvas_size[0] + sign * gap) / 2, upper_border)
        self.canvas.create_polygon(*i3, *weld_line_1, *weld_line_2, *i3, fill=self.fill_color, outline='red')
        self.canvas.create_polygon(*i3, *weld_line_2, *i4, *i3, fill=self.fill_color, outline='red')
        self.canvas.create_line(*i3, *i4, *i5, *i6, *i1, fill=self.border_color, width=1)

        # Weld area
        area_1 = pi * radius ** 2 * angle / 360
        area_2 = self.triangle_area(i3, weld_line_1, weld_line_2)
        area_3 = self.triangle_area(i3, weld_line_2, i4)
        area = (area_1 + area_2 + area_3) / proportion ** 2
        self.weld_area[key] += area

        # Weld coordinates
        self.bottom_reinforcement.append(i1)
        self.top_reinforcement.append(i4)

    def draw_compound(self, position):
        """ Method to draw a compound bevel """

        if position == 'left':
            sign = -1
            edge = 0
            key = 'Left Weld Area'
            vars_list = self.left_options_vars_list
            options = self.left_options
        else:
            sign = 1
            edge = self.canvas_size[0]
            key = 'Right Weld Area'
            vars_list = self.right_options_vars_list
            options = self.right_options

        # General data
        thickness_in_drawing = self.drawing_limits['relative_thickness']
        gap = self.drawing_limits['weld_gap']
        lower_border = self.drawing_limits['lower_border']
        upper_border = self.drawing_limits['upper_border']
        proportion = self.drawing_limits['proportion']

        # Bevel specific data
        angle_1 = float(vars_list[options.index('Bevel Angle 1 [°]')].get())
        angle_2 = float(vars_list[options.index('Bevel Angle 2 [°]')].get())
        transition_depth = float(vars_list[options.index('Transition Depth [mm]')].get()) * proportion
        try:
            land = float(self.left_options_vars_list[self.left_options.index('Root Land [mm]')].get()) * proportion
        except ValueError:
            land = float(self.right_options_vars_list[self.right_options.index('Root Land [mm]')].get()) * proportion
        aperture_1 = tan(radians(angle_1)) * (thickness_in_drawing - land - transition_depth)
        aperture_2 = tan(radians(angle_2)) * transition_depth

        # Drawing points
        i1 = ((self.canvas_size[0] + sign * gap) / 2, lower_border)
        i2 = ((self.canvas_size[0] + sign * gap) / 2, lower_border - land)
        i3 = ((self.canvas_size[0] + sign * gap) / 2 + sign * aperture_1, upper_border + transition_depth)
        i4 = ((self.canvas_size[0] + sign * gap) / 2 + sign * aperture_1 + sign * aperture_2, upper_border)
        i5 = (edge, upper_border)
        i6 = (edge, lower_border)
        weld_line = ((self.canvas_size[0] + sign * gap) / 2, upper_border)
        self.canvas.create_polygon(*i2, *weld_line, *i3, *i2, fill=self.fill_color, outline='red')
        self.canvas.create_polygon(*i3, *weld_line, *i4, *i3, fill=self.fill_color, outline='red')
        self.canvas.create_line(*i1, *i2, *i3, *i4, *i5, *i6, *i1, fill=self.border_color, width=1)

        # Weld area
        area_1 = self.triangle_area(i2, i3, weld_line)
        area_2 = self.triangle_area(i3, i4, weld_line)
        area = (area_1 + area_2) / proportion ** 2
        self.weld_area[key] += area

        # Weld coordinates
        self.bottom_reinforcement.append(i1)
        self.top_reinforcement.append(i4)

    def draw_double_v(self, position):
        """ Method to draw a Double V bevel """

        if position == 'left':
            sign = -1
            edge = 0
            key = 'Left Weld Area'
            vars_list = self.left_options_vars_list
            options = self.left_options
        else:
            sign = 1
            edge = self.canvas_size[0]
            key = 'Right Weld Area'
            vars_list = self.right_options_vars_list
            options = self.right_options

        # General data
        thickness_in_drawing = self.drawing_limits['relative_thickness']
        gap = self.drawing_limits['weld_gap']
        lower_border = self.drawing_limits['lower_border']
        upper_border = self.drawing_limits['upper_border']
        proportion = self.drawing_limits['proportion']

        # Bevel specific data
        side_1_angle = float(vars_list[options.index('Bevel Angle Side 1 [°]')].get())
        side_2_angle = float(vars_list[options.index('Bevel Angle Side 2 [°]')].get())
        try:
            land = float(self.left_options_vars_list[self.left_options.index('Root Land [mm]')].get()) * proportion
        except ValueError:
            land = float(self.right_options_vars_list[self.right_options.index('Root Land [mm]')].get()) * proportion
        try:
            side_1_depth = float(
                self.left_options_vars_list[self.left_options.index('Side 1 Depth [mm]')].get()) * proportion
        except ValueError:
            side_1_depth = float(
                self.right_options_vars_list[self.right_options.index('Side 1 Depth [mm]')].get()) * proportion
        aperture_1 = tan(radians(side_1_angle)) * (side_1_depth - land / 2)
        aperture_2 = \
            tan(radians(side_2_angle)) * (thickness_in_drawing - side_1_depth - land / 2)

        # Drawing points
        i1 = ((self.canvas_size[0] + sign * gap) / 2 + sign * aperture_2, lower_border)
        i2 = ((self.canvas_size[0] + sign * gap) / 2, upper_border + side_1_depth + land / 2)
        i3 = ((self.canvas_size[0] + sign * gap) / 2, upper_border + side_1_depth - land / 2)
        i4 = ((self.canvas_size[0] + sign * gap) / 2 + sign * aperture_1, upper_border)
        i5 = (edge, upper_border)
        i6 = (edge, lower_border)
        weld_line_1 = ((self.canvas_size[0] + sign * gap) / 2, upper_border)
        weld_line_2 = ((self.canvas_size[0] + sign * gap) / 2, lower_border)
        self.canvas.create_polygon(*i1, *i2, *weld_line_2, *i1, fill=self.fill_color, outline='red')
        self.canvas.create_polygon(*i3, *i4, *weld_line_1, *i3, fill=self.fill_color, outline='red')
        self.canvas.create_line(*i1, *i2, *i3, *i4, *i5, *i6, *i1, fill=self.border_color, width=1)

        # Weld area
        area_1 = self.triangle_area(i1, i2, weld_line_2) / proportion ** 2
        area_2 = self.triangle_area(i3, i4, weld_line_1) / proportion ** 2

        self.weld_area[key] += (area_1 + area_2)

        # Weld coordinates
        self.bottom_reinforcement.append(i1)
        self.top_reinforcement.append(i4)

    def draw_double_j(self, position):
        """ Method to draw a Double J bevel """

        if position == 'left':
            sign = -1
            edge = 0
            key = 'Left Weld Area'
            vars_list = self.left_options_vars_list
            options = self.left_options
        else:
            sign = 1
            edge = self.canvas_size[0]
            key = 'Right Weld Area'
            vars_list = self.right_options_vars_list
            options = self.right_options

        # General data
        thickness_in_drawing = self.drawing_limits['relative_thickness']
        gap = self.drawing_limits['weld_gap']
        lower_border = self.drawing_limits['lower_border']
        upper_border = self.drawing_limits['upper_border']
        proportion = self.drawing_limits['proportion']

        # Bevel specific data
        try:
            side_1_depth = float(
                self.left_options_vars_list[self.left_options.index('Side 1 Depth [mm]')].get()) * proportion
        except ValueError:
            side_1_depth = float(
                self.right_options_vars_list[self.right_options.index('Side 1 Depth [mm]')].get()) * proportion
        try:
            land = float(self.left_options_vars_list[self.left_options.index('Root Land [mm]')].get()) * proportion
        except ValueError:
            land = float(self.right_options_vars_list[self.right_options.index('Root Land [mm]')].get()) * proportion

        angle_1 = float(vars_list[options.index('Bevel Angle Side 1 [°]')].get())
        radius_1 = float(vars_list[options.index('Bevel Radius Side 1 [mm]')].get()) * proportion

        height_1 = radius_1 * (1 - sin(radians(angle_1)))
        width_1 = radius_1 * cos(radians(angle_1))
        aperture_1 = tan(radians(angle_1)) * (thickness_in_drawing - side_1_depth - land / 2 - height_1)

        angle_2 = float(vars_list[options.index('Bevel Angle Side 2 [°]')].get())
        radius_2 = float(vars_list[options.index('Bevel Radius Side 2 [mm]')].get()) * proportion

        height_2 = radius_2 * (1 - sin(radians(angle_2)))
        width_2 = radius_2 * cos(radians(angle_2))
        aperture_2 = tan(radians(angle_2)) * (thickness_in_drawing - side_1_depth - land / 2 - height_2)

        # Drawing points
        i1 = ((self.canvas_size[0] + sign * gap) / 2 + sign * aperture_2 + sign * width_2, lower_border)
        i2 = ((self.canvas_size[0] + sign * gap) / 2 + sign * width_2,
              upper_border + side_1_depth + land / 2 + height_2)
        weld_line_2 = ((self.canvas_size[0] + sign * gap) / 2, upper_border + side_1_depth + land/2 + radius_2)
        weld_line_1 = ((self.canvas_size[0] + sign * gap) / 2, lower_border)
        self.canvas.create_polygon(*i1, *i2, *weld_line_1, *i1, fill=self.fill_color, outline='red')
        self.canvas.create_polygon(*i2, *weld_line_1, *weld_line_2, *i2, fill=self.fill_color, outline='red')
        self.canvas.create_line(*i1, *i2, fill=self.border_color, width=1)

        arc_initial_pos_1 = ((self.canvas_size[0] + sign * gap) / 2 - radius_2,
                             upper_border + side_1_depth + land / 2)
        arc_final_pos_1 = ((self.canvas_size[0] + sign * gap) / 2 + radius_2,
                           upper_border + side_1_depth + land / 2 + 2 * radius_2)
        self.canvas.create_arc(*arc_initial_pos_1, *arc_final_pos_1, start=90, extent=sign * (angle_2 - 90),
                               style='pieslice', fill=self.fill_color, outline='red')
        self.canvas.create_arc(*arc_initial_pos_1, *arc_final_pos_1, start=90, extent=sign * (angle_2 - 90),
                               outline=self.border_color, style='arc', width=1)

        i3 = ((self.canvas_size[0] + sign * gap) / 2, upper_border + side_1_depth + land / 2)
        i4 = ((self.canvas_size[0] + sign * gap) / 2, upper_border + side_1_depth - land / 2)
        self.canvas.create_line(*i3, *i4, fill=self.border_color, width=1)

        arc_initial_pos_2 = ((self.canvas_size[0] + sign * gap) / 2 - radius_1,
                             upper_border + side_1_depth - land / 2 - 2 * radius_1)
        arc_final_pos_2 = ((self.canvas_size[0] + sign * gap) / 2 + radius_1,
                           upper_border + side_1_depth - land / 2)
        self.canvas.create_arc(*arc_initial_pos_2, *arc_final_pos_2, start=270, extent=sign * (90 - angle_1),
                               style='pieslice', fill=self.fill_color, outline='red')
        self.canvas.create_arc(*arc_initial_pos_2, *arc_final_pos_2, start=270, extent=sign * (90 - angle_1),
                               outline=self.border_color, style='arc', width=1)

        i5 = ((self.canvas_size[0] + sign * gap) / 2 + sign * width_1,
              upper_border + side_1_depth - land / 2 - height_1)
        i6 = ((self.canvas_size[0] + sign * gap) / 2 + sign * aperture_1 + sign * width_1, upper_border)
        i7 = (edge, upper_border)
        i8 = (edge, lower_border)
        weld_line_3 = ((self.canvas_size[0] + sign * gap) / 2, upper_border + side_1_depth - land / 2 - radius_1)
        weld_line_4 = ((self.canvas_size[0] + sign * gap) / 2, upper_border)
        self.canvas.create_polygon(*i5, *weld_line_3, *weld_line_4, *i5, fill=self.fill_color, outline='red')
        self.canvas.create_polygon(*i5, *weld_line_4, *i6, *i5, fill=self.fill_color, outline='red')
        self.canvas.create_line(*i5, *i6, *i7, *i8, *i1, fill=self.border_color, width=1)

        # Weld area
        area_1 = pi * radius_2 ** 2 * angle_2 / 360 / proportion ** 2
        area_2 = self.triangle_area(i1, i2, weld_line_1) / proportion ** 2
        area_3 = self.triangle_area(i2, weld_line_1, weld_line_2) / proportion ** 2

        area_4 = pi * radius_1 ** 2 * angle_1 / 360 / proportion ** 2
        area_5 = self.triangle_area(i5, weld_line_3, weld_line_4) / proportion ** 2
        area_6 = self.triangle_area(i5, weld_line_4, i6) / proportion ** 2

        self.weld_area[key] += (area_1 + area_2 + area_3 + area_4 + area_5 + area_6)

        # Weld coordinates
        self.bottom_reinforcement.append(i1)
        self.top_reinforcement.append(i6)

    def draw_double_compound(self, position):
        """ Method to draw a Double Compound bevel """

        if position == 'left':
            sign = -1
            edge = 0
            key = 'Left Weld Area'
            vars_list = self.left_options_vars_list
            options = self.left_options
        else:
            sign = 1
            edge = self.canvas_size[0]
            key = 'Right Weld Area'
            vars_list = self.right_options_vars_list
            options = self.right_options

        # General data
        thickness_in_drawing = self.drawing_limits['relative_thickness']
        gap = self.drawing_limits['weld_gap']
        lower_border = self.drawing_limits['lower_border']
        upper_border = self.drawing_limits['upper_border']
        proportion = self.drawing_limits['proportion']

        # Bevel specific data
        try:
            land = float(self.left_options_vars_list[self.left_options.index('Root Land [mm]')].get()) * proportion
        except ValueError:
            land = float(self.right_options_vars_list[self.right_options.index('Root Land [mm]')].get()) * proportion
        try:
            side_1_depth = float(
                self.left_options_vars_list[self.left_options.index('Side 1 Depth [mm]')].get()) * proportion
        except ValueError:
            side_1_depth = float(
                self.right_options_vars_list[self.right_options.index('Side 1 Depth [mm]')].get()) * proportion

        angle_1_1 = float(vars_list[options.index('Bevel Angle 1 - Side 1 [°]')].get())
        angle_1_2 = float(vars_list[options.index('Bevel Angle 2 - Side 1 [°]')].get())
        transition_depth_1 = float(vars_list[options.index('Transition Depth 1 [mm]')].get()) * proportion

        aperture_1_1 = tan(radians(angle_1_1)) * (side_1_depth - land/2 - transition_depth_1)
        aperture_1_2 = tan(radians(angle_1_2)) * transition_depth_1

        angle_2_1 = float(vars_list[options.index('Bevel Angle 1 - Side 2 [°]')].get())
        angle_2_2 = float(vars_list[options.index('Bevel Angle 2 - Side 2 [°]')].get())
        transition_depth_2 = float(vars_list[options.index('Transition Depth 2 [mm]')].get()) * proportion
        aperture_2_1 = \
            tan(radians(angle_2_1)) * (thickness_in_drawing - side_1_depth - land/2 - transition_depth_2)
        aperture_2_2 = tan(radians(angle_2_2)) * transition_depth_2

        # Drawing points
        i1 = ((self.canvas_size[0] + sign * gap) / 2 + sign * aperture_2_1 + sign * aperture_2_2, lower_border)
        i2 = ((self.canvas_size[0] + sign * gap) / 2 + sign * aperture_2_1, lower_border - transition_depth_2)
        i3 = ((self.canvas_size[0] + sign * gap) / 2, upper_border + side_1_depth + land/2)
        i4 = ((self.canvas_size[0] + sign * gap) / 2, upper_border + side_1_depth - land/2)
        i5 = ((self.canvas_size[0] + sign * gap) / 2 + sign * aperture_1_1, upper_border + transition_depth_1)
        i6 = ((self.canvas_size[0] + sign * gap) / 2 + sign * aperture_1_1 + sign * aperture_1_2, upper_border)
        i7 = (edge, upper_border)
        i8 = (edge, lower_border)
        weld_line_1 = ((self.canvas_size[0] + sign * gap) / 2, lower_border)
        weld_line_2 = ((self.canvas_size[0] + sign * gap) / 2, upper_border)

        self.canvas.create_polygon(*i1, *i2, *weld_line_1, *i1, fill=self.fill_color, outline='red')
        self.canvas.create_polygon(*i2, *weld_line_1, *i3, *i2, fill=self.fill_color, outline='red')
        self.canvas.create_polygon(*i4, *weld_line_2, *i5, *i4, fill=self.fill_color, outline='red')
        self.canvas.create_polygon(*i5, *weld_line_2, *i6, *i5, fill=self.fill_color, outline='red')
        self.canvas.create_line(*i1, *i2, *i3, *i4, *i5, *i6, *i7, *i8, *i1, fill=self.border_color, width=1)

        # Weld area
        area_1 = self.triangle_area(i1, i2, weld_line_1) / proportion ** 2
        area_2 = self.triangle_area(i2, weld_line_1, i3) / proportion ** 2

        area_3 = self.triangle_area(i4, weld_line_2, i5) / proportion ** 2
        area_4 = self.triangle_area(i5, weld_line_2, i6) / proportion ** 2

        self.weld_area[key] += (area_1 + area_2 + area_3 + area_4)

        # Weld coordinates
        self.bottom_reinforcement.append(i1)
        self.top_reinforcement.append(i6)

    # Other Weld Plot Methods ------------------------------------------------------------------------------------------
    def draw_weld_reinforcement(self):
        """ Draws the weld reinforcement """

        # Weld Reinforcements Areas
        if True:
            proportion = self.drawing_limits['proportion']
            weld_1 = self.drawing_limits['weld_reinforcement_1']
            weld_2 = self.drawing_limits['weld_reinforcement_2']

            # Top reinforcement
            start = (self.top_reinforcement[0][0], self.top_reinforcement[0][1] - weld_1)
            end = (self.top_reinforcement[1][0], self.top_reinforcement[1][1] + weld_1)
            self.canvas.create_arc(*start, *end, start=0, extent=180, style='chord',
                                   fill=self.fill_color, outline='red')
            self.canvas.create_arc(*start, *end, start=0, extent=180, outline=self.border_color, style='arc', width=1)

            top_area = pi * abs((self.top_reinforcement[0][0] - self.top_reinforcement[1][0]) / 2) * weld_1 / 2
            top_area = top_area / proportion ** 2
            self.weld_area['Top Reinforcement Area'] = top_area

            # Bottom
            start = (self.bottom_reinforcement[0][0], self.bottom_reinforcement[0][1] - weld_2)
            end = (self.bottom_reinforcement[1][0], self.bottom_reinforcement[1][1] + weld_2)
            self.canvas.create_arc(*start, *end, start=0, extent=-180, style='chord',
                                   fill=self.fill_color, outline='red')
            self.canvas.create_arc(*start, *end, start=0, extent=-180, outline=self.border_color, style='arc', width=1)

            bottom_area = pi * abs(
                (self.bottom_reinforcement[0][0] - self.bottom_reinforcement[1][0]) / 2) * weld_2 / 2
            bottom_area = bottom_area / proportion ** 2
            self.weld_area['Bottom Reinforcement Area'] = bottom_area

        # Mid weld area
        if True:
            color = self.fill_color
            upper_border = self.drawing_limits['upper_border']
            lower_border = self.drawing_limits['lower_border']
            gap = self.drawing_limits['weld_gap']
            thickness = self.drawing_limits['relative_thickness']
            left_edge = self.drawing_limits['mid_length'] - gap / 2
            right_edge = self.drawing_limits['mid_length'] + gap / 2

            # Central Area
            if True:
                area = gap * thickness / proportion**2
                r1 = (left_edge + 1, upper_border)
                r2 = (right_edge - 1, lower_border)
                self.canvas.create_rectangle(*r1, *r2, fill=color, outline=color)
                self.weld_area['Left Weld Area'] += area / 2
                self.weld_area['Right Weld Area'] += area / 2

        self.show_weld_area()

    def show_weld_area(self):
        """ Shows the weld areas calculated """

        if not self.weld_area:
            return

        if self.text_ids:
            for _id in self.text_ids:
                self.canvas.delete(_id)

        if self.show_area_var.get():
            state = 'normal'
        else:
            state = 'hidden'

        weld_1 = self.drawing_limits['weld_reinforcement_1']
        weld_2 = self.drawing_limits['weld_reinforcement_2']
        locations = {
            'Top Reinforcement Area': (
                self.drawing_limits['mid_length'], self.drawing_limits['upper_border'] - 40 - weld_1),
            'Bottom Reinforcement Area': (
                self.drawing_limits['mid_length'], self.drawing_limits['lower_border'] + 40 + weld_2),
            'Left Weld Area': (
                self.drawing_limits['mid_length'] / 3, self.drawing_limits['mid_thickness']),
            'Right Weld Area': (
                self.drawing_limits['mid_length'] * 5 / 3, self.drawing_limits['mid_thickness'])}

        total = 0
        self.text_ids = []
        for k, v in self.weld_area.items():
            total += v
            _id = self.canvas.create_text(*locations[k], text=f'{k}\n{v:.2f} mm²', justify='center', state=state,
                                          fill=self.border_color)
            self.text_ids.append(_id)

        location = (self.drawing_limits['mid_length'], self.canvas_size[1] - 20)
        _id = self.canvas.create_text(*location, text=f'Weld Total Area: {total:.2f} mm²',
                                      justify='center', state=state, fill=self.border_color)
        self.text_ids.append(_id)

    # App Related Methods ----------------------------------------------------------------------------------------------
    def exit_application(self):
        answer = MessageBox(self.parent, title='Exit Application',
                            message='This will close the application.\nDo you want to proceed?').show()
        if not answer:
            return
        else:
            self.parent.destroy()


def main():
    """ Initialization method """

    my_root = MyLocalRoot()
    my_frame = WeldBevelDesigner(my_root)
    my_frame.grid(row=0, column=0, sticky='nsew', padx=5, pady=5)
    my_root.mainloop()


if __name__ == '__main__':
    main()

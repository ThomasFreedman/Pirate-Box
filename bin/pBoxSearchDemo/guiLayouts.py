#!/usr/bin/python3PROPERTY
import PySimpleGUI as sg

# GUI layouts for PBox Search

class pBoxGUI:
    def __init__(self, ipfs):
        self.Ipfs = ipfs        # This is the ONLY instance!

        self.Icon = r'/usr/share/raspberrypi-artwork/pirateSkull98x128.png'
        self.Font = ("Helvetica", 10)
        self.Max7 = 1000000     # TODO - come up with a better way to handle widget defaults.
        self.LBox = []          # Each numeric field may require a different max value for example
        self.LBoxMode = sg.LISTBOX_SELECT_MODE_MULTIPLE
        self.ThemeMenuGroups = []
        self.AppWin = None      # These with hold the window objects returned by sg.Window
        self.ResultWin = None   # Result window - this could be an array or dictionary
        self.InputWidget = []   # Input widget window, layout, defaults dictionary

        top = self.topMenuBar()                            # Flatten this
        topList = lambda top: [ element for item   in top  # Flatten it here
                                        for element in topList(item) ] if type(top) is list else [top]
        self.TopMenuList = topList(top)   # Useful as in: "if event in TopMenuList: ..."

        sg.set_global_icon(self.Icon)

        # Define a custom theme for this app:
        sg.LOOK_AND_FEEL_TABLE['PirateTheme'] = {'BACKGROUND': '#000000', "TEXT": "gold",
                                                 "FONT": self.Font,
                                                 "INPUT": "#393a32", "TEXT_INPUT": "#E7C855",
                                                 "SCROLL": "#E7C855", "BORDER": 1,
                                                 "BUTTON": ("red", "gold"),
                                                 'PROGRESS': ('#D1826B', '#CC8019'), "SLIDER_DEPTH": 1,
                                                 "PROGRESS_DEPTH": 0, "ACCENT1": "#c15226",
                                                 "ACCENT2": "#7a4d5f", "ACCENT3": "#889743"}

        sg.theme("PirateTheme")  # Activate the custom pirate theme colors and settings

    # Split array lst into segments of size items in each segment
    def splitList(self, lst, size):
        for i in range(0, len(lst), size):
            yield lst[i:i + size]

    # Set all of the window elements of the input widget to their default states
    def resetWidget(self):
        if self.InputWidget:
            win, lay, defaults = self.InputWidget[0:3]
            for element in defaults.keys():
                win[element].update(defaults[element])
            return win


    # --------- ELEMENT LAYOUTS used to gather search criteria inputs and their defaults ---------- #
    # --- If reset specified return dictionary of element defaults otherwise return the layout ---- #

    # Listbox input widget layout and defaults
    def qbMetaInput1(self, reset=None):
        tooltip = "Selection of multiple items is allowed here"
        if reset:    # Return element default value dictionary
            return {
                '-LBOX1-': [], 'Ok1-': ['disabled=True']
            }
        else:           # Return widget GUI layout list
            return [
            [sg.Listbox(self.LBox, select_mode=self.LBoxMode, key='-LBOX1-', enable_events=True,
                        size=(60, 6), tooltip=tooltip, pad=((10, 5), (15, 15)))],

            [sg.Text('Use the controls above to set a value and click', font=("Helvetica", 10),
                     size=(40, 1), pad=((5, 0), (0, 10))),
             sg.Button('Ok', font=("Helvetica", 10, "bold"), key='Ok1-', disabled=True, pad=((5, 0), (0, 15))),
             sg.Text('or', size=(2, 1), pad=((5, 5), (0, 10))),
             sg.Button('Cancel', font=("Helvetica", 10, "bold"), pad=((5, 10), (0, 15)))]
            ]


    # Text input widget layout and defaults
    def qbMetaInput2(self, reset=None):
        if reset:    # Return element default value dictionary
            return {
                '-TXT2-': ["''"],
                '-HAS2-': ['value=True'],
                'Ok2-': ['disabled=True']
            }
        else:           # Return widget GUI layout list
            return [
                [sg.Text('', size=(80, 1), font=("Helvetica", 4))],  # Empty row for vertical spacing
                [sg.InputText(key='-TXT2-', enable_events=True, size=(62, 1), pad=((5, 10), (0, 0)),
                              text_color="black", background_color="gold")],
                [sg.Radio('Contains', "TXT", key='-HAS2-', enable_events=True, default=True, pad=((32, 0), (7, 5))),
                 sg.Radio('Starts with', "TXT", key='-STR2-', enable_events=True, pad=((15, 0), (7, 5))),
                 sg.Radio('Ends with', "TXT", key='-END2-', enable_events=True, pad=((15, 0), (7, 5))),
                 sg.Radio('Equals', "TXT", key='-EQU2-', enable_events=True, pad=((15, 0), (7, 5)))],

                [sg.Text('Use the controls above to set a value and click', font=("Helvetica", 10),
                         size=(40, 1), pad=((5, 0), (0, 10))),
                 sg.Button('Ok', font=("Helvetica", 10, "bold"), key='Ok2-', disabled=True, pad=((5, 0), (0, 15))),
                 sg.Text('or', size=(2, 1), pad=((5, 5), (0, 10))),
                 sg.Button('Cancel', font=("Helvetica", 10, "bold"), pad=((5, 10), (0, 15)))]
            ]

    # TODO: ComboBox input widget layout and defaults
    def qbMetaInput3(self, reset=None):
        if reset:    # Return element default value dictionary
            return {
                'Ok3-': ['disabled=True']
            }
        else:           # Return widget GUI layout list
            return [
                [sg.Text('Use the controls above to set a value and click', font=("Helvetica", 10),
                         size=(40, 1), pad=((10, 5), (0, 10))),
                 sg.Button('Ok', font=("Helvetica", 10, "bold"), key='Ok3-', disabled=True, pad=((10, 10), (0, 15))),
                 sg.Text('or', size=(2, 1), pad=((5, 5), (0, 10))),
                 sg.Button('Cancel', font=("Helvetica", 10, "bold"), pad=((5, 20), (0, 15)))]
            ]


    # TODO: Radio Buttons input widget layout and defaults
    def qbMetaInput4(self, reset=None):
        if reset:    # Return element default value dictionary
            return {
                'Ok4-': ['disabled=True']
            }
        else: return [[ # Return widget GUI layout list
            [sg.Text('Use the controls above to set a value and click', font=("Helvetica", 10),
                     size=(40, 1), pad=((10, 5), (0, 10))),
             sg.Button('Ok', font=("Helvetica", 10, "bold"), key='Ok4-', disabled=True, pad=((10, 10), (0, 15))),
             sg.Text('or', size=(2, 1), pad=((5, 5), (0, 10))),
             sg.Button('Cancel', font=("Helvetica", 10, "bold"), pad=((5, 20), (0, 15)))]
            ]]


    # TODO: Checkbox input widget layout and defaults
    def qbMetaInput5(self, reset=None):
        if reset:    # Return element default value dictionary
            return {
                'Ok5-': ['disabled=True']
            }
        else: return [ # Return widget GUI layout list
            [sg.Text('Use the controls above to set a value and click', font=("Helvetica", 10),
                     size=(40, 1), pad=((10, 5), (0, 10))),
             sg.Button('Ok', font=("Helvetica", 10, "bold"), key='Ok5-', disabled=True, pad=((10, 10), (0, 15))),
             sg.Text('or', size=(2, 1), pad=((5, 5), (0, 10))),
             sg.Button('Cancel', font=("Helvetica", 10, "bold"), pad=((5, 20), (0, 15)))]
            ]


    # Date and optional time of day input widget layout and defaults
    def qbMetaInput6(self, reset=None):
        toolTip="Slide button to pick a time. Click or hold to" \
                "\nleft or right of button for fine adjustment."
        if reset:    # Return element default value dictionary
            return {
                '-DAT6-': ["''"],
                '-TMV6-': ['disabled=True', "''"],
                '-SLD6-': ['disabled=True', 'value=0'],
                '-MAX6-': ['disabled=True'],
                '-MIN6-': ['disabled=True'],
                '-EQU6-': ['disabled=True','default=True'],
                'Ok6-':   ['disabled=True']
            }
        else: return [  # Return widget GUI layout list
            [sg.Text('Slide to set a time or enter it below', font=("Helvetica", 9),
                     size=(27, 1), pad=((10, 10), (14, 7))),
             sg.Text('', key='-DAT6-', size=(18, 1), pad=((5, 25), (7, 5))),
             sg.Button('Calendar', font=("Helvetica", 10, "bold"))],
             
            [sg.Slider(key='-SLD6-', disabled=True, enable_events=True, size=(50, 15),
                       disable_number_display=True, orientation='h', range=(0, 86399),
                       tooltip=toolTip, default_value=0, pad=((10, 0), (0, 0)))],
                       
            [sg.InputText(key='-TMV6-', enable_events=True, font=("Helvetica", 10), size=(8, 1),
                          text_color="black", disabled=True, background_color="gold",
                          default_text="", pad=((10, 25), (0, 0))),            
             sg.Radio('Earlier than', "ERQ", key='-MAX6-', disabled=True, enable_events=True, pad=((10, 0), (7, 5))),
             sg.Radio('Later than', "ERQ", key='-MIN6-', disabled=True, enable_events=True, pad=((15, 0), (7, 5))),
             sg.Radio('Equal to', "ERQ", key='-EQU6-', disabled=True, enable_events=True, default=True, pad=((15, 0), (7, 5)))],

            [sg.Text('Use the controls above to set a value and click', font=("Helvetica", 10),
                     size=(40, 1), pad=((10, 5), (0, 10))),
             sg.Button('Ok', font=("Helvetica", 10, "bold"), key='Ok6-', disabled=True, pad=((5, 10), (0, 15))),
             sg.Text('or', size=(2, 1), pad=((5, 5), (0, 10))),
             sg.Button('Cancel', font=("Helvetica", 10, "bold"), pad=((5, 20), (0, 15)))]
            ]


    # Numeric input widget layout and defaults
    def qbMetaInput7(self, reset=None):
        tooltip = "Slide button to pick a time. Click or hold to\n" \
                  "left or right of button for fine adjustment."
        if reset:    # Return element default value dictionary
            return {
                '-NUM7-': ["'0'"],
                '-MIN7-': ['value=True'],
                '-SLD7-': ['range=(0, self.Max7)', 'default=0'],
                'Ok7-': ['disabled=True']
            }
        else: return [  # Return widget GUI layout list
            [sg.Text('', size=(80, 1), font=("Helvetica", 4))],  # Empty row for vertical spacing
            [sg.Radio('Less or =', "LME", key='-MAX7-',  enable_events=True, pad=((130, 0), (0, 0))),
             sg.Radio('More or =', "LME", key='-MIN7-',  enable_events=True, default=True, pad=((15, 0), (0, 0))),
             sg.Radio('Equal to', "LME", key='-EQU7-', enable_events=True, pad=((15, 0), (0, 0)))],
            [sg.InputText(key='-NUM7-', enable_events=True, size=(7, 1), pad=((10, 0), (10, 5)),
                          default_text='0', text_color="black", background_color="gold"),
             sg.Slider(key='-SLD7-', enable_events=True, size=(44, 15), orientation='h',
                       disable_number_display=True, pad=((12, 0), (5, 0)),
                       tooltip=tooltip, range=(0, self.Max7), default_value='')],

            [sg.Text('Use the controls above to set a value and click', font=("Helvetica", 10),
                     size=(40, 1), pad=((10, 5), (0, 10))),
             sg.Button('Ok', font=("Helvetica", 10, "bold"), key='Ok7-', disabled=True, pad=((10, 10), (0, 15))),
             sg.Text('or', size=(2, 1), pad=((5, 5), (0, 10))),
             sg.Button('Cancel', font=("Helvetica", 10, "bold"), pad=((8, 20), (0, 15)))]
            ]


    # Duration in seconds input widget  layout and defaults
    def qbMetaInput8(self, reset=None):
        tooltip = "Slide button to pick a time. Click or hold to\nleft or right of button for fine adjustment."
        if reset:    # Return element default value dictionary
            return {
                '-MIN8-': ['default=True'],
                '-TIM8-': ["'00:00:00'"],
                '-SEC8-': ['value="0"'],
                '-SLD8-': ['value=0', 'disabled=False', 'range=(0, 9000)'],
                'Ok8-': ['disabled=True']
            }
        else: return [  # Return widget GUI layout list
            [sg.Radio('Minimum', "MNX", key='-MIN8-', enable_events=True, default=True, pad=((180, 0), (15, 0))),
             sg.Radio('Maximum', "MNX", key='-MAX8-',enable_events=True, pad=((0, 0), (15, 0)))],
            [sg.Text('Seconds', font=("Helvetica", 10), pad=((10, 120), (5, 5))),
             sg.Text('Time (hh:mm:ss)=', font=("Helvetica", 10), pad=((0, 0), (17, 10))),
             sg.Text('00:00:00', key='-TIM8-', font=("Helvetica", 10), pad=((0, 0), (10, 5)), size=(8, 1))],

            [sg.InputText('', key='-SEC8-', enable_events=True, size=(7, 1),
                          text_color="black", background_color="gold", pad=((10, 0), (0, 10))),
             sg.Slider(key='-SLD8-', enable_events=True, disable_number_display=True, disabled=True, size=(44, 15),
                       orientation='h', tooltip=tooltip, range=(0, 9000), pad=((10, 0), (0, 10)), default_value=0)],

            [sg.Text('Use the controls above to set a value and click', font=("Helvetica", 10),
                     size=(40, 1), pad=((10, 5), (0, 10))),
             sg.Button('Ok', font=("Helvetica", 10, "bold"), key='Ok8-', disabled=True, pad=((10, 10), (0, 15))),
             sg.Text('or', size=(2, 1), pad=((5, 5), (0, 10))),
             sg.Button('Cancel', font=("Helvetica", 10, "bold"), pad=((5, 20), (0, 15)))
             ]
        ]

    # Text input widget for MULTI field keyword search - layout and defaults
    def qbMetaInput9(self, reset=None):
        if reset:    # Return element default value dictionary
            return {
                '-TXT9-': ["''"],
                '-HAS9-': ['value=True'],
                'Ok9-': ['disabled=True']
            }
        else:           # Return widget GUI layout list
            return [
                [sg.Text('', size=(80, 1), font=("Helvetica", 4))],  # Empty row for vertical spacing
                [sg.InputText(key='-TXT9-', enable_events=True, size=(62, 1), pad=((5, 10), (0, 0)),
                              text_color="black", background_color="gold")],
                [sg.Radio('Keyword list', "TXT", key='-HAS9-', enable_events=True, default=True, pad=((32, 0), (7, 5))),
                 sg.Radio('Phrase', "TXT", key='-ALL9-', enable_events=True, pad=((15, 0), (7, 5)))],

                [sg.Text('Use the controls above to set a value and click', font=("Helvetica", 10),
                         size=(40, 1), pad=((5, 0), (0, 10))),
                 sg.Button('Ok', font=("Helvetica", 10, "bold"), key='Ok9-', disabled=True, pad=((5, 0), (0, 15))),
                 sg.Text('or', size=(2, 1), pad=((5, 5), (0, 10))),
                 sg.Button('Cancel', font=("Helvetica", 10, "bold"), pad=((5, 10), (0, 15)))]
            ]

    # ------ Progress bar function & window definition ------ #
    # Set window == "open" to start, progress == -1 to close. 
    # Set seconds == -1 to hide the timer. 
    # Return value on open is window obj to pass back in to close
    # or update. Update every second, set progress 0 - 50 (2% incr)
    def progressWindow(self, window, x, y, progress, seconds, max):
        show = False
        if seconds >= 0:
            minutes, s = divmod(seconds, 60)
            h, m = divmod(minutes, 60)
            timer = "%02d:%02d:%02d" % (h, m, s)
            show = True
        if window == "open":
            return sg.Window("Progress", 
                             [[sg.Text(timer, key='-T-', size=(8,1), 
                                       font=("Helvetica", 10, 'bold'),
                                       visible=show),
                               sg.ProgressBar(None, size=(50, 10), key='-P-',
                                              style='classic',
                                              orientation='horizontal',
                                              relief=sg.RELIEF_SUNKEN,
                                              bar_color=("gold", "orange"))]],
                             location=(x, y), finalize=True)
        elif progress < 0:
            window.close()
        else:
            if show: window['-T-'].update(timer)
            window['-P-'].update(current_count=progress, max=max)


    # ------ Top menu bar definition ------ #
    def topMenuBar(self):
        return [['File',   ['Open Search Source', list(self.Ipfs.DBlist.keys()),
                            'Metadata Info...',
                            'Exit']
                ],
                ['Config', ['Settings',    ['Default Search Source', ["Use " + sub for sub in self.Ipfs.DBlist.keys()],
                                            'Criteria Renewal Interval...',
                                            'Maximum IPFS Wait Time...',
                                            'File Export Directory...',
                                            'Save Settings']
                            ]
                ],
                ['Help', ['Basic Operation...', 'About...']
                ]]

    # ------ Query builder - left column ------ #
    def queryBuilder(self):
        return [
            [sg.Frame('Search Criteria', [[  # Criteria Selection layouts
                sg.Listbox([], disabled=True, key='-META-', enable_events=True, size=(25, 15)),
                sg.Listbox([], key='-TODO-', background_color="black", size=(70, 15),
                           select_mode=self.LBoxMode, enable_events=True,
                           pad=((20,0), (0,0)))]],
                size=(100, 20))
            ]
        ]

    # Right column listbox is used for search results
    def queryResults(self, reset=None):
        if reset:    # Return element default value dictionary
            return {
                '-TIMR-': ['visible=False'], '-PROG-': ['visible=False']
            }
        else:        # Return widget GUI layout list
            return [
                [sg.Frame('Search Results', [
                [sg.Listbox('', key='-RESULTS-', background_color="black", size=(127, 25),
                            font=('Courier', 10, 'bold'), enable_events=True,
                            select_mode=sg.LISTBOX_SELECT_MODE_MULTIPLE,
                            right_click_menu=['unused', ['View', 'Pin']])
                 ],

                [sg.Button('Close', key='-CLOSE-', font=("Helvetica", 10, "bold"),
                          pad=((120, 0), (0, 0))),
                 sg.Button('Open', key='-OPEN-', disabled=True, font=("Helvetica", 10, "bold"),
                          pad=((125, 0), (0, 0))),
                 sg.Button('Pin Selected', key='-PIN-', disabled=True, font=("Helvetica", 10, "bold"),
                        pad=((15, 0), (0, 0))),
                 sg.Button('All / None', key='-ALL-', font=("Helvetica", 10, "bold"),
                        pad=((15, 0), (0, 0))),
                 sg.Button('TXT', key='-TXT-', disabled=True, font=("Helvetica", 10, "bold"),
                          pad=((15, 0), (0, 0))),
                 sg.Button('CSV', key='-CSV-', disabled=True, font=("Helvetica", 10, "bold"),
                          pad=((15, 0), (0, 0))),
                 sg.Button('VLC', key='-VLC-', disabled=True, font=("Helvetica", 10, "bold"),
                          pad=((15, 0), (0, 0))),
                 sg.Text('', key='-ROWS-', size=(10, 1), pad=((20, 0), (0, 0)), font=("Helvetica", 10))],

                [sg.ProgressBar(None, size=(94, 10), key='-PROG-', orientation='horizontal',
                                bar_color=("gold", "orange"), relief=sg.RELIEF_SUNKEN,
                                style='classic', border_width=3, visible=False)]
                ])
            ]
        ]

        # ----------- This is the main GUI window layout - popup windows ----------- #
    def pBoxSearchApp(self):
        return [
            [sg.Menu(pBoxGUI.topMenuBar(self), key='-MENU-', tearoff=False)],  # Top Menu bar
            [sg.Column(pBoxGUI.queryBuilder(self), visible=True)],

            [sg.Button('Search', key='-SEARCH-', disabled=True, font=("Helvetica", 10, "bold"),
                       pad=((90,0),(0,0))),

             sg.Button('Clear All', key='-CLEAR-', disabled=True, font=("Helvetica", 10, "bold"),
                       pad=((250,20),(0,0))),
             sg.Button('Delete Selected Criteria', key='-DEL-', disabled=True, 
                       font=("Helvetica", 10, "bold"),
                       pad=((20, 0), (0, 0))),
             ]
        ]

#!/usr/bin/python3
import PySimpleGUI as sg
import ipfs        # Only used here for top menu server list

# GUI layouts for PBox Search

class pBoxGUI:
    def __init__(self):
        self.Icon = r'/usr/share/Raspberrypi-artwork/pirateSkull230x300Black.png'
        self.Font = ("Helvetica", 8)
        self.Max7 = 1000000     # TODO - come up with a better way to handle widget defaults.
        self.LBox = []          # Each numeric field may require a different max value for example
        self.LBoxMode = sg.LISTBOX_SELECT_MODE_MULTIPLE
        self.ThemeMenuGroups = []
        self.AppWin = None      # These with hold the window objects returned by sg.Window
        self.ResultWin = None   # Result window - this could be an array or dictionary
        self.InputWidget = []   # Input widget window, layout, defaults disctionary

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


    # ----------- ELEMENT LAYOUTS used to gather search criteria inputs and their defaults ----------- #
    # --- If property specified return dictionary of element defaults otherwise return the layout ---- #

    # Listbox input widget layout and defaults
    def qbMetaInput1(self, property=None):
        tooltip = "Selection of multiple items is allowed here"
        if property:    # Return element default value dictionary
            return {
                '-LBOX1-': [], 'Ok1-': ['disabled=True']
            }
        else:           # Return widget GUI layout list
            return [
            [sg.Listbox(self.LBox, select_mode=self.LBoxMode, key='-LBOX1-', enable_events=True,
                        size=(60, 6), tooltip=tooltip, pad=((10, 5), (15, 15)))],

            [sg.Text('Use the controls above to set a value and click', size=(36, 1), pad=((20, 5), (0, 10))),
             sg.Button('Ok', font=("Helvetica", 8, "bold"), key='Ok1-', disabled=True, pad=((10, 10), (0, 15))),
             sg.Text('or', size=(2, 1), pad=((5, 5), (0, 10))),
             sg.Button('Cancel', font=("Helvetica", 8, "bold"), pad=((5, 20), (0, 15)))]
            ]


    # Text input widget layout and defaults
    def qbMetaInput2(self, property=None):
        if property:    # Return element default value dictionary
            return {
                '-TXT2-': ["''"],
                '-HAS2-': ['value=True'],
                'Ok2-': ['disabled=True']
            }
        else:           # Return widget GUI layout list
            return [
                [sg.Text('', size=(80, 1), font=("Helvetica", 4))],  # Empty row for vertical spacing
                [sg.InputText(key='-TXT2-', enable_events=True, size=(60, 1), pad=((5, 10), (0, 0)),
                              text_color="black", background_color="gold")],
                [sg.Radio('Contains', "TXT", key='-HAS2-', enable_events=True, default=True, pad=((40, 0), (7, 5))),
                 sg.Radio('Starts with', "TXT", key='-STR2-', enable_events=True, pad=((15, 0), (7, 5))),
                 sg.Radio('Ends with', "TXT", key='-END2-', enable_events=True, pad=((15, 0), (7, 5))),
                 sg.Radio('Equals', "TXT", key='-EQU2-', enable_events=True, pad=((15, 0), (7, 5)))],

                [sg.Text('Use the controls above to set a value and click', size=(36, 1), pad=((0, 5), (0, 10))),
                 sg.Button('Ok', font=("Helvetica", 8, "bold"), key='Ok2-', disabled=True, pad=((10, 10), (0, 15))),
                 sg.Text('or', size=(2, 1), pad=((5, 5), (0, 10))),
                 sg.Button('Cancel', font=("Helvetica", 8, "bold"), pad=((5, 20), (0, 15)))]
            ]

    # TODO: ComboBox input widget layout and defaults
    def qbMetaInput3(self, property=None):
        if property:    # Return element default value dictionary
            return {
                'Ok3-': ['disabled=True']
            }
        else:           # Return widget GUI layout list
            return [
                [sg.Text('Use the controls above to set a value and click', size=(36, 1), pad=((100, 5), (0, 10))),
                 sg.Button('Ok', font=("Helvetica", 8, "bold"), key='Ok3-', disabled=True, pad=((10, 10), (0, 15))),
                 sg.Text('or', size=(2, 1), pad=((5, 5), (0, 10))),
                 sg.Button('Cancel', font=("Helvetica", 8, "bold"), pad=((5, 20), (0, 15)))]
            ]


    # TODO: Radio Buttons input widget layout and defaults
    def qbMetaInput4(self, property=None):
        if property:    # Return element default value dictionary
            return {
                'Ok4-': ['disabled=True']
            }
        else: return [[ # Return widget GUI layout list
            [sg.Text('Use the controls above to set a value and click', size=(36, 1), pad=((100, 5), (0, 10))),
             sg.Button('Ok', font=("Helvetica", 8, "bold"), key='Ok4-', disabled=True, pad=((10, 10), (0, 15))),
             sg.Text('or', size=(2, 1), pad=((5, 5), (0, 10))),
             sg.Button('Cancel', font=("Helvetica", 8, "bold"), pad=((5, 20), (0, 15)))]
            ]]


    # TODO: Checkbox input widget layout and defaults
    def qbMetaInput5(self, property=None):
        if property:    # Return element default value dictionary
            return {
                'Ok5-': ['disabled=True']
            }
        else: return [ # Return widget GUI layout list
            [sg.Text('Use the controls above to set a value and click', size=(36, 1), pad=((100, 5), (0, 10))),
             sg.Button('Ok', font=("Helvetica", 8, "bold"), key='Ok5-', disabled=True, pad=((10, 10), (0, 15))),
             sg.Text('or', size=(2, 1), pad=((5, 5), (0, 10))),
             sg.Button('Cancel', font=("Helvetica", 8, "bold"), pad=((5, 20), (0, 15)))]
            ]


    # Date and optional time of day input widget layout and defaults
    def qbMetaInput6(self, property=None):
        toolTip="Slide button to pick a time. Click or hold to" \
                "\nleft or right of button for fine adjustment."
        if property:    # Return element default value dictionary
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
                     size=(26, 1), pad=((25, 10), (14, 7))),
             sg.Text('', key='-DAT6-', size=(18, 1), pad=((5, 5), (7, 5))),
             sg.Button('Calendar', font=("Helvetica", 8, "bold"))],
             
            [sg.Slider(key='-SLD6-', disabled=True, enable_events=True, size=(46, 15),
                       disable_number_display=True, orientation='h', range=(0, 86399),
                       tooltip=toolTip, default_value=0, pad=((25, 0), (0, 0)))],
                       
            [sg.InputText(key='-TMV6-', enable_events=True, font=("Helvetica", 8), size=(8, 1),
                          text_color="black", disabled=True, background_color="gold",
                          default_text="", pad=((25, 25), (0, 0))),            
             sg.Radio('Earlier than', "ERQ", key='-MAX6-', disabled=True, enable_events=True, pad=((10, 0), (7, 5))),
             sg.Radio('Later than', "ERQ", key='-MIN6-', disabled=True, enable_events=True, pad=((15, 0), (7, 5))),
             sg.Radio('Equal to', "ERQ", key='-EQU6-', disabled=True, enable_events=True, default=True, pad=((15, 0), (7, 5)))],

            [sg.Text('Use the controls above to set a value and click', size=(36, 1), font=("Helvetica", 9), pad=((25, 3), (0, 10))),
             sg.Button('Ok', font=("Helvetica", 8, "bold"), key='Ok6-', disabled=True, pad=((5, 10), (0, 15))),
             sg.Text('or', size=(2, 1), pad=((5, 5), (0, 10))),
             sg.Button('Cancel', font=("Helvetica", 8, "bold"), pad=((5, 20), (0, 15)))]
            ]


    # Numeric input widget layout and defaults
    def qbMetaInput7(self, property=None):
        tooltip = "Slide button to pick a time. Click or hold to\n" \
                  "left or right of button for fine adjustment."
        if property:    # Return element default value dictionary
            return {
                '-NUM7-': ["'0'"],
                '-MIN7-': ['value=True'],
                '-SLD7-': ['range=(0, self.Max7)', 'default=0'],
                'Ok7-': ['disabled=True']
            }
        else: return [  # Return widget GUI layout list
            [sg.Text('', size=(80, 1), font=("Helvetica", 4))],  # Empty row for vertical spacing
            [sg.Radio('Less or =', "LME", key='-MAX7-',  enable_events=True, pad=((100, 0), (0, 0))),
             sg.Radio('More or =', "LME", key='-MIN7-',  enable_events=True, default=True, pad=((15, 0), (0, 0))),
             sg.Radio('Equal to', "LME", key='-EQU7-', enable_events=True, pad=((15, 0), (0, 0)))],
            [sg.InputText(key='-NUM7-', enable_events=True, size=(7, 1), pad=((5, 0), (10, 5)),
                          default_text='0', text_color="black", background_color="gold"),
             sg.Slider(key='-SLD7-', enable_events=True, size=(40, 15), orientation='h',
                       disable_number_display=True, pad=((12, 0), (5, 0)),
                       tooltip=tooltip, range=(0, self.Max7), default_value='')],

            [sg.Text('Use the controls above to set a value and click', size=(36, 1), font=("Helvetica", 8), pad=((25, 5), (0, 10))),
             sg.Button('Ok', font=("Helvetica", 8, "bold"), key='Ok7-', disabled=True, pad=((10, 10), (0, 15))),
             sg.Text('or', size=(2, 1), pad=((5, 5), (0, 10))),
             sg.Button('Cancel', font=("Helvetica", 8, "bold"), pad=((5, 20), (0, 15)))]
            ]


    # Duration in seconds input widget  layout and defaults
    def qbMetaInput8(self, property=None):
        tooltip = "Slide button to pick a time. Click or hold to\nleft or right of button for fine adjustment."
        if property:    # Return element default value dictionary
            return {
                '-MIN8-': ['default=True'],
                '-TIM8-': ["'00:00:00'"],
                '-SEC8-': ['value="0"'],
                '-SLD8-': ['value=0', 'disabled=False', 'range=(0, 9000)'],
                'Ok8-': ['disabled=True']
            }
        else: return [  # Return widget GUI layout list
            [sg.Radio('Minimum', "MNX", key='-MIN8-', enable_events=True, default=True, pad=((220, 0), (15, 0))),
             sg.Radio('Maximum', "MNX", key='-MAX8-',enable_events=True, pad=((0, 0), (15, 0)))],
            [sg.Text('Seconds', font=("Helvetica", 8), pad=((0, 140), (5, 5))),
             sg.Text('Time (hh:mm:ss)=', font=("Helvetica", 8), pad=((0, 0), (17, 10))),
             sg.Text('00:00:00', key='-TIM8-', font=("Helvetica", 8), pad=((0, 0), (10, 5)), size=(8, 1))],

            [sg.InputText('', key='-SEC8-', enable_events=True, size=(7, 1),
                          text_color="black", background_color="gold", pad=((5, 0), (0, 10))),
             sg.Slider(key='-SLD8-', enable_events=True, disable_number_display=True, disabled=True, size=(48, 15),
                       orientation='h', tooltip=tooltip, range=(0, 9000), pad=((20, 0), (0, 10)), default_value=0)],

            [sg.Text('Use the controls above to set a value and click', size=(36, 1), pad=((20, 5), (0, 10))),
             sg.Button('Ok', font=("Helvetica", 8, "bold"), key='Ok8-', disabled=True, pad=((10, 10), (0, 15))),
             sg.Text('or', size=(2, 1), pad=((5, 5), (0, 10))),
             sg.Button('Cancel', font=("Helvetica", 8, "bold"), pad=((5, 20), (0, 15)))
             ]
        ]

    # ------ Top menu bar definition ------ #
    def topMenuBar(self):
        return [['File',   ['Save as',
                            'Pin', ['Pin File Local', 'Pin Search Results'],
                            'Open IPFS Address',
                            'Exit']],
                ['Config', ['IPFS Server', list(ipfs.Ipfs().DBlist.keys()),
                            'Settings',    ['Favorites', ['London Real','Truthstream Media', 'Crrow77 Radio',
                                                          '5G Summit','Clive DeCarle'],
                ]]],
                ['Help', 'About...']]

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
    def queryResults(self):
        return [
            [sg.Frame('Search Results', [
                [sg.Listbox('', key='-RESULTS-', background_color="black", size=(100, 25),
                           font=('Courier', 8, 'bold'), enable_events=True,
                            right_click_menu=['unu6sed', ['View', 'Pin']])
                 ],
                [sg.Button('Close', key='-CLOSE-', font=("Helvetica", 8, "bold"),
                          pad=((100, 0), (0, 0))),
                 sg.Button('Next', key='-NEXTP-', disabled=True, font=("Helvetica", 8, "bold"),
                          pad=((150, 0), (0, 0))),
                 sg.Button('Previous', key='-PREVP-', disabled=True, font=("Helvetica", 8, "bold"),
                          pad=((15, 0), (0, 0))),
                 sg.Text('Page 1', key='-PAGE-', font=("Helvetica", 8),
                        pad=((15, 30), (0, 0))),
                 sg.Text('', key='-ROWS-', size=(12, 1), font=("Helvetica", 8))]])
            ]
        ]

        # ----------- This is the main GUI window layout - popup windows ----------- #
    def pBoxSearchApp(self):
        return [
            [sg.Menu(pBoxGUI.topMenuBar(self), key='-MENU-', tearoff=True)],  # Top Menu bar
            [sg.Column(pBoxGUI.queryBuilder(self), visible=True)],

            [sg.Button('Search', key='-SEARCH-', disabled=True, font=("Helvetica", 8, "bold"),
                       pad=((40,0),(0,0))),
             sg.Button('Clear', key='-CLEAR-', disabled=True, font=("Helvetica", 8, "bold"),
                       pad=((15,100),(0,0))),

             sg.Button('Delete Selected Criteria', key='-DEL-', disabled=True, 
                       font=("Helvetica", 8, "bold"),
                       pad=((15, 0), (0, 0))),
             ]
        ]


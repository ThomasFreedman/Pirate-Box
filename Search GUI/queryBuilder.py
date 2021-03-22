#!/usr/bin/python3
import PySimpleGUI as sg
import guiLayouts as gl
import sqlDB
import ipfs
import os

# GUI layouts and Event Processing for PBox Search

class pBoxQuery:


    def __init__(self):
        self.Pwd = os.path.dirname(os.path.realpath(__file__)) + '/'
        self.Sql = sqlDB.sql()
        self.Gui = gl.pBoxGUI()
        self.Ipfs = ipfs.Ipfs()
        self.Day6 = ''          # Need to persist date and time b/c can't read value of text field
        self.Tmv6 = ''
        self.Display = []
        self.Where = []
        self.Grupes = []
        self.Ext = []
        self.ExKey = []
        self.Format = []

        # Metadata fields in SQLite DB available to use as search criteria.
        # Each field (column in SQLite) is categorized under an input state.
        # These names define those states for each field to select the right
        # widget to obtain user input for that field. TODO: implement code
        # for ComboBox, Radio and CheckBox input types.

        # These are the query builder states as the filter criteria is selected.
        self.Start     = 0      # Starting state where users select a field
        self.ListBox   = 1      # Select value(s) from a list (like Start state)
        self.TextBox   = 2      # any; if int > < =, starts with ends with contains, exact...
        self.ComboBox  = 3      # Choice from a list or can type in items not in list
        self.Radio     = 4      # Choose 1 of n
        self.CheckBox  = 5      # Choose any / all of n
        self.Calendar  = 6      # Date and optional time in SQLite3 format: 'YYYYMMDD HH:MM:SS'
        self.NumSlide  = 7      # Linear slider to select a numeric value or type one in
        self.Time      = 8      # Returns number of seconds. Displayed as HH:MM:SS

        #
        # CONSIDER LOADING THE FOLLOWING FROM A JSON CONFIG FILE
        #

        # This dictionary maps Search Criteria to DB metadata fields and thru that input states
        self.SearchCriteria = {
            "Item #": ["pky", self.NumSlide],
            "Title": ["title", self.TextBox],
            "Publisher": ["grupe", self.ListBox],
            "Publish Date": ["upload_date", self.Calendar],
            "Source": ["extractor_key", self.ListBox],
            "Description": ["description", self.TextBox],
            "Length": ["duration", self.NumSlide],
            "Views": ["view_count", self.NumSlide],
            "Likes": ["like_count", self.NumSlide],
            "Dislikes": ["dislike_count", self.NumSlide],
            "Avg. Rating": ["average_rating", self.NumSlide],
            "ID": ["id", self.ListBox],
            "Type": ["format_note", self.ListBox],
            "Size": ["vsize", self.NumSlide],
            "Width": ["width", self.NumSlide],
            "Height": ["height", self.NumSlide],
            "Format": ["ext", self.ListBox],
            "IPFS CID":  ["vhash", self.TextBox],
            "IPFS Date": ["sqlts", self.Calendar],
            "IPFS File": ["_filename", self.TextBox]
        }

    # Open the chosen SQLite database file, initialize lists and display popup of DB stats
    def serverOpen(self, server, x ,y):
        self.Sql.openDatabase(server)        

        # Get selections for multi-select items (radio buttons, checkboxes, listboxes & comboboxes
        grpSql = "select distinct grupe from IPFS_HASH_INDEX;"
        self.Grupes = self.Sql.getListFromSql(grpSql)
        extSql = "select distinct ext from IPFS_HASH_INDEX where ext not like '%unknown%';"
        self.Ext = self.Sql.getListFromSql(extSql)
        exKSql = "select distinct extractor_key from IPFS_HASH_INDEX where extractor_key not like '%unknown%';"
        self.ExKey = self.Sql.getListFromSql(exKSql)
        fmtSql = "select distinct format_note from IPFS_HASH_INDEX where format_note not like '%unknown%';"
        self.Format = self.Sql.getListFromSql(fmtSql)

        # Not sure of best way to present multiselect elements whose selections come from the DB
        self.LBox = self.SearchCriteria

        count = self.Sql.runQuery("SELECT COUNT(*) FROM IPFS_HASH_INDEX;")[0][0]

        # Show some stats about the DB in a popup
        sg.popup(f"{count} items on the {server} node",
                 f"in {len(self.Grupes)} groups and ",
                 f"with {len(self.Ext)} media types from",
                 f"{len(self.ExKey)} sources",
                 location=((x+450, y+75)), font=("Helvetica", 11, "bold"),
                 modal=True, keep_on_top=True)

        self.Gui.AppWin['-META-'].update(values=list(self.SearchCriteria.keys()), disabled=False)

    def resetAll(self, ):
        state = pBoxQuery.resetToState0(self)
        self.Where = []                                     # Clear search criteria list
        self.Gui.AppWin['-META-'].update(values=[])         # Clear metadata select list
        self.Gui.AppWin['-META-'].update(disabled=True)     # Disable it too
        if self.Gui.ResultWin: self.Gui.ResultWin.close()
        self.Gui.AppWin['-TODO-'].update(values=[])         # Clear search criteria list
        self.Gui.AppWin['-SEARCH-'].update(disabled=True)   # Disable buttons
        self.Gui.AppWin['-CLEAR-'].update(disabled=True)

        #self.Gui.AppWin['-ROWS-'].update('')                # Clear # rows under results
        #self.Gui.AppWin['-RESULTS-'].update(values=[])
        return state

    # Clear search results, close input windows and return to state 0 to select other criteria
    def resetToState0(self):
        self.Gui.AppWin['-META-'].Widget.selection_clear(0, len(self.SearchCriteria)) # Remove selection
        self.Gui.AppWin['-META-'].update(scroll_to_index=0)                       # Scroll to top
        if len(self.Gui.InputWidget) > 0: 
            self.Gui.resetWidget().close()                                        # Close input window
            self.Gui.InputWidget = []
        if self.Gui.ResultWin: self.Gui.ResultWin.close()                         # Close this too?
        return 0

    # Run the search query using the criteria in the Where list. Title must be last in select list.
    # The x and y parameters are where the result window is opened on the desktop.
    def doSearch(self, x, y):
        result = []
        query = "SELECT pky, upload_date, ext, CAST(vsize as FLOAT) / 1000000000 as size, "
        query +=        "CAST(duration as int) as dur, title from IPFS_HASH_INDEX WHERE "
        if len(self.Where) == 0:
            query += " 1=1 limit 50"
        else:
            for clause in self.Where:
                query += clause
        rows = self.Sql.runQuery(query)
        items = len(rows)
        if len(rows) > 0:
            result = ['  KEY UPLOAD DATE  TYPE    SIZE  DURATION  TITLE']
            for r in rows:
                # Strip unicode characters Tcl doesn't like and handle nulls
                cols = list(range(len(r)))
                for col in range(0, len(r)):  # for each column in the row
                    if r[col] is not None:
                        vLst = str(r[col])
                        vLst = [vLst[i] for i in range(len(vLst)) if ord(vLst[i]) in range(65536)]
                        cols[col] = ''
                        for char in vLst: cols[col] += char
                        if cols[col].startswith('unknown'): cols[col] = '?'
                    else: cols[col] = '?'  # Replace nulls (None values)

                # Add hyphens to make date easier to read
                if len(cols[1]) > 1: d = f"{cols[1][0:4]}-{cols[1][4:6]}-{cols[1][6:8]}"  # YYYY-MM-DD format
                else: d = '?'

                # Truncate sizes less than 10MB
                if len(cols[3]) > 1: s = "%5s" % str(cols[3])[0:4]
                else: s = '?'

                result.append("%5s %11s %5s  %5sg  %5ssec  %s" %
                              (cols[0], d, cols[2], s, cols[4], cols[5]))

        else: result.append("No results found based on your search criteria")
        self.Gui.ResultWin = sg.Window('Search Results', self.Gui.queryResults(),
                                        location=(x, y), modal=True, force_toplevel=True,
                                       keep_on_top=False, disable_close=True, finalize=True)
        self.Gui.ResultWin['-ROWS-'].update(f"{items} items")
        self.Gui.ResultWin['-RESULTS-'].update(values=result)

    # Process input collected from user and create SQL where clause for it
    # TODO: create a display list to correlate with DB where clause
    def addSQL2SearchCriteriaList(self, state, criteria, input):
        self.Gui.AppWin['-SEARCH-'].update(disabled=False)
        self.Gui.AppWin['-CLEAR-'].update(disabled=False)

        if len(self.Where) > 0: clause = ' and '
        else: clause = ''
        show = clause

        # Process selections from a list
        field = self.SearchCriteria[criteria][0]   # Translate display criteria into DB field
        if state == self.ListBox:
            choices = len(input['list'])
            if choices > 0:
                c = 0
                clause += f"{field} in ("
                show += f"{criteria} is "
                for choice in input['list']:
                    clause += f"'{choice}'"
                    show += choice
                    c += 1
                    if c < choices:
                        clause += ','
                        show += ' or '
                clause += ')'
                self.Display.append(show)
                self.Where.append(clause)
                self.Gui.AppWin['-TODO-'].update(values=self.Display)

        # Process text input
        elif state == self.TextBox:
            if input['equ']: val = f"{field} = {input['text']}"
            elif input['has']: val = f"{field} like '%" + input['text'] + "%'"
            elif input['str']: val = f"{field} like '" + input['text'] + "%'"
            elif input['end']: val = f"{field} like '%" + input['text'] + "'"
            clause += val
            self.Where.append(clause)
            self.Gui.AppWin['-TODO-'].update(values=self.Where)
        elif state == self.ComboBox:
            pass
        elif state == self.Radio:
            pass
        elif state == self.CheckBox:
            pass

        # Process Date and optional time input
        elif state == self.Calendar:
            if input['max']: mnx = '<='
            elif input['min']: mnx = '>='
            else: mnx = '='
            dateTime = input['datetm']
            clause += f"julianday({field}) {mnx} julianday('{dateTime}')"
            self.Where.append(clause)
            self.Gui.AppWin['-TODO-'].update(values=self.Where)

        # Process numeric input
        elif state == self.NumSlide:
            if input['max']: mnx = '<='
            elif input['min']: mnx = '>='
            else: mnx = '='
            clause += f"CAST({field} as int) {mnx} {input['number']}"
            self.Where.append(clause)
            self.Gui.AppWin['-TODO-'].update(values=self.Where)

        # Process time input
        elif state == self.Time:
            if input['min']: mnx = '>='
            else: mnx = '<='
            clause += f"CAST({field} as int) {mnx} {input['seconds']}"
            self.Where.append(clause)
            self.Gui.AppWin['-TODO-'].update(values=self.Where)


    # ----------- Widget EVENT PROCESSING methods ----------- #
    # These methods process events generated from the gui layouts.
    def handleState1(self, event, values):
        if event == '-LBOX1-':
            self.Gui.InputWidget[0]['Ok1-'].update(disabled=False)
            if values and len(values) > 0:
                return {'list': values['-LBOX1-']}

    def handleState2(self, event, values):
        txtInput = None
        if event in ('-TXT2-','-HAS2-','-STR2-','-END2-','-EQU2-'):
            if event in ('-TXT2-'):
                txtInput = str(values['-TXT2-'])
                self.Gui.InputWidget[0]['-HAS2-'].update(disabled=False)
                self.Gui.InputWidget[0]['-STR2-'].update(disabled=False)
                self.Gui.InputWidget[0]['-END2-'].update(disabled=False)
                self.Gui.InputWidget[0]['Ok2-'].update(disabled=False)
            if txtInput is not None and len(txtInput) > 0:
                self.Txt2 = txtInput
                return {'text': self.Txt2, 'has': values['-HAS2-'], 'str': values['-STR2-'],
                        'end': values['-END2-'], 'equ': values['-EQU2-']}

    def handleState3(self, event, values):
        pass

    def handleState4(self, event, values):
        pass

    def handleState5(self, event, values):
        pass

    def handleState6(self, event, values):
        if event in ('Calendar','-SLD6-','-TMV6-','-MIN6-','-MAX6-','-EQU6-'):
            if event == 'Calendar':
                self.Gui.InputWidget[0]['-DAT6-'].update("")
                self.Gui.InputWidget[0]['-SLD6-'].update(disabled=True)
                d = sg.popup_get_date(no_titlebar=False)
                if d is not None:
                    date = "%d-%02d-%02d " % (d[2], d[0], d[1])
                    self.Day6 = date  # These 2 values need to be persistent
                    self.Tmv6 = ''    # Reset time when a new date is selected
                    self.Gui.InputWidget[0]['-TMV6-'].update(self.Tmv6, disabled=False)
                    self.Gui.InputWidget[0]['-TMV6-'].update(disabled=False)
                    self.Gui.InputWidget[0]['Ok6-'].update(disabled=False)
                    self.Gui.InputWidget[0]['-SLD6-'].update(disabled=False)
                    self.Gui.InputWidget[0]['-MAX6-'].update(disabled=False)
                    self.Gui.InputWidget[0]['-MIN6-'].update(disabled=False)
                    self.Gui.InputWidget[0]['-EQU6-'].update(disabled=False)

            if event == '-SLD6-':
                slider = int(values['-SLD6-'])
                if slider > 0:
                    minutes, s = divmod(slider, 60)
                    h, m = divmod(minutes, 60)
                    self.Tmv6 = "%02d:%02d:%02d" % (h, m, s)
                else:
                    self.Tmv6 = ""
                self.Gui.InputWidget[0]['-TMV6-'].update(self.Tmv6)
            elif event == '-TMV6-':
                t = values['-TMV6-'].split(':')
                if len(t) == 3 and t[0].isdecimal() and \
                        t[1].isdecimal() and t[2].isdecimal():
                    h = int(t[0]) % 24
                    m = int(t[1]) % 60
                    s = int(t[2]) % 60
                    self.Tmv6 = "%02d:%02d:%02d" % (h, m, s)
                else:  self.Tmv6 = ""

            if len(self.Day6) > 0:
                date = "%s %s" % (self.Day6, self.Tmv6)
                self.Gui.InputWidget[0]['-DAT6-'].update(date)
                return {'datetm': date.rstrip(), 'min': values['-MIN6-'],
                        'max': values['-MAX6-'], 'equ': values['-EQU6-']}

    # Get a numeric value. If a number is entered into the input box,
    # update the slider with that value. Max value allowed is set in self.Max7
    def handleState7(self, event, values):
        if event in ('-SLD7-', '-NUM7-','-MIN7-','-MAX7-','-EQU7-'):
            numInput = 0
            if event == '-SLD7-':
                numInput = int(values['-SLD7-'])
                self.Gui.InputWidget[0]['-NUM7-'].update(numInput)
            elif event == '-NUM7-':
                numInput = str(values['-NUM7-'])[0:7]
                if numInput.isdecimal():
                    numInput = int(numInput)
                    self.Gui.InputWidget[0]['-SLD7-'].update(numInput)
                else:
                    numInput = 0
                    self.Gui.InputWidget[0]['-NUM7-'].update(numInput)

            self.Gui.InputWidget[0]['-NUM7-'].update(numInput)
            self.Gui.InputWidget[0]['Ok7-'].update(disabled=False)
            return {'number': numInput, 'min': values['-MIN7-'], 'max': values['-MAX7-'], 'equ': values['-EQU7-']}

    # Update the text element with time as hrs, mins, secs string,
    # and slider input to value in seconds. If a number is entered
    # into the input box, update the slider with that value.
    def handleState8(self, event, values):
        if event in ('-SLD8-', '-SEC8-', '-MIN8-', '-MAX8-'):
            self.Gui.InputWidget[0]['-SLD8-'].update(disabled=False)
            secInput = None
            if event == '-SLD8-':
                secInput = int(values['-SLD8-'])
                self.Gui.InputWidget[0]['-SEC8-'].update(secInput)          # Update text input to match
            elif event == '-SEC8-':
                secInput = str(values['-SEC8-'])[0:5]
                if secInput.isdecimal():
                    secInput = int(secInput)
                    self.Gui.InputWidget[0]['-SLD8-'].update(secInput)      # Update slider imput to match
                else:
                    secInput = 0
                    self.Gui.InputWidget[0]['-SEC8-'].update(secInput)

            # Update the time text element based on slider or text input
            if secInput is not None:
                minutes, s = divmod(secInput, 60)
                h, m = divmod(minutes, 60)
                self.Gui.InputWidget[0]['-TIM8-'].update("%02d:%02d:%02d" % (h, m, s))
                self.Gui.InputWidget[0]['Ok8-'].update(disabled=False)
                return {'seconds': secInput, 'min': values['-MIN8-'], 'max': values['-MAX8-']}


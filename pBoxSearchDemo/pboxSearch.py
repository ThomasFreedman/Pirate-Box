#!/usr/bin/python3
import PySimpleGUI  as sg   # Simple GUI
import queryBuilder as qb   # Query Builder
import subprocess   as sp
import sys
import os

def initialize():
    pbq = qb.pBoxQuery()    # Creates all object classes
    gui = pbq.Gui           # This is reference to pBoxGUI class

    gui.AppWin = sg.Window('Pirate Box - IPFS Search / Viewer DEMO', gui.pBoxSearchApp(),
                           location=(200, 200), finalize=True)   # Set ref main win

    state = pbq.resetAll()  # Initialize to state 0
    cfg = sys.argv[0].replace(".py", ".json")
    pbq.restoreSettings(cfg)
    return [cfg, pbq, gui, gui.AppWin, state]


def main():
    cfgFile, pbq, gui, window, state = initialize()
    idx = None
    deList = []    # List of search conditions selected
    while True:
        if state == 0:
            idx = 0
            field = ''
            input = None

        # MAIN WINDOW EVENT LOOP
        values = None
        event = '_SKIP_'
        while event == '_SKIP_':
            win, event, values = sg.read_all_windows(timeout=20, timeout_key="_SKIP_")
            if win == gui.ResultWin and event == '-CLOSE-':
                state = pbq.resetToState0()             # Return to state 0
                event = '_SKIP_'

        if event in (None, 'Exit'):                     # Exit this application
            break

        locX, locY = window.current_location()

        # Ignore metadata listbox selections unless in state 0
        if event == '-META-' and state != 0 and idx is not None:
            window['-META-'].update(set_to_index=idx, scroll_to_index=idx)

        # Handle top menu bar events
        if event in gui.TopMenuList:
            if event == 'Basic Operation...':
                with open("basics.txt", 'r') as txt:
                    basics = "".join(txt.readlines())
                sg.popup_scrolled(basics, size=(60, 24),
                                  # image=gui.Icon,
                                  location=(locX + 300, locY - 100),
                                  modal=True, keep_on_top=True)

            if event == 'About...':
                with open("about.txt", 'r') as txt:
                    about = "".join(txt.readlines())
                sg.popup_scrolled(about, size=(60, 24),
                                  image=gui.Icon,
                                  location=(locX + 300, locY -100),
                                  modal=True, keep_on_top=True)

            # Show some stats about the DB in a popup
            elif event == 'Database Info...':
                if pbq.Sql.Sever is not None:
                    count = pbq.Sql.runQuery("SELECT COUNT(*) FROM IPFS_HASH_INDEX;")[0][0]
                    sg.popup(f"{count} items on the {pbq.Sql.Sever} server",
                             f"in {len(pbq.Grupes)} publishers and ",
                             f"with {len(pbq.Ext)} media types from",
                             f"{len(pbq.ExKey)} sources",
                             location=((locX + 450, locY + 75)),
                             font=("Helvetica", 11, "bold"),
                             modal=True, keep_on_top=True)

            elif event == "Criteria Renewal Interval":
                msg = "Enter metadata lifetime (# of hours):"
                cacheLife = sg.popup_get_text(msg, msg, pbq.Ipfs.DBcacheTime,
                                    no_titlebar=True,
                                    size=(20,3),
                                    location=(locX + 420, locY + 120),
                                    background_color="#3E3030",
                                    grab_anywhere=True)

                if cacheLife and cacheLife.isdecimal():
                    pbq.Ipfs.DBcacheTime = int(cacheLife)

            elif event == "File Save Directory":
                msg = "Enter the folder to save search results:"
                sg.popup_get_folder(msg, msg, pbq.SaveFolder,
                                    no_titlebar=True,
                                    size=(20, 3),
                                    location=(locX + 420, locY + 120),
                                    background_color="#3E3030",
                                    grab_anywhere=True)

            # Select a different server
            elif event in pbq.Ipfs.DBlist.keys():
                server = event
                pbq.serverOpen(server, locX, locY)

            # Select the server to use on startup (default server)
            elif event in ["Use " + sub for sub in pbq.Ipfs.DBlist.keys()]:
                svr = event.lstrip("Use ")
                pbq.Settings['server'] = svr

            # Save settings now (also saved on exit)
            elif event == "Save Settings":              # Save current settings
                pbq.saveSettings(cfgFile)

        # Metadata field selected
        if event == '-META-' and state == 0:            # Starting state - select a metadata field
            idx = window['-META-'].GetIndexes()[0]      # Get index of selected listbox item
            field = values['-META-'][0]                 # Only 1 selection at a time is possible
            dbCol, state = pbq.SearchCriteria[field]    # Database column and widget / state

            widget = getattr(gui, f"qbMetaInput{state}")  # GUI widget method
            layout = widget()
            defaults = widget('defaults')
            modal = sg.Window(f'Enter your search criteria for {field}', layout,
                              modal=True, location=(locX + 285, locY + 60),
                              force_toplevel=True, keep_on_top=True, disable_close=True,
                              finalize=True)
            gui.InputWidget = [modal, layout, defaults]

            # Load the multiple choice selection data into the appropriate elements
            # TODO: for now these are all HARD-coded as listboxes
            if field == "Publisher": modal['-LBOX1-'].update(pbq.Grupes)
            if field == "Format": modal['-LBOX1-'].update(pbq.Ext)
            if field == "Source": modal['-LBOX1-'].update(pbq.ExKey)
            if field == "Type": modal['-LBOX1-'].update(pbq.Format)

            # Create a window to obtain user input based on metadata field
            input = None
            while True:                                 # Modal widget event loop
                evnt, valz = modal.read()               # Wait for user input
                handler = getattr(pbq, f"handleState{state}")
                inp = handler(evnt, valz)               # Get results from input handler
                if inp: input = inp                     # Save widget output if any

                if evnt in (None, 'Exit'):              # Exit the modal
                    modal.close()
                    break

                elif evnt.startswith('Cancel'):         # Ignore this field and return to state 0
                    break

                elif evnt.startswith('Ok'):             # Accept the user input and add to list
                    if input is not None:               # Should never be None with this event
                        pbq.addSQL2SearchCriteriaList(field, input)
                    break

            if len(gui.InputWidget) > 0:
                state = pbq.resetToState0()             # Return to state 0

        # Process other events

        # Manage Result window button logic when items are selected or deselected
        # The column heading row needs to be ignored for Open and Pin actions.
        # For Open only 1 item can be selected, all other actions any numbr is OK
        #
        elif event == '-RESULTS-':
            noExport = True # Default state is all buttons disabled
            noOpen = True
            noPin = True
            selected = len(gui.ResultWin[event].get_indexes())
            if selected == 1: # Don't allow export of 1 item
                if gui.ResultWin[event].get_indexes()[0] != 0:
                    noOpen = False
                    noPin = False
            elif selected > 1: # User selected multiple items in result window
                noExport = False
                noPin = False # We'll ignore header row if selected

            gui.ResultWin['-OPEN-'].update(disabled=noOpen)
            gui.ResultWin['-PIN-'].update(disabled=noPin)
            gui.ResultWin['-TXT-'].update(disabled=noExport)
            gui.ResultWin['-CSV-'].update(disabled=noExport)
            gui.ResultWin['-JSON-'].update(disabled=noExport)

        # One of the save buttons was clicked - save selected results to a file
        elif event in ['-TXT-', '-CSV-', '-JSON-']:
            type = event.lower().strip('-')
            tkType = {'txt': ("Text", "*.txt"),
                      'csv': ("Comma Separted Values", "*.csv"),
                      'json': ("JSON format", "*.json")}
            file = sg.popup_get_file(f"Save results as a {type} file", save_as=True,
                                     file_types=[tkType[type]],
                                     default_extension=type,
                                     default_path=pbq.SaveFolder)
            pbq.SaveFolder = os.path.basename(file)  # Remember the folder for next time
            pbq.saveResults(file, type)

        # Open button clicked - launch Chromium web browser with hash (CID) to open
        elif event == '-OPEN-':  # User clicked on open button in result window
            fields = values['-RESULTS-'][0].split()
            if fields[0].isdecimal():
                hash = pbq.Sql.getHash(fields[0])
                sp.Popen(["/usr/bin/chromium-browser",
                         f"http://127.0.0.1:8080/ipfs/{hash}"],
                         stdout=sp.DEVNULL, stderr=sp.DEVNULL)
                gui.ResultWin.send_to_back()

        # Pin selected button clicked - pin item(s) from results on local IPFS node
        elif event == '-PIN-':
            pbq.pinSelected(locX, locY)  # Show progress as each item is pinned

        # Toggle selected button clicked - none selected: select all; any: select none
        elif event == '-ALL-':
            rows = list(range(0, len(gui.ResultWin['-RESULTS-'].get_list_values())))
            if len(gui.ResultWin['-RESULTS-'].get_indexes()) > 0:
                lst = []
                exp = pin = True  # Disable pin & export buttons
            else:
                lst = rows
                exp = pin = False # Enable pin & export buttons
            gui.ResultWin['-RESULTS-'].update(set_to_index=lst)
            gui.ResultWin['-OPEN-'].update(disabled=True)  # Always disable open
            gui.ResultWin['-PIN-'].update(disabled=pin)
            gui.ResultWin['-TXT-'].update(disabled=exp)
            gui.ResultWin['-CSV-'].update(disabled=exp)
            gui.ResultWin['-JSON-'].update(disabled=exp)

        # User selected one or more from criteria list
        elif event == '-TODO-' and len(values) > 0:
            deList = list(window['-TODO-'].get_indexes())
            if len(deList) > 0: disabled = False
            else: disabled = True
            window['-DEL-'].update(disabled=False)

        # Remove selected criteria, mindful of first item which is a special case
        # BUG FIXED: s = w = [] equate to same array, not 2 empty arrays
        elif event == '-DEL-':
            s = []
            w = []                                            # w = s probably no good either
            if len(pbq.Where['Clause']) > 1:                  # More than 1 criteria exists now
                if deList[0] == 0:                            # Delete first item?
                    s = ['1=1']
                    w = ['1=1']                               # First item is a special case
                else:
                    w = [ pbq.Where['Clause'][0] ]            # Keep first item
                    s = [ pbq.Where['Show'][0] ]
                for i in range(1, len(pbq.Where['Clause'])):  # Build a new list of keepers
                    if i not in deList:
                        w.append(pbq.Where['Clause'][i])
                        s.append(pbq.Where['Show'][i])
            if len(w) == 0 or len(w) == 1 and w[0] == '1=1':  # If there are none...
                pbq.Where['Clause'] = []
                pbq.Where['Show'] = []
                window['-DEL-'].update(disabled=True)
            else:
                pbq.Where['Clause'] = w
                pbq.Where['Show'] = s

            deList = []  # None of the selected should now remain
            window['-TODO-'].update(values=pbq.Where['Show'])    # Replace old list with new

        # Run the search query to get results
        elif event == '-SEARCH-' and len(pbq.Where['Clause']) > 0:
            pbq.doSearch(locX + 200, locY)

        # Reset to start a new search with current database
        if event == '-CLEAR-':
            state = pbq.resetToState0()
            pbq.Where['Clause'] = []
            window['-TODO-'].update(values=[])
            if gui.ResultWin: gui.ResultWin.close()

    window.close()
    pbq.saveSettings(cfgFile)

###############################################################################
# main is only called if this file is a script not an object class definition.#
# If this code is useful as a class it will be easy to make it one.           #
###############################################################################
if __name__ == "__main__":
    main()

exit(0)

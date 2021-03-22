#!/usr/bin/python3
import PySimpleGUI  as sg   # Simple GUI
import queryBuilder as qb   # Query Builder
import subprocess   as sp
import time

def initialize():
    pbq = qb.pBoxQuery()    # Creates all object classes
    gui = pbq.Gui           # This is reference to pBoxGUI class
    gui.AppWin = sg.Window('Pirate Box - IPFS Search / Viewer DEMO', gui.pBoxSearchApp(),
                           location=(200, 200), finalize=True)   # Set ref main win
    state = pbq.resetAll()  # Initialize to state 0
    return [pbq, gui.AppWin, state]


def main():
    pbq, gui, state = initialize()
    idx = None
    where = []
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
            if win == pbq.Gui.ResultWin and event == '-CLOSE-':
                state = pbq.resetToState0()             # Return to state 0
                event = '_SKIP_'

        if event in (None, 'Exit'):                     # Exit this application
            break

        locX, locY = pbq.Gui.AppWin.current_location()

        # Ignore metadata listbox selections unless in state 0
        if event == '-META-' and state != 0 and idx is not None:
            gui['-META-'].update(set_to_index=idx, scroll_to_index=idx)

        # Handle top menu bar events
        if values and '-MENU-' in values:
            if event == 'About...':
                sg.popup("     pBoxSearch v0.0.2 3/2021",
                         image=pbq.Gui.Icon,
                         location=(locX + 450, locY + 125),
                         custom_text='   Thomas Freedman    ',
                         modal=True, keep_on_top=True)
            elif event in ('Texas', 'New York'):
                pbq.serverOpen(event, locX, locY)

        # Metadata field selected
        if event == '-META-' and state == 0:            # Starting state - select a metadata field
            idx = gui['-META-'].GetIndexes()[0]         # Get index of selected listbox item
            field = values['-META-'][0]                 # Only 1 selection at a time is possible
            dbCol, state = pbq.SearchCriteria[field]    # Database column and widget / state

            widget = getattr(pbq.Gui, f"qbMetaInput{state}")  # GUI widget method
            layout = widget()
            defaults = widget('defaults')
            modal = sg.Window(f'Enter your search criteria for {field}', layout,
                              modal=True, location=(locX + 285, locY + 60),
                              force_toplevel=True, keep_on_top=True, disable_close=True,
                              finalize=True)
            pbq.Gui.InputWidget = [modal, layout, defaults]

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

                if evnt in (None, 'Exit'):              # Exit this modal
                    modal.close()
                    break

                elif evnt.startswith('Cancel'):         # Ignore this field and return to state 0
                    break

                elif evnt.startswith('Ok'):             # Accept the user input and add to list
                    if input is not None:               # Should never be None with Ok event
                        pbq.addSQL2SearchCriteriaList(state, field, input)
                    break

            if len(pbq.Gui.InputWidget) > 0:
                state = pbq.resetToState0()             # Return to state 0

        # Process other events

        # BUG - keep_on_top only keeps this popup on top of AppWin, not on top of resultWin
        # Launch Chromium web browser with hash (CID) from item user click in results.
        elif event == '-RESULTS-':                      # User clicked in result window
            fields = values[event][0].strip().split()
            if fields[0].isdecimal():
                hash = pbq.Sql.getHash(fields[0])
                sp.Popen(["/usr/bin/chromium-browser",
                         f"http://localhost:8080/ipfs/{hash}"], 
                         stdout=sp.DEVNULL, stderr=sp.DEVNULL)
                pbq.Gui.ResultWin.send_to_back()

        # User selected one or more from criteria list
        elif event == '-TODO-' and len(values) > 0:
            where = list(gui['-TODO-'].get_indexes())
            if len(where) > 0: disabled = False
            else: disabled = True
            gui['-DEL-'].update(disabled=disabled)

        # Remove selected criteria, mindful of first item which is a special case
        elif event == '-DEL-':
            w = []
            if len(pbq.Where) >  1:                 # More than 1 criteria exists now
                if where[0] == 0: w = ['1=1']       # First item is a special case
                else: w = [ pbq.Where[0] ]          # Keep first item
                for i in range(1, len(pbq.Where)):
                    if i not in where:
                        w.append(pbq.Where[i])      # Build another list of keepers
            if len(w) == 0 or len(w) == 1 and w[0] == '1=1':  # If there are none...
                pbq.Where = where = []
                gui['-DEL-'].update(disabled=True)
            else: pbq.Where = w
            gui['-TODO-'].update(values=pbq.Where)  # Replace old list with new

        # Run the search query to get results
        elif event == '-SEARCH-' and len(pbq.Where) > 0:
            pbq.doSearch(locX + 200, locY)

        # Reset to start a new search with current database
        if event == '-CLEAR-':
            state = pbq.resetToState0()
            pbq.Where = []
            gui['-TODO-'].update(values=[])
            if pbq.Gui.ResultWin: pbq.Gui.ResultWin.close()

    gui.close()

###############################################################################
# main is only called if this file is a script not an object class definition.#
# If this code is useful as a class it will be easy to make it one.           #
###############################################################################
if __name__ == "__main__":
    main()

exit(0)

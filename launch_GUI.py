from core_tools.gui.live_plotter_GUI_class import LivePlotter
from core_tools.MKSPDR2000_pressure.save_pressure_readings_functions import create_pressure_log_csv
from core_tools.flowrate.save_gas_flow_readings_functions import create_flow_log_csv

'''Launches run control GUI for the 40L system as specified by the user in this file.'''
#Create the CSV files for logging data BEFORE adding the relevant plot to the GUI window because the plotter will look for the file when it is created. Use the create_X_log_csv functions to create the files.
#Do NOT use any filenames with whitespaces in them, as this will cause issues with the terminal command buttons.
#The widgets (plots, buttons, etc.) are added to the GUI window in the order they are written here and fill from left to right, top to bottom.
#For more infromation on how to use the LivePlotter class, see GitHub readme file or the source code at core_tools/gui/live_plotter_GUI_class.py

plotter = LivePlotter("Test Live Plotter")

pressure_log_filepath = '40L_run_control/outer_vessel_pressure_log.csv'
inner_vessel_pressure_log_filepath = '40L_run_control/inner_vessel_pressure_log.csv'
gas_flow_log_filepath = '40L_run_control/gas_flow_log.csv'

create_pressure_log_csv(pressure_log_filepath)
create_flow_log_csv(gas_flow_log_filepath)

pressure_tab = plotter.create_tab(tab_name='Pressure', plots_per_row=2)

#pressure tab plots
pressure_tab.add_plot(title='Plot Inner Vessel Pressure', x_axis=('Time since present', 's'), y_axis=('Pressure', 'Torr'), buffer_size=10, csv_filepath=inner_vessel_pressure_log_filepath, datatype='inner_vessel_pressure')
pressure_tab.start_timer(title='Plot Inner Vessel Pressure', interval_ms=1000)

pressure_tab.add_plot(title='Plot Outer Vessel Pressure', x_axis=('Time since present', 's'), y_axis=('Pressure', 'Torr'), buffer_size=10, csv_filepath=pressure_log_filepath, datatype='outer_vessel_pressure')
pressure_tab.start_timer(title='Plot Outer Vessel Pressure', interval_ms=1000)

pressure_tab.add_subtraction_plot(title='Plot Gauge Pressure', x_axis=('Time since present', 's'), y_axis=('Pressure', 'Torr'), buffer_size=10)
pressure_tab.start_subtraction_plot_timer(title='Plot Gauge Pressure', plot1_title='Plot Inner Vessel Pressure', plot2_title='Plot Outer Vessel Pressure', interval_ms=1000)

pressure_tab.add_plot(title='Plot Gas Flowrate', x_axis=('Time since present', 's'), y_axis=('Flowrate', 'L/min'), buffer_size=10, csv_filepath=gas_flow_log_filepath, datatype='flowrate')
pressure_tab.start_timer(title='Plot Gas Flowrate', interval_ms=1000)

#pressure tab controls
pressure_tab.add_dropdown_menu(title='Pressure log increment', option_names=['2s', '10s', '1m', '10m', '1hr'], option_values=[2, 10, 60, 600, 600*6], ctrl_var='Log Outer Vessel Pressure', on_change_callback=pressure_tab.change_pressure_or_flowrate_cmd)
pressure_tab.add_command_button(title='Log Outer Vessel Pressure', command=f'.venv\Scripts\python.exe 40L_run_control/log_pressure.py {pressure_log_filepath} COM4 2')

pressure_tab.add_dropdown_menu(title='Gas flowrate log increment', option_names=['2s', '10s', '1m', '10m', '1hr'], option_values=[2, 10, 60, 600, 600*6], ctrl_var='Log Gas Flowrate', on_change_callback=pressure_tab.change_pressure_or_flowrate_cmd)
pressure_tab.add_command_button(title='Log Gas Flowrate', command=f'.venv\Scripts\python.exe 40L_run_control/log_gas_flowrate.py {gas_flow_log_filepath} COM3 2')

pressure_tab.add_dropdown_menu(title='Gas Flowrate Setting', option_names=['0%', '5%', '25%', '50%', '75%', '100%'], option_values=[0, 5, 25, 50, 75, 100], ctrl_var='Change Gas Flowrate', on_change_callback=pressure_tab.change_pressure_or_flowrate_cmd)
pressure_tab.add_command_button(title='Change Gas Flowrate', command=f'.venv\Scripts\python.exe 40L_run_control/change_gas_flowrate.py COM3 0')

pressure_ctrl_titles = ['Plot Inner Vessel Pressure', 'Plot Outer Vessel Pressure', 'Plot Gauge Pressure', 'Plot Gas Flowrate']
pressure_tab.add_dropdown_menu(title='# data points shown', option_names=['10', '50', '100', '1000', '10000'], option_values=[10, 50, 100, 1000, 10000], ctrl_var=pressure_ctrl_titles, on_change_callback=pressure_tab.change_buffer_size_multiple)


pressure_tab.cmd_timer(500)

'''temp_tab = plotter.create_tab(tab_name='Temperature', plots_per_row=4)
num_vmms = 32
temp_ctrl_titles = []
for i in range(0, num_vmms):
    temp_tab.add_plot(title=f'Plot VMM {i} Temperature', x_axis=('Time since present', 's'), y_axis=('Temperature', 'deg C'), buffer_size=10, csv_filepath=pressure_log_filepath, datatype='outer_vessel_pressure')
    temp_tab.start_timer(title=f'Plot VMM {i} Temperature', interval_ms=1000)
    temp_ctrl_titles.append(f'Plot VMM {i} Temperature')
temp_tab.add_dropdown_menu(title='# data points shown', option_names=['10', '50', '100', '1000', '10000'], option_values=[10, 50, 100, 1000, 10000], ctrl_var=temp_ctrl_titles, on_change_callback=temp_tab.change_buffer_size_multiple)
'''

plotter.run()
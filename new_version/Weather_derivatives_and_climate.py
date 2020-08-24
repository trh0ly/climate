# -------------------------------------------
# module import
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from pandas import read_csv, to_datetime, DataFrame, date_range, set_option
from numpy import setdiff1d, where, polyfit, poly1d, median, mean, array
from matplotlib.backend_bases import NavigationToolbar2
from sklearn.linear_model import LinearRegression
import matplotlib.pyplot as plt
from os import getcwd, listdir
from threading import Thread
from tkinter import ttk
from tkinter import *
from math import exp

# -------------------------------
# module settings
# -------------
# pandas
set_option('display.max_rows', 500)
set_option('display.max_columns', 500)
set_option('display.width', 1000)
# -------------
# matplotlib
NavigationToolbar2.toolitems = (('Home', 'Reset original view', 'home', 'home'),
                                              # ('Back', 'Back to previous view', 'back', 'back'),
                                              # ('Forward', 'Forward to next view', 'forward', 'forward'),
                                              # (None, None, None, None),
                                              ('Pan', 'Pan axes with left mouse, zoom with right', 'move', 'pan'),
                                              ('Zoom', 'Zoom to rectangle', 'zoom_to_rect', 'zoom'),
                                              ('Subplots', 'Configure subplots', 'subplots', 'configure_subplots'),
                                              # (None, None, None, None),
                                              ('Save', 'Save the figure', 'filesave', 'save_figure'))

class GUI(Tk):
    def __init__(self, **kwargs):
        Tk.__init__(self, **kwargs)
        # ---------------------------
        # call initial functions and set inital values
        self.scrollbar_width = 75
        self.scrollbar_height = 43
        self.combobox_width = 25
        self.calculation_scrollbar_height = 29
        self.calculation_scrollbar_width = 159
        self.analysis_level_index = 0
        self.figures = []
        self.axes = []

        # ---------------------------
        # PLACE WIDGETS
        # ---------------------
        # button_frame
        self.button_frame = Frame()
        self.button_frame.grid(row=0, column=0, rowspan=3, columnspan=3, sticky='W')
        # -------------
        # set_up_dataset_menu
        self.set_up_dataset_menu()
        self.dataset_menu_label.grid(row=1, column=0, padx=5, pady=5, sticky='W')
        self.dataset_menu_drop_down.grid(row=1, column=1, padx=5, pady=5, sticky='E')
        # -------------
        # set_up_modus_menu
        self.set_up_modus_menu()
        self.modus_input_label.grid(row=4, column=0, padx=5, pady=5, sticky='W')
        self.modus_menu_value_drop_down.grid(row=4, column=1, padx=5, pady=5, sticky='E')
        # -------------
        # set_up_moving_average_menu
        self.set_up_moving_average_menu()
        self.moving_average_menu_label.grid(row=3, column=0, padx=5, pady=5, sticky='W')
        self.moving_average_menu_drop_down.grid(row=3, column=1, padx=5, pady=5, sticky='E')
        self.widget_state(widget=self.moving_average_menu_drop_down, state=False)
        # -------------
        # set_up_trend_adjustment_check_box
        self.set_up_trend_adjustment_check_box()
        self.trend_adjustment_check_box_label.grid(row=5, column=0, padx=5, pady=5, sticky='W')
        self.trend_adjustment_check_box.grid(row=5, column=1, padx=5, pady=5, sticky='E')
        # -------------
        # set_up_interest_rate_menu
        self.set_up_interest_rate_menu()
        self.interest_rate_menu_label.grid(row=6, column=0, padx=5, pady=5, sticky='W')
        self.interest_rate_menu_drop_down.grid(row=6, column=1, padx=5, pady=5, sticky='E')
        # -------------
        # set_up_tick_size_menu
        self.set_up_tick_size_menu()
        self.tick_size_menu_label.grid(row=7, column=0, padx=5, pady=5, sticky='W')
        self.tick_size_menu_drop_down.grid(row=7, column=1, padx=5, pady=5, sticky='E')
        # -------------
        # set_up_show_plots_check_box
        self.set_up_show_plots_check_box()
        self.show_plots_check_box_label.grid(row=8, column=0, padx=5, pady=5, sticky='W')
        self.show_plots_check_box_box.grid(row=8, column=1, padx=5, pady=5, sticky='E')
        # -------------
        # set_up_observation_length_menu
        self.set_up_observation_length_menu()
        self.observation_length_menu_label.grid(row=2, column=0, padx=5, pady=5, sticky='W')
        self.observation_length_menu_drop_down.grid(row=2, column=1, padx=5, pady=5, sticky='E')
        self.widget_state(widget=self.observation_length_menu_drop_down, state=False)
        # -------------
        # set_up_start_button
        self.set_up_start_button()
        self.start_button.grid(row=9, column=0, columnspan=1, padx=5, pady=5, sticky='NSWE')
        # -------------
        # set_up_continue_button
        self.set_up_continue_button()
        self.continue_button.grid(row=9, column=1, columnspan=1, padx=5, pady=5, sticky='NSWE')
        self.widget_state(widget=self.continue_button, state=False)
        # -------------
        # set_up_output_scrollbar
        self.set_up_output_scrollbar()
        self.output_scrollbar_text.grid(row=10, column=0, columnspan=2, sticky='NSEW')
        self.output_scrollbar.grid(row=10, column=3, sticky='NSEW')
        # -------------
        # separator
        self.separator(orient_=VERTICAL, col_=3, row_=0, rowspan_=18, sticky_='NS')

        # ---------------------
        # plot_and_calculation_frame
        self.plot_and_calculation_frame = Frame()
        self.plot_and_calculation_frame.grid(row=0, column=4, rowspan=3, columnspan=3, sticky='W')
        # -------------
        # set_up_calculation_scrollbar
        self.set_up_calculation_scrollbar()
        self.calculation_scrollbar_text.grid(row=3, column=2, sticky='NSEW')
        self.calculation_scrollbar.grid(row=3, column=3, sticky='NSEW')
        # -------------
        # set_up_source_label
        self.set_up_source_label()
        self.source_label.grid(row=4, column=2)
        # ---------------------------
        # call initial functions
        self.init_output()

    # -------------------------------------------
    # Define functions for GUI
    # -------------------------------
    # GUI WIDGETS
    # -------------
    # set_up_source_label
    def set_up_source_label(self):
        self.source_label = Label(self.plot_and_calculation_frame, text=r"https://github.com/trh0ly/weather-derivative-pricing-and-climate", fg="blue", cursor="hand2")
        return self.source_label

    # -------------
    # set_up_output_scrollbar
    def set_up_output_scrollbar(self):
        self.output_scrollbar = Scrollbar(self.button_frame)
        self.output_scrollbar_text = Text(self.button_frame, height=self.scrollbar_height, width=self.scrollbar_width)
        self.output_scrollbar.config(command=self.output_scrollbar_text.yview)

    # -------------
    # set_up_observation_length_menu
    def set_up_observation_length_menu(self):
        self.observation_length_menu_value = StringVar()
        self.observation_length_menu_value.set('Betrachtungszeitraum wählen')
        self.observation_length_menu_label = Label(self.button_frame, text="Betrachtungszeitraum", font=self.font_bold(()))
        self.observation_length_menu_drop_down = ttk.Combobox(self.button_frame, textvariable=self.observation_length_menu_value, width=self.combobox_width)
        self.observation_length_menu_drop_down.bind("<<ComboboxSelected>>", self.with_selecting_observation_length)
        self.observation_length_menu_drop_down.config(font=self.font_normal())

    # -------------
    # set_up_start_button
    def set_up_start_button(self):
        self.start_button = Button(self.button_frame, text="Analyse starten", font=self.font_normal(), command=self.start_button_on_click)

    # -------------
    # set_up_continue_button
    def set_up_continue_button(self):
        self.continue_button = Button(self.button_frame, text="Analyse fortsetzen", font=self.font_normal())
        self.continue_button.bind('<Button-1>', self.continue_button_on_click)

    # -------------
    # set_up_calculation_scrollbar
    def set_up_calculation_scrollbar(self):
        self.calculation_scrollbar = Scrollbar(self.plot_and_calculation_frame)
        self.calculation_scrollbar_text = Text(self.plot_and_calculation_frame, height=self.calculation_scrollbar_height, width=self.calculation_scrollbar_width)
        self.calculation_scrollbar.config(command=self.calculation_scrollbar_text.yview)

    # -------------
    # set_up_trend_adjustment_check_box
    def set_up_trend_adjustment_check_box(self):
        self.trend_adjustment_check_box_value = BooleanVar()
        self.trend_adjustment_check_box_value.set(True)
        self.trend_adjustment_check_box_label = Label(self.button_frame, text="Trendbereinigung", font=self.font_bold(()))
        self.trend_adjustment_check_box = Checkbutton(self.button_frame, variable=self.trend_adjustment_check_box_value)

    # -------------
    # set_up_show_plots_check_box
    def set_up_show_plots_check_box(self):
        self.show_plots_check_box_value = BooleanVar()
        self.show_plots_check_box_value.set(True)
        self.show_plots_check_box_label = Label(self.button_frame, text="Zeige Plots", font=self.font_bold(()))
        self.show_plots_check_box_box = Checkbutton(self.button_frame, variable=self.show_plots_check_box_value)

    # -------------
    # set_up_dataset_menu
    def set_up_dataset_menu(self):
        options = self.get_datasets_in_path()
        self.dataset_menu_value = StringVar()
        self.dataset_menu_value.set('Datensatz wählen')
        self.dataset_menu_label = Label(self.button_frame, text="Verfügbare Wetterstationen", font=self.font_bold(()))
        self.dataset_menu_drop_down = ttk.Combobox(self.button_frame, textvariable=self.dataset_menu_value, value=options, width=self.combobox_width)
        self.dataset_menu_drop_down.bind("<<ComboboxSelected>>", self.with_selecting_dataset_or_modus)
        self.dataset_menu_drop_down.config(font=self.font_normal())

    # -------------
    # set_up_interest_rate_menu
    def set_up_interest_rate_menu(self):
        options = self.interest_rate_options()
        self.interest_rate_menu_value = StringVar()
        self.interest_rate_menu_value.set(options[5])
        self.interest_rate_menu_label = Label(self.button_frame, text="Kapitalmarktzins in %", font=self.font_bold(()))
        self.interest_rate_menu_drop_down = ttk.Combobox(self.button_frame, textvariable=self.interest_rate_menu_value, value=options, width=self.combobox_width)
        self.interest_rate_menu_drop_down.config(font=self.font_normal())

    # -------------
    # set_up_moving_average_menu
    def set_up_moving_average_menu(self):
        self.moving_average_menu_value = StringVar()
        self.moving_average_menu_value.set(1)
        self.moving_average_menu_label = Label(self.button_frame, text="Moving-Average-Fenster in Perioden", font=self.font_bold(()))
        self.moving_average_menu_drop_down = ttk.Combobox(self.button_frame, textvariable=self.moving_average_menu_value, width=self.combobox_width)
        self.moving_average_menu_drop_down.config(font=self.font_normal())

    # -------------
    # set_up_tick_size_menu
    def set_up_tick_size_menu(self):
        options = self.tick_size_options()
        self.tick_size_menu_value = StringVar()
        self.tick_size_menu_value.set(options[0])
        self.tick_size_menu_label = Label(self.button_frame, text="Tick-Size in $", font=self.font_bold(()))
        self.tick_size_menu_drop_down = ttk.Combobox(self.button_frame, textvariable=self.tick_size_menu_value, value=options, width=self.combobox_width)
        self.tick_size_menu_drop_down.config(font=self.font_normal())

    # -------------
    # set_up_modus_menu
    def set_up_modus_menu(self):
        options = self.modus_options()
        self.modus_menu_value = StringVar()
        self.modus_menu_value.set(options[0])
        self.modus_input_label = Label(self.button_frame, text="Modus (Periodendurchschnitt)", font=self.font_bold(()))
        self.modus_menu_value_drop_down = ttk.Combobox(self.button_frame, textvariable=self.modus_menu_value, value=options, width=self.combobox_width)
        self.modus_menu_value_drop_down.bind("<<ComboboxSelected>>", self.with_selecting_dataset_or_modus)
        self.modus_menu_value_drop_down.config(font=self.font_normal())

    """
    #-------------
    # set_up_plot_window
    """
    def set_up_plot_window(self, fig):
        self.plot_canvas = FigureCanvasTkAgg(fig, master=self.plot_and_calculation_frame)
        self.plot_canvas.get_tk_widget().grid(row=1, column=2, padx=5, pady=5, sticky='NSEW')
        self.toolbarFrame = Frame(master=self.plot_and_calculation_frame)
        self.toolbarFrame.grid(row=2, column=2, padx=25, pady=25, sticky='NS')
        _ = NavigationToolbar2Tk(self.plot_canvas, self.toolbarFrame)

    # -------------
    # clear_fig
    def clear_fig(self):
        [plt.close(fig) for fig in self.figures]
        [ax_.clear() for ax_ in self.axes]
        self.figures = []
        self.axes = []

    # -------------------------------
    # OPTION GENERATORS
    # ----------------------
    # interest_rate_options
    def interest_rate_options(self):
        return [(i / 100) for i in range(0, (15 + 1), 1)]

    # ----------------------
    # observation_length_options
    def observation_length_options(self, first_last_year):
        options = [i for i in list(range(10, (first_last_year[1] - first_last_year[0])))]
        self.observation_length_menu_drop_down.configure(values=options)
        self.observation_length_menu_drop_down.set(min(options[int(len(options) * 0.25)], 30))
        self.moving_average_menu_drop_down.set(1)

    # ----------------------
    # moving_average_options
    def moving_average_options(self):
        self.get_runtime_settings()
        options = [i for i in list(range(1, (int(int(self.current_observation_length_menu_value) * 0.25)) + 1))]
        self.moving_average_menu_drop_down.configure(values=options)

    # ----------------------
    # dataset_options
    def dataset_options(self):
        options = self.get_datasets_in_path()
        self.dataset_menu.configure(values=options)

    # ----------------------
    # modus_options
    def modus_options(self):
        #return ['CDD', 'HDD', 'TMK', 'RSK']
        return ['CDD (Cooling-Degree-Day)', 'HDD (Heating-Degree-Day)', 'TMK (Tagesmittel Temperatur)', 'RSK (Tägliche Niederschlagshöhe)',
                'SDK (Tägliche Sonnenscheindauer)', 'SHK (Tageswert Schneehöhe)', 'NM (Tagesmittel Bedeckungsgrad)', 'VPM (Tagesmittel Dampfdruck)',
                'PM (Tagesmittel Luftdruck)', 'UPM (Tagesmittel relative Feuchte)', 'TXK (Tagesmaximum Lufttemperatur)', 'TNK (Tagesminimum Lufttemperatur)']

    # ----------------------
    # tick_size_options
    def tick_size_options(self):
        return [i for i in range(10, (100 + 1), 5)]

    # -------------------------------
    # ON BUTTON CLICK / GUI INTERACTIVE
    # -------------
    # update_output_scrollbar
    def update_output_scrollbar(self, text_update, blank_size=72):
        self.output_scrollbar_text.config(yscrollcommand=self.output_scrollbar.set, state='normal')
        self.output_scrollbar_text.insert(END, str('#' + '-' * blank_size + '#\n'))
        self.output_scrollbar_text.insert(END, str(text_update) + '\n')
        self.output_scrollbar_text.config(yscrollcommand=self.output_scrollbar.set, state='disabled')
        self.output_scrollbar_text.see("end")

    # -------------
    # change_all_widget_states
    def change_all_widget_states(self, state_):
        all_menus = [self.dataset_menu_drop_down, self.modus_menu_value_drop_down, self.moving_average_menu_drop_down,
                     self.trend_adjustment_check_box, self.tick_size_menu_drop_down, self.interest_rate_menu_drop_down, self.show_plots_check_box_box, self.observation_length_menu_drop_down]
        for menu in all_menus: self.widget_state(widget=menu, state=state_)

    # -------------
    # analysis_level_manager
    def analysis_level_manager(self):
        self.get_runtime_settings()
        if self.current_modus_menu_value in ['HDD', 'CDD', 'TMK'] and self.current_trend_adjustment_check_box_value == True:
            self.analysis_levels = [0, 1, 2]
            if self.analysis_level_index == self.analysis_levels[-2]:
                self.widget_state(widget=self.continue_button, state=False)
                self.change_all_widget_states(state_=True)
                self.continue_button.unbind('<Button-1>')
            elif self.analysis_level_index >= self.analysis_levels[-1]:
                self.analysis_level_index = 0

        elif self.current_modus_menu_value in ['HDD', 'CDD', 'TMK'] and self.current_trend_adjustment_check_box_value == False:
            self.analysis_levels = [0, 2]
            #if self.analysis_level_index >= self.analysis_levels[0]:
            self.widget_state(widget=self.continue_button, state=False)
            self.change_all_widget_states(state_=True)
            self.analysis_level_index = 0
            self.continue_button.unbind('<Button-1>')

        elif self.current_modus_menu_value not in ['HDD', 'CDD', 'TMK'] and self.current_trend_adjustment_check_box_value == True:
            self.analysis_levels = [0, 1]
            #if self.analysis_level_index >= self.analysis_levels[0]:
            self.widget_state(widget=self.continue_button, state=False)
            self.change_all_widget_states(state_=True)
            self.analysis_level_index = 0
            self.continue_button.unbind('<Button-1>')

    # -------------
    # continue_button_on_click
    def continue_button_on_click(self, event):
        self.get_runtime_settings()
        self.analysis_level_manager()
        self.analysis_level_index += 1
        level = self.analysis_levels[self.analysis_level_index]
        self.core_calculation_and_plot_function(level=level)
        self.get_runtime_settings()

    # -------------
    # with_selecting_dataset_or_modus
    def with_selecting_dataset_or_modus(self, event):
        self.get_runtime_settings()
        self.with_selecting_modus()
        raw_data = self.read_in_raw_dataset(raw_data_=self.current_dataset_menu_value)
        data_df = self.create_data_df(raw_data_=raw_data)
        first_last_year = self.get_first_and_last_year(data_df_=data_df)

        compared_date_range = self.compare_date_range(first_last_year_=first_last_year, mode_=self.current_modus_menu_value, data_df_=data_df)
        least_valid_year = self.get_least_valid_year(compared_date_range_=compared_date_range)
        updated_first_last_year = (least_valid_year, first_last_year[1])

        self.observation_length_options(updated_first_last_year)
        self.moving_average_options()
        self.widget_state(widget=self.observation_length_menu_drop_down, state=True)
        self.widget_state(widget=self.moving_average_menu_drop_down, state=True)

    # -------------
    # with_selecting_observation_length
    def with_selecting_observation_length(self, event):
        self.moving_average_options()

    # -------------
    # with_selecting_modus
    def with_selecting_modus(self):
        all_nnon_derivative_menus = [self.tick_size_menu_drop_down, self.interest_rate_menu_drop_down]
        if self.current_modus_menu_value not in ['HDD', 'CDD', 'TMK']: [self.widget_state(widget=menu, state=False) for menu in all_nnon_derivative_menus]
        else: [self.widget_state(widget=menu, state=True) for menu in all_nnon_derivative_menus]


    # -------------
    # update_calculation_scrollbar
    def update_calculation_scrollbar(self, text_update, blank_size=150):
        self.calculation_scrollbar_text.config(yscrollcommand=self.calculation_scrollbar.set, state='normal')
        self.calculation_scrollbar_text.insert(END, str('#' + '-' * blank_size + '#\n'))
        self.calculation_scrollbar_text.insert(END, str(text_update) + '\n')
        self.calculation_scrollbar_text.config(yscrollcommand=self.calculation_scrollbar.set, state='disabled')
        self.calculation_scrollbar_text.see("end")

    # -------------
    # start_button_on_click
    def start_button_on_click(self):
        self.start_thread(task=self.core_calculation_and_plot_function(level=0), task_name='start_button_pressed')
        self.change_all_widget_states(state_=False)
        self.analysis_level_index = 0
        self.continue_button.bind('<Button-1>', self.continue_button_on_click)
        self.clear_fig()

        self.get_runtime_settings()
        if self.current_modus_menu_value not in ['HDD', 'CDD', 'TMK'] and self.current_trend_adjustment_check_box_value == False:
            self.continue_button.unbind('<Button-1>')
            self.widget_state(widget=self.continue_button, state=False)
            self.change_all_widget_states(state_=True)
            self.analysis_level_index = 0
        else: pass

    # -------------
    # core_calculation_and_plot_function
    def core_calculation_and_plot_function(self, level):
        self.get_runtime_settings()

        # -------------
        # basic level
        if level == 0:
            # -------------
            # update_output_scrollbar
            text_ = str('Folgende Einstellungen wurden übernommen:\nTrend-Status: {};\nDatensatz: {};\nKapitalmarktzins: {};\nModus: {};\nTick-Size: {};\nMoving-Average-Zeitraum: {};\nPlot-Status: {};\nBetrachtungszeitraum: {}'
                        .format(self.current_trend_adjustment_check_box_value, self.current_dataset_menu_value, self.current_interest_rate_menu_value, self.current_modus_menu_value,
                                self.current_tick_size_menu_value, self.current_moving_average_menu_value, self.current_show_plots_check_box_value, self.current_observation_length_menu_value))
            self.start_thread(task=self.update_output_scrollbar(text_), task_name='text_update')

            # -------------
            # update_calculation_scrollbar/ read raw_data
            text_ = str('Ein Auszug des eingelesenen Datensatzes:')
            self.start_thread(task=self.update_calculation_scrollbar(text_), task_name='text_update')
            raw_data = self.read_in_raw_dataset(raw_data_=self.current_dataset_menu_value)
            self.start_thread(task=self.update_calculation_scrollbar(raw_data), task_name='text_raw_data')

            # -------------
            # update_calculation_scrollbar/ data_df
            text_ = str('Errechnete Messwerte aus diesem Datensatz:')
            self.start_thread(task=self.update_calculation_scrollbar(text_), task_name='text_update')
            data_df = self.create_data_df(raw_data_=raw_data)
            self.start_thread(task=self.update_calculation_scrollbar(data_df), task_name='text_data_df')

            # -------------
            # update_calculation_scrollbar/ first_last_year
            first_last_year = self.get_first_and_last_year(data_df_=data_df)
            text_ = str('Der Datensatz reicht von {} bis {}, sodass der maximale Betrachtungszeitraum {} Jahre umfasst'
                        .format(first_last_year[0], first_last_year[1], (first_last_year[1] - first_last_year[0])))
            self.start_thread(task=self.update_calculation_scrollbar(text_), task_name='text_update')

            # -------------
            # compared_date_range/ update_calculation_scrollbar
            compared_date_range = self.compare_date_range(first_last_year_=first_last_year, mode_=self.current_modus_menu_value, data_df_=data_df)
            least_valid_year = self.get_least_valid_year(compared_date_range_=compared_date_range)
            text_ = str('In dem aufgerufenen Datensatz fehlen Datenpunkte, weshalb sich der maximal mögliche Betrachtungszeitraum auf {} Jahre verkürzt.\nDie Analyse ist somit ab dem Jahr {} möglich.'
                        .format((first_last_year[1] - least_valid_year), least_valid_year))
            self.start_thread(task=self.update_calculation_scrollbar(text_), task_name='text_update')

            # -------------
            # update_calculation_scrollbar
            if len(compared_date_range) > 1:
                text_ = str('Ein Auszug aus den im dem Datensatz fehlenden Einträgen:')
                self.start_thread(task=self.update_calculation_scrollbar(text_), task_name='text_update')
                if len(compared_date_range) < 10: self.start_thread(task=self.update_calculation_scrollbar(str(compared_date_range)), task_name='text_compared_date_range')
                else: self.start_thread(task=self.update_calculation_scrollbar(str(compared_date_range[:6]) + '\n...\n' + str(compared_date_range[-6:])), task_name='text_compared_date_range')

            # -------------
            # valid_data_range/ obervation_sum_df
            valid_data_range = (first_last_year[1] - int(self.current_observation_length_menu_value))
            first_last_year = (max(least_valid_year + 1, valid_data_range), first_last_year[1])
            self.obervation_sum_df = self.calculate_observation_sum(first_last_year_=first_last_year, data_df_=data_df, mode_=self.current_modus_menu_value)

            # -------------
            # update_calculation_scrollbar
            text_ = str('Folgende {}-Werte wurden brechnet:'.format(self.current_modus_menu_value))
            self.start_thread(task=self.update_calculation_scrollbar(text_), task_name='text_update')
            self.start_thread(task=self.update_calculation_scrollbar(self.obervation_sum_df.observation_sum), task_name='text_update')

            # -------------
            # plot_measurement_fig
            if self.current_show_plots_check_box_value == True:
                measurement_fig = self.measurement_plot(observation_sum_df_=self.obervation_sum_df, moving_average_mode_=self.current_moving_average_menu_value, mode_=self.current_modus_menu_value, font_size_=12)
                self.start_thread(task=self.set_up_plot_window(fig=measurement_fig), task_name='plot_measurement_fig')
                text_ = str('Die Grafik für die Darstellung der Messwerte wurde generiert')
                self.start_thread(task=self.update_calculation_scrollbar(text_), task_name='text_update')
            else: pass
            # -------------
            # continue_button state
            self.widget_state(widget=self.continue_button, state=True)

        # -------------
        # trend_adjustment level
        if level == 1:
            # -------------
            # check adjustment_check_box_value
            if self.current_trend_adjustment_check_box_value == True:
                observation_sum_adjusted = self.trend_adjustment(observation_sum_df_=self.obervation_sum_df)
                # -------------
                # check show_plots_check_box_value
                if self.current_show_plots_check_box_value == True:
                    measurement_fig_adjusted = self.measurement_plot(observation_sum_df_=observation_sum_adjusted, moving_average_mode_=self.current_moving_average_menu_value, mode_=self.current_modus_menu_value, font_size_=12)
                    self.start_thread(task=self.set_up_plot_window(fig=measurement_fig_adjusted), task_name='plot_measurement_fig_adjusted')
                    text_ = str('Die Grafik für die Darstellung der Messwerte wurde generiert')
                    self.start_thread(task=self.update_calculation_scrollbar(text_), task_name='text_update')
                else: pass
            else: pass

        # -------------
        # fair value level
        if level == 2:
            # -------------
            # update_calculation_scrollbar / payoff_df
            text_ = str('Die Payoffs ergeben sich wie folgt:')
            self.start_thread(task=self.update_calculation_scrollbar(text_), task_name='text_update')
            payoff_df = self.calculate_payoff(obervation_sum_df_=self.obervation_sum_df, tick_size_=self.current_tick_size_menu_value)
            self.start_thread(task=self.update_calculation_scrollbar(payoff_df), task_name='text_payoff_df')

            # -------------
            # update_calculation_scrollbar / fair_value_df
            text_ = str('Daraus resultieren folgende Fair-Values:')
            self.start_thread(task=self.update_calculation_scrollbar(text_), task_name='text_update')
            fair_value_df = self.calculate_fair_value(obervation_sum_df_=self.obervation_sum_df, interest_rate_=self.current_interest_rate_menu_value, payoff_df_=payoff_df)
            self.start_thread(task=self.update_calculation_scrollbar(fair_value_df), task_name='text_fair_value_df')

            # -------------
            # check show_plots_check_box_value
            if self.current_show_plots_check_box_value == True:
                fair_value_fig = self.fair_value_plot(obervation_sum_df_=self.obervation_sum_df, fair_value_df_=fair_value_df, mode_=self.current_modus_menu_value, font_size_=12)
                self.start_thread(task=self.set_up_plot_window(fig=fair_value_fig), task_name='plot_fair_value_fig')
                text_ = str('Die Grafik für die Darstellung der Fair-Values wurde generiert')
                self.start_thread(task=self.update_calculation_scrollbar(text_), task_name='text_update')
            else: pass

    # -------------
    # widget_state
    def widget_state(self, widget, state):
        if state == True: widget.configure(state='normal')
        else: widget.configure(state='disabled')

    # -------------
    # get_runtime_settings
    def get_runtime_settings(self):
        try: self.current_trend_adjustment_check_box_value = self.trend_adjustment_check_box_value.get()
        except: self.current_trend_adjustment_check_box_value = None

        try: self.current_dataset_menu_value = self.dataset_menu_value.get()
        except: self.current_dataset_menu_value = None

        try: self.current_interest_rate_menu_value = self.interest_rate_menu_value.get()
        except: self.current_interest_rate_menu_value= None

        try: self.current_modus_menu_value = self.modus_menu_value.get()[:3]
        except: self.current_modus_menu_value = None

        try: self.current_tick_size_menu_value = self.tick_size_menu_value.get()
        except: self.current_tick_size_menu_value = None

        try: self.current_moving_average_menu_value = self.moving_average_menu_value.get()
        except: self.current_moving_average_menu_value = None

        try: self.current_show_plots_check_box_value = self.show_plots_check_box_value.get()
        except: self.current_show_plots_check_box_value = None

        try: self.current_observation_length_menu_value = self.observation_length_menu_value.get()
        except: self.current_observation_length_menu_value = None

    # -------------------------------
    # APPEARANCE
    # -------------
    # font_normal
    def font_normal(self, font='Helvetica', size=12):
        return (font, size)

    # -------------
    # font_bold
    def font_bold(self, font='Helvetica', size=12):
        return (font, size, 'bold')

    # -------------
    # separator
    def separator(self, orient_, col_, row_, rowspan_, sticky_):
        ttk.Separator(self, orient=orient_).grid(column=col_, row=row_, rowspan=rowspan_, sticky=sticky_)

    # -------------------------------
    # PATHS AND FILES
    # -------------
    # get_local_path
    def get_local_path(self):
        return getcwd() + '\\'

    # -------------
    # get_datasets_in_path
    def get_datasets_in_path(self):
        local_path = self.get_local_path()
        return [file[:-4] for file in listdir(str(local_path)) if file.endswith(".csv")]

    # -------------------------------
    # MULTITHREADING
    # -------------
    # start_thread
    def start_thread(self, task, task_name=None):
        thread_ = Thread(target=task)
        if task_name: thread_.name = task_name
        else: pass
        thread_.start()

    # -------------------------------
    # INIT
    # -------------
    # init_plot
    def init_output(self):
        init_fig, _ = plt.subplots()
        self.figures.append(init_fig)
        self.start_thread(task=self.set_up_plot_window(fig=init_fig), task_name='init_fig_plot')
        self.start_thread(task=self.update_output_scrollbar('Hier werden Programminformationen und Fehlermeldungen ausgegeben'))
        self.start_thread(task=self.update_calculation_scrollbar('Hier werden Berechnungsergebnisse und Informationen zur Analyse ausgegeben'))

    # -------------------------------------------
    # define functions for WEATHER PROGRAM
    # -------------
    # read_in_raw_dataset
    def read_in_raw_dataset(self, raw_data_):
        raw_data = read_csv(str(raw_data_) + '.csv', sep=";", decimal=".")
        raw_data.columns = [column.replace(' ', '') for column in raw_data.columns]
        return raw_data

    # -------------
    # replace_missing_value
    def replace_missing_value_999(self, raw_values_, value_to_replace_, new_value_):
        return where(raw_values_ == value_to_replace_, new_value_, raw_values_)

    # -------------
    # calculate_HDD
    def calculate_HDD(self, raw_data_):
        temperature = self.replace_missing_value_999(raw_values_=raw_data_.TMK, value_to_replace_=-999, new_value_=18)
        return [max(0, (18 - temperature_)) for temperature_ in temperature]

    # -------------
    # calculate_CDD
    def calculate_CDD(self, raw_data_):
        temperature = self.replace_missing_value_999(raw_values_=raw_data_.TMK, value_to_replace_=-999, new_value_=18)
        return [max(0, (temperature_ - 18)) for temperature_ in temperature]

    # -------------
    # create_data_df
    def create_data_df(self, raw_data_):
        measurement_date = to_datetime(raw_data_.MESS_DATUM, format='%Y%m%d')
        temperature = self.replace_missing_value_999(raw_values_=raw_data_.TMK, value_to_replace_=-999.0, new_value_=18)
        rainfall = self.replace_missing_value_999(raw_values_=raw_data_.RSK, value_to_replace_=-999.0, new_value_=0)
        HDD = self.calculate_HDD(raw_data_=raw_data_)
        CDD = self.calculate_CDD(raw_data_=raw_data_)
        """
        create_data_df_dict = {'TMK': temperature,
                   'RSK': rainfall,
                   'HDD': HDD,
                   'CDD': CDD}
        """
        SDK = self.replace_missing_value_999(raw_values_=raw_data_.SDK, value_to_replace_=-999.0, new_value_=0)
        SHK = self.replace_missing_value_999(raw_values_=raw_data_.SHK_TAG, value_to_replace_=-999.0, new_value_=0)
        NM = self.replace_missing_value_999(raw_values_=raw_data_.NM, value_to_replace_=-999.0, new_value_=0)
        VPM = self.replace_missing_value_999(raw_values_=raw_data_.VPM, value_to_replace_=-999.0, new_value_=0)
        PM = self.replace_missing_value_999(raw_values_=raw_data_.PM, value_to_replace_=-999.0, new_value_=0)
        UPM = self.replace_missing_value_999(raw_values_=raw_data_.UPM, value_to_replace_=-999.0, new_value_=0)
        TXK = self.replace_missing_value_999(raw_values_=raw_data_.TXK, value_to_replace_=-999.0, new_value_=0)
        TNK = self.replace_missing_value_999(raw_values_=raw_data_.TNK, value_to_replace_=-999.0, new_value_=0)

        create_data_df_dict = {'TMK': temperature,
                   'RSK': rainfall,
                   'HDD': HDD,
                   'CDD': CDD,
                   'SDK': SDK,
                   'SHK': SHK,
                   'NM': NM,
                   'VPM': VPM,
                   'PM': PM,
                   'UPM': UPM,
                   'TXK': TXK,
                   'TNK':TNK}

        data_df = DataFrame(create_data_df_dict, index=measurement_date)
        data_df.index.name = 'MESS_DATUM'
        return data_df

    # -------------
    # get_first_and_last_year
    def get_first_and_last_year(self, data_df_):
        index_values = data_df_.index.to_list()
        return (int(str(index_values[0])[:4]), int(str(index_values[-1])[:4]))

    # -------------
    # dynamic_range_for_plots
    def dynamic_range_for_plots(self, values_):
        sorted_values = sorted(values_)
        plot_min = max(0, (sorted_values[0] - sorted_values[0] * 0.25))
        plot_max = (sorted_values[-1] * 1.25)
        return (plot_min, plot_max)

    # -------------
    # leap_years_conditions_
    def leap_years_conditions_(self, year_):
        condition1 = (year_ % 4 == 0)
        condition2 = (year_ % 100 == 0)
        condition3 = (year_ % 400 == 0)
        if (condition1 and not condition2) or condition3: return year_
        else: pass

    # -------------
    # get_leap_years
    def get_leap_years(self, observations_):
        return [self.leap_years_conditions_(year_=year) for year in observations_ if self.leap_years_conditions_(year_=year) is not None]

    # -------------
    # get_should_date_range
    def get_should_date_range(self, first_last_year_, mode_):
        observated_years = list(range(first_last_year_[0], (first_last_year_[1] + 1)))
        if str(mode_) == 'CDD': start_end_date = [(str(year) + '-05-01', str(year) + '-09-30') for year in observated_years]
        elif str(mode_) == 'HDD':
            leap_years = self.get_leap_years(observations_=observated_years)
            start_end_date = [(str(year - 1) + '-11-01', str(year) + '-02-29') if year in leap_years else (str(year - 1) + '-11-01', str(year) + '-02-28') for year in observated_years]
        else: start_end_date = [(str(year) + '-01-01', str(year) + '-12-31') for year in observated_years]
        mask = [date_range(date[0], date[1], freq='1D') for date in start_end_date]
        whole_mask = [mask_ for sub_list in mask for mask_ in sub_list]
        return to_datetime(whole_mask)

    """
    # -------------
    # compare_date_range    
    """
    def compare_date_range(self, first_last_year_, mode_, data_df_):
        should_date_range = self.get_should_date_range(first_last_year_=first_last_year_, mode_=str(mode_))
        return setdiff1d(should_date_range, data_df_.index)

    # -------------
    # get_least_valid_year
    def get_least_valid_year(self, compared_date_range_):
        return (int(str(compared_date_range_[-1])[:4]))

    # -------------
    # calculate_observation_sum
    def calculate_observation_sum(self, first_last_year_, data_df_, mode_):
        observated_years = list(range(first_last_year_[0], (first_last_year_[1] + 1)))
        if str(mode_) == 'CDD': start_end_date = [(str(year) + '-05-01', str(year) + '-09-30') for year in observated_years]
        elif str(mode_) == 'HDD':
            leap_years = self.get_leap_years(observations_=observated_years)
            start_end_date = [(str(year) + '-11-01', str(year + 1) + '-02-28') if year in leap_years else (str(year) + '-11-01', str(year + 1) + '-02-28') for year in observated_years[:-1]]
            observated_years = observated_years[:-1]
        else: start_end_date = [(str(year) + '-01-01', str(year) + '-12-31') for year in observated_years]
        mask = [date_range(date[0], date[1], freq='1D') for date in start_end_date]
        if str(mode_) in ['HDD', 'CDD']: observation_sum = [round(data_df_.loc[mask_, str(mode_)].sum(), 2) for mask_ in mask]
        else: observation_sum = [round((data_df_.loc[mask_, str(mode_)].sum() / len(data_df_.loc[mask_, str(mode_)])), 2) for mask_ in mask]

        observation_sum_df = DataFrame({'observation_sum': observation_sum}, index=observated_years)
        observation_sum_df.index.name = 'observated_years'
        return observation_sum_df

    # -------------
    # measurement_plot
    def measurement_plot(self, observation_sum_df_, mode_, moving_average_mode_, font_size_=12):
        measurements = observation_sum_df_.observation_sum
        observated_years = observation_sum_df_.index

        plot_min_max = self.dynamic_range_for_plots(values_=measurements)
        z = polyfit(observated_years, measurements, 1)
        p = poly1d(z)

        fig, ax = plt.subplots()
        ax.grid()
        ax.bar(observated_years, measurements, label='{}s'.format(str(mode_)))
        if int(moving_average_mode_) > 1:
            moving_average = observation_sum_df_['observation_sum'].rolling(window=int(moving_average_mode_), min_periods=0).mean().values.tolist()
            ax.plot(observated_years, moving_average, color='orange', label='Moving-Average'.format(str(mode_)))
        else: pass
        ax = plt.gca()
        ax.set_title('{}-Werte innerhalb der Akkumulationsperiode'.format(str(mode_)), fontsize=font_size_)
        ax.set_ylabel('{}s'.format(str(mode_)), fontsize=font_size_);
        ax.set_xlabel('Jahr', fontsize=font_size_);
        ax.set_ylim(plot_min_max)
        for patch in ax.patches: ax.text(patch.get_x() + .04, patch.get_height() + (median(measurements) * 0.025), str(round((patch.get_height()), 2)), fontsize=font_size_, color='dimgrey', rotation=90)
        _ = plt.plot(observated_years, p(observated_years), "r--", label='Trendlinie', color='black')
        _ = plt.axhline(mean(measurements), color='red', label="Mittelwert")
        ax.legend(loc='best')
        self.figures.append(fig)
        self.axes.append(ax)
        return fig

    # -------------
    # calculate_payoff
    def calculate_payoff(self, obervation_sum_df_, tick_size_):
        measurements = array([round(measurement, 3) for measurement in obervation_sum_df_.observation_sum])
        operational_time = [year for year in range(len(measurements), 0, -1)]
        measurements_mean = [mean(measurements) for _ in measurements]
        tick_size = [int(tick_size_)] * len(measurements)
        payoff = where(measurements >= measurements_mean, ((measurements - measurements_mean) * int(tick_size_)), 0)

        payoff_dict = {'Messwert': measurements,
                   'Strike': measurements_mean,
                   'Tick-Size': tick_size,
                   'Payoff': payoff}

        payoff_df = DataFrame(payoff_dict, index=operational_time)
        payoff_df.index.name = 'Laufzeit'
        return payoff_df

    # -------------
    # calculate_fair_value
    def calculate_fair_value(self, obervation_sum_df_, interest_rate_, payoff_df_):
        observated_years = obervation_sum_df_.index
        operational_time = payoff_df_.index
        payoff = array(payoff_df_.Payoff)

        future_years = [(year + len(observated_years)) for year in observated_years]
        discount_factor = [exp(-year * float(interest_rate_)) for year in operational_time[::-1]]
        fair_value = ([payoff.mean()] * len(future_years)) * array(discount_factor)

        my_dict = {'Fälligkeit': future_years,
                   'Diskontfaktor': discount_factor,
                   'Fair_Value': fair_value}

        fair_value_df = DataFrame(my_dict, index=operational_time[::-1])
        fair_value_df.index.name = 'Laufzeit'
        return fair_value_df

    # -------------
    # fair_value_plot
    def fair_value_plot(self, obervation_sum_df_, fair_value_df_, mode_, font_size_=12):
        observated_years = obervation_sum_df_.index
        future_years = [(year + len(observated_years) + 1) for year in observated_years]
        fair_values = fair_value_df_.Fair_Value

        plot_min_max = self.dynamic_range_for_plots(values_=fair_values)
        fig, ax = plt.subplots()
        ax.grid()
        ax.bar(future_years, fair_values, label='Fair-Value')
        ax = plt.gca()
        ax.set_title('Fair-Values der {}-Wetter-Option'.format(str(mode_)), fontsize=font_size_)
        ax.set_ylabel('Fair-Value', fontsize=font_size_);
        ax.set_xlabel('Jahr', fontsize=font_size_);
        ax.set_ylim(plot_min_max)
        for patch in ax.patches: ax.text(patch.get_x() + .04, patch.get_height() + (mean(fair_values) * 0.025), str(round((patch.get_height()), 2)), fontsize=font_size_, color='dimgrey', rotation=90)
        ax.legend(loc='best')
        self.figures.append(fig)
        self.axes.append(ax)
        return fig

    # -------------
    # trend_adjustment_by_linear_regression
    def trend_adjustment_by_linear_regression(self, x_, y_):
        linear_model = LinearRegression()
        linear_model.fit(x_, y_)
        predictions = linear_model.predict(x_)
        return [true_value - predicted_value for true_value, predicted_value in zip(y_, predictions)] + mean(y_)

    # -------------
    # trend_adjustment
    def trend_adjustment(self, observation_sum_df_):
        x_values, y_values = array(observation_sum_df_.index).reshape(-1, 1), array(observation_sum_df_.observation_sum)
        adjusted_values = self.trend_adjustment_by_linear_regression(x_=x_values, y_=y_values)
        observation_sum_df_['observation_sum'] = adjusted_values
        return observation_sum_df_

# ---------------------------
# main definition of program
def main_func():
    root = GUI()
    root.title('Wetterderivate und Klima v_b0.1.0')
    icon_path = root.get_local_path()
    root.iconbitmap(icon_path + 'icon.ico')
    root.geometry("1920x1080")
    root.resizable(width=False, height=False)
    root.mainloop()

if __name__ == "__main__":
    main_func()
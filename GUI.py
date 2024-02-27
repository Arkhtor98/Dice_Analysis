import sys
import os
from PyQt6.QtWidgets import QRadioButton, QPushButton, QGroupBox, QHBoxLayout, \
    QSpinBox, QLabel, QButtonGroup, QApplication, QVBoxLayout, QWidget, QDoubleSpinBox, QProgressBar, \
    QGridLayout, QSizePolicy, QCheckBox
from PyQt6.QtCore import QThread , pyqtSignal, Qt
from PyQt6 import QtGui
from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg as FigureCanvas
from matplotlib import pyplot as plt
import time
import pandas as pd



class handle_simulation(QThread):
    simulation = pyqtSignal(int)
    def __init__(self, parameters, results):
        super().__init__()
        self.parameters = parameters
        self.results = results
    def run(self):
        #sim.run_sim(self.parameters,self.results)
        self.simulation.emit(1)

class update_progress_bar(QThread):
    progress = pyqtSignal(int)
    def __init__(self, results, parameters):
        super().__init__()
        self.parameters = parameters
        self.results = results
    def run(self):
        #check every 100ms the number of line or results and update the progress bar
        while len(self.results) < self.parameters["GEN"]:
            time.sleep(0.1)
            percent = int(len(self.results) / self.parameters["GEN"] * 100)
            self.progress.emit(percent)
        self.progress.emit(100)





class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.parameters = {}
        self.initUI()

# TODO : backend-link for sim launch
    def launch_sim(self):
        self.prog_bar.setValue(0)
        self.results = pd.DataFrame(columns=["generation", "total population",
                                        "population increase %",
                                        "proportion of dove", "proportion of hawk", "avg life expectancy","prop_dove_rolling","total_pop_avg"])

        if self.seed.value() < 0:
            self.parameters["SEED"] = -1
        else:
            self.parameters["SEED"] = self.seed.value()


        self.thread = handle_simulation(self.parameters, self.results)
        self.th2 = update_progress_bar(self.results, self.parameters)

        self.th2.progress.connect(self.update_babar)
        self.thread.simulation.connect(self.gen_graph)

        self.thread.start()
        self.th2.start()
        self.thread.quit()
        self.th2.quit()
# TODO : link the plot function
    def gen_graph(self, a):
        #new_fig = ds.get_plot_2(self.results, self.parameters)
        #self.handle_simulation_result(new_fig)
        pass

    def stop_threads(self):
        if hasattr(self,'thread') and self.thread.isRunning():
            self.thread.quit()
            self.thread.terminate()
            self.thread.wait()

        if hasattr(self,'th2') and self.th2.isRunning():
            self.th2.quit()
            self.th2.terminate()
            self.th2.wait()
        self.handle_simulation_result(None)
        self.update_babar(0)
    def update_babar(self, percent):
        self.prog_bar.setValue(percent)
        self.prog_bar.update()


    def handle_simulation_result(self, new_fig):
        self.fig = new_fig

        new_canvas = FigureCanvas(self.fig)
        #self.fig_box.removeWidget(self.image)
        self.fig_box.replaceWidget(self.canvas, new_canvas)
        self.canvas = new_canvas
        self.change_to_graph()
        self.switch_graph.setChecked(True)

    def update_groupbox_graph(self):
        self.groupbox_graph.update()

    def change_to_graph(self):
            self.image.hide()
            self.canvas.show()


    def change_to_default(self,):
        self.image.show()
        self.canvas.hide()

    ################
    # creating the UI main definition and layout
    ################
    def fishing_hit_change(self,value):
        state = Qt.CheckState(value)
        if state == Qt.CheckState.Checked:
            self.rall_hit.setChecked(True)

    def fishing_wound_change(self,value):
        state = Qt.CheckState(value)
        if state == Qt.CheckState.Checked:
            self.rall_wound.setChecked(True)
    def initUI(self):
        # Get screen dimensions
        screen = QtGui.QGuiApplication.primaryScreen()
        screen_geo = screen.availableGeometry()
        screen_width = screen_geo.width()
        screen_height = screen_geo.height()

        #create progress bar
        self.prog_bar = QProgressBar(self)


        #create the threads
        self.thread = handle_simulation(None,None)
        self.th2 = update_progress_bar(None,None)
        #create the matrix of parameters


        # Create a QVBoxLayout and add the FigureCanvasQTAgg widget to it

        #self.fig_box = QVBoxLayout()
        #self.fig_box.addWidget(self.canvas)

        # Create a layout for the start and stop buttons
        #lunch_box = QVBoxLayout()
        #lunch_box.addWidget(self.launch)
        #lunch_box.addWidget(self.stop_button)

        ################
        # creating layouts for the left side ( all the settings )
        ################

        #button groups, qlayouts

        ################
        # creating the group boxes for the left side ( all the settings )
        ################
        #groupbox for grouping shit

        ################
        # creating the layouts and the group boxes for the right side ( viewing the graph
        ################

        # choice_graph = QHBoxLayout()
        # choice_graph.addWidget(self.switch_default)
        # choice_graph.addWidget(self.switch_graph)
        # choice_graph.addWidget(self.save)
        #
        #
        # display_box = QGroupBox('Graph', self)
        # display_box.setStyleSheet('QGroupBox{border: 2px solid black;}')
        # display_box.setContentsMargins(10, 10, 10, 10)
        # display_box.setLayout(self.fig_box)
        #
        # right_side = QVBoxLayout()
        # right_side.addWidget(self.prog_bar)
        # right_side.addLayout(choice_graph)
        # right_side.addWidget(display_box)

       #Setup main windows

        main_layout = QHBoxLayout()
        ###################################################
        ### LEFT SIDE
        ###################################################
        left_side = QVBoxLayout()
        base_stats = QGroupBox("Statlines")
        modifiers_box = QGroupBox("Modifiers")
        comparative_box = QGroupBox("Comparisons")

        ########### base stats
        box_stats = QVBoxLayout()
        base_stats.setLayout(box_stats)


        attacks_box = QGridLayout()
        attacks_label = QLabel("Attacks")
        self.number_dice_attacks = QSpinBox()
        attacks_random_lab =QLabel("D")

        self.attacks_random = QSpinBox()
        self.attacks_random.setMinimum(0)
        self.attacks_random.setValue(0)
        attacks_add_lab = QLabel("+")
        attacks_add_lab.adjustSize()
        self.attacks_det = QSpinBox()
        self.attacks_det.setMinimum(0)
        box_stats.addLayout(attacks_box)
        attacks_box.addWidget(attacks_label,0,0)
        attacks_box.addWidget(self.number_dice_attacks,0,1)
        attacks_box.addWidget(attacks_random_lab,0,2)
        attacks_box.addWidget(self.attacks_random,0,3)
        attacks_box.addWidget(attacks_add_lab,0,4)
        attacks_box.addWidget(self.attacks_det,0,5)

        other_stats = QGridLayout()
        to_hit_lab = QLabel("To hit")
        self.to_hit = QSpinBox()
        self.to_hit.setMinimum(2)
        self.to_hit.setMaximum(6)
        other_stats.addWidget(to_hit_lab,0,0)
        other_stats.addWidget(self.to_hit,0,1)

        strength_lab = QLabel("Strength")
        self.strength = QSpinBox()
        other_stats.addWidget(strength_lab,0,2)
        other_stats.addWidget(self.strength,0,3)

        toughness_lab = QLabel("Target toughness")
        self.toughness = QSpinBox()
        other_stats.addWidget(toughness_lab,2,0)
        other_stats.addWidget(self.toughness,2,1)

        armor_pen_lab = QLabel("Armor Penetration")
        self.armor_pen = QSpinBox()
        self.armor_pen.setMinimum(0)
        other_stats.addWidget(armor_pen_lab,2,2)
        other_stats.addWidget(self.armor_pen,2,3)

        save_lab = QLabel("Target save")
        self.save = QSpinBox()
        other_stats.addWidget(save_lab,4,0)
        other_stats.addWidget(self.save,4,1)

        inv_save_lab = QLabel("Target invulnerable save")
        self.inv_save = QSpinBox()
        self.inv_save.setValue(7)
        self.inv_save.setMaximum(7)
        other_stats.addWidget(inv_save_lab,4,2)
        other_stats.addWidget(self.inv_save,4,3)

        fnp_lab = QLabel("Feel No Pain")
        self.fnp = QSpinBox()
        self.fnp.setValue(7)
        other_stats.addWidget(fnp_lab,6,0)
        other_stats.addWidget(self.fnp,6,1)

        wpm_lab = QLabel("Wounds per model")
        self.wpm = QSpinBox()
        self.wpm.setMinimum(1)
        other_stats.addWidget(wpm_lab,6,2)
        other_stats.addWidget(self.wpm,6,3)
        box_stats.addLayout(other_stats)

        left_side.addWidget(base_stats)

        ### Modifiers
        modifiers = QGridLayout()
        modifiers_box.setLayout(modifiers)

        self.r1_hit = QCheckBox("Reroll 1 to hit")
        modifiers.addWidget(self.r1_hit,0,0)
        self.r1_wound = QCheckBox("Reroll 1 to wound")
        modifiers.addWidget(self.r1_wound,0,1)
        self.rall_hit = QCheckBox("Reroll hits")
        modifiers.addWidget(self.rall_hit,1,0)
        self.rall_wound = QCheckBox("Reroll wounds")
        modifiers.addWidget(self.rall_wound,1,1)
        self.fishing_hits = QCheckBox("Fishing for crits, hits")
        self.fishing_hits.stateChanged.connect(self.fishing_hit_change)
        modifiers.addWidget(self.fishing_hits,2,0)
        self.fishing_wounds = QCheckBox("Fishing for crits, wounds")
        self.fishing_wounds.stateChanged.connect(self.fishing_wound_change)
        modifiers.addWidget(self.fishing_wounds,2,1)
        sustained_label = QLabel("Sustained Hits")
        self.sustained = QSpinBox()
        modifiers.addWidget(sustained_label,4,0)
        modifiers.addWidget(self.sustained,4,1)
        self.lethal = QCheckBox("Lethal hits")
        modifiers.addWidget(self.lethal,3,0)
        self.deva= QCheckBox("Devastating Wounds")
        modifiers.addWidget(self.deva,3,1)
        anti_lab = QLabel("Anti")
        self.anti = QSpinBox()
        modifiers.addWidget(anti_lab,5,0)
        modifiers.addWidget(self.anti,5,1)
        crit_hits_lab = QLabel("Critical Hits")
        self.crit_hits = QSpinBox()
        modifiers.addWidget(crit_hits_lab,6,0)
        modifiers.addWidget(self.crit_hits,6,1)



        left_side.addWidget(modifiers_box)


        main_layout.addLayout(left_side)

        ###################################################
        ### RIGHT SIDE
        ###################################################
        right_side = QVBoxLayout()
        main_layout.addLayout(right_side)
        dummy = QRadioButton("dummy")
        right_side.addWidget(dummy)


        # Set the main layout
        self.setLayout(main_layout)
        # Set default window size as a ratio of the screen size
        # Set window size to 80% of screen size
        window_width = int(screen_width * 0.8)
        window_height = int(screen_height * 0.8)
        self.setGeometry(0, 0, window_width, window_height)
        self.setWindowTitle('Dice Analysis')
        self.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()

    sys.exit(app.exec())
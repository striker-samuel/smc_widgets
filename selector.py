# Created by samuel.martin199@outlook.com at 22/05/2023

from PySide2 import QtWidgets
from PySide2.QtCore import Signal


class Selector(QtWidgets.QWidget):
    """
    QtWidget containing comboboxes to perform selection from submitted control dictionary
    """

    SELECTION_CHANGED = Signal(str, str)
    INFO_UPDATED = Signal(dict)

    def __init__(self, control_structure):
        super(Selector, self).__init__()

        self._selection_state = {}
        self.cbbs = {}

        main_layout = QtWidgets.QVBoxLayout()
        main_layout.setSpacing(0)

        self.setLayout(main_layout)

        self._control_structure = control_structure

        self.SELECTION_CHANGED.connect(self.register_state_change)

        self._widgets = {}

        self.populate()
        self.show()

    def setup_cbbs(self, setup_state):

        print(self.cbbs)

        for key, value in setup_state.items():
            print(key, value)

            if key in self.cbbs.keys():
                self.cbbs[key].setCurrentText(value)

    def update_combo_box(self, to_update, list, key, uno=""):

        to_update.blockSignals(True)
        to_update.clear()
        to_update.blockSignals(False)

        if list == []:
            self.SELECTION_CHANGED.emit(key, "%s__%s" % (uno, ""))

        to_update.addItems(list)

    @property
    def selection_state(self):
        return self._selection_state

    def register_state_change(self, key, value):

        parent_key_name, child_key_name = key.split("__")

        if "__" in value:
            val, val_child = value.split("__")
        else:
            val = value
            val_child = ""

        if parent_key_name:
            self._selection_state[parent_key_name] = val

        if child_key_name:
            self._selection_state[child_key_name] = val_child

        self.INFO_UPDATED.emit(self._selection_state)

    def populate(self):

        if self.layout():

            for i in reversed(range(self.layout().count())):
                self.layout().itemAt(i).widget().setParent(None)

        for key, values in self.control_structure.items():

            if "__" not in key:
                raise Exception("Control dic keys must follow format aaa__aaa")

            if type(values) == dict:

                dic_combo = QtWidgets.QComboBox()

                pretty_name = " ".join(["--"] + [x.capitalize() for x in key.split("__")[0].split("_")] + [":"])
                label = QtWidgets.QLabel(pretty_name)
                selector_wdg = QtWidgets.QWidget()
                selector_wdg_lyt = QtWidgets.QHBoxLayout()
                selector_wdg_lyt.setContentsMargins(0, 5, 0, 0)
                selector_wdg_lyt.addWidget(label)
                selector_wdg_lyt.addWidget(dic_combo)
                selector_wdg.setLayout(selector_wdg_lyt)

                self.layout().addWidget(selector_wdg)

                dic_combo.addItems(values.keys())
                dic_combo_second_lvl = QtWidgets.QComboBox()

                dic_combo.currentIndexChanged.connect(

                    lambda x, local_key=key, combo_box_uno=dic_combo, combo_box_dos=dic_combo_second_lvl:
                    self.update_combo_box(combo_box_dos, self.control_structure[local_key][combo_box_uno.itemText(x)],
                                          local_key, combo_box_uno.currentText())

                )

                self.update_combo_box(dic_combo_second_lvl, self.control_structure[key][dic_combo.itemText(0)], key=key)

                # dic_combo_second_lvl.addItems(values)
                dic_combo_second_lvl.currentIndexChanged.connect(
                    lambda x, local_key=key, combo_box_uno=dic_combo,
                           combo_box_dos=dic_combo_second_lvl: self.SELECTION_CHANGED.emit(local_key,
                                                                                           "%s__%s" % (
                                                                                               combo_box_uno.currentText(),
                                                                                               combo_box_dos.itemText(
                                                                                                   x))))

                self.SELECTION_CHANGED.emit(key,
                                            "%s__%s" % (
                                                dic_combo.currentText(),
                                                dic_combo_second_lvl.itemText(0)))

                label = QtWidgets.QLabel("  >  %s:" % (key.split("__")[1].capitalize()))
                selector_wdg = QtWidgets.QWidget()
                selector_wdg_lyt = QtWidgets.QHBoxLayout()
                selector_wdg_lyt.setContentsMargins(0, 5, 0, 0)
                selector_wdg_lyt.addWidget(label)
                selector_wdg_lyt.addWidget(dic_combo_second_lvl)
                selector_wdg.setLayout(selector_wdg_lyt)

                self.cbbs[key.split("__")[0]] = dic_combo
                self.cbbs[key.split("__")[1]] = dic_combo_second_lvl

                dic_combo.setCurrentIndex(0)
                dic_combo_second_lvl.setCurrentIndex(0)
                self.layout().addWidget(selector_wdg)


            else:

                dic_combo = QtWidgets.QComboBox()

                self.cbbs[key.split("__")[0]] = dic_combo

                pretty_name = " ".join([">"] + [x.capitalize() for x in key.split("__")[0].split("_")] + [":"])

                label = QtWidgets.QLabel(pretty_name)
                selector_wdg = QtWidgets.QWidget()
                selector_wdg_lyt = QtWidgets.QHBoxLayout()
                selector_wdg_lyt.setContentsMargins(0, 5, 0, 0)
                selector_wdg_lyt.addWidget(label)
                selector_wdg_lyt.addWidget(dic_combo)
                selector_wdg.setLayout(selector_wdg_lyt)

                self.layout().addWidget(selector_wdg)

                dic_combo.currentIndexChanged.connect(
                    lambda x, local_key=key, combo_box=dic_combo: self.SELECTION_CHANGED.emit(local_key,
                                                                                              combo_box.itemText(x)))
                dic_combo.addItems(values)
                dic_combo.setCurrentIndex(0)

        # spacer = QtWidgets.QWidget()
        # spacer.setLayout(QtWidgets.QVBoxLayout())
        # self.layout().addWidget(spacer)
        # self.layout().setStretch(self.layout().count()-1,1)

    @property
    def control_structure(self):
        return self._control_structure


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    app.setApplicationDisplayName("Selector")

    sequences_control_dic = {

        "sequence_group__": ["film", "demo", "marketing"],
        "task__step": {"animation": ["blocking", "splines", "refine"]},
        "silo__": ["work", "publish"],

    }

    selector = Selector(sequences_control_dic)
    selector.INFO_UPDATED.connect(print)
    # selector.SELECTION_CHANGED.connect(print)
    print(selector.selection_state)

    sys.exit(app.exec_())

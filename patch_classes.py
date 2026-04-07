import re

with open('domain_generator_gui.py', 'r', encoding='utf-8') as f:
    content = f.read()

start = content.find("class GeneratorThread(QThread):")

new_classes = """class GeneratorThread(QThread):
    progress = pyqtSignal(str)
    finished = pyqtSignal(int, str)
    error = pyqtSignal(str)

    def __init__(self, mode, min_len, max_len, charset, exclude, custom_words, pattern_str, tlds, batch_size, out_dir, lang="zh"):
        super().__init__()
        self.mode = mode
        self.min_len = min_len
        self.max_len = max_len
        self.charset = charset
        self.exclude = exclude
        self.custom_words = custom_words
        self.pattern_str = pattern_str
        self.tlds = tlds
        self.batch_size = batch_size
        self.out_dir = out_dir
        self.lang = lang

    def run(self):
        try:
            t = TRANSLATIONS[self.lang]
            if not os.path.exists(self.out_dir):
                os.makedirs(self.out_dir)

            self.progress.emit(t["msg_gen_combo"])
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            
            if self.mode == "hacks":
                words = []
                words.extend(WORDS_2 + WORDS_3 + WORDS_4 + WORDS_5 + WORDS_6)
                if self.custom_words:
                    cw_list = [w.strip().lower() for w in self.custom_words.split(',') if w.strip()]
                    words.extend(cw_list)
                words = list(set(words))
                domain_gen = generate_hacks(words, self.tlds)
                
            else:
                prefixes = []
                if self.mode == "brute":
                    prefixes = generate_brute_prefixes(self.min_len, self.max_len, self.charset, self.exclude)
                elif self.mode == "words":
                    if self.min_len <= 2 <= self.max_len:
                        prefixes.extend(WORDS_2)
                    if self.min_len <= 3 <= self.max_len:
                        prefixes.extend(WORDS_3)
                    if self.min_len <= 4 <= self.max_len:
                        prefixes.extend(WORDS_4)
                    if self.min_len <= 5 <= self.max_len:
                        prefixes.extend(WORDS_5)
                    if self.min_len <= 6 <= self.max_len:
                        prefixes.extend(WORDS_6)
                    
                    if self.custom_words:
                        cw_list = [w.strip().lower() for w in self.custom_words.split(',') if w.strip()]
                        prefixes.extend(cw_list)
                        
                    prefixes = list(set(prefixes))
                    if not prefixes:
                        self.error.emit(t["err_no_words"])
                        return
                elif self.mode == "pattern":
                    prefixes = generate_pattern_prefixes(self.pattern_str)
                    if not prefixes:
                        self.error.emit(t["err_pattern_empty"])
                        return
                
                self.progress.emit(t["msg_gen_prefix"].format(len(prefixes)))
                domain_gen = generate_domains(prefixes, self.tlds)

            batch = []
            file_index = 1
            total_generated = 0

            for domain in domain_gen:
                batch.append(domain)
                if len(batch) >= self.batch_size:
                    self._write_batch(batch, file_index, self.out_dir, timestamp)
                    total_generated += len(batch)
                    batch = []
                    file_index += 1
                    self.progress.emit(t["msg_gen_count"].format(total_generated))

            if batch:
                self._write_batch(batch, file_index, self.out_dir, timestamp)
                total_generated += len(batch)

            self.finished.emit(total_generated, self.out_dir)

        except Exception as e:
            self.error.emit(str(e))

    def _write_batch(self, batch, file_index, output_dir, timestamp):
        filename = os.path.join(output_dir, f"domains_{timestamp}_part_{file_index}.txt")
        with open(filename, "w", encoding="utf-8") as f:
            for domain in batch:
                f.write(f"{domain},\\n")

class DomainGeneratorApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.lang = "zh"
        self.setWindowTitle(TRANSLATIONS[self.lang]["title"])
        self.resize(750, 650)

        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        main_layout = QVBoxLayout(main_widget)

        # Top layout for language switch
        top_layout = QHBoxLayout()
        top_layout.addStretch()
        self.btn_lang = QPushButton(TRANSLATIONS[self.lang]["btn_lang"])
        self.btn_lang.clicked.connect(self.toggle_language)
        top_layout.addWidget(self.btn_lang)
        main_layout.addLayout(top_layout)

        self.tabs = QTabWidget()
        main_layout.addWidget(self.tabs)

        self.init_mode_tab()
        self.init_tld_tab()
        self.init_output_tab()

        # Status & Generate (Global at bottom)
        bottom_layout = QVBoxLayout()
        self.status_label = QLabel(TRANSLATIONS[self.lang]["status_ready"])
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setStyleSheet("color: blue; font-weight: bold;")
        bottom_layout.addWidget(self.status_label)

        self.btn_generate = QPushButton(TRANSLATIONS[self.lang]["btn_generate"])
        self.btn_generate.setMinimumHeight(40)
        self.btn_generate.setStyleSheet("font-size: 16px; font-weight: bold;")
        self.btn_generate.clicked.connect(self.start_generation)
        bottom_layout.addWidget(self.btn_generate)
        
        # Copyright
        self.copyright_label = QLabel(TRANSLATIONS[self.lang]["copyright"])
        self.copyright_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.copyright_label.setStyleSheet("color: gray; font-size: 12px; margin-top: 10px;")
        bottom_layout.addWidget(self.copyright_label)

        main_layout.addLayout(bottom_layout)
        self.update_ui_language()

    def toggle_language(self):
        self.lang = "en" if self.lang == "zh" else "zh"
        self.update_ui_language()

    def update_ui_language(self):
        t = TRANSLATIONS[self.lang]
        self.setWindowTitle(t["title"])
        self.btn_lang.setText(t["btn_lang"])
        
        self.tabs.setTabText(0, t["tab_mode"])
        self.tabs.setTabText(1, t["tab_tld"])
        self.tabs.setTabText(2, t["tab_output"])
        
        self.mode_group.setTitle(t["group_mode"])
        self.radio_brute.setText(t["radio_brute"])
        self.radio_words.setText(t["radio_words"])
        self.radio_pattern.setText(t["radio_pattern"])
        self.radio_hacks.setText(t["radio_hacks"])
        
        self.lbl_brute_min.setText(t["brute_min"])
        self.lbl_brute_max.setText(t["brute_max"])
        self.lbl_brute_charset.setText(t["brute_charset"])
        self.lbl_brute_exclude.setText(t["brute_exclude"])
        self.cb_lowercase.setText(t["cb_lower"])
        self.cb_numbers.setText(t["cb_num"])
        self.exclude_edit.setPlaceholderText(t["exclude_ph"])
        
        self.lbl_words_len.setText(t["words_len"])
        self.lbl_words_to.setText(t["words_to"])
        self.lbl_words_custom.setText(t["words_custom"])
        self.custom_words_edit.setPlaceholderText(t["words_custom_ph"])
        
        self.lbl_pattern.setText(t["pattern_label"])
        self.pattern_edit.setPlaceholderText(t["pattern_ph"])
        self.lbl_pattern_ex.setText(t["pattern_ex"])
        
        self.lbl_hacks.setText(t["hacks_label"])
        self.lbl_hacks_desc.setText(t["hacks_desc"])
        self.hacks_custom_edit.setPlaceholderText(t["hacks_ph"])
        
        self.lbl_tld_len.setText(t["tld_len_label"])
        self.btn_len2.setText(t["btn_len2"])
        self.btn_len3.setText(t["btn_len3"])
        self.btn_len4.setText(t["btn_len4"])
        self.lbl_tld_cat.setText(t["tld_cat_label"])
        self.btn_clear_all.setText(t["btn_clear_all"])
        
        for btn, cat in self.cat_buttons:
            btn.setText(f"+ {cat}")
            
        self.group_output.setTitle(t["group_output"])
        self.lbl_batch.setText(t["batch_label"])
        self.lbl_out_dir.setText(t["out_dir_label"])
        self.btn_browse.setText(t["btn_browse"])
        
        self.btn_generate.setText(t["btn_generate"])
        self.copyright_label.setText(t["copyright"])
        if self.btn_generate.isEnabled():
            self.status_label.setText(t["status_ready"])

    def init_mode_tab(self):
        mode_tab = QWidget()
        layout = QVBoxLayout(mode_tab)

        self.mode_group = QGroupBox()
        mode_h_layout = QHBoxLayout()
        
        self.radio_brute = QRadioButton()
        self.radio_words = QRadioButton()
        self.radio_pattern = QRadioButton()
        self.radio_hacks = QRadioButton()
        
        self.radio_brute.setChecked(True)
        
        self.mode_btn_group = QButtonGroup()
        self.mode_btn_group.addButton(self.radio_brute, 0)
        self.mode_btn_group.addButton(self.radio_words, 1)
        self.mode_btn_group.addButton(self.radio_pattern, 2)
        self.mode_btn_group.addButton(self.radio_hacks, 3)
        
        mode_h_layout.addWidget(self.radio_brute)
        mode_h_layout.addWidget(self.radio_words)
        mode_h_layout.addWidget(self.radio_pattern)
        mode_h_layout.addWidget(self.radio_hacks)
        self.mode_group.setLayout(mode_h_layout)
        layout.addWidget(self.mode_group)

        self.settings_stack = QStackedWidget()
        
        # 1. Brute Settings
        brute_widget = QWidget()
        brute_layout = QGridLayout(brute_widget)
        self.lbl_brute_min = QLabel()
        brute_layout.addWidget(self.lbl_brute_min, 0, 0)
        self.brute_min_spin = QSpinBox()
        self.brute_min_spin.setRange(1, 20)
        self.brute_min_spin.setValue(1)
        brute_layout.addWidget(self.brute_min_spin, 0, 1)
        
        self.lbl_brute_max = QLabel()
        brute_layout.addWidget(self.lbl_brute_max, 1, 0)
        self.brute_max_spin = QSpinBox()
        self.brute_max_spin.setRange(1, 20)
        self.brute_max_spin.setValue(2)
        brute_layout.addWidget(self.brute_max_spin, 1, 1)
        
        self.lbl_brute_charset = QLabel()
        brute_layout.addWidget(self.lbl_brute_charset, 2, 0)
        charset_layout = QHBoxLayout()
        self.cb_lowercase = QCheckBox()
        self.cb_lowercase.setChecked(True)
        self.cb_numbers = QCheckBox()
        self.cb_numbers.setChecked(True)
        charset_layout.addWidget(self.cb_lowercase)
        charset_layout.addWidget(self.cb_numbers)
        brute_layout.addLayout(charset_layout, 2, 1)
        
        self.lbl_brute_exclude = QLabel()
        brute_layout.addWidget(self.lbl_brute_exclude, 3, 0)
        self.exclude_edit = QLineEdit()
        brute_layout.addWidget(self.exclude_edit, 3, 1)
        self.settings_stack.addWidget(brute_widget)

        # 2. Words Settings
        words_widget = QWidget()
        words_layout = QGridLayout(words_widget)
        self.lbl_words_len = QLabel()
        words_layout.addWidget(self.lbl_words_len, 0, 0)
        
        len_layout = QHBoxLayout()
        self.words_min_spin = QSpinBox()
        self.words_min_spin.setRange(2, 6)
        self.words_min_spin.setValue(2)
        len_layout.addWidget(self.words_min_spin)
        self.lbl_words_to = QLabel()
        len_layout.addWidget(self.lbl_words_to)
        self.words_max_spin = QSpinBox()
        self.words_max_spin.setRange(2, 6)
        self.words_max_spin.setValue(6)
        len_layout.addWidget(self.words_max_spin)
        words_layout.addLayout(len_layout, 0, 1)
        
        self.lbl_words_custom = QLabel()
        words_layout.addWidget(self.lbl_words_custom, 1, 0)
        self.custom_words_edit = QLineEdit()
        words_layout.addWidget(self.custom_words_edit, 1, 1)
        self.settings_stack.addWidget(words_widget)

        # 3. Pattern Settings
        pattern_widget = QWidget()
        pattern_layout = QVBoxLayout(pattern_widget)
        self.lbl_pattern = QLabel()
        pattern_layout.addWidget(self.lbl_pattern)
        self.pattern_edit = QLineEdit()
        pattern_layout.addWidget(self.pattern_edit)
        self.lbl_pattern_ex = QLabel()
        pattern_layout.addWidget(self.lbl_pattern_ex)
        pattern_layout.addStretch()
        self.settings_stack.addWidget(pattern_widget)

        # 4. Hacks Settings
        hacks_widget = QWidget()
        hacks_layout = QVBoxLayout(hacks_widget)
        self.lbl_hacks = QLabel()
        hacks_layout.addWidget(self.lbl_hacks)
        self.lbl_hacks_desc = QLabel()
        hacks_layout.addWidget(self.lbl_hacks_desc)
        self.hacks_custom_edit = QLineEdit()
        hacks_layout.addWidget(self.hacks_custom_edit)
        hacks_layout.addStretch()
        self.settings_stack.addWidget(hacks_widget)

        layout.addWidget(self.settings_stack)
        self.tabs.addTab(mode_tab, "")

        self.mode_btn_group.idClicked.connect(self.settings_stack.setCurrentIndex)

    def init_tld_tab(self):
        tld_tab = QWidget()
        tld_main_layout = QHBoxLayout(tld_tab)
        
        quick_layout = QVBoxLayout()
        self.lbl_tld_len = QLabel()
        quick_layout.addWidget(self.lbl_tld_len)
        self.btn_len2 = QPushButton()
        self.btn_len2.clicked.connect(lambda: self.select_by_length(2))
        quick_layout.addWidget(self.btn_len2)
        self.btn_len3 = QPushButton()
        self.btn_len3.clicked.connect(lambda: self.select_by_length(3))
        quick_layout.addWidget(self.btn_len3)
        self.btn_len4 = QPushButton()
        self.btn_len4.clicked.connect(lambda: self.select_by_length(4))
        quick_layout.addWidget(self.btn_len4)
        
        quick_layout.addSpacing(10)
        self.lbl_tld_cat = QLabel()
        quick_layout.addWidget(self.lbl_tld_cat)
        
        self.cat_buttons = []
        for cat_name in CATEGORIZED_TLDS.keys():
            btn = QPushButton()
            btn.clicked.connect(lambda checked, c=cat_name: self.select_by_category(c))
            quick_layout.addWidget(btn)
            self.cat_buttons.append((btn, cat_name))
            
        quick_layout.addStretch()
        self.btn_clear_all = QPushButton()
        self.btn_clear_all.setStyleSheet("color: red;")
        self.btn_clear_all.clicked.connect(self.clear_selection)
        quick_layout.addWidget(self.btn_clear_all)

        tld_main_layout.addLayout(quick_layout, 1)

        list_layout = QVBoxLayout()
        self.tld_list = QListWidget()
        self.tld_list.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)
        self.tld_list.addItems(ALL_TLDS)
        
        default_tlds = ["com", "net", "org", "io", "co", "ai", "cc", "so"]
        for i in range(self.tld_list.count()):
            item = self.tld_list.item(i)
            if item.text() in default_tlds:
                item.setSelected(True)

        list_layout.addWidget(self.tld_list)
        tld_main_layout.addLayout(list_layout, 2)

        self.tabs.addTab(tld_tab, "")

    def init_output_tab(self):
        out_tab = QWidget()
        layout = QVBoxLayout(out_tab)
        
        self.group_output = QGroupBox()
        g_layout = QGridLayout(self.group_output)
        
        self.lbl_batch = QLabel()
        g_layout.addWidget(self.lbl_batch, 0, 0)
        self.batch_spin = QSpinBox()
        self.batch_spin.setRange(1, 1000000)
        self.batch_spin.setValue(5000)
        g_layout.addWidget(self.batch_spin, 0, 1)
        
        self.lbl_out_dir = QLabel()
        g_layout.addWidget(self.lbl_out_dir, 1, 0)
        dir_layout = QHBoxLayout()
        self.out_dir_edit = QLineEdit(os.path.join(os.path.expanduser("~"), "Desktop", "DomainOutput"))
        self.out_dir_edit.setReadOnly(True)
        dir_layout.addWidget(self.out_dir_edit)
        self.btn_browse = QPushButton()
        self.btn_browse.clicked.connect(self.browse_dir)
        dir_layout.addWidget(self.btn_browse)
        g_layout.addLayout(dir_layout, 1, 1)
        
        layout.addWidget(self.group_output)
        layout.addStretch()
        
        self.tabs.addTab(out_tab, "")

    def select_by_length(self, length):
        for i in range(self.tld_list.count()):
            item = self.tld_list.item(i)
            tld = item.text()
            if length == 4:
                if len(tld) >= 4:
                    item.setSelected(True)
            else:
                if len(tld) == length:
                    item.setSelected(True)

    def select_by_category(self, category):
        tlds_in_cat = set(CATEGORIZED_TLDS[category])
        for i in range(self.tld_list.count()):
            item = self.tld_list.item(i)
            if item.text() in tlds_in_cat:
                item.setSelected(True)
                
    def clear_selection(self):
        self.tld_list.clearSelection()

    def browse_dir(self):
        t = TRANSLATIONS[self.lang]
        dir_path = QFileDialog.getExistingDirectory(self, t["out_dir_label"])
        if dir_path:
            self.out_dir_edit.setText(dir_path)

    def start_generation(self):
        t = TRANSLATIONS[self.lang]
        mode_id = self.mode_btn_group.checkedId()
        modes = ["brute", "words", "pattern", "hacks"]
        mode = modes[mode_id]
        
        min_len = 1
        max_len = 1
        charset = ""
        exclude = ""
        custom_words = ""
        pattern_str = ""
        
        if mode == "brute":
            min_len = self.brute_min_spin.value()
            max_len = self.brute_max_spin.value()
            exclude = self.exclude_edit.text()
            if self.cb_lowercase.isChecked(): charset += string.ascii_lowercase
            if self.cb_numbers.isChecked(): charset += string.digits
            if not charset:
                QMessageBox.warning(self, t["box_err"], t["err_charset"])
                return
            if min_len > max_len:
                QMessageBox.warning(self, t["box_err"], t["err_len"])
                return
                
        elif mode == "words":
            min_len = self.words_min_spin.value()
            max_len = self.words_max_spin.value()
            custom_words = self.custom_words_edit.text()
            if min_len > max_len:
                QMessageBox.warning(self, t["box_err"], t["err_len"])
                return
                
        elif mode == "pattern":
            pattern_str = self.pattern_edit.text().strip()
            if not pattern_str:
                QMessageBox.warning(self, t["box_err"], t["err_pattern"])
                return
                
        elif mode == "hacks":
            custom_words = self.hacks_custom_edit.text()

        batch_size = self.batch_spin.value()
        out_dir = self.out_dir_edit.text()

        selected_tlds = [item.text() for item in self.tld_list.selectedItems()]
        if not selected_tlds:
            QMessageBox.warning(self, t["box_err"], t["err_tld"])
            return

        self.btn_generate.setEnabled(False)
        self.status_label.setText(t["status_generating"])
        self.status_label.setStyleSheet("color: orange; font-weight: bold;")

        self.thread = GeneratorThread(mode, min_len, max_len, charset, exclude, custom_words, pattern_str, selected_tlds, batch_size, out_dir, self.lang)
        self.thread.progress.connect(self.update_progress)
        self.thread.finished.connect(self.on_finished)
        self.thread.error.connect(self.on_error)
        self.thread.start()

    def update_progress(self, msg):
        self.status_label.setText(msg)

    def on_finished(self, total, out_dir):
        t = TRANSLATIONS[self.lang]
        self.status_label.setText(t["msg_done"].format(total))
        self.status_label.setStyleSheet("color: green; font-weight: bold;")
        self.btn_generate.setEnabled(True)
        QMessageBox.information(self, t["box_success"], t["box_success_msg"].format(total, out_dir))

    def on_error(self, err_msg):
        t = TRANSLATIONS[self.lang]
        self.status_label.setText(t["msg_err"].format(err_msg))
        self.status_label.setStyleSheet("color: red; font-weight: bold;")
        self.btn_generate.setEnabled(True)
        QMessageBox.critical(self, t["box_err"], t["box_err_msg"].format(err_msg))

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = DomainGeneratorApp()
    window.show()
    sys.exit(app.exec())
"""

content = content[:start] + new_classes

with open('domain_generator_gui.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("Classes updated.")

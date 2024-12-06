from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QLabel, 
                             QPushButton, QComboBox, QGridLayout, QFrame,
                             QScrollArea, QLineEdit, QSizePolicy)
from PyQt6.QtCore import Qt, pyqtSignal, QSize, QTimer
from PyQt6.QtGui import QPixmap, QColor, QPalette, QFont, QIcon

from ...models.draft import DraftState, DraftPhase, Champion
from ...models.team import Team
from ...models.player import Role
from ...utils.champion_assets import ChampionAssets
from ...ai.draft_ai import DraftAI

class ChampionIcon(QPushButton):
    """Custom widget for champion icons in the selection grid."""
    def __init__(self, champion: Champion, parent=None):
        super().__init__(parent)
        self.champion = champion
        self.setFixedSize(80, 80)
        self.setStyleSheet("""
            QPushButton {
                background-color: #1a1a1a;
                border: 1px solid #333333;
                border-radius: 5px;
                padding: 2px;
            }
            QPushButton:hover {
                background-color: #2a2a2a;
                border: 1px solid #666666;
            }
            QPushButton:disabled {
                background-color: #0a0a0a;
                border: 1px solid #222222;
                opacity: 0.5;
            }
        """)
        
        try:
            # Load champion portrait
            portrait_path = ChampionAssets.get_portrait_path(champion.name)
            icon = QIcon(portrait_path)
            self.setIcon(icon)
            self.setIconSize(QSize(76, 76))  # Slightly smaller than button size
            
            # Add tooltip with champion name
            self.setToolTip(champion.name)
        except FileNotFoundError:
            # If portrait not found, fallback to text
            self.setText(champion.name)

class PickBanSlot(QFrame):
    """Custom widget for pick/ban slots."""
    def __init__(self, slot_id: str, is_blue_side: bool):
        super().__init__()
        self.setFixedSize(80, 80)
        self.slot_id = slot_id
        color = "#4169E1" if is_blue_side else "#DC143C"
        self.setStyleSheet(f"""
            QFrame {{
                background-color: #1a1a1a;
                border: 2px solid {color};
                border-radius: 5px;
            }}
        """)
        self.champion = None
        
        # Add slot label
        layout = QVBoxLayout()
        label = QLabel(slot_id)
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        label.setStyleSheet("color: white;")
        layout.addWidget(label)
        self.setLayout(layout)

class DraftScreen(QWidget):
    draft_completed = pyqtSignal(DraftState)

    def __init__(self, draft_state: DraftState, main_window):
        super().__init__()
        self.draft_state = draft_state
        self.main_window = main_window
        self.selected_champion = None
        self.blue_pick_slots = []
        self.red_pick_slots = []
        self.blue_ban_slots = []
        self.red_ban_slots = []
        self.role_buttons = {}
        self.search_bar = None
        self.phase_label = None
        self.timer_label = None
        self.init_ui()
        
    def init_ui(self):
        """Initialize the draft screen UI."""
        self.setStyleSheet("""
            QWidget {
                background-color: #0a0a0a;
                color: white;
            }
        """)
        
        main_layout = QVBoxLayout()
        
        # Header with team names and phase
        header_layout = self._create_header()
        main_layout.addLayout(header_layout)
        
        # Main content area
        content_layout = QHBoxLayout()
        
        # Blue side picks/bans
        blue_layout = self._create_team_panel(self.draft_state.blue_team, True)
        content_layout.addLayout(blue_layout)
        
        # Champion selection area
        selection_layout = self._create_champion_selection()
        content_layout.addLayout(selection_layout, stretch=2)
        
        # Red side picks/bans
        red_layout = self._create_team_panel(self.draft_state.red_team, False)
        content_layout.addLayout(red_layout)
        
        main_layout.addLayout(content_layout)
        
        # Add lock-in button
        self.lock_in_button = QPushButton("Lock In")
        self.lock_in_button.setStyleSheet("""
            QPushButton {
                background-color: #1a1a1a;
                border: 2px solid #4CAF50;
                border-radius: 5px;
                color: white;
                padding: 8px 16px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #2a2a2a;
                border-color: #45a049;
            }
            QPushButton:disabled {
                background-color: #0a0a0a;
                border-color: #333333;
                color: #666666;
            }
        """)
        self.lock_in_button.setEnabled(False)
        self.lock_in_button.clicked.connect(self._handle_lock_in)
        
        # Add controls to footer
        controls_layout = QHBoxLayout()
        controls_layout.addStretch()
        controls_layout.addWidget(self.lock_in_button)
        
        main_layout.addLayout(controls_layout)
        self.setLayout(main_layout)
        
        # Set up timer
        self.timer = QTimer()
        self.timer.timeout.connect(self._update_timer)
        self.time_remaining = 30
        
        # Update UI and start first turn
        self.update_ui()
        self._start_turn()
    
    def _create_header(self):
        """Create the header with team names and current phase."""
        layout = QHBoxLayout()
        
        # Blue side (Home) team name
        blue_team_label = QLabel(f"{self.draft_state.blue_team.name} (Home)")
        blue_team_label.setStyleSheet("""
            QLabel {
                color: #4169E1;
                font-size: 18px;
                font-weight: bold;
            }
        """)
        layout.addWidget(blue_team_label)
        
        # Phase label in center
        self.phase_label = QLabel("Ban Phase 1")
        self.phase_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 20px;
                font-weight: bold;
            }
        """)
        layout.addWidget(self.phase_label)
        
        # Timer label
        self.timer_label = QLabel("30")
        self.timer_label.setStyleSheet("""
            QLabel {
                color: white;
                font-size: 20px;
                font-weight: bold;
                margin: 0 20px;
            }
        """)
        layout.addWidget(self.timer_label)
        
        # Red side (Away) team name
        red_team_label = QLabel(f"{self.draft_state.red_team.name} (Away)")
        red_team_label.setStyleSheet("""
            QLabel {
                color: #DC143C;
                font-size: 18px;
                font-weight: bold;
            }
        """)
        layout.addWidget(red_team_label)
        
        return layout

    def _create_team_panel(self, team: Team, is_blue_side: bool) -> QVBoxLayout:
        """Create a panel showing team's picks and bans."""
        layout = QVBoxLayout()
        
        # Bans (3 + 2)
        bans_layout = QGridLayout()
        for i in range(5):
            slot = PickBanSlot(f"B{i+1}", is_blue_side)
            row = 0 if i < 3 else 1
            col = i if i < 3 else i-3
            bans_layout.addWidget(slot, row, col)
            if is_blue_side:
                self.blue_ban_slots.append(slot)
            else:
                self.red_ban_slots.append(slot)
        layout.addLayout(bans_layout)
        
        # Spacing
        layout.addStretch()
        
        # Picks (5)
        picks_layout = QVBoxLayout()
        for i in range(5):
            slot = PickBanSlot(f"P{i+1}", is_blue_side)
            picks_layout.addWidget(slot)
            if is_blue_side:
                self.blue_pick_slots.append(slot)
            else:
                self.red_pick_slots.append(slot)
        layout.addLayout(picks_layout)
        
        return layout

    def _create_champion_selection(self) -> QVBoxLayout:
        """Create the champion selection area."""
        layout = QVBoxLayout()
        
        # Search bar
        self.search_bar = QLineEdit()
        self.search_bar.setPlaceholderText("Search champions...")
        self.search_bar.textChanged.connect(self._filter_champions)
        self.search_bar.setStyleSheet("""
            QLineEdit {
                background-color: #2a2a2a;
                border: 1px solid #444444;
                border-radius: 5px;
                padding: 8px;
                color: white;
                font-size: 14px;
            }
            QLineEdit:focus {
                border: 1px solid #666666;
            }
        """)
        layout.addWidget(self.search_bar)
        
        # Role filter buttons (optional)
        role_layout = QHBoxLayout()
        role_layout.setSpacing(5)
        for role in Role:
            role_btn = QPushButton(role.value)
            role_btn.setCheckable(True)
            role_btn.setFixedSize(80, 30)
            role_btn.setStyleSheet("""
                QPushButton {
                    background-color: #2a2a2a;
                    border: 1px solid #444444;
                    border-radius: 5px;
                    color: white;
                }
                QPushButton:checked {
                    background-color: #4a4a4a;
                    border: 1px solid #666666;
                }
                QPushButton:hover {
                    background-color: #3a3a3a;
                }
            """)
            role_btn.clicked.connect(lambda checked, r=role: self._filter_by_role(r, checked))
            role_layout.addWidget(role_btn)
            self.role_buttons[role] = role_btn
        role_layout.addStretch()
        layout.addLayout(role_layout)
        
        # Champion grid in a scroll area
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)
        scroll_area.setStyleSheet("""
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background: #2a2a2a;
                width: 10px;
                margin: 0px;
            }
            QScrollBar::handle:vertical {
                background: #666666;
                min-height: 20px;
                border-radius: 5px;
            }
            QScrollBar::add-line:vertical, QScrollBar::sub-line:vertical {
                height: 0px;
            }
        """)
        
        # Create widget for the grid
        grid_widget = QWidget()
        self.champion_grid = QGridLayout()
        self.champion_grid.setSpacing(5)
        self.champion_grid.setContentsMargins(5, 5, 5, 5)
        
        # Add champions to grid
        self._populate_champion_grid()
        
        grid_widget.setLayout(self.champion_grid)
        scroll_area.setWidget(grid_widget)
        layout.addWidget(scroll_area)
        
        return layout

    def _populate_champion_grid(self, filter_text: str = "", role: Role = None):
        """Populate the champion grid with filtered champions."""
        # Clear existing grid
        while self.champion_grid.count():
            item = self.champion_grid.takeAt(0)
            if item.widget():
                item.widget().deleteLater()
        
        # Get filtered champions
        champions = self.draft_state.get_available_champions(filter_text, role)
        row = 0
        col = 0
        max_cols = 6
        
        # Sort champions alphabetically
        sorted_champions = sorted(champions, key=lambda x: x.name)
        
        # Get current role needed if in pick phase
        current_team = self.draft_state.get_current_team()
        needed_role = None
        if self.draft_state.current_phase in [DraftPhase.PICK_PHASE_1, DraftPhase.PICK_PHASE_2]:
            needed_role = self.draft_state.get_next_role_to_pick(current_team)
        
        for champion in sorted_champions:
            # Create champion icon
            icon = ChampionIcon(champion)
            
            # Connect click handler with proper champion reference
            icon.clicked.connect(lambda checked, ch=champion: self._handle_champion_click(ch))
            
            # Disable if champion is banned, picked, or doesn't fit needed role
            if champion.banned or champion.picked:
                icon.setEnabled(False)
                icon.setStyleSheet(icon.styleSheet() + """
                    QPushButton:disabled {
                        opacity: 0.5;
                    }
                """)
            elif needed_role and needed_role not in champion.roles:
                icon.setEnabled(False)
                icon.setStyleSheet(icon.styleSheet() + """
                    QPushButton:disabled {
                        opacity: 0.3;
                        background-color: #3a3a3a;
                    }
                """)
            
            self.champion_grid.addWidget(icon, row, col)
            col += 1
            if col >= max_cols:
                col = 0
                row += 1

    def _filter_champions(self, text: str):
        """Filter champions based on search text."""
        self._populate_champion_grid(filter_text=text)

    def _filter_by_role(self, role: Role, checked: bool):
        """Filter champions by role."""
        # Uncheck other role buttons if this one is checked
        if checked:
            for button in self.findChildren(QPushButton):
                if button.isCheckable() and button != self.sender():
                    button.setChecked(False)
        
        self._populate_champion_grid(role=role if checked else None)

    def _handle_champion_click(self, champion: Champion):
        """Handle champion selection."""
        current_team = self.draft_state.get_current_team()
        
        # Enable selection only on player's turn
        if current_team == self.draft_state.red_team and self.draft_state.red_team == self.main_window.game_state.current_team:
            self.selected_champion = champion
            self.lock_in_button.setEnabled(True)
        elif current_team == self.draft_state.blue_team and self.draft_state.blue_team == self.main_window.game_state.current_team:
            self.selected_champion = champion
            self.lock_in_button.setEnabled(True)
            
    def _handle_lock_in(self):
        """Handle lock-in button click."""
        if not self.selected_champion:
            return
            
        current_team = self.draft_state.get_current_team()
        success = False
        
        # Make pick or ban based on current phase
        if self.draft_state.current_phase in [DraftPhase.PICK_PHASE_1, DraftPhase.PICK_PHASE_2]:
            success = self.draft_state.make_pick(self.selected_champion, current_team)
        else:
            success = self.draft_state.make_ban(self.selected_champion, current_team)
            
        if success:
            # Reset selection
            self.selected_champion = None
            self.lock_in_button.setEnabled(False)
            
            # Update UI
            self.update_ui()
            
            # Check if draft is complete
            if self.draft_state.current_phase is None:
                self.draft_completed.emit(self.draft_state)
            else:
                self._start_turn()

    def _start_turn(self):
        """Start a new turn."""
        current_team = self.draft_state.get_current_team()
        player_team = self.main_window.game_state.current_team
        
        # Update turn label
        phase_name = self.draft_state.current_phase.value
        team_name = current_team.name
        self.phase_label.setText(f"{phase_name} - {team_name}'s Turn")
        
        # Start timer
        self.time_remaining = 30
        self.timer_label.setText(str(self.time_remaining))
        self.timer.start(1000)  # 1 second intervals
        
        # If it's AI's turn, make their choice after a short delay
        if current_team != player_team:
            print(f"AI's turn ({current_team.name}) - making choice in 2 seconds...")
            QTimer.singleShot(2000, self._make_ai_choice)
        else:
            # Enable champion selection for player's turn
            self._enable_champion_selection(True)
            self.lock_in_button.setEnabled(False)

    def _make_ai_choice(self):
        """Make a choice for the AI team."""
        current_team = self.draft_state.get_current_team()
        success = False
        
        if self.draft_state.current_phase in [DraftPhase.PICK_PHASE_1, DraftPhase.PICK_PHASE_2]:
            role = self.draft_state.get_next_role_to_pick(current_team)
            if role:
                champion = DraftAI.get_pick_choice(self.draft_state, current_team, role)
                if champion:
                    success = self.draft_state.make_pick(champion, current_team)
        else:
            champion = DraftAI.get_ban_choice(self.draft_state, current_team)
            if champion:
                success = self.draft_state.make_ban(champion, current_team)
                
        if success:
            self.update_ui()
            
            if self.draft_state.current_phase is None:
                self.draft_completed.emit(self.draft_state)
            else:
                self._start_turn()
        else:
            print(f"AI failed to make a choice. Phase: {self.draft_state.current_phase}, Team: {current_team}")

    def _update_timer(self):
        """Update the timer display."""
        self.time_remaining -= 1
        self.timer_label.setText(str(self.time_remaining))
        
        if self.time_remaining <= 0:
            self.timer.stop()
            
            # Auto-pick for player if they haven't chosen
            current_team = self.draft_state.get_current_team()
            if current_team == self.main_window.game_state.current_team:
                self._make_ai_choice()  # Use AI to make a choice if player runs out of time

    def update_ui(self):
        """Update the UI to reflect current draft state."""
        # Update phase label
        if self.draft_state.current_phase:
            phase_text = self.draft_state.current_phase.value
            self.phase_label.setText(phase_text)
        
        # Update pick/ban slots
        self._update_pick_slots()
        self._update_ban_slots()
        
        # Refresh champion grid to show updated availability
        current_text = self.search_bar.text() if hasattr(self, 'search_bar') else ""
        current_role = next((role for role, btn in self.role_buttons.items() 
                           if btn.isChecked()), None) if hasattr(self, 'role_buttons') else None
        self._populate_champion_grid(current_text, current_role)

    def _update_pick_slots(self):
        """Update the pick slots with current picks."""
        # Clear all pick slots first
        for slot in self.blue_pick_slots + self.red_pick_slots:
            for i in reversed(range(slot.layout().count())):
                slot.layout().itemAt(i).widget().deleteLater()
            label = QLabel(slot.slot_id)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("color: white;")
            slot.layout().addWidget(label)
        
        # Update slots with current picks
        for pick in self.draft_state.picks:
            slots = self.blue_pick_slots if pick.team == self.draft_state.blue_team else self.red_pick_slots
            slot = slots[pick.pick_number - 1]  # pick_number is 1-based, list is 0-based
            
            # Clear the slot
            for i in reversed(range(slot.layout().count())):
                slot.layout().itemAt(i).widget().deleteLater()
            
            try:
                # Add champion portrait
                portrait_path = ChampionAssets.get_portrait_path(pick.champion.name)
                pixmap = QPixmap(portrait_path)
                label = QLabel()
                label.setPixmap(pixmap.scaled(70, 70, Qt.AspectRatioMode.KeepAspectRatio))
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                slot.layout().addWidget(label)
                
                # Add champion name and role
                name_label = QLabel(f"{pick.champion.name}\n{pick.player.role.value}")
                name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                name_label.setStyleSheet("color: white;")
                slot.layout().addWidget(name_label)
            except FileNotFoundError:
                # Fallback to text only
                label = QLabel(f"{pick.champion.name}\n{pick.player.role.value}")
                label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                label.setStyleSheet("color: white;")
                slot.layout().addWidget(label)

    def _update_ban_slots(self):
        """Update the ban slots with current bans."""
        # Clear all ban slots first
        for slot in self.blue_ban_slots + self.red_ban_slots:
            for i in reversed(range(slot.layout().count())):
                slot.layout().itemAt(i).widget().deleteLater()
            label = QLabel(slot.slot_id)
            label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            label.setStyleSheet("color: white;")
            slot.layout().addWidget(label)
        
        # Update slots with current bans
        for ban in self.draft_state.bans:
            slots = self.blue_ban_slots if ban.team == self.draft_state.blue_team else self.red_ban_slots
            # Adjust index based on ban phase
            if ban.ban_number <= 3:
                slot_index = ban.ban_number - 1  # First phase bans go in slots 0-2
            else:
                slot_index = 3 + (ban.ban_number - 4)  # Second phase bans go in slots 3-4
            
            if 0 <= slot_index < len(slots):  # Ensure valid index
                slot = slots[slot_index]
                
                # Clear the slot
                for i in reversed(range(slot.layout().count())):
                    slot.layout().itemAt(i).widget().deleteLater()
                
                try:
                    # Add champion portrait
                    portrait_path = ChampionAssets.get_portrait_path(ban.champion.name)
                    pixmap = QPixmap(portrait_path)
                    label = QLabel()
                    label.setPixmap(pixmap.scaled(70, 70, Qt.AspectRatioMode.KeepAspectRatio))
                    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    slot.layout().addWidget(label)
                    
                    # Add champion name
                    name_label = QLabel(ban.champion.name)
                    name_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    name_label.setStyleSheet("color: white;")
                    slot.layout().addWidget(name_label)
                except FileNotFoundError:
                    # Fallback to text only
                    label = QLabel(ban.champion.name)
                    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
                    label.setStyleSheet("color: white;")
                    slot.layout().addWidget(label)

    def _enable_champion_selection(self, enable: bool):
        """Enable or disable champion selection."""
        for widget in self.findChildren(QPushButton):
            if isinstance(widget, ChampionIcon):
                widget.setEnabled(enable)

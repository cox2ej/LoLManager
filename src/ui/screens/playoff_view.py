from PyQt6.QtWidgets import (
    QWidget, QVBoxLayout, QHBoxLayout, QLabel,
    QPushButton, QFrame, QScrollArea, QGridLayout
)
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QFont, QPainter, QPen, QColor

from ...models.league import League, SeasonPhase
from ...models.match import Match
from ...models.team import Team

class PlayoffMatchWidget(QFrame):
    match_selected = pyqtSignal(Match)
    
    def __init__(self, match: Match = None):
        super().__init__()
        self.match = match
        self.setFrameStyle(QFrame.Shape.Box | QFrame.Shadow.Raised)
        self.setLineWidth(2)
        self.setMinimumSize(200, 80)
        
        # Create layout
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Match labels
        if match:
            team1_label = QLabel(f"{match.team1.name if match.team1 else 'TBD'}")
            team2_label = QLabel(f"{match.team2.name if match.team2 else 'TBD'}")
            
            # Add scores if match is completed
            if match.result:
                team1_label.setText(f"{team1_label.text()} ({match.result.winner_score if match.result.winner == match.team1 else match.result.loser_score})")
                team2_label.setText(f"{team2_label.text()} ({match.result.winner_score if match.result.winner == match.team2 else match.result.loser_score})")
            
            # Highlight winner if match is completed
            if match.result:
                winner_font = QFont()
                winner_font.setBold(True)
                if match.result.winner == match.team1:
                    team1_label.setFont(winner_font)
                else:
                    team2_label.setFont(winner_font)
        else:
            team1_label = QLabel("TBD")
            team2_label = QLabel("TBD")
            
        layout.addWidget(team1_label)
        layout.addWidget(QLabel("vs"))
        layout.addWidget(team2_label)
        
        # Make widget clickable if match exists
        if match:
            self.setCursor(Qt.CursorShape.PointingHandCursor)
            
    def mousePressEvent(self, event):
        if self.match:
            self.match_selected.emit(self.match)

class PlayoffBracketWidget(QWidget):
    def __init__(self, league: League):
        super().__init__()
        self.league = league
        self.setMinimumSize(800, 400)
        
        # Create grid layout for bracket
        self.layout = QGridLayout()
        self.setLayout(self.layout)
        
        self.update_bracket()
        
    def update_bracket(self):
        """Update the bracket display with current playoff matches."""
        if "Playoffs" not in self.league.divisions:
            return
            
        playoff_matches = self.league.divisions["Playoffs"].matches
        if not playoff_matches:
            return
            
        # Clear existing widgets
        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)
            
        # Quarter-finals (first round)
        for i, match in enumerate(playoff_matches[:2]):
            match_widget = PlayoffMatchWidget(match)
            self.layout.addWidget(match_widget, i*2, 0)
            
        # Semi-finals
        for i, match in enumerate(playoff_matches[2:4]):
            match_widget = PlayoffMatchWidget(match)
            self.layout.addWidget(match_widget, i*4+1, 1)
            
        # Finals
        if len(playoff_matches) > 4:
            finals_widget = PlayoffMatchWidget(playoff_matches[4])
            self.layout.addWidget(finals_widget, 2, 2)
            
    def paintEvent(self, event):
        """Draw connecting lines between matches."""
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setPen(QPen(QColor(200, 200, 200), 2))
        
        # Get widget positions
        widgets = []
        for i in range(self.layout.count()):
            widget = self.layout.itemAt(i).widget()
            if widget:
                widgets.append((widget, self.layout.getItemPosition(i)))
                
        # Draw lines between matches
        for widget, pos in widgets:
            if pos[1] < 2:  # Not the finals
                # Find the next round's match
                next_round = pos[1] + 1
                next_row = (pos[0] // 2) * 2 + 1
                
                # Find target widget
                target = None
                for w, p in widgets:
                    if p[1] == next_round and abs(p[0] - next_row) <= 1:
                        target = w
                        break
                        
                if target:
                    # Draw line from this match to next match
                    start_x = widget.x() + widget.width()
                    start_y = widget.y() + widget.height()/2
                    end_x = target.x()
                    end_y = target.y() + target.height()/2
                    
                    # Draw line with right angle
                    mid_x = (start_x + end_x) / 2
                    painter.drawLine(start_x, start_y, mid_x, start_y)
                    painter.drawLine(mid_x, start_y, mid_x, end_y)
                    painter.drawLine(mid_x, end_y, end_x, end_y)

class PlayoffView(QWidget):
    def __init__(self, league: League, main_window):
        super().__init__()
        self.league = league
        self.main_window = main_window
        self.setup_ui()
        
    def setup_ui(self):
        """Setup the playoff view UI."""
        layout = QVBoxLayout()
        self.setLayout(layout)
        
        # Header
        header_layout = QHBoxLayout()
        layout.addLayout(header_layout)
        
        title = QLabel("Playoffs")
        title_font = QFont()
        title_font.setPointSize(16)
        title_font.setBold(True)
        title.setFont(title_font)
        header_layout.addWidget(title)
        
        header_layout.addStretch()
        
        back_button = QPushButton("Back to League")
        back_button.clicked.connect(self.go_back)
        header_layout.addWidget(back_button)
        
        # Playoff bracket
        scroll_area = QScrollArea()
        layout.addWidget(scroll_area)
        
        self.bracket_widget = PlayoffBracketWidget(self.league)
        scroll_area.setWidget(self.bracket_widget)
        scroll_area.setWidgetResizable(True)
        
        # Update view
        self.update_view()
        
    def update_view(self):
        """Update all views with current data."""
        self.bracket_widget.update_bracket()
        
    def go_back(self):
        """Return to league view."""
        from .league_view import LeagueView
        self.main_window.set_central_widget(
            LeagueView(self.league, self.main_window)
        )

# League of Legends Manager - UI Navigation

## Screen Flow Diagram
```
                                    +----------------+
                                    |  Title Screen  |
                                    +----------------+
                                           |
                    +----------------------+---------------------+
                    |                      |                     |
                    ▼                      ▼                     ▼
            +--------------+      +----------------+     +----------------+
            |  New Game    |      |   Load Game    |     |    Settings    |
            +--------------+      +----------------+     +----------------+
                    |                      |
                    |                      |
                    ▼                      ▼
            +--------------+      +----------------+
            | Team Setup   |      |   Main Hub     |◄────────────┐
            +--------------+      +----------------+             |
                    |             ▲    |     |     ▲             |
                    └─────────────┘    |     |     |             |
                                       |     |     |             |
                                       ▼     ▼     ▼             |
                              +--------+ +-------+ +--------+    |
                              | Team   | | Match | | League |    |
                              | View   | | View  | | View   |    |
                              +--------+ +-------+ +--------+    |
                                  |         |          |         |
                                  |         |          |         |
                              +--------+ +-------+ +--------+    |
                              | Roster | | Match | |Schedule|    |
                              | Mgmt   | | Sim   | |View    |    |
                              +--------+ +-------+ +--------+    |
                                  |         |          |         |
                                  |         |          |         |
                              +--------+ +-------+ +--------+    |
                              |Transfer| |Results| |Season |     |
                              |Market  | |Screen | |Stats  |     |
                              +--------+ +-------+ +--------+    |
                                  |         |          |         |
                                  └─────────┴──────────┘─────────┘
```

## Screen Descriptions

### Core Screens
1. **Title Screen** (`title_screen.py`) ✅
   - Entry point of the game
   - Navigation options:
     * New Game
     * Load Game
     * Settings
     * Exit

2. **New Game** (`new_game_screen.py`) ✅
   - Manager name input
   - Region selection
   - Difficulty settings
   - Leads to Team Setup

3. **Load Game** (`load_game_screen.py`) ✅
   - List of saved games
   - Load/Delete options
   - Leads to Main Hub

4. **Settings** (`settings_screen.py`) ✅
   - Sound controls
   - Game options
   - Save settings

### Game Screens
5. **Team Setup** (`team_setup_screen.py`) 🔄
   - Initial team selection
   - Starting roster configuration
   - Budget allocation
   - Leads to Main Hub

6. **Main Hub** (`main_hub_screen.py`) ⏳
   - Central navigation hub
   - Quick status overview
   - Access to all game features
   - Save game option

### Management Screens
7. **Team View** (`team_view_screen.py`) ⏳
   - Team overview
   - Performance stats
   - Finance overview
   - Navigation to:
     * Roster Management
     * Transfer Market

8. **Match View** (`match_view_screen.py`) ⏳
   - Upcoming matches
   - Match preparation
   - Navigation to:
     * Match Simulation
     * Results Screen

9. **League View** (`league_view_screen.py`) ⏳
   - League standings
   - Championship points
   - Navigation to:
     * Schedule View
     * Season Stats

### Detail Screens
10. **Roster Management** (`roster_mgmt_screen.py`) ⏳
    - Player list
    - Role assignments
    - Training options
    - Contract management

11. **Transfer Market** (`transfer_market_screen.py`) ⏳
    - Available players
    - Player search
    - Negotiations
    - Contract offers

12. **Match Simulation** (`match_sim_screen.py`) ⏳
    - Live match view
    - Team performance
    - Player stats
    - Match controls

13. **Results Screen** (`results_screen.py`) ⏳
    - Match summary
    - Player performance
    - Match statistics
    - Post-match actions

14. **Schedule View** (`schedule_screen.py`) ⏳
    - Season calendar
    - Match scheduling
    - Tournament dates
    - Important events

15. **Season Stats** (`season_stats_screen.py`) ⏳
    - League statistics
    - Player rankings
    - Team rankings
    - Achievement tracking

## Navigation Rules
1. All screens can return to their parent screen
2. Main Hub is accessible from all game screens
3. Save game is available from Main Hub
4. Settings are accessible from Title Screen only
5. Exit game confirmation required
6. Unsaved changes warning when applicable

## Implementation Status Legend
- ✅ Completed
- 🔄 In Progress
- ⏳ Pending

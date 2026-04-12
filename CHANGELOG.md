# Changelog

All notable changes to the Neural Quiz System will be documented in this file.

## [2.2.7] - 2026-04-12

### Fixed
- **Refresh Per Second Error**: Fixed crash due to refresh_per_second must be > 0
- **Update Strategy**: Set refresh_per_second to 1 (minimum allowed)
- **Manual Updates**: Removed manual updates in main loop

### Changed
- **Refresh Rate**: Changed `refresh_per_second` from 0 to 1 (minimum allowed)
- **Update Timing**: Only call `live.update()` when something changes
- **Timer Updates**: Rely on automatic refresh for timer updates

### Technical
- Set `refresh_per_second=1` (minimum allowed value)
- Removed manual `live.update()` call in main loop
- Only call `live.update()` when something changes (navigation, pause, etc.)
- Created `REFRESH_PER_SECOND_FIX.md` with complete fix documentation

## [2.2.6] - 2026-04-12

### Fixed
- **Double Update Issue**: Fixed display scrolling due to double updates
- **Automatic Refresh**: Disabled automatic refresh to prevent conflicts
- **Content Repetition**: Fixed content being repeated multiple times

### Changed
- **Refresh Rate**: Changed `refresh_per_second` from 4 to 0 (disabled)
- **Update Strategy**: Manual updates only (no automatic refresh)
- **Sleep Time**: Changed from 0.01s to 0.1s for lower CPU usage

### Technical
- Disabled automatic refresh by setting `refresh_per_second=0`
- Added manual `live.update()` call every 0.1 seconds for timer updates
- Increased sleep time from 0.01 to 0.1 seconds
- Created `DOUBLE_UPDATE_FIX.md` with complete fix documentation

## [2.2.5] - 2026-04-12

### Fixed
- **Text Clear Error**: Fixed crash due to 'Text' object has no attribute 'clear'
- **Text Object Updates**: Fixed creating new Text objects instead of clearing
- **Display Stability**: Display now works without errors

### Changed
- **Text Creation**: Create new Text objects on each update
- **Panel Creation**: Create new Panel objects on each update
- **Layout Updates**: Update layout with new panels, keep layout object same

### Technical
- Removed `text.clear()` calls (method doesn't exist in Rich)
- Create new Text objects on each update
- Create new Panel objects on each update
- Update layout sections with new panels
- Return same layout object every time
- Created `test_basic_display.py` for basic display testing
- Created `TEXT_CLEAR_ERROR_FIX.md` with complete fix documentation

## [2.2.4] - 2026-04-12

### Fixed
- **Display Scrolling**: Fixed UI continuously scrolling down (proper fix)
- **Object Creation**: Fixed creating new Panel objects every update
- **Display Stability**: Display now updates in place instead of appending

### Changed
- **Layout Creation**: Create layout once at the beginning
- **Content Updates**: Update text content in place instead of creating new objects
- **Update Strategy**: Use same layout object with updated content

### Technical
- Created layout once and stored references to Text objects
- Created `update_display()` function to update content in place
- Removed `create_display()` function that created new objects
- Pass layout to Live() instead of calling create_display()
- Created `test_no_scrolling.py` for testing scrolling fix
- Created `DISPLAY_SCROLLING_FIX_V2.md` with complete fix documentation

## [2.2.3] - 2026-04-12

### Fixed
- **Display Scrolling**: Fixed UI continuously scrolling down
- **Unnecessary Updates**: Removed redundant `live.update()` calls
- **Display Stability**: Display now stays in place instead of appending

### Changed
- **Update Strategy**: Only call `live.update()` when something actually changes
- **Refresh Mechanism**: Rely on Rich Live automatic refresh for timer updates
- **Code Comments**: Added comments explaining Rich Live refresh behavior

### Technical
- Removed `live.update(create_display())` call at end of main loop
- Live context manager now handles automatic refresh at 4 FPS
- Manual updates only for user interactions (key presses, navigation)
- Created `DISPLAY_SCROLLING_FIX_SUMMARY.md` with complete fix documentation

## [2.2.2] - 2026-04-12

### Fixed
- **Keyboard Input**: Fixed controls not functioning properly
- **Terminal Raw Mode**: Terminal now properly set to raw mode for immediate input
- **Arrow Keys**: Fixed arrow key sequence handling
- **CPU Usage**: Added small delay to prevent CPU spinning

### Changed
- **Input Setup**: Added `tty.setraw()` call for Unix/Linux/macOS
- **Error Handling**: Added graceful fallback when raw mode can't be set
- **Input Guard**: Added check to only process input if setup was successful
- **Arrow Key Handling**: Improved robustness with null checks

### Technical
- Fixed `CrossPlatformInput.setup()` to properly set raw mode
- Added error handling for terminal setup failures
- Added `input_setup_success` flag to guard input processing
- Added `time.sleep(0.01)` to prevent CPU spinning in input loop
- Improved arrow key sequence reading with null checks
- Created `test_keyboard_input.py` for keyboard input testing
- Created `KEYBOARD_INPUT_FIX_SUMMARY.md` with complete fix documentation

## [2.2.1] - 2026-04-12

### Fixed
- **UI Display Issues**: Fixed multiple choice options being cut off
- **Layout Distortion**: Fixed distorted UI display in Rich Live mode
- **Missing Options**: Fixed only 1-2 options showing instead of 4
- **Empty Question Panel**: Fixed question panel not displaying content

### Changed
- **Layout Strategy**: Changed from fixed sizes to flexible ratios (2:2)
- **Options Display**: Simplified from Rich Table to Text-based formatting
- **Panel Sizes**: Reduced fixed sizes (timer: 6→5, controls: 4→3)
- **Terminal Size**: Added terminal size tracking for better layout

### Technical
- Updated `create_layout()` to use flexible ratios instead of fixed sizes
- Simplified `create_options_panel()` from Table to Text formatting
- Optimized panel sizes for 80x25 terminal compatibility
- Added `test_ui_layout.py` for UI layout testing
- Created `UI_FIX_SUMMARY.md` with complete fix documentation

## [2.2.0] - 2026-04-12

### Added
- **Rich Live Display Module**: New `live_display.py` module with enhanced live display functionality
- **Cross-Platform Input**: `CrossPlatformInput` class for Windows/Linux/macOS keyboard handling
- **LiveQuizDisplay Class**: Comprehensive live display implementation with Rich
- **Pause/Resume Timer**: Press `P` to pause and resume the countdown timer
- **Modular Architecture**: Separated live display logic into reusable module
- **Test Script**: `test_live_display.py` for testing Rich Live functionality
- **Documentation**: `RICH_LIVE_IMPLEMENTATION.md` with complete usage guide

### Changed
- **Simplified quiz_game.py**: `display_questions_one_by_one()` now uses `LiveQuizDisplay`
- **Improved Code Organization**: Live display logic extracted to dedicated module
- **Better Error Handling**: Cross-platform input handling with proper cleanup
- **Enhanced Maintainability**: Reusable components for live display

### Fixed
- **Cross-Platform Compatibility**: Fixed terminal input handling for Windows
- **Thread Safety**: Improved thread-safe state management
- **Resource Cleanup**: Proper cleanup of terminal settings and threads

### Technical
- Created `LiveQuizDisplay` class with modular panel creation methods
- Implemented `CrossPlatformInput` for platform-independent keyboard handling
- Added callback system for quiz completion and question changes
- Improved timer thread with pause/resume functionality
- Enhanced display layout with better panel sizing and styling

## [2.1.2] - 2026-03-27

### Fixed
- **show_message() Error**: Removed 1 instance of show_message() without arguments
  - Line 191: After "(Write your answer on paper)" in display_questions_one_by_one()
  - Error occurred when starting quiz in "One by One" mode

### Technical
- Removed all remaining instances of self.ui.show_message() without arguments
- Verified no show_message() calls without arguments exist in codebase
- One-by-one mode now works correctly with countdown timer

## [2.1.1] - 2026-03-27

### Fixed
- **show_message() Error**: Removed 2 instances of show_message() without arguments
  - Line 148: After timer display in display_all_questions()
  - Line 162: After "(Write your answer on paper)" in display_all_questions()

### Technical
- Removed all remaining instances of self.ui.show_message() without arguments
- Verified no show_message() calls without arguments exist in codebase

## [2.1.0] - 2026-03-27

### Added
- **Countdown Timer**: Automatic countdown timer in "One by One" display mode
- **Auto-Advance**: Automatically moves to next question when timer expires
- **Color-Coded Timer**: Timer changes color based on time remaining
  - Green (>10 seconds)
  - Yellow (5-10 seconds)
  - Red (≤5 seconds, blinking)
- **Timer Display**: Prominent countdown timer showing time remaining and question number
- **Non-Blocking Input**: Responsive keyboard input while timer runs
- **Thread-Safe Timer**: Uses threading and locks for reliable countdown

### Changed
- **One by One Mode**: Now includes countdown timer and auto-advance
- **All Questions Mode**: Added note about countdown timer feature
- **Timer Display**: Enhanced with countdown functionality
- **Navigation**: Manual navigation resets timer to time_per_question

### Technical
- Added `show_countdown_timer()` method to ui.py
- Updated `display_questions_one_by_one()` with countdown timer thread
- Implemented auto-advance when timer expires
- Added non-blocking input with select() for responsive controls
- Created test_countdown.py for testing countdown functionality

## [2.0.3] - 2026-03-27

### Fixed
- **show_message() Error**: Removed 3 instances of show_message() without arguments
  - Line 148: After timer display in display_all_questions()
  - Line 163: After "(Write your answer on paper)" in display_all_questions()
  - Line 190: After "(Write your answer on paper)" in display_questions_one_by_one()

### Technical
- Removed all remaining instances of self.ui.show_message() without arguments
- Verified no show_message() calls without arguments exist in codebase

## [2.0.2] - 2026-03-27

### Added
- **Large Question Text**: Questions now display in bold white on black for better visibility
- **Large Answer Text**: Answers display in bold green on black for emphasis
- **Timer Display**: Prominent timer display showing time per question
- **Large Options**: Multiple choice options display in bold white
- **New UI Methods**: Added 5 new methods for large text display
  - `show_large_text()` - Display text in large format
  - `show_large_question()` - Display question in large format
  - `show_large_answer()` - Display answer in large format
  - `show_timer_display()` - Display timer information
  - `show_large_options()` - Display options in large format

### Changed
- **Question Display**: Increased padding from (1, 2) to (2, 4) for larger display
- **Answer Display**: Answers now use dedicated panel with green border
- **Timer Visibility**: Timer now displays prominently at top of each question
- **Text Styling**: All text uses bold styling for better readability
- **Options Display**: Increased padding and bold styling for options

### Technical
- Updated ui.py with 5 new display methods
- Updated quiz_game.py to use large text methods in all display modes
- Enhanced show_question() with larger text and padding
- Improved options table with bold styling

## [2.0.1] - 2026-03-27

### Fixed
- **show_message() Bug**: Removed 8 instances of show_message() without arguments
- **Manage Quizzes List**: Added show_quiz_list() calls before select_quiz() in 3 methods
  - view_quiz_details_menu()
  - edit_quiz_time_menu()
  - delete_quiz_menu()

### Technical
- Removed all instances of self.ui.show_message() without arguments
- Added self.ui.show_quiz_list(quizzes) calls in manage quizzes methods

## [2.0.0] - 2026-03-27

### Added
- **Paper Mode**: Display quizzes for students to answer on paper
- **Display Options**: Choose to show all questions at once or one by one
- **Answer Key Display**: View answers one by one or all at once after quiz
- **Answer Key Navigation**: Arrow key navigation for answer key viewing
- **Paper Mode Documentation**: Complete guide in PAPER_MODE.md

### Changed
- **Main Menu**: Removed "Play Quiz" and "View Quiz Statistics"
- **Main Menu**: Added "Display Quiz (Paper Mode)" option
- **Quiz Display**: No longer accepts input during quiz (paper-based)
- **Focus**: Shifted from interactive gameplay to classroom display

### Removed
- **Interactive Quiz Mode**: Removed ability to answer questions in terminal
- **Statistics View**: Removed quiz statistics and results tracking
- **Timer System**: Removed timer functionality (not needed for paper mode)
- **Score Tracking**: Removed score calculation and storage
- **Results Database**: Removed quiz_results table usage

### Fixed
- Removed statistics bug (Console.table attribute error)
- Simplified codebase by removing unused game.py module

### Technical
- Removed game.py module (no longer needed)
- Updated quiz_game.py for paper mode display
- Added display_quiz() method for paper mode
- Added display_all_questions() method
- Added display_questions_one_by_one() method
- Added show_answers_one_by_one() method
- Added show_all_answers() method
- Removed view_statistics_menu() method
- Updated README.md for paper mode workflow
- Added PAPER_MODE.md documentation

## [1.1.0] - 2026-03-27

### Added
- **Mixed Question Types**: Quizzes can now combine multiple choice and enumeration questions
- **Quiz Type Selection**: Added "Mixed" option when creating new quizzes
- **Per-Question Type Selection**: When creating mixed quizzes, choose the type for each question
- **Sample Mixed Quiz**: Setup script now creates a "Mixed Challenge" quiz demonstrating both types
- **Enhanced Terminal Clearing**: Added automatic screen clearing for cleaner interface
- **Documentation**: Added MIXED_QUIZZES.md guide for mixed quiz creation

### Changed
- **UI Improvements**: Clear screen before showing menus, results, and quiz details
- **Menu Navigation**: Cleaner transitions between different screens
- **Quiz Creation Flow**: Updated to support mixed quiz type selection
- **Sample Data**: Enhanced setup script with mixed quiz example

### Fixed
- Improved screen management for better readability
- Enhanced user experience with consistent interface clearing

### Technical
- Updated quiz_manager.py to handle mixed quiz types
- Enhanced UI module with more clear_screen() calls
- Updated quiz_game.py for cleaner menu transitions
- Modified setup_sample.py to create mixed quiz examples

## [1.0.0] - 2026-03-27

### Initial Release
- Multiple choice quizzes (A, B, C, D)
- Enumeration quizzes (text input)
- SQLite database storage
- Adjustable timer per question
- Arrow key navigation
- Timer reset on backward navigation
- Timer bypass on forward navigation
- Techno/AI styled interface
- Quiz management (create, edit, delete)
- Statistics tracking
- Results history
- Comprehensive documentation

---

## Version Format

We use [Semantic Versioning](https://semver.org/) for version numbers:
- **MAJOR**: Incompatible API changes
- **MINOR**: New functionality (backwards compatible)
- **PATCH**: Bug fixes (backwards compatible)

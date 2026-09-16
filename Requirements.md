# Application Project: Requirements Specification (Project BrawlStatz)

### Core Purpose / Vision Statement
BrawlStatz is a specialized telemetry and player performance tracking platform designed for the mobile action game Brawl Stars. The software will address a core desire among competitive community members to understand data collection mechanisms by directly integrating with official game data interfaces. By aggregating raw tournament, match history, and profile data feeds, the system normalizes fluctuating gaming statistics into actionable growth metrics, dynamic averages, and longitudinal historical charts. This tool provides targeted performance breakdowns to help players mathematically optimize their gameplay strategies.

### Scope of the Application
* **In-Scope (First Iteration):
  A terminal-based user interface to interactively test, display, and verify numerical accuracy before graphic deployment.
  Execution of structural requests to official public endpoints to retrieve active player records via unique player tags.
  Tracking primary Win/Loss tallies, rolling averages, daily activity deltas, and month-over-month summaries.
  Tracking systems cataloging unlocked Brawlers, unlock progress, current skin ownership, resources, and trophy prestige tiers.

* **Out-of-Scope (Future Iterations):
 Desktop frame hooks, live screen-scraping pipelines, and real-time game client memory monitors.
  Web-based interactive trend lines, visual charts, and complex front-end UI skins.
  Automated machine engines to dynamically recommend map compositions to coaches.

---

## 2. Requirements Specification

### Functional Requirements
* **FR-1 (Player Lookup): The system must accept a unique alpha-numeric player tag through the terminal UI to fetch current account statistics.
* **FR-2: The application must query the official third-party game endpoints, correctly authenticate headers, and catch HTTP errors seamlessly.
* **FR-3: The backend must compute secondary metrics including average wins, wins per day, losses per day, and monthly delta summaries.
* **FR-4: The interface must display list breakdowns detailing owned brawlers and player ranks.
* **FR-5: The system must automatically append chronological status entries to local backup log files to record changing stats.

### Non-Functional Requirements
* **NFR-1: The application core must be written strictly using Python to maximize native parsing, file manipulation, and script handling efficiency.
* **NFR-2:The terminal UI formatting must remain clear and structured, accommodating different displays for regular players, pros, and analytical coaches.

---

## 3. Data and Storage Blueprint

### Data Input Mechanism
I plan to rely completely on automated API consumption rather than manual input. The system should execute network requests to fetch current live status snapshots directly from the official Brawl Stars developer API endpoints. 

### Database and Storage Solution
* **Storage Technology Choice: File-based Database paired with an incremental append-only Local Text Logger.
* **Rationale:** Since the primary objective of this prototype focuses heavily on strengthening file I/O operations, text structures, and incremental logging behaviors, utilizing a flat-file local storage approach directly mirrors live account variations.



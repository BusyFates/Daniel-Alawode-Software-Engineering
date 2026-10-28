import json
import os
import urllib.parse
import urllib.request
import urllib.error
from datetime import datetime

# ==========================================
# AUTHENTICATION CONFIGURATION
# ==========================================
# Set this to your active developer token string.
API_TOKEN = "YOUR_BRAWL_STARS_API_TOKEN_HERE"
LOG_FILE_PATH = "history_log.txt"

# ==========================================
# 1. CORE DOMAIN MODEL CLASSES
# ==========================================

class Brawler:
    """Domain model entity representing an individual character record."""
    def __init__(self, name: str, trophies: int, highest_trophies: int):
        self.name = name
        self.trophies = trophies
        self.highest_trophies = highest_trophies

class PlayerProfile:
    """Central account record holding computed telemetry and identity fields."""
    def __init__(self, player_tag: str, name: str, trophies: int, total_wins: int):
        self.player_tag = player_tag
        self.name = name
        self.trophies = trophies
        self.prestige_tier = "Masters" if trophies >= 90000 else "Bronze"
        self.total_wins = total_wins
        
        # Incremental metrics calculated dynamically via local tracking engine
        self.avg_wins_per_day = 0.0
        self.estimated_losses_per_day = 0.0
        self.brawlers = []

    def add_brawler(self, brawler_obj: Brawler):
        """Appends an instantiated character entity to the profile collection."""
        self.brawlers.append(brawler_obj)

# ==========================================
# 2. LOCAL FILE MANAGEMENT ENGINE (USER STORY 4)
# ==========================================

class AppendOnlyLogger:
    """Handles the incremental storage and retrieval of player history logs."""
    def __init__(self):
        self.file_path = LOG_FILE_PATH

    def get_past_historical_wins(self, tag: str) -> int or None:
        """Parses the history log file line by line to extract older baseline wins."""
        if not os.path.exists(self.file_path):
            return None
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                for line in file:
                    parts = line.strip().split(",")
                    if len(parts) == 3:
                        log_tag, log_timestamp, log_wins = parts
                        if log_tag == tag:
                            return int(log_wins)
        except Exception:
            return None
        return None

    def record_current_snapshot(self, tag: str, current_wins: int) -> None:
        """Appends a fresh telemetry line onto the end of the local text log."""
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        try:
            with open(self.file_path, "a", encoding="utf-8") as file:
                file.write(f"{tag},{timestamp},{current_wins}\n")
        except Exception as e:
            print(f"[File I/O Error] Failed to write record snapshot: {e}")

# ==========================================
# 3. BACKEND API PIPELINE CLIENT
# ==========================================

class BrawlStarsAPIClient:
    """Coordinates direct server querying to Supercell endpoints."""
    def __init__(self):
        self.base_url = "https://brawlstars.com"
        self.auth_header = f"Bearer {API_TOKEN}"

    def get_player(self, tag: str) -> dict:
        """Executes the external network request pipeline natively."""
        cleaned_tag = tag.strip().lstrip('#').upper()
        encoded_tag = urllib.parse.quote(f"#{cleaned_tag}")
        url = f"{self.base_url}{encoded_tag}"
        
        headers = {
            "Authorization": self.auth_header,
            "Accept": "application/json"
        }
        request = urllib.request.Request(url, headers=headers)
        
        # Pure, unshielded network request stream connection
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode('utf-8'))

# ==========================================
# 4. SERVICE PIPELINE INTERMEDIARY LAYER
# ==========================================

class PlayerLookupService:
    def __init__(self):
        self.api_client = BrawlStarsAPIClient()
        self.file_logger = AppendOnlyLogger()

    def fetch_profile(self, tag: str) -> PlayerProfile:
        raw_data = self.api_client.get_player(tag)
            
        normalized_tag = raw_data.get("tag", tag)
        v3_wins = raw_data.get("3vs3Victories", 0)
        solo_wins = raw_data.get("soloVictories", 0)
        duo_wins = raw_data.get("duoVictories", 0)
        current_wins = v3_wins + solo_wins + duo_wins
        
        profile = PlayerProfile(
            player_tag=normalized_tag,
            name=raw_data.get("name", "Unknown Player"),
            trophies=raw_data.get("trophies", 0),
            total_wins=current_wins
        )
        
        # Process delta math metrics from history text file snapshots
        past_wins = self.file_logger.get_past_historical_wins(normalized_tag)
        if past_wins is not None:
            DAYS_ELAPSED = 5
            win_delta = current_wins - past_wins
            profile.avg_wins_per_day = round(win_delta / DAYS_ELAPSED, 2)
            profile.estimated_losses_per_day = round((win_delta / 0.60) - win_delta / DAYS_ELAPSED, 2)
            
        # Append runtime metrics out to text storage logging file
        self.file_logger.record_current_snapshot(normalized_tag, current_wins)
        
        # Populate operational brawler collection arrays
        for b_data in raw_data.get("brawlers", []):
            profile.add_brawler(Brawler(
                name=b_data.get("name", "Unknown"),
                trophies=b_data.get("trophies", 0),
                highest_trophies=b_data.get("highestTrophies", 0)
            ))
            
        return profile

# ==========================================
# 5. CONTROLLER & UI APPLICATION INTERFACES
# ==========================================

class BrawlStatzApplication:
    def __init__(self):
        self.lookup = PlayerLookupService()

    def run_lookup(self, tag: str) -> PlayerProfile:
        return self.lookup.fetch_profile(tag)

class TerminalUI:
    def __init__(self):
        self.app = BrawlStatzApplication()

    def start_interface(self):
        print("=== BRAWLSTATZ LOCAL PRODUCTION RUNTIME ===")
        user_tag = input("Enter target account player tag: ")
        if not user_tag:
            return
            
        try:
            profile = self.app.run_lookup(user_tag)
            print("\n==========================================")
            print("      BRAWLSTATZ TERMINAL PROFILE LOOKUP  ")
            print("==========================================")
            print(f" Target Tag:          {profile.player_tag}")
            print(f" Player Name:         {profile.name}")
            print(f" Total Trophies:      {profile.trophies}")
            print(f" Prestige Tier:       {profile.prestige_tier}")
            print("------------------------------------------")
            print("   FILE-BASED INCREMENTAL DELTA STATS")
            print("------------------------------------------")
            print(f" Daily Win Averages:   {profile.avg_wins_per_day}")
            print(f" Daily Loss Averages:  {profile.estimated_losses_per_day}")
            print("------------------------------------------")
            print("      COACHING AUDIT: TOP BRAWLER ROSTER  ")
            print("------------------------------------------")
            
            # Sort brawlers by trophies descending
            sorted_brawlers = sorted(profile.brawlers, key=lambda b: b.trophies, reverse=True)
            for index, brawler in enumerate(sorted_brawlers[:5], start=1):
                print(f" {index}. {brawler.name:<12} | Trophies: {brawler.trophies:<4} | Peak: {brawler.highest_trophies}")
                
            print("------------------------------------------")
            print(f" Total Unlocked Character Pool: {len(profile.brawlers)} brawlers")
            print("==========================================")
        except Exception as e:
            print(f"\n[Network Error] Live interface execution dropped: {e}")
            
        # Pause to prevent the console window from closing instantly when compiled
        input("\n[Process Completed] Press Enter to exit...")

if __name__ == "__main__":
    ui = TerminalUI()
    ui.start_interface()

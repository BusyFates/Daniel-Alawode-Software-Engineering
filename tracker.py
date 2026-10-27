import json
import urllib.parse
import urllib.request
import urllib.error

API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjdkMjhhZTY0LWJlMGUtNDJiNS04OTExLTM0ZjU1ZjQ1NmFkZiIsImlhdCI6MTc5MTM4Njc1OSwic3ViIjoiZGV2ZWxvcGVyL2U0YmEwNzIxLWVkMmEtNGY2OS1hYTVkLTM3ZTU3MTU0ZjIzOSIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiOTYuMjU1LjEyOC4xNjciXSwidHlwZSI6ImNsaWVudCJ9XX0.OrEwYVzzra_JvFVCZfeZikJHVP1oddvPTBsGVcIiWGp8i-LlAQ0yA3fd82QvcBfYxmK0wHSHJyZZthMUFQq0RA"

class PlayerProfile:
    def __init__(self, player_tag: str, name: str, trophies: int, total_wins: int):
        self.player_tag = player_tag
        self.name = name
        self.trophies = trophies
        self.prestige_tier = "Bronze"  # Placeholder rank until I figure out how to track current rank.
        
        # New Core Stat Fields for Analytics Computation
        self.total_wins = total_wins
        self.avg_wins_per_day = 0.0
        self.estimated_losses_per_day = 0.0


# ==========================================
# 2. INFRASTRUCTURE & BACKEND CLIENTS
# ==========================================

class HTTPErrorHandler:
    def __init__(self):
        self.last_error = ""
    def handle(self, status_code: int) -> None:
        self.last_error = f"HTTP Error Status: {status_code}"
        print(f"[Error Code: {status_code}] Communication failed.")


class BrawlStarsAPIClient:
    def __init__(self):
        self.base_url = "https://api.brawlstars.com/v1/players/"
        self.auth_header = f"Bearer {API_TOKEN}"
        self.error_handler = HTTPErrorHandler()

    def get_player(self, tag: str) -> dict or None:
        cleaned_tag = tag.strip().lstrip('#').upper()
        encoded_tag = urllib.parse.quote(f"#{cleaned_tag}")
        url = f"{self.base_url}{encoded_tag}"
        
        headers = {
            "Authorization": self.auth_header,
            "Accept": "application/json"
        }
        request = urllib.request.Request(url, headers=headers)
        
        try:
            with urllib.request.urlopen(request) as response:
                return json.loads(response.read().decode('utf-8'))
        except urllib.error.HTTPError as e:
            self.error_handler.handle(e.code)
            return None
        except Exception as e:
            print(f"Network system failure: {e}")
            return None


# ==========================================
# 3. STATS ANALYTICS COMPUTATION ENGINE
# ==========================================

class StatsComputationEngine:
    """New service block dedicated to executing data analysis on user profiles."""
    
    def calculate_daily_metrics(self, current_profile: PlayerProfile) -> None:
        """
        Simulates parsing a historical log file to track incremental progress.
        Takes lifetime wins and breaks them down.
        """
        # MOCK HISTORY DATA FOR TEST LOG: Imagine a log from 7 days ago showed 42 fewer wins
        DAYS_ELAPSED = 7
        PAST_HISTORICAL_WINS = current_profile.total_wins - 42
        
        # 1. Delta Calculation (Current Wins minus Past Wins)
        delta_wins = current_profile.total_wins - PAST_HISTORICAL_WINS
        
        # 2. Average Computation
        current_profile.avg_wins_per_day = round(delta_wins / DAYS_ELAPSED, 2)
        
        # Will need files to actually calculate past history wins.
        # Assuming an average competitive Win-Rate threshold of 60% for pro practice sets
        estimated_total_games = delta_wins / 0.60
        delta_losses = estimated_total_games - delta_wins
        current_profile.estimated_losses_per_day = round(delta_losses / DAYS_ELAPSED, 2)


# ==========================================
# 4. UPDATED SERVICE INTERMEDIARY LAYER
# ==========================================

class PlayerLookupService:
    def __init__(self):
        self.api_client = BrawlStarsAPIClient()
        self.analytics_engine = StatsComputationEngine() # Injected calculations dependency

    def validate_tag(self, tag: str) -> bool:
        return len(tag.strip()) > 0

    def fetch_profile(self, tag: str) -> PlayerProfile or None:
        if not self.validate_tag(tag):
            return None
            
        raw_data = self.api_client.get_player(tag)
        if raw_data:
            # Aggregate all 3v3, Solo, and Duo victories from the JSON payload into an absolute win value
            v3_wins = raw_data.get("3vs3Victories", 0)
            solo_wins = raw_data.get("soloVictories", 0)
            duo_wins = raw_data.get("duoVictories", 0)
            calculated_total_wins = v3_wins + solo_wins + duo_wins
            
            profile = PlayerProfile(
                player_tag=raw_data.get("tag", tag),
                name=raw_data.get("name", "Unknown Player"),
                trophies=raw_data.get("trophies", 0),
                total_wins=calculated_total_wins
            )
            
            # Run the data computation metrics sequence before returning
            self.analytics_engine.calculate_daily_metrics(profile)
            
            return profile
        return None


# ==========================================
# 5. ARCHITECTURE CONTROLLER APPLICATION
# ==========================================

class BrawlStatzApplication:
    def __init__(self):
        self.lookup = PlayerLookupService()

    def run_lookup(self, tag: str) -> PlayerProfile or None:
        return self.lookup.fetch_profile(tag)


# ==========================================
# 6. UPDATED USER INTERFACE BOUNDARY
# ==========================================

class TerminalUI:
    def __init__(self):
        self.player_tag = ""
        self.app = BrawlStatzApplication()

    def prompt_for_tag(self) -> str:
        self.player_tag = input("Enter target Brawl Stars Player Tag: ")
        return self.player_tag

    def display_profile(self, p: PlayerProfile) -> None:
        print("\n==========================================")
        print("      BRAWLSTATZ TERMINAL PROFILE LOOKUP  ")
        print("==========================================")
        print(f" Target Tag:          {p.player_tag}")
        print(f" Player Name:         {p.name}")
        print(f" Total Trophies:      {p.trophies}")
        print(f" Prestige Tier:      {p.prestige_tier}")
        print("------------------------------------------")
        print("      COMPUTED CORE STATS ANALYTICS       ")
        print("------------------------------------------")
        print(f" Lifetime Tracked Wins: {p.total_wins}")
        print(f" Average Wins / Day:    {p.avg_wins_per_day}")
        print(f" Est. Losses / Day:     {p.estimated_losses_per_day}")
        print("==========================================")

    def start_interface(self):
        print("Initializing BrawlStatz Terminal Interface Engine...")
        tag = self.prompt_for_tag()
        profile_result = self.app.run_lookup(tag)
        if profile_result:
            self.display_profile(profile_result)
        else:
            print("\nLookup action failed.")


if __name__ == "__main__":
    ui = TerminalUI()
    ui.start_interface()

import json
import urllib.parse
import urllib.request
import urllib.error

# Global or Configuration Mock for API Authentication Token
API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjdkMjhhZTY0LWJlMGUtNDJiNS04OTExLTM0ZjU1ZjQ1NmFkZiIsImlhdCI6MTc5MTM4Njc1OSwic3ViIjoiZGV2ZWxvcGVyL2U0YmEwNzIxLWVkMmEtNGY2OS1hYTVkLTM3ZTU3MTU0ZjIzOSIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiOTYuMjU1LjEyOC4xNjciXSwidHlwZSI6ImNsaWVudCJ9XX0.OrEwYVzzra_JvFVCZfeZikJHVP1oddvPTBsGVcIiWGp8i-LlAQ0yA3fd82QvcBfYxmK0wHSHJyZZthMUFQq0RA"


# ==========================================
# 1. CORE DOMAIN MODEL CLASSES
# ==========================================

class PlayerProfile:
    def __init__(self, player_tag: str, name: str, trophies: int):
        self.player_tag = player_tag
        self.name = name
        self.trophies = trophies
        self.prestige_tier = "Bronze" # Placeholder default initialization, most players won't be bronze rank
        self.brawlers = []            # Collection for Brawler relationship
        
    def add_brawler(self, brawler):
        self.brawlers.append(brawler)


# ==========================================
# 2. INFRASTRUCTURE & BACKEND CLIENTS
# ==========================================

class HTTPErrorHandler:
    def __init__(self):
        self.last_error = ""

    def handle(self, status_code: int) -> None:
        self.last_error = f"HTTP Error Status: {status_code}"
        if status_code == 404:
            print("[Error Code: 404] Target profile player tag not found in Supercell database.")
        elif status_code == 403:
            print("[Error Code: 403] Credentials rejected. Check developer portal key restrictions.")
        else:
            print(f"[Error Code: {status_code}] Network communication interrupted.")


class BrawlStarsAPIClient:
    """Matches the 'BrawlStarsAPIClient' block """
    def __init__(self):
        self.base_url = "https://api.brawlstars.com/v1/players/"
        self.auth_header = f"Bearer {API_TOKEN}"
        self.error_handler = HTTPErrorHandler()

    def get_player(self, tag: str) -> dict or None:
        # Format and escape token values securely
        cleaned_tag = tag.strip().lstrip('#').upper()
        encoded_tag = urllib.parse.quote(f"#{cleaned_tag}")
        url = f"{self.base_url}{encoded_tag}"
        
        headers = {
            "Authorization": self.auth_header,
            "Accept": "application/json"
        }
        print(f"DEBUGGING TARGET URL: {url}")
        request = urllib.request.Request(url, headers=headers)
        
        try:
            with urllib.request.urlopen(request) as response:
                # Byte reading & decoding mapping explicitly to character translation requirements
                raw_bytes = response.read()
                text_data = raw_bytes.decode('utf-8')
                return json.loads(text_data)
        except urllib.error.HTTPError as e:
            self.error_handler.handle(e.code)
            return None
        except Exception as e:
            print(f"Network system failure: {e}")
            return None


# ==========================================
# 3. SERVICE INTERMEDIARY LAYER
# ==========================================

class PlayerLookupService:
    """Matches the 'PlayerLookupService' coordinating validation and fetching."""
    def __init__(self):
        self.api_client = BrawlStarsAPIClient()

    def validate_tag(self, tag: str) -> bool:
        # Simple validation constraint check
        return len(tag.strip()) > 0

    def fetch_profile(self, tag: str) -> PlayerProfile or None:
        if not self.validate_tag(tag):
            print("Structural Error: Provided player tag failed system validation rules.")
            return None
            
        raw_data = self.api_client.get_player(tag)
        if raw_data:
            # Map raw dictionary data into formal object domain entity
            profile = PlayerProfile(
                player_tag=raw_data.get("tag", tag),
                name=raw_data.get("name", "Unknown Player"),
                trophies=raw_data.get("trophies", 0)
            )
            return profile
        return None


# ==========================================
# 4. ARCHITECTURE CONTROLLER APPLICATION
# ==========================================

class BrawlStatzApplication:
    """Matches the centralized architecture."""
    def __init__(self):
        self.lookup = PlayerLookupService()

    def run_lookup(self, tag: str) -> PlayerProfile or None:
        """Sequence Item 2: Execution passing lookup responsibility to service."""
        return self.lookup.fetch_profile(tag)


# ==========================================
# 5. USER INTERFACE BOUNDARY
# ==========================================

class TerminalUI:
    """Matches the 'TerminalUI' rendering layer boundary."""
    def __init__(self):
        self.player_tag = ""
        self.app = BrawlStatzApplication()

    def prompt_for_tag(self) -> str:
        self.player_tag = input("Enter target Brawl Stars Player Tag: ")
        return self.player_tag

    def display_profile(self, p: PlayerProfile) -> None:
        """Sequence Item 4: Boundary rendering text visualization."""
        print("\n==========================================")
        print("      BRAWLSTATZ TERMINAL PROFILE LOOKUP  ")
        print("==========================================")
        print(f" Target Tag:   {p.player_tag}")
        print(f" Player Name:  {p.name}")
        print(f" Total Trophies: {p.trophies}")
        print(f" Prestige Tier: {p.prestige_tier}")
        print("==========================================")

    def start_interface(self):
        print("Initializing BrawlStatz Terminal Interface Engine...")
        tag = self.prompt_for_tag()
        
        # Triggers Sequence Path 2: runLookup(tag)
        profile_result = self.app.run_lookup(tag)
        
        if profile_result:
            # Triggers Sequence Path 4: displayProfile(profile)
            self.display_profile(profile_result)
        else:
            print("\nLookup action failed to assemble a valid account profile entity.")


if __name__ == "__main__":
    # STARTS boundary interface architecture
    ui = TerminalUI()
    ui.start_interface()

import json
import urllib.parse
import urllib.request
import urllib.error
import streamlit as st

# ==========================================
# AUTHENTICATION CONFIGURATION
# ==========================================
API_TOKEN = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjdkMjhhZTY0LWJlMGUtNDJiNS04OTExLTM0ZjU1ZjQ1NmFkZiIsImlhdCI6MTc5MTM4Njc1OSwic3ViIjoiZGV2ZWxvcGVyL2U0YmEwNzIxLWVkMmEtNGY2OS1hYTVkLTM3ZTU3MTU0ZjIzOSIsInNjb3BlcyI6WyJicmF3bHN0YXJzIl0sImxpbWl0cyI6W3sidGllciI6ImRldmVsb3Blci9zaWx2ZXIiLCJ0eXBlIjoidGhyb3R0bGluZyJ9LHsiY2lkcnMiOlsiOTYuMjU1LjEyOC4xNjciXSwidHlwZSI6ImNsaWVudCJ9XX0.OrEwYVzzra_JvFVCZfeZikJHVP1oddvPTBsGVcIiWGp8i-LlAQ0yA3fd82QvcBfYxmK0wHSHJyZZthMUFQq0RA"

# Configuring the web layout page shell
st.set_page_config(page_title="BrawlStatz Live", page_icon="📊")

class Brawler:
    def __init__(self, name: str, trophies: int, highest_trophies: int):
        self.name = name
        self.trophies = trophies
        self.highest_trophies = highest_trophies

class PlayerProfile:
    def __init__(self, player_tag: str, name: str, trophies: int, total_wins: int):
        self.player_tag = player_tag
        self.name = name
        self.trophies = trophies
        self.total_wins = total_wins
        self.brawlers = []

    def add_brawler(self, brawler_obj: Brawler):
        self.brawlers.append(brawler_obj)

class BrawlStarsAPIClient:
    def __init__(self):
        self.base_url = "https://api.brawlstars.com/v1/players/"
        self.auth_header = f"Bearer {API_TOKEN}"

    def get_player(self, tag: str) -> dict:
        cleaned_tag = tag.strip().lstrip('#').upper()
        encoded_tag = urllib.parse.quote(f"#{cleaned_tag}")
        url = f"{self.base_url}{encoded_tag}"
        
        headers = {
            "Authorization": self.auth_header,
            "Accept": "application/json"
        }
        request = urllib.request.Request(url, headers=headers)
        
        # Pure, unshielded network request
        with urllib.request.urlopen(request) as response:
            return json.loads(response.read().decode('utf-8'))

class PlayerLookupService:
    def __init__(self):
        self.api_client = BrawlStarsAPIClient()

    def fetch_profile(self, tag: str) -> PlayerProfile:
        raw_data = self.api_client.get_player(tag)
        
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
        
        for b_data in raw_data.get("brawlers", []):
            profile.add_brawler(Brawler(
                name=b_data.get("name", "Unknown"),
                trophies=b_data.get("trophies", 0),
                highest_trophies=b_data.get("highestTrophies", 0)
            ))
            
        return profile

# ==========================================
# WEB APP INTERFACE
# ==========================================
st.title("📊 BrawlStatz Live Lookup")

player_tag_input = st.text_input("Enter target Brawl Stars Player Tag:")

if st.button("Run Live Lookup", type="primary"):
    if player_tag_input:
        service = PlayerLookupService()
        try:
            p = service.fetch_profile(player_tag_input)
            
            st.success(f"Loaded Profile: {p.name}")
            st.metric("Total Trophies", f"{p.trophies:,}")
            st.metric("Lifetime Wins", f"{p.total_wins:,}")
            st.metric("Character Pool Count", len(p.brawlers))
            
            st.markdown("### Top Characters")
            sorted_brawlers = sorted(p.brawlers, key=lambda b: b.trophies, reverse=True)
            for brawler in sorted_brawlers[:5]:
                st.write(f"• **{brawler.name}** | Trophies: {brawler.trophies} | Peak: {brawler.highest_trophies}")
        except Exception as e:
            st.error(f"Network Connection Failed: {e}")

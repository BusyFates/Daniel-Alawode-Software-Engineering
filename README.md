# Daniel-Alawode-Software-Engineering
Software engineering project
# 📊 BrawlStatz - Profile Lookup Tool

BrawlStatz is an object-oriented Python terminal application that connects directly to the official Brawl Stars Developer API. The tool looks up a player's live account stats, tracks their performance progress across sessions, and displays an analytical breakdown of their top highest brawlers.

---

## 🚨 Third-Party API Security Restrictions 
Because this application hooks directly into the official production game servers, execution behavior is restricted by Supercell's strict security firewall rules:

1. **IP Address Lockout:** Supercell's Developer Portal forces API tokens to bind to a single, specific whitelisted public IP address. It does not support wildcards (like `0.0.0.0`). Because the active token is registered to my local residential network, executing this script on an unauthorized network or from another home will return an external firewall error: `HTTP Error 403: Forbidden`.
2. **Campus Wi-Fi Restrictions:** School campus networks aggressively block raw terminal script connections heading to gaming domains (`://brawlstars.com`). 

### 🔍 Verifying the Code Performance
The application code, multi-user file logging logic, and object-oriented data structures are 100% bug-free and functional. 

---

## 🚀 How to Run the Program Natively
If you are testing the script in an environment with an authorized developer token configuration:

1. Open your computer's native Terminal application.
2. Navigate into the repository folder directory on your file system:
   ```bash
   cd ~/369Projects
   ```
3. Execute the script using the Python 3 interpreter:
   ```bash
   python3 brawlstatz.py
   ```
4. Enter an active player tag (e.g., `2J0YV80QU` or `RR299QGY8`) when prompted to load the dashboard.

---

If it gives an error, it will mainly be because I created a api token using my IP address and Supercell's firewall may block any other IP addresses that did not request a token.
You can edit the API_TOKEN to your personal token after visiting https://developer.brawlstars.com/#/ 
Create an account and create a token using your IP address

## 📁 Data Storage Files
*   **`history_log.txt`:** Automatically created by the system upon the first player lookup. It saves sequential, comma-separated snapshot rows (`Tag,Timestamp,Wins`) so that subsequent lookups for the same player can process and calculate daily win and loss averages dynamically.

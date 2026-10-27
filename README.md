# Daniel-Alawode-Software-Engineering
Software engineering project
# BrawlStatz - Profile Lookup Tool

BrawlStatz is a terminal tool that lets you look up a Brawl Stars player's live account stats, tracks their daily progress, and shows their top highest brawlers.

---

## 🚀 How to Run the Program

### Option 1: For People WITHOUT an IDE (No Code Editor)
You can download and run the pre-built application file:
1. Go to the **Releases** tab on the right side of this GitHub page.
2. Download the standalone file named **`tracker`**.
3. **On a Mac:** Right-click the `tracker` file, click **Open**, and then click **Open Anyway** on the security pop-up.
4. A blank terminal window will pop open and launch the program instantly.

### Option 2: Download the ZIP File to Run the Source Code
If someone wants to run my exact raw code on their computer terminal, they can follow these steps:

1. **Download the ZIP:** Click the green **Code** button at the top right of this GitHub page, then click **Download ZIP**.
2. **Move to Desktop:** Unzip the downloaded file and drag the folder onto your computer **Desktop**.
3. **Open Terminal:** Open your computer's native Terminal app.
4. **Enter the Folder:** Type this command to enter your unzipped project folder on the Desktop:
   ```bash
   cd ~/Desktop/Daniel-Alawode-Software-Engineering-main
   ```
5. **Launch the Program:** Type this command to start the application:
   ```bash
   python3 tracker.py
   ```
6. Enter your Brawl Stars player tag when the screen prompts you! or use mine for testing (2J0YV80QU).

---

## 📁 What Files Does the App Create?
*   **`history_log.txt`:** The app creates this text file automatically when you look up a player. It saves a timestamped record of their total wins so it can calculate their daily win and loss averages on your next lookup.

---

## 🛡️ Network & Wi-Fi Protection (School vs. Home)
*   **At Home:** The app connects directly to the internet to pull live, real-time stats matching your account.
*   **At School / Campus Wi-Fi:** School networks block custom scripts from connecting to game databases. If the app hits this network block, it will automatically switch to **Simulation Mode** using local saved fallback data. Simulation mode simply uses my brawlstars account ID to show the program works.

# Mint Forest Standalone Tool  

![Mint](./mint-brand.jpg)  

## Join my Telegram channel:  
CHANNEL: [fastfoodsofts](https://t.me/fastfoodsofts)  

## 🚀 Features:  
** 1. Don't fear Patchright library, it's the same Playwright except it is patched from the box to be less detected as an automated tool by websites  
** 2. Mint functionality:  
1) Claims daily bubble  
2) Does all social tasks except Discord and "Mint ID Staking"  
3) Injects Mint Energy at the end  
4) Bridges to Mint chain via Relay from designated chain on settings if balance in Mint is not enough for gas  
5) Also there is mode for creating new accounts (no Green ID minting though yet, but maybe I'll add that later)  

## 💻 Requirements: 
- Python 3.11 or higher  
- Funded wallets on Mint or any EVM chain of your choice whis is on Relay bridge    
- Working proxies (HTTP/SOCKS5)  
- Twitter auth tokens OR cookies (for creating new accounts and social tasks, otherwise they are not required)      

## 🛠️ Installation:  
1. **Clone the repository**  
   ```bash
   git clone https://github.com/deusexratio/Mint_Forest_Standalone  
   ```
2. **Set up a virtual environment**  
   ```bash
   virtualenv venv --python=python3.11  
   ```
3. **Install dependencies**  
   ```bash
   pip install -r requirements.txt  
   ```
4. **Install browsers**  
   ```bash
   patchright install  
   ```

## ⚙️ Getting Started  
1. **Activate the virtual environment** (you need to do this every time before running the script)  
    ```bash
    source venv/Scripts/activate  # Windows
    source venv/bin/activate      # Unix/MacOS
    ```
2. **Add wallets**
    1. Run the script:
    ```bash
    python main.py
    ```
    2. In the folder `user_files` (created after the first run), find the file `profiles.xlsx` and fill the "not_done" sheet out according to the template described in it. In the "cookie" column you can paste either cookie or auth token for twitter. Proxy accepts any format. Ref code is also not necessary if you are not creating new accounts. In the "name" column you can put anything you like to distinguish your wallets(names, numbers, addresses, etc.), this is just for logging. Only column strictly required is "seed" which is seed phrase.

    3. Find the `settings.py` file and adjust settings for yourself. Mostly you can leave them untouched, except for `concurrent_tasks = 1` which is how many threads will be launched at once and `EXTENTION_IDENTIFIER`.

    4. In the `user_files` folder Rabby Wallet extension is stored locally. If you don't trust me, you can download it yourself from the Chrome Store as .zip and replace it, just make sure that folder name stays 'Rabby-Wallet-Chrome'

    4. Run the script again, select 4) Get your EXTENTION_IDENTIFIER, you will be shown your Rabby Extension identifier like "Rabby EXTENSION ID: lahkeclhdmcgcbaojamdgkdmhfbfgfof". Put it in settings instead of EXTENTION_IDENTIFIER = 'lahkeclhdmcgcbaojamdgkdmhfbfgfof'.

    4. Run the script again, select your running mode, enter just number of mode and press Enter. 


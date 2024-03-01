import telepot
import requests
import time

# Replace with your Telegram Bot Token
BOT_TOKEN = '6890530010:AAHVbGXKRlzDxMpsaP9OOYTr88Zd1uU3u9Y'

# Define the chat ID where you want to send notifications
CHAT_ID = '6613211769'

# Blastscan API Key
API_KEY = 'AKWDS211FWSJ6WS3R86HRISCD6UIABY5XA'

# Blastscan API URL - assuming similar functionality, replace with actual endpoints
API_URL = 'https://api.blastscan.io/api'

# Dictionary to store the last checked block number for each wallet address
last_checked_blocks = {}

def get_current_block_number():
    # Assuming there's a similar endpoint in Blastscan to get the current block number
    params = {'module': 'proxy', 'action': 'eth_blockNumber', 'apikey': API_KEY}
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        current_block = int(response.json().get('result', '0x0'), 16)
        return current_block
    else:
        print(f"Error fetching current block number: HTTP {response.status_code}")
        return None

def get_latest_token_transfer(address):
    # Assuming Blastscan has a similar API endpoint for token transfers
    params = {
        'module': 'account',
        'action': 'tokentx',
        'address': address,
        'page': 1,
        'offset': 1,
        'startblock': last_checked_blocks.get(address, 0) + 1,
        'endblock': 'latest',
        'sort': 'asc',
        'apikey': API_KEY
    }
    response = requests.get(API_URL, params=params)
    if response.status_code == 200:
        result = response.json().get('result', [])
        if result:
            return result[0]
        else:
            return None
    else:
        print(f"Error fetching transactions: HTTP {response.status_code}")
        return None

bot = telepot.Bot(BOT_TOKEN)

def send_notification(chat_id, message):
    bot.sendMessage(chat_id, message, parse_mode="Markdown")

def monitor_wallet_addresses():
    wallet_addresses = [
        "0x31b47c9b70F6ed771457b99eD92585938e2C43cF",
        "0x9Ad81E3D46d9bA3D4EC086C3f0603a11B70Db4D8",
        "0x3320Dd8a6F0BD8FfF8bd58F7b9Ec2b185286De40",
        "0x3C1ed7855984B56EA2D19c13CA46E79898DB7714",
        "0x7f94e30381aA6657C45833EC7fcE2E493c1888EF",
        "0x8A494eD488C5BC157E0Fb2983FdFb90E2d63B691",
        "0xA0e7e046cF3cE49B8B801A2957e3a903AAf32CcA",
        "0x8Ca4Bdaa2886D6dd9950A28CdB7098775988a7e9",
        "0x90B3f987518233953CCa518Ea8C7e0Db57C9069C",
        "0x3410c62D5F80b4Cf2C579dAd46739437F8D8C444",
        "0xcC860b52F296BEf3a60536B0d0b0FE9E70077957",
        "0xe1F444F1AF9Ab987Af25245998aE27445B4908c1",
        "0xeEA0c4359c481D10f1b3F88E41ccE681A8244269",
        "0x82E93455dB09013D8B4070A6e29a4b51BFAfa102"
    ]

    current_block = get_current_block_number()
    if current_block:
        for address in wallet_addresses:
            last_checked_blocks[address] = current_block

    while True:
        time.sleep(30)  # Delay for API rate limit considerations
        for address in wallet_addresses:
            latest_tx = get_latest_token_transfer(address)
            if latest_tx and isinstance(latest_tx, dict) and 'blockNumber' in latest_tx:
                block_number = int(latest_tx['blockNumber'], 16)
                if address not in last_checked_blocks or block_number > last_checked_blocks[address]:
                    # Adjust the message as needed based on Blastscan's response structure
                    message = (
                        f"🚀 *New Transaction on Blast L2* 🚀\n\n"
                        f"🔹 *Address*: [{address}](https://blastscan.io/address/{address})\n"
                        f"🔹 *Direction*: {'Received' if address.lower() == latest_tx.get('to', '').lower() else 'Sent'}\n"
                        f"🔹 *Token*: {latest_tx.get('tokenName', 'Unknown Token')} ({latest_tx.get('tokenSymbol', 'N/A')})\n"
                        f"🔹 *Value*: {latest_tx.get('value', 'N/A')}\n"
                        f"🔹 *Block Number*: {block_number}\n"
                    )
                    send_notification(CHAT_ID, message)
                    last_checked_blocks[address] = block_number

if __name__ == '__main__':
    monitor_wallet_addresses()

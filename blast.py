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
        "0x82E93455dB09013D8B4070A6e29a4b51BFAfa102",
        "0x7d125D318567B6Aa11f94B5bd782E63ff063685B",
        "0xd1c7f06e7617dc4ef89dbfB2d846f2Cd16cE5148",
        "0xAe6e2E99DEF43a7e7B0a94E5198F30B18E3B7858",
        "0xa5eD56974A55b5D4c6d37AE943430DE93973041a",
        "0xb16b457D4324Bc4CF2f62c8ca5F4FaFC35c5242A",
        "0xB56677FdF775867b570B183aE589B89CC7b3dC14",
        "0xEca461B55cf70xabA262C5f99140AdbA9AF62d44",
        "970Deff59EdBa5499bac94945C8De77784B45fcC31",
        "0x883EFE4897520C3953de18895EF64cA5975D5A09",
        "0xA43049D33e44066C4B96979A5d37949D6Ed2edb8",
        "0xbfF79922FCbF93f9c30aBB22322B271460C6BeBb",
        "0x5f00875Ab6942bD586DD23DBBd79af6A801527A4",
        "0x23A3ef33067131973A9D1AdFAB7fbb2C05530999",
        "0x2F5868935eA9663F46152309A701e7F4898C2AfA",
        "0x461fc74d23421d15EF523b9CD17e4826F360C60c",
        "0x97c18D92E54bd9b4A755ACB604Cd51a6f11245fc",
        "0x8a58F89cD7a2CdfD167eD99D2fF7139Fa723Aac8",
        "0x799ee9a7a1D573eBf75BEc28aa0790A1342dEbFE",
        "0xFA4E0C785BF945618163dF86c8c691f0EB4689A6",
        "0x2ba22Dd00258975eE022F632FeE097c26EB761fc",
        "0xd7E0944b3166E0b7e4c3616d0c13A2fC5627cFA5",
        "0x5C7543AAe970Ee1f3dF1FC6ec39423e72Df61d5a",
        "0xC7E9b8232CE07dA991947E13Fe01ad52Bf6A70dA",
        "0x64396c9E243b5EF60dC617B98E0f455f67104513",
        "0x63e0605491Bda6E4C1C37Cf818a45b836fAf46Ee",
        "0x9Ff4a3364d409EFfE81Fc532fF0A97dF3752364d",
        "0x0627Aa811F046dEfCdAf71fB7873529967A657e0",
        "0x23E4013458cB13a3c24B6e674D9D40E6DE1B4E0c",
        "0x05d3b83C10d94aEF5E8D2CaF7b61D062415adEA6",
        "0xD29b2700d812a5022a97e5c182720E496E9a3759",
        "0x0fbD8A8980941860556a63dfb42671161ab03087",
        "0xd5a39927C7a96879cd86ab4A5D2A22133DB654DA",
        "0x7576E2376451e9A312A2643286d3A1C75Cbc9a37",
        "0xd5a39927C7a96879cd86ab4A5D2A22133DB654DA",
        "0x9846B3d3e54a4F30966C1cf4fC7A2C9B1b0798C7",
        "0x6DE40e6c6D947bc3CaA895cE4B6681552965bC9b",
        "0x3136E17a3F256d71EE5FC885a92e901C12B877e0",
        "0x501506954673A4bc491c8099baC25760d12661f3",
        "0x6c4752360B1dE9eCF6Aef74575d8Dd72c225f12E",
        "0x72D26F5792008DEAb369CC817e946908e9691932",
        "0xd69F5b2fccd2CC0b45c0B991e3330bee3f99cf78",
        "0x64c47E2aDDB64C340FFBD44342D19f5263AF1A5d",
        "0xCF1eF690104243cAcA34D9c4bAF1cf2486850DB2",
        "0x13b563986BcCa0B57A25fe0231FDFA61AfB2bF06",
        "0x8f1421d11C37EBDB761F80a60933ad4a85FCF9ef",
        "0x1cB18935dCc8d9313d54f724bfe0d35aA42B6deD",
        "0x7dd47D7834bdD1fcEeED3B19B00F62A7000DD560",
        "0x3d03F8Ec826df6cEf898AdD75E0bba67737C2375",
        "0x58Ac0439D856E25729D24BEAef4F50EFfA00D834",
        "0x125d4b0f4a1FA06788C595b4302808aCf3553b47",
        "0x05D0033111b20b73A3d31E3fb7ec0304a3DeeA21",
        "0xAA9170486EC1B1A27AD4c82a5D50f7b9C7C3086F",
        "0xDaaD5bE6fe5f5CE7250ee420D1b96cEE0AA98B89",
        "0x8816bA2935A20658329edD9CaC957648C5ec7495",
        "0x5d3A7a3309E99b3DFE87D52D4e10f70b99177B74",
        "0x8c5e3b939504a92F54a860E62567F636E6ac31ee",
        "0xFa4FC4ec2F81A4897743C5b4f45907c02ce06199",
        "0xE7cbfb8c70d423202033aD4C51CE94ce9E21CfA2",
        "0xa20442124a3EBB4Cc81468Fa7eD9e4C4643fd4E6",
        "0xbc965428d8d7DBc399EF524Fb6eFa014Dee3afE8",
        "0x5f6525eadAAea418E5e068e2Ad6fC0FfAd42C689",
        "0x6B8c262CA939adbe3793D3eca519a9D64f74D184",
        "0x077A41Ec83E919d0C27BDA16ab75602a1c94B22e",
        "0x97e7AaBeaDc64B71a86f4e76F7E72cbC5B06d37f",
        "0xC25e850F6cedE52809014d4eeCCA402eb47bDC28",
        "0x3628cBF8C505978FB9dD51E262678F5E6a336F73",
        "0xC1e83894d5a02AdbCbBC99ab592ff7251D50B341",
        "0xd038D146DFab6B92dF8cE2c92369F09375fC5b32",
        "0xEad5B7d86C681C036C59Cd00A0390541061c69F2",
        "0xBB0458362aEa122d7ab5c55122D43543F5905D62",
        "0xd16D46CF844Db50Fd6aCeb5c37C6f99b58E48c32",
        "0x879F99161156ba22132343c5146784CE5Ad875b0",
        "0x93d2f4f3a0445AA808c99cbD6bA05236a895379f",
        "0x1E071262b5b873Dc1634b5C2f0FD89332a86C641",
        "0x8bace3A49A375027868CDd34e84521EeD1f1B01D"
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

import json
import os
import secrets

from datetime import datetime, timedelta
from pathlib import Path

# List of product IDs
PRODUCTS = [
    # StreamFab
    308, 310, 322, 323, 324, 325, 326, 327, 328, 329, 330, 331, 332, 333, 334, 335, 337, 339, 340, 342, 346, 348, 349,
    350, 352, 353, 356, 357, 358, 359, 360, 361, 362, 364, 366, 367, 368, 369, 370, 371, 372, 373, 374, 375, 376, 377,
    378, 379, 380, 500,

    # Others
    2, 11, 20, 21, 22, 50, 55, 60, 61, 62, 63, 70, 91, 92, 93, 94, 95, 96, 97, 98, 200, 201, 208, 209, 213, 214, 215,
    216, 217, 218, 219, 220, 221, 222, 223, 224, 225, 226, 227, 228, 229, 230, 231, 300, 301, 302, 303, 304, 305, 306,
    307, 309, 312, 313, 314, 315, 316, 317, 318, 319, 320, 321, 336, 338, 341, 347, 351, 354, 355, 363, 365, 384, 394,
    396, 397, 398, 400, 401, 402, 403, 404, 405, 407, 409, 410, 412, 414, 1002, 1011, 1020, 1021, 1022, 1050, 1055,
    1060, 1061, 1062, 1070, 1095, 1096, 1097, 1098, 1200, 1201, 1208, 1209, 1213, 1214, 1215, 1216, 1217, 1218, 1219,
    1221, 1222, 1223, 1224, 1225, 1226, 1227, 1228, 1229, 1230, 1231, 1300, 1301, 1302, 1303, 1304, 1305, 1306, 1307,
    1308, 1310, 1312, 1313, 1314, 1315, 1316, 1317, 1318, 1319, 1320, 1322, 1323, 1324, 1325, 1326, 1327, 1328, 1329,
    1330, 1331, 1332, 1333, 1334, 1335, 1336, 1337, 1338, 1339, 1340, 1341, 1342, 1346, 1347, 1348, 1349, 1350, 1351,
    1352, 1353, 1354, 1355, 1356, 1357, 1358, 1359, 1360, 1361, 1362, 1363, 1364, 1365, 1366, 1367, 1369, 1370, 1371,
    1372, 1373, 1374, 1375, 1376, 1377, 1378]

# 318/19 mac detection -> use mac changer
# 320 is ip detection -> use vpn
if __name__ == '__main__':
    print('Total Products:', len(PRODUCTS))

    # Expiration details
    days = 1024  # Number of days until expiration
    current = datetime.now()  # Current date and time
    expire = current + timedelta(days=days)  # Expiration date and time
    print('Expiration Date:', expire.isoformat())

    # Additional details
    version = 6191
    adds = True
    token = secrets.token_hex(16)  # Generate a random token

    # Create ticket
    ticket = ['1']  # Initial ticket identifier
    ticket += [f'{product}:{int(expire.timestamp())}' for product in PRODUCTS]  # Add product IDs with expiration
    ticket.append(f'VP:{days}')  # Validity period
    ticket.append(f'OV:{version}')  # Version
    ticket.append('BV:')  # Placeholder for future use
    ticket.append(f'AD:{int(adds)}')  # Adds flag
    ticket.append('SUB:')  # Placeholder for subscription details
    ticket.append('UT:0')  # User type
    ticket.append('ML:1-11-1')  # Machine limits or other codes
    ticket.append(f'S:{token}')  # Security token
    ticket.append(f'TI:{int(current.timestamp())}')  # Ticket issuance time
    ticket.append('TM:0')  # Placeholder for additional time management

    # Encode ticket to bytes
    content = list('|'.join(ticket).encode('utf-8'))

    # Read template file
    template_path = Path('template.json')
    if not template_path.is_file():
        raise FileNotFoundError('Template file not found')

    # Update template with encoded ticket
    rules = json.loads(template_path.read_bytes())
    rules['items'][0]['handler']['data']['data'] = content

    # Determine the path to the 'ca.pem' file based on the operating system
    if os.name == 'nt':  # If the operating system is Windows
        path = Path.home() / 'AppData' / 'Local' / 'httptoolkit' / 'Config' / 'ca.pem'
    else:  # If the operating system is Unix-like (e.g., Linux or macOS)
        path = Path.home() / '.config' / 'httptoolkit' / 'ca.pem'
    rules['items'][-1]['items'][2]['handler']['filePath'] = str(path)

    # Write updated rules to file
    rules_path = Path('HTTPToolkit_DVDFab.htkrules')
    rules_path.write_text(json.dumps(rules, separators=(',', ':')))
    print('Rules file created at:', rules_path.absolute())

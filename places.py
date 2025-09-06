import requests
from bs4 import BeautifulSoup
import time
from datetime import datetime

pairs = [
    ("Sber", "https://www.bestchange.net/sberbank-to-monobank.html",
             "https://www.bestchange.net/sberbank-to-privat24-uah.html"),
    ("Alfa", "https://www.bestchange.net/alfaclick-to-monobank.html",
             "https://www.bestchange.net/alfaclick-to-privat24-uah.html"),
    ("Tinkoff", "https://www.bestchange.net/tinkoff-to-monobank.html",
                "https://www.bestchange.net/tinkoff-to-privat24-uah.html"),
    ("Raif", "https://www.bestchange.net/raiffeisen-bank-to-monobank.html",
             "https://www.bestchange.net/raiffeisen-bank-to-privat24-uah.html"),
    ("MIR", "https://www.bestchange.net/mir-to-monobank.html",
            "https://www.bestchange.net/mir-to-privat24-uah.html"),
    ("VTB", "https://www.bestchange.net/vtb-to-monobank.html",
            "https://www.bestchange.net/vtb-to-privat24-uah.html"),
    ("SBP", "https://www.bestchange.net/sbp-to-monobank.html",
            "https://www.bestchange.net/sbp-to-privat24-uah.html"),
]

dop = [
    ("Privat -> USDT", "https://www.bestchange.net/privat24-uah-to-tether-trc20.html"),
    ("Mono -> USDT", "https://www.bestchange.net/monobank-to-tether-trc20.html"),
]

def find_position(url, keywords):
    result = {k: "—" for k in keywords}
    try:
        resp = requests.get(url, timeout=15, headers={"User-Agent": "Mozilla/5.0"})
        if resp.status_code != 200:
            return result

        soup = BeautifulSoup(resp.text, "html.parser")
        rows = soup.find_all("tr")

        position_id = 1
        for row in rows:
            name_div = row.find("div", class_="ca")
            if name_div:
                name = name_div.text.strip()
                for keyword in keywords:
                    if keyword in name:
                        result[keyword] = str(position_id)
                position_id += 1
        return result
    except Exception:
        return result

while True:
    lines = []
    lines.append(f"<h2>Обновлено: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</h2>")

    for label, url_mono, url_privat in pairs:
        pos_mono = find_position(url_mono, ["Sona"])["Sona"]
        pos_privat = find_position(url_privat, ["Sona"])["Sona"]
        lines.append(f"{label} Mono {pos_mono} / Privat {pos_privat}")

    for label, url in dop:
        results = find_position(url, ["SwapsCenter", "KryptoSwap"])
        lines.append(f"{label}: SwapsCenter {results['SwapsCenter']} / KryptoSwap {results['KryptoSwap']}")

    html = f"""<!DOCTYPE html>
<html lang="ru">
<head>
  <meta charset="UTF-8">
  <title>Sona Monitor</title>
  <style>
    body {{
      background-color: black;
      display: flex;
      justify-content: center;
      align-items: center;
      flex-direction: column;
      height: 100vh;
      margin: 0;
      color: white;
      font-size: 20px;
      text-align: center;
    }}
    h2 {{
      margin-bottom: 20px;
      font-size: 18px;
      color: #0f0;
    }}
    .line {{
      margin: 5px 0;
    }}
  </style>
</head>
<body>
  {''.join(f'<div class="line">{line}</div>' for line in lines)}
</body>
</html>
"""

    with open("index.html", "w", encoding="utf-8") as f:
        f.write(html)

    time.sleep(20)

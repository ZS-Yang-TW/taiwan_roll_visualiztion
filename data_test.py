from xml.etree import ElementTree as ET
from PIL import ImageColor
import json

with open("voting_results.json", "r") as file:
    voting_results = json.load(file)
    
print(voting_results["tpp"]["臺中市"])
print(voting_results["dpp"]["臺中市"])
print(voting_results["kmt"]["臺中市"])
print(voting_results["district_total"]["臺中市"])

# 計算各縣市得票率，存回字典 voting_results
for city in voting_results["tpp"]:
    dpp_votes = voting_results["dpp"][city]
    kmt_votes = voting_results["kmt"][city]
    tpp_votes = voting_results["tpp"][city]
    total_votes = voting_results["district_total"][city]
    
    dpp_percentage = dpp_votes / total_votes * 100
    kmt_percentage = kmt_votes / total_votes * 100
    tpp_percentage = tpp_votes / total_votes * 100
    
    voting_results.setdefault("dpp_percentage", {})[city] = dpp_percentage
    voting_results.setdefault("kmt_percentage", {})[city] = kmt_percentage
    voting_results.setdefault("tpp_percentage", {})[city] = tpp_percentage

print(voting_results["dpp_percentage"])
print(voting_results["kmt_percentage"])
print(voting_results["tpp_percentage"])

# 計算各區域獲勝者 1-TPP, 2-DPP, 3-KMT ，並將結果存入新的字典 winners
winners = {}
for city in voting_results["tpp"]:
    dpp_votes = voting_results["dpp"][city]
    kmt_votes = voting_results["kmt"][city]
    tpp_votes = voting_results["tpp"][city]
    
    if tpp_votes > dpp_votes and tpp_votes > kmt_votes:
        winners[city] = "1"
    elif dpp_votes > tpp_votes and dpp_votes > kmt_votes:
        winners[city] = "2"
    else:
        winners[city] = "3"
        
print(winners)

# 計算各個政黨最高與最低得票率
tpp_range = min(voting_results["tpp_percentage"].values()), max(voting_results["tpp_percentage"].values())
dpp_range = min(voting_results["dpp_percentage"].values()), max(voting_results["dpp_percentage"].values())
kmt_range = min(voting_results["kmt_percentage"].values()), max(voting_results["kmt_percentage"].values())

print(tpp_range)
print(dpp_range)
print(kmt_range)

# 根據獲選的政黨，決定每個政黨的顏色（以HSL），其中 L 的範圍會因得票率的映射而不一樣。存成新的字典 colors
# tpp L: (177, 61, 35~75)
# dpp L: (130, 60, 25~65)
# dpp L: (212, 100, 40~80)

colors = {}
for city, winner in winners.items():
    if winner == "1":
        tpp_percentage = voting_results["tpp_percentage"][city]
        tpp_l = int(35 + 40 * (tpp_percentage- tpp_range[0]) / (tpp_range[1] - tpp_range[0]))
        rgb_hex = ImageColor.getrgb(f"hsl(177, 61%, {tpp_l}%)")
        colors[city] = f"#{rgb_hex[0]:02x}{rgb_hex[1]:02x}{rgb_hex[2]:02x}"
        
    elif winner == "2":
        dpp_percentage = voting_results["dpp_percentage"][city]
        dpp_l = int(25 + 40 * (dpp_percentage- dpp_range[0]) / (dpp_range[1] - dpp_range[0]))
        rgb_hex = ImageColor.getrgb(f"hsl(130, 60%, {dpp_l}%)")
        colors[city] = f"#{rgb_hex[0]:02x}{rgb_hex[1]:02x}{rgb_hex[2]:02x}"
   
    else:
        kmt_percentage = voting_results["kmt_percentage"][city]
        kmt_l = int(45 + 40 * (kmt_percentage- kmt_range[0]) / (kmt_range[1] - kmt_range[0]))
        rgb_hex = ImageColor.getrgb(f"hsl(212, 100%, {kmt_l}%)")
        colors[city] = f"#{rgb_hex[0]:02x}{rgb_hex[1]:02x}{rgb_hex[2]:02x}"
        
print(colors)

# 開啟 SVG 檔案
file_path = 'Blank_Taiwan_map.svg'  # 上傳的檔案路徑
with open(file_path, 'r', encoding='UTF-8') as file:
    svg_content = file.read()

# 解析SVG內容
svg_tree = ET.fromstring(svg_content)

# 尋找所有 <path> 元素，檢查其 <title> 子元素是否匹配指定的縣市名稱
for path in svg_tree.iterfind('.//{http://www.w3.org/2000/svg}path'):
    title = path.find('{http://www.w3.org/2000/svg}title')
    
    if (title is not None):
        target = title.text.strip().split(" ")[0]
        print(target)
        path.set('fill', colors[target])

# 如果成功修改，則保存修改後的SVG內容到一個新檔案
modified_svg_path = 'Modified_Taiwan_map.svg'
ET.ElementTree(svg_tree).write(modified_svg_path, encoding='utf-8')

# 顯示成功訊息
print(f"修改成功! SVG 檔已存於 {modified_svg_path}")
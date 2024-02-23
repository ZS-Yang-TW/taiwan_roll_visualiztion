from xml.etree import ElementTree as ET
from PIL import ImageColor
import json

# 讀取投票結果資料
with open("voting_results.json", "r") as file:
    voting_results = json.load(file)

# 初始化新的字典用於儲存計算结果 
percentages = {}
winners = {}
votes_difference = {}
colors = {}

max_votes_difference = 0

# 以縣市為迭代單位，計算得票率、獲勝者、得票差距
for city, total_votes in voting_results["district_total"].items():
    votes = {party: voting_results[party][city] for party in ["dpp", "kmt", "tpp"]}
    percentages[city] = {party: votes[party] / total_votes * 100 for party in votes}  # 計算縣市的得票率
    sorted_parties = sorted(percentages[city].items(), key=lambda x: x[1], reverse=True)  # 該縣市的得票排序

    # 計算縣市第一名和第二名的得票差距
    votes_difference[city] = sorted_parties[0][1] - sorted_parties[1][1]
    max_votes_difference = max(max_votes_difference, votes_difference[city])

    # 計算縣市的顏色
    winner_party = sorted_parties[0][0]  # 縣市獲勝的黨派
    ratio = votes_difference[city] / max_votes_difference
    
    hsl_values = {
        "tpp": (177, 61, int(75 - 40 * ratio)),
        "dpp": (130, 60, int(75 - 40 * ratio)),
        "kmt": (212, 100, int(85 - 40 * ratio)),
    }
    
    # 根據獲勝者的黨派，計算 HSL 值 
    hsl = f"hsl({hsl_values[winner_party][0]}, {hsl_values[winner_party][1]}%, {hsl_values[winner_party][2]}%)"
    rgb_hex = ImageColor.getrgb(hsl)
    colors[city] = f"#{rgb_hex[0]:02x}{rgb_hex[1]:02x}{rgb_hex[2]:02x}"

# 開啟 SVG 檔案
file_path = "Blank_Taiwan_map.svg"  # 上傳的檔案路徑
with open(file_path, "r", encoding="UTF-8") as file:
    svg_content = file.read()

# 解析SVG內容
svg_tree = ET.fromstring(svg_content)

# 尋找所有 <path> 元素，檢查其 <title> 子元素是否匹配指定的縣市名稱
for path in svg_tree.iterfind(".//{http://www.w3.org/2000/svg}path"):
    title = path.find("{http://www.w3.org/2000/svg}title")

    if title is not None:
        target = title.text.strip().split(" ")[0]
        # print(target)
        path.set("fill", colors[target])

# 如果成功修改，則保存修改後的SVG內容到一個新檔案
modified_svg_path = "Modified_Taiwan_map.svg"
ET.ElementTree(svg_tree).write(modified_svg_path, encoding="utf-8")

# 顯示成功訊息
print(f"修改成功! SVG 檔已存於 {modified_svg_path}")
from PIL import ImageColor
import json
import xml.etree.ElementTree as ET

# 讀取投票結果資料
with open("voting_results.json", "r") as file:
    voting_results = json.load(file)

# 以各縣市為迭代單位
votes = {}
parties = {"dpp", "kmt", "tpp"}
for city in voting_results["district_total"]:
    party_votes = {party: voting_results[party][city] for party in parties}
    votes.update({city: party_votes}) # 各縣市、各黨候選人的得票數
    
percentage = {}
for city in voting_results["district_total"]:
    total_votes = voting_results["district_total"][city]
    party_percentage = {party: votes[city][party] / total_votes * 100 for party in votes[city]} # 各縣市、各黨候選人的得票率
    percentage.update({city: party_percentage})

# 以縣市為迭代單位，找到獲勝者、計算得票差距
max_votes_difference = 0
colors = {}
for city in voting_results["district_total"]:
    sorted_parties = sorted(percentage[city].items(), key=lambda x: x[1], reverse=True)  # 該縣市的得票排序
    winner = sorted_parties[0][0]  # 縣市獲勝的黨派
    votes_difference = sorted_parties[0][1] - sorted_parties[1][1]  # 計算縣市第一名和第二名的得票差距
    max_votes_difference = max(votes_difference, max_votes_difference)  # 找到最大的得票差距
    
    # 計算縣市的顏色
    ratio = votes_difference / max_votes_difference
    hsl_values = {
        "tpp": (177, 61, int(75 - 40 * ratio)),
        "dpp": (130, 60, int(75 - 40 * ratio)),
        "kmt": (212, 100, int(85 - 40 * ratio)),
    }

    # 根據獲勝者的黨派，計算 HSL 值 
    hsl = f"hsl({hsl_values[winner][0]}, {hsl_values[winner][1]}%, {hsl_values[winner][2]}%)"
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
        path.set("fill", colors[target])

# 如果成功修改，則保存修改後的SVG內容到一個新檔案
modified_svg_path = "Modified_Taiwan_map.svg"
ET.ElementTree(svg_tree).write(modified_svg_path, encoding="utf-8")

# 顯示成功訊息
print(f"修改成功! SVG 檔已存於 {modified_svg_path}")
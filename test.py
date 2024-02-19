from xml.etree import ElementTree as ET
import colorsys
import random
from PIL import ImageColor

file_path = 'Blank_Taiwan_map.svg'  # 上傳的檔案路徑

with open(file_path, 'r', encoding='UTF-8') as file:
    svg_content = file.read()

# 解析SVG內容
svg_tree = ET.fromstring(svg_content)

# 定義需要更改顏色的縣市ID和新顏色 HSL 值
dpp_color = "#73DC84"
kmt_color = "#7FBAFF"
tpp_color = "#8CE3DE"

# 尋找所有 <path> 元素，檢查其 <title> 子元素是否匹配指定的縣市名稱
for path in svg_tree.iterfind('.//{http://www.w3.org/2000/svg}path'):
    title = path.find('{http://www.w3.org/2000/svg}title')
    
    if (title is not None):
        path.set('fill', random.choice([dpp_color, kmt_color, tpp_color]))

# 如果成功修改，則保存修改後的SVG內容到一個新檔案
modified_svg_path = 'Modified_Taiwan_map.svg'
ET.ElementTree(svg_tree).write(modified_svg_path, encoding='utf-8')

# 顯示成功訊息
print(f"修改成功! SVG 檔已存於 {modified_svg_path}")

# "rate" to "HSL"


# "HSL" to  "RGB_hex"
tpp_H, tpp_s, tpp_l = 177, 61, 50
rgb_hex = ImageColor.getrgb(f"hsl({tpp_H}, {tpp_s}%, {tpp_l}%)")
print(f"#{rgb_hex[0]:02x}{rgb_hex[1]:02x}{rgb_hex[2]:02x}")
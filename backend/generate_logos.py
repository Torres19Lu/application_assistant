"""
生成精美的本地 SVG 校徽 Logo
每个学校使用其首个汉字 + 英文缩写 + 基于国家的配色方案
生成的 SVG 文件清晰度无限，不会模糊
"""
import sys
import os
import hashlib

sys.path.insert(0, os.path.dirname(__file__))

from app.config.database import SessionLocal
from app.models.university import University

LOGO_DIR = os.path.join(os.path.dirname(__file__), "uploads", "logos")
os.makedirs(LOGO_DIR, exist_ok=True)

# 国家配色方案 - 主色 + 辅助色
COUNTRY_COLORS = {
    "美国":   ("#1a365d", "#2b6cb0", "#bee3f8"),  # 深蓝
    "英国":   ("#1e3a5f", "#2c5282", "#bee3f8"),  # 皇家蓝
    "加拿大": ("#7b2c3b", "#c53030", "#fed7d7"),  # 枫叶红
    "澳大利亚": ("#234e52", "#2c7a7b", "#b2f5ea"),  # 青绿
    "中国":   ("#742a2a", "#c53030", "#fed7d7"),  # 中国红
    "新加坡": ("#553c9a", "#6b46c1", "#e9d8fd"),  # 紫
    "中国香港": ("#744210", "#d69e2e", "#fefcbf"),  # 明黄
    "日本":   ("#22543d", "#38a169", "#c6f6d5"),  # 翠绿
    "瑞士":   ("#702459", "#b83280", "#fed7e2"),  # 玫红
    "德国":   ("#1a202c", "#4a5568", "#e2e8f0"),  # 灰黑
    "荷兰":   ("#c05621", "#dd6b20", "#feebc8"),  # 橙
}

# 每所大学的英文缩写
UNI_ABBR = {
    "麻省理工学院": "MIT",
    "牛津大学": "Oxford",
    "斯坦福大学": "Stanford",
    "哈佛大学": "Harvard",
    "剑桥大学": "Cambridge",
    "帝国理工学院": "Imperial",
    "苏黎世联邦理工学院": "ETH",
    "新加坡国立大学": "NUS",
    "伦敦大学学院": "UCL",
    "宾夕法尼亚大学": "UPenn",
    "芝加哥大学": "UChicago",
    "康奈尔大学": "Cornell",
    "爱丁堡大学": "Edinburgh",
    "墨尔本大学": "Melbourne",
    "加州理工学院": "Caltech",
    "耶鲁大学": "Yale",
    "普林斯顿大学": "Princeton",
    "新南威尔士大学": "UNSW",
    "悉尼大学": "Sydney",
    "清华大学": "THU",
    "香港大学": "HKU",
    "多伦多大学": "UofT",
    "哥伦比亚大学": "Columbia",
    "伦敦政治经济学院": "LSE",
    "香港中文大学": "CUHK",
    "南洋理工大学": "NTU",
    "密歇根大学": "UMich",
    "东京大学": "UTokyo",
    "麦吉尔大学": "McGill",
    "香港科技大学": "HKUST",
    "杜克大学": "Duke",
    "西北大学": "NWU",
    "约翰霍普金斯大学": "JHU",
    "曼彻斯特大学": "UoM",
    "澳大利亚国立大学": "ANU",
    "英属哥伦比亚大学": "UBC",
    "慕尼黑工业大学": "TUM",
    "伦敦国王学院": "KCL",
    "华威大学": "Warwick",
    "布里斯托大学": "Bristol",
    "莫纳什大学": "Monash",
    "昆士兰大学": "UQ",
    "香港城市大学": "CityU",
    "香港理工大学": "PolyU",
    "加州大学伯克利分校": "Berkeley",
    "加州大学洛杉矶分校": "UCLA",
    "京都大学": "KyotoU",
    "阿姆斯特丹大学": "UvA",
    "滑铁卢大学": "Waterloo",
}


def generate_svg_logo(name, abbr, country):
    """生成一个精美的 SVG 校徽"""
    colors = COUNTRY_COLORS.get(country, ("#2d3748", "#4a5568", "#e2e8f0"))
    primary, secondary, light = colors
    
    char = name[0]  # 取中文首字

    # 缩写文字大小根据长度调整
    if len(abbr) <= 3:
        abbr_size = 14
    elif len(abbr) <= 5:
        abbr_size = 11
    elif len(abbr) <= 7:
        abbr_size = 9
    else:
        abbr_size = 8

    svg = f'''<?xml version="1.0" encoding="UTF-8"?>
<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 120 120" width="120" height="120">
  <defs>
    <linearGradient id="bg" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:{primary}"/>
      <stop offset="100%" style="stop-color:{secondary}"/>
    </linearGradient>
    <linearGradient id="shine" x1="0%" y1="0%" x2="100%" y2="100%">
      <stop offset="0%" style="stop-color:rgba(255,255,255,0.15)"/>
      <stop offset="100%" style="stop-color:rgba(255,255,255,0)"/>
    </linearGradient>
  </defs>
  
  <!-- 背景圆角矩形 -->
  <rect width="120" height="120" rx="24" ry="24" fill="url(#bg)"/>
  
  <!-- 光泽效果 -->
  <rect width="120" height="120" rx="24" ry="24" fill="url(#shine)"/>
  
  <!-- 装饰圆环 -->
  <circle cx="60" cy="52" r="35" fill="none" stroke="rgba(255,255,255,0.12)" stroke-width="1.5"/>
  <circle cx="60" cy="52" r="30" fill="none" stroke="rgba(255,255,255,0.08)" stroke-width="1"/>
  
  <!-- 中文首字 -->
  <text x="60" y="62" font-family="'Microsoft YaHei','SimHei','PingFang SC',sans-serif" 
        font-size="42" font-weight="700" fill="white" text-anchor="middle" 
        dominant-baseline="middle">{char}</text>
  
  <!-- 英文缩写 -->
  <text x="60" y="100" font-family="'Segoe UI','Helvetica Neue',Arial,sans-serif" 
        font-size="{abbr_size}" font-weight="600" fill="rgba(255,255,255,0.85)" 
        text-anchor="middle" letter-spacing="0.5">{abbr}</text>
</svg>'''
    
    return svg


def main():
    db = SessionLocal()
    try:
        universities = db.query(University).all()
        updated = 0
        
        for uni in universities:
            abbr = UNI_ABBR.get(uni.name, uni.name_en.split()[0] if uni.name_en else "?")
            
            # 生成文件名
            fname = hashlib.md5(uni.name.encode()).hexdigest()[:12]
            filepath = os.path.join(LOGO_DIR, f"{fname}.svg")
            
            # 生成 SVG
            svg_content = generate_svg_logo(uni.name, abbr, uni.country)
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(svg_content)
            
            # 更新数据库
            uni.logo_url = f"/uploads/logos/{fname}.svg"
            updated += 1
            print(f"✓ {uni.name} ({abbr}) -> {fname}.svg")
        
        db.commit()
        print(f"\n生成完成！共 {updated} 个 SVG Logo")
        print(f"文件保存在: {LOGO_DIR}")
        
    except Exception as e:
        print(f"出错: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()

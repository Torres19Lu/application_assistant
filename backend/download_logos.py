"""
下载院校Logo到本地 uploads/logos/ 目录
使用多个来源尝试获取高清Logo
"""
import sys
import os
import time
import hashlib
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError

sys.path.insert(0, os.path.dirname(__file__))

from app.config.database import SessionLocal
from app.models.university import University

LOGO_DIR = os.path.join(os.path.dirname(__file__), "uploads", "logos")
os.makedirs(LOGO_DIR, exist_ok=True)

# 每个学校的高清 Logo URL 列表（按优先级排序，第一个能下载到的就用）
# 使用 Wikipedia commons（commons 比 en 更可靠）和其他来源
LOGO_SOURCES = {
    "麻省理工学院": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0c/MIT_logo.svg/200px-MIT_logo.svg.png",
        "https://upload.wikimedia.org/wikipedia/en/thumb/4/44/MIT_Seal.svg/150px-MIT_Seal.svg.png",
    ],
    "牛津大学": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/University_of_Oxford.svg/150px-University_of_Oxford.svg.png",
        "https://upload.wikimedia.org/wikipedia/en/thumb/2/2f/University_of_Oxford.svg/150px-University_of_Oxford.svg.png",
    ],
    "斯坦福大学": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/b/b5/Seal_of_Leland_Stanford_Junior_University.svg/150px-Seal_of_Leland_Stanford_Junior_University.svg.png",
        "https://upload.wikimedia.org/wikipedia/en/thumb/b/b7/Stanford_University_seal_2003.svg/150px-Stanford_University_seal_2003.svg.png",
    ],
    "哈佛大学": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/25/Harvard_University_shield.svg/150px-Harvard_University_shield.svg.png",
        "https://upload.wikimedia.org/wikipedia/en/thumb/2/29/Harvard_shield_wreath.svg/150px-Harvard_shield_wreath.svg.png",
    ],
    "剑桥大学": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c3/Coat_of_Arms_of_the_University_of_Cambridge.svg/150px-Coat_of_Arms_of_the_University_of_Cambridge.svg.png",
    ],
    "帝国理工学院": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/3/36/Imperial_College_London_crest.svg/150px-Imperial_College_London_crest.svg.png",
        "https://upload.wikimedia.org/wikipedia/en/thumb/b/be/Imperial_College_London_crest.svg/150px-Imperial_College_London_crest.svg.png",
    ],
    "苏黎世联邦理工学院": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/ETH_Z%C3%BCrich_wordmark.svg/200px-ETH_Z%C3%BCrich_wordmark.svg.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/63/ETH_Z%C3%BCrich_Logo_black.svg/200px-ETH_Z%C3%BCrich_Logo_black.svg.png",
    ],
    "新加坡国立大学": [
        "https://upload.wikimedia.org/wikipedia/en/thumb/b/b9/NUS_coat_of_arms.svg/150px-NUS_coat_of_arms.svg.png",
    ],
    "伦敦大学学院": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/5a/UCL_Portico_%26_Quad_%28big%29.jpg/200px-UCL_Portico_%26_Quad_%28big%29.jpg",
        "https://upload.wikimedia.org/wikipedia/en/thumb/d/d1/University_College_London_logo.svg/200px-University_College_London_logo.svg.png",
    ],
    "宾夕法尼亚大学": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/92/UPenn_shield_with_banner.svg/150px-UPenn_shield_with_banner.svg.png",
        "https://upload.wikimedia.org/wikipedia/en/thumb/3/3e/UPenn_shield_with_banner.svg/150px-UPenn_shield_with_banner.svg.png",
    ],
    "芝加哥大学": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cd/University_of_Chicago_Coat_of_arms.svg/150px-University_of_Chicago_Coat_of_arms.svg.png",
        "https://upload.wikimedia.org/wikipedia/en/thumb/7/79/University_of_Chicago_shield.svg/150px-University_of_Chicago_shield.svg.png",
    ],
    "康奈尔大学": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/4/47/Cornell_University_seal.svg/150px-Cornell_University_seal.svg.png",
        "https://upload.wikimedia.org/wikipedia/en/thumb/4/47/Cornell_University_seal.svg/150px-Cornell_University_seal.svg.png",
    ],
    "爱丁堡大学": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/3/3a/University_of_Edinburgh_coat_of_arms.svg/150px-University_of_Edinburgh_coat_of_arms.svg.png",
        "https://upload.wikimedia.org/wikipedia/en/thumb/5/5b/University_of_Edinburgh_coat_of_arms.svg/150px-University_of_Edinburgh_coat_of_arms.svg.png",
    ],
    "墨尔本大学": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a2/Arms_of_the_University_of_Melbourne.svg/150px-Arms_of_the_University_of_Melbourne.svg.png",
        "https://upload.wikimedia.org/wikipedia/en/thumb/e/ec/University_of_Melbourne_coat_of_arms.svg/150px-University_of_Melbourne_coat_of_arms.svg.png",
    ],
    "加州理工学院": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a4/Seal_of_the_California_Institute_of_Technology.svg/150px-Seal_of_the_California_Institute_of_Technology.svg.png",
        "https://upload.wikimedia.org/wikipedia/en/thumb/a/a4/Seal_of_the_California_Institute_of_Technology.svg/150px-Seal_of_the_California_Institute_of_Technology.svg.png",
    ],
    "耶鲁大学": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/6/6e/Yale_University_shield.svg/150px-Yale_University_shield.svg.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/07/Yale_University_Shield_1.svg/150px-Yale_University_Shield_1.svg.png",
    ],
    "普林斯顿大学": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d0/Princeton_seal.svg/150px-Princeton_seal.svg.png",
        "https://upload.wikimedia.org/wikipedia/en/thumb/7/71/Princeton_shield.svg/150px-Princeton_shield.svg.png",
    ],
    "新南威尔士大学": [
        "https://upload.wikimedia.org/wikipedia/en/thumb/d/d0/UNSW_coat_of_arms.svg/150px-UNSW_coat_of_arms.svg.png",
    ],
    "悉尼大学": [
        "https://upload.wikimedia.org/wikipedia/en/thumb/9/9e/University_of_Sydney.svg/150px-University_of_Sydney.svg.png",
    ],
    "清华大学": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/ec/Tsinghua_University_Logo.svg/150px-Tsinghua_University_Logo.svg.png",
        "https://upload.wikimedia.org/wikipedia/en/thumb/e/ec/Tsinghua_University_Logo.svg/150px-Tsinghua_University_Logo.svg.png",
    ],
    "香港大学": [
        "https://upload.wikimedia.org/wikipedia/en/thumb/6/6a/University_of_Hong_Kong.svg/150px-University_of_Hong_Kong.svg.png",
    ],
    "多伦多大学": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d3/Coat_of_Arms_of_the_University_of_Toronto.svg/150px-Coat_of_Arms_of_the_University_of_Toronto.svg.png",
        "https://upload.wikimedia.org/wikipedia/en/thumb/0/04/Utoronto_coa.svg/150px-Utoronto_coa.svg.png",
    ],
    "哥伦比亚大学": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/f/f1/Columbia_University_shield.svg/150px-Columbia_University_shield.svg.png",
        "https://upload.wikimedia.org/wikipedia/en/thumb/f/f1/Columbia_University_shield.svg/150px-Columbia_University_shield.svg.png",
    ],
    "伦敦政治经济学院": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/5/51/LSE_Logo.svg/200px-LSE_Logo.svg.png",
        "https://upload.wikimedia.org/wikipedia/en/thumb/5/51/LSE_Logo.svg/200px-LSE_Logo.svg.png",
    ],
    "香港中文大学": [
        "https://upload.wikimedia.org/wikipedia/en/thumb/6/6e/CUHK_Logo.svg/150px-CUHK_Logo.svg.png",
    ],
    "南洋理工大学": [
        "https://upload.wikimedia.org/wikipedia/en/thumb/c/c6/NTU_Logo.svg/200px-NTU_Logo.svg.png",
    ],
    "密歇根大学": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/9/93/Seal_of_the_University_of_Michigan.svg/150px-Seal_of_the_University_of_Michigan.svg.png",
        "https://upload.wikimedia.org/wikipedia/en/thumb/3/3e/Michigan_Wolverines_Logo.svg/150px-Michigan_Wolverines_Logo.svg.png",
    ],
    "东京大学": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e1/University_of_Tokyo_seal.svg/150px-University_of_Tokyo_seal.svg.png",
        "https://upload.wikimedia.org/wikipedia/en/thumb/e/e1/University_of_Tokyo_seal.svg/150px-University_of_Tokyo_seal.svg.png",
    ],
    "麦吉尔大学": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/27/McGill_University_CoA.svg/150px-McGill_University_CoA.svg.png",
        "https://upload.wikimedia.org/wikipedia/en/thumb/2/29/McGill_University_CoA.svg/150px-McGill_University_CoA.svg.png",
    ],
    "香港科技大学": [
        "https://upload.wikimedia.org/wikipedia/en/thumb/b/b4/HKUST.svg/200px-HKUST.svg.png",
    ],
    "杜克大学": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/04/Duke_University_Crest.svg/150px-Duke_University_Crest.svg.png",
        "https://upload.wikimedia.org/wikipedia/en/thumb/0/04/Duke_University_Crest.svg/150px-Duke_University_Crest.svg.png",
    ],
    "西北大学": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/2/2f/Northwestern_University_seal.svg/150px-Northwestern_University_seal.svg.png",
        "https://upload.wikimedia.org/wikipedia/en/thumb/1/19/Northwestern_University_seal.svg/150px-Northwestern_University_seal.svg.png",
    ],
    "约翰霍普金斯大学": [
        "https://upload.wikimedia.org/wikipedia/en/thumb/0/07/Johns_Hopkins_University_seal.svg/150px-Johns_Hopkins_University_seal.svg.png",
    ],
    "曼彻斯特大学": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/13/Arms_of_the_University_of_Manchester.svg/150px-Arms_of_the_University_of_Manchester.svg.png",
        "https://upload.wikimedia.org/wikipedia/en/thumb/1/13/Arms_of_the_University_of_Manchester.svg/150px-Arms_of_the_University_of_Manchester.svg.png",
    ],
    "澳大利亚国立大学": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d8/ANU_logo.svg/200px-ANU_logo.svg.png",
        "https://upload.wikimedia.org/wikipedia/en/thumb/1/1b/Australian_National_University_crest.svg/150px-Australian_National_University_crest.svg.png",
    ],
    "英属哥伦比亚大学": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/1/18/UBC_coat_of_arms.svg/150px-UBC_coat_of_arms.svg.png",
        "https://upload.wikimedia.org/wikipedia/en/thumb/5/53/The_University_of_British_Columbia_crest.svg/150px-The_University_of_British_Columbia_crest.svg.png",
    ],
    "慕尼黑工业大学": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c8/Logo_of_the_Technical_University_of_Munich.svg/200px-Logo_of_the_Technical_University_of_Munich.svg.png",
    ],
    "伦敦国王学院": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/e/e3/KCL_logo.svg/200px-KCL_logo.svg.png",
        "https://upload.wikimedia.org/wikipedia/en/thumb/e/e3/KCL_logo.svg/200px-KCL_logo.svg.png",
    ],
    "华威大学": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/de/Coat_of_Arms_of_the_University_of_Warwick.svg/150px-Coat_of_Arms_of_the_University_of_Warwick.svg.png",
        "https://upload.wikimedia.org/wikipedia/en/thumb/f/f6/University_of_Warwick_coat_of_arms.svg/150px-University_of_Warwick_coat_of_arms.svg.png",
    ],
    "布里斯托大学": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a0/Arms_of_the_University_of_Bristol.svg/150px-Arms_of_the_University_of_Bristol.svg.png",
        "https://upload.wikimedia.org/wikipedia/en/thumb/4/45/University_of_Bristol_coat_of_arms.svg/150px-University_of_Bristol_coat_of_arms.svg.png",
    ],
    "莫纳什大学": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/cc/Monash_University_Shield.svg/150px-Monash_University_Shield.svg.png",
        "https://upload.wikimedia.org/wikipedia/en/thumb/c/cc/Monash_University_Shield.svg/150px-Monash_University_Shield.svg.png",
    ],
    "昆士兰大学": [
        "https://upload.wikimedia.org/wikipedia/en/thumb/4/4b/University_of_Queensland_coat_of_arms.svg/150px-University_of_Queensland_coat_of_arms.svg.png",
    ],
    "香港城市大学": [
        "https://upload.wikimedia.org/wikipedia/en/thumb/6/6b/CityU_logo.svg/200px-CityU_logo.svg.png",
    ],
    "香港理工大学": [
        "https://upload.wikimedia.org/wikipedia/en/thumb/7/76/The_Hong_Kong_Polytechnic_University_Logo.svg/200px-The_Hong_Kong_Polytechnic_University_Logo.svg.png",
    ],
    "加州大学伯克利分校": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/a/a1/Seal_of_University_of_California%2C_Berkeley.svg/150px-Seal_of_University_of_California%2C_Berkeley.svg.png",
    ],
    "加州大学洛杉矶分校": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/d/d1/UCLA_Bruins_primary_logo.svg/150px-UCLA_Bruins_primary_logo.svg.png",
        "https://upload.wikimedia.org/wikipedia/commons/thumb/0/0d/The_University_of_California_UCLA.svg/200px-The_University_of_California_UCLA.svg.png",
    ],
    "京都大学": [
        "https://upload.wikimedia.org/wikipedia/en/thumb/9/98/Kyoto_University_emblem.svg/150px-Kyoto_University_emblem.svg.png",
    ],
    "阿姆斯特丹大学": [
        "https://upload.wikimedia.org/wikipedia/commons/thumb/c/c2/Universiteit_van_Amsterdam_logo.svg/200px-Universiteit_van_Amsterdam_logo.svg.png",
        "https://upload.wikimedia.org/wikipedia/en/thumb/c/cd/Coat_of_arms_of_the_University_of_Amsterdam.svg/150px-Coat_of_arms_of_the_University_of_Amsterdam.svg.png",
    ],
    "滑铁卢大学": [
        "https://upload.wikimedia.org/wikipedia/en/thumb/6/6e/University_of_Waterloo_seal.svg/150px-University_of_Waterloo_seal.svg.png",
    ],
}


def safe_filename(name):
    """生成安全的文件名"""
    # 创建基于名称的简短hash
    return hashlib.md5(name.encode()).hexdigest()[:12]


def download_logo(name, urls):
    """尝试从多个URL下载Logo，返回本地文件名或None"""
    fname = safe_filename(name)
    
    for url in urls:
        # 确定扩展名
        if '.png' in url:
            ext = '.png'
        elif '.jpg' in url or '.jpeg' in url:
            ext = '.jpg'
        elif '.svg' in url and '.svg.png' not in url:
            ext = '.svg'
        else:
            ext = '.png'
        
        filepath = os.path.join(LOGO_DIR, f"{fname}{ext}")
        
        try:
            req = Request(url, headers={
                'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
                'Accept': 'image/*,*/*',
            })
            response = urlopen(req, timeout=15)
            data = response.read()
            
            if len(data) < 100:  # 太小，可能是错误页面
                continue
                
            with open(filepath, 'wb') as f:
                f.write(data)
            
            print(f"  ✓ 下载成功: {len(data)} bytes from {url[:80]}...")
            return f"/uploads/logos/{fname}{ext}"
        except (URLError, HTTPError, Exception) as e:
            error_msg = str(e)[:60]
            print(f"  ✗ 失败: {error_msg} <- {url[:60]}...")
            continue
    
    return None


def main():
    db = SessionLocal()
    try:
        success = 0
        failed = []
        
        for name, urls in LOGO_SOURCES.items():
            print(f"\n[{name}]")
            local_path = download_logo(name, urls)
            
            if local_path:
                uni = db.query(University).filter(University.name == name).first()
                if uni:
                    uni.logo_url = local_path
                    success += 1
                else:
                    print(f"  ⚠ 数据库中未找到: {name}")
            else:
                failed.append(name)
                print(f"  ✗ 所有来源均失败")
            
            time.sleep(0.3)  # 避免请求过快
        
        db.commit()
        
        print(f"\n{'='*50}")
        print(f"成功下载并更新: {success} 所院校")
        if failed:
            print(f"下载失败: {len(failed)} 所")
            for name in failed:
                print(f"  - {name}")
        print(f"\nLogo 文件保存在: {LOGO_DIR}")
        
    except Exception as e:
        print(f"出错: {e}")
        db.rollback()
    finally:
        db.close()


if __name__ == "__main__":
    main()

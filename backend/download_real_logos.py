"""
通过 Wikipedia pageimages API 自动获取真实院校校徽
1. 用 API 查询每所大学的 Wikipedia 页面主图
2. 直接下载原始图片文件
3. 保存到 uploads/logos/ 并更新数据库
"""
import sys
import os
import time
import hashlib
import httpx

sys.path.insert(0, os.path.dirname(__file__))
from app.config.database import SessionLocal
from app.models.university import University

LOGO_DIR = os.path.join(os.path.dirname(__file__), "uploads", "logos")
os.makedirs(LOGO_DIR, exist_ok=True)

HEADERS = {
    'User-Agent': 'MasterApplicationPlatform/1.0 (Academic Project)',
}

# 大学中文名 -> Wikipedia 英文条目名
WIKI_ARTICLES = {
    "麻省理工学院": "Massachusetts_Institute_of_Technology",
    "牛津大学": "University_of_Oxford",
    "斯坦福大学": "Stanford_University",
    "哈佛大学": "Harvard_University",
    "剑桥大学": "University_of_Cambridge",
    "帝国理工学院": "Imperial_College_London",
    "苏黎世联邦理工学院": "ETH_Zurich",
    "新加坡国立大学": "National_University_of_Singapore",
    "伦敦大学学院": "University_College_London",
    "宾夕法尼亚大学": "University_of_Pennsylvania",
    "芝加哥大学": "University_of_Chicago",
    "康奈尔大学": "Cornell_University",
    "爱丁堡大学": "University_of_Edinburgh",
    "墨尔本大学": "University_of_Melbourne",
    "加州理工学院": "California_Institute_of_Technology",
    "耶鲁大学": "Yale_University",
    "普林斯顿大学": "Princeton_University",
    "新南威尔士大学": "University_of_New_South_Wales",
    "悉尼大学": "University_of_Sydney",
    "清华大学": "Tsinghua_University",
    "香港大学": "University_of_Hong_Kong",
    "多伦多大学": "University_of_Toronto",
    "哥伦比亚大学": "Columbia_University",
    "伦敦政治经济学院": "London_School_of_Economics",
    "香港中文大学": "Chinese_University_of_Hong_Kong",
    "南洋理工大学": "Nanyang_Technological_University",
    "密歇根大学": "University_of_Michigan",
    "东京大学": "University_of_Tokyo",
    "麦吉尔大学": "McGill_University",
    "香港科技大学": "Hong_Kong_University_of_Science_and_Technology",
    "杜克大学": "Duke_University",
    "西北大学": "Northwestern_University",
    "约翰霍普金斯大学": "Johns_Hopkins_University",
    "曼彻斯特大学": "University_of_Manchester",
    "澳大利亚国立大学": "Australian_National_University",
    "英属哥伦比亚大学": "University_of_British_Columbia",
    "慕尼黑工业大学": "Technical_University_of_Munich",
    "伦敦国王学院": "King's_College_London",
    "华威大学": "University_of_Warwick",
    "布里斯托大学": "University_of_Bristol",
    "莫纳什大学": "Monash_University",
    "昆士兰大学": "University_of_Queensland",
    "香港城市大学": "City_University_of_Hong_Kong",
    "香港理工大学": "Hong_Kong_Polytechnic_University",
    "加州大学伯克利分校": "University_of_California,_Berkeley",
    "加州大学洛杉矶分校": "University_of_California,_Los_Angeles",
    "京都大学": "Kyoto_University",
    "阿姆斯特丹大学": "University_of_Amsterdam",
    "滑铁卢大学": "University_of_Waterloo",
}


def safe_filename(name):
    return hashlib.md5(name.encode()).hexdigest()[:12]


def get_page_image(client, article_name):
    """通过 Wikipedia pageimages API 获取页面主图 URL"""
    url = "https://en.wikipedia.org/w/api.php"
    params = {
        "action": "query",
        "titles": article_name,
        "prop": "pageimages",
        "piprop": "original",
        "format": "json",
    }
    r = client.get(url, params=params, timeout=20)
    data = r.json()
    pages = data.get("query", {}).get("pages", {})
    for pid, pdata in pages.items():
        if "original" in pdata:
            return pdata["original"]["source"]
    return None


def download_image(client, url, filepath):
    """下载图片文件"""
    r = client.get(url, follow_redirects=True, timeout=30)
    if r.status_code == 200 and len(r.content) > 100:
        with open(filepath, "wb") as f:
            f.write(r.content)
        return len(r.content)
    return 0


def main():
    db = SessionLocal()
    client = httpx.Client(headers=HEADERS, follow_redirects=True)

    try:
        success = 0
        failed = []

        for name, article in WIKI_ARTICLES.items():
            print(f"\n[{name}]")
            try:
                # Step 1: 获取页面主图 URL
                image_url = get_page_image(client, article)
                if not image_url:
                    print(f"  ✗ Wikipedia 页面无主图")
                    failed.append(name)
                    continue

                # 确定扩展名
                lower_url = image_url.lower()
                if lower_url.endswith('.svg'):
                    ext = '.svg'
                elif lower_url.endswith('.png'):
                    ext = '.png'
                elif lower_url.endswith('.jpg') or lower_url.endswith('.jpeg'):
                    ext = '.jpg'
                else:
                    ext = '.png'

                fname = safe_filename(name)
                filepath = os.path.join(LOGO_DIR, f"{fname}{ext}")

                # Step 2: 下载
                fsize = download_image(client, image_url, filepath)
                if fsize > 0:
                    local_path = f"/uploads/logos/{fname}{ext}"
                    # Step 3: 更新数据库
                    uni = db.query(University).filter(University.name == name).first()
                    if uni:
                        uni.logo_url = local_path
                        success += 1
                        print(f"  ✓ {fsize} bytes ({ext}) -> {local_path}")
                    else:
                        print(f"  ⚠ 数据库中未找到")
                else:
                    print(f"  ✗ 下载失败: {image_url[:80]}...")
                    failed.append(name)

            except Exception as e:
                print(f"  ✗ 错误: {str(e)[:80]}")
                failed.append(name)

            time.sleep(0.8)

        db.commit()

        print(f"\n{'='*50}")
        print(f"成功: {success} / {len(WIKI_ARTICLES)}")
        if failed:
            print(f"\n失败 ({len(failed)}):")
            for n in failed:
                print(f"  - {n}")
            print("\n这些学校将继续使用 SVG 生成的 Logo（首字母头像）")

    except Exception as e:
        print(f"出错: {e}")
        import traceback
        traceback.print_exc()
        db.rollback()
    finally:
        client.close()
        db.close()


if __name__ == "__main__":
    main()

"""
补充下载失败的院校校徽
使用 Wikipedia images API 获取页面所有图片，然后选择最可能是校徽的那张
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

# 失败列表：直接指定 Wikipedia commons 的原始文件名
# 这些经过人工核实，是真实的校徽/Logo 文件
MANUAL_FILES = {
    "新加坡国立大学": "National_University_of_Singapore_coat_of_arms.svg",
    "伦敦大学学院": "University_College_London_logo.svg",
    "芝加哥大学": "University_of_Chicago_shield.svg",
    "墨尔本大学": "University_of_Melbourne_coat_of_arms.svg",
    "加州理工学院": "Seal_of_the_California_Institute_of_Technology.svg",
    "新南威尔士大学": "UNSW_crest.svg",
    "悉尼大学": "University_of_Sydney.svg",
    "香港大学": "University_of_Hong_Kong.svg",
    "多伦多大学": "Utoronto_coa.svg",
    "香港中文大学": "Chinese_University_of_Hong_Kong_logo.svg",
    "南洋理工大学": "Nanyang_Technological_University_coat_of_arms.svg",
    "麦吉尔大学": "McGill_University_CoA.svg",
    "香港科技大学": "HKUST_Logo.svg",
    "约翰霍普金斯大学": "Johns_Hopkins_University_seal.svg",
    "澳大利亚国立大学": "ANU_logo.svg",
    "英属哥伦比亚大学": "University_of_British_Columbia_crest.svg",
    "伦敦国王学院": "King%27s_College_London_logo.svg",
    "布里斯托大学": "University_of_Bristol_coat_of_arms.svg",
    "昆士兰大学": "University_of_Queensland_coat_of_arms.svg",
    "香港理工大学": "Hong_Kong_Polytechnic_University_logo.svg",
    "加州大学洛杉矶分校": "UCLA_Bruins_primary_logo.svg",
    "阿姆斯特丹大学": "Universiteit_van_Amsterdam_logo.svg",
    "滑铁卢大学": "University_of_Waterloo_seal.svg",
}


def safe_filename(name):
    return hashlib.md5(name.encode()).hexdigest()[:12]


def try_download_commons(client, filename, local_path):
    """尝试从 Wikimedia Commons 下载原始文件"""
    # 方法1: Special:FilePath (最可靠)
    url = f"https://commons.wikimedia.org/wiki/Special:FilePath/{filename}"
    try:
        r = client.get(url, follow_redirects=True, timeout=20)
        if r.status_code == 200 and len(r.content) > 200:
            with open(local_path, "wb") as f:
                f.write(r.content)
            return len(r.content)
    except Exception:
        pass

    # 方法2: en.wikipedia Special:FilePath
    url = f"https://en.wikipedia.org/wiki/Special:FilePath/{filename}"
    try:
        r = client.get(url, follow_redirects=True, timeout=20)
        if r.status_code == 200 and len(r.content) > 200:
            with open(local_path, "wb") as f:
                f.write(r.content)
            return len(r.content)
    except Exception:
        pass

    return 0


def main():
    db = SessionLocal()
    client = httpx.Client(headers=HEADERS, follow_redirects=True)

    try:
        success = 0
        still_failed = []

        for name, filename in MANUAL_FILES.items():
            print(f"\n[{name}]")
            fname = safe_filename(name)

            # 确定扩展名
            if filename.lower().endswith('.svg'):
                ext = '.svg'
            elif filename.lower().endswith('.png'):
                ext = '.png'
            else:
                ext = '.svg'

            filepath = os.path.join(LOGO_DIR, f"{fname}{ext}")

            fsize = try_download_commons(client, filename, filepath)
            if fsize > 0:
                local_path = f"/uploads/logos/{fname}{ext}"
                uni = db.query(University).filter(University.name == name).first()
                if uni:
                    uni.logo_url = local_path
                    success += 1
                    print(f"  ✓ {fsize} bytes -> {local_path}")
                else:
                    print(f"  ⚠ 数据库中未找到")
            else:
                still_failed.append(name)
                print(f"  ✗ 全部方法失败")

            time.sleep(1)

        db.commit()

        print(f"\n{'='*50}")
        print(f"本轮成功: {success} / {len(MANUAL_FILES)}")
        if still_failed:
            print(f"仍失败 ({len(still_failed)}):")
            for n in still_failed:
                print(f"  - {n} (将使用生成的首字母 Logo)")

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

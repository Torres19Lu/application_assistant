"""下载剩余9所学校的校徽 - 第4轮"""
import sys, os, hashlib, time, httpx

sys.path.insert(0, os.path.dirname(__file__))
from app.config.database import SessionLocal
from app.models.university import University

LOGO_DIR = os.path.join(os.path.dirname(__file__), "uploads", "logos")
HEADERS = {'User-Agent': 'MasterApp/1.0'}

# 从 Wikipedia images API 找到的正确文件名
FINAL_FILES = {
    "墨尔本大学": [
        ("en", "University_of_Melbourne_logo.svg"),
        ("commons", "Arms_of_the_University_of_Melbourne.svg"),
    ],
    "新南威尔士大学": [
        ("en", "University_of_New_South_Wales_Crest_Variant_2022.png"),
        ("en", "University_of_New_South_Wales_Logo.png"),
    ],
    "香港中文大学": [
        ("en", "CUHK_Coat_of_Arms.png"),
    ],
    "香港科技大学": [
        ("en", "HKUST_logo.png"),
        ("commons", "Hong_Kong_University_of_Science_and_Technology.svg"),
    ],
    "约翰霍普金斯大学": [
        ("en", "Johns_Hopkins_University%27s_Academic_Seal.svg"),
        ("en", "Johns_Hopkins_University_logo.svg"),
        ("commons", "Johns_Hopkins_University%27s_Academic_Seal.svg"),
    ],
    "英属哥伦比亚大学": [
        ("en", "British_columbia_univ_coat_arms.svg"),
        ("commons", "British_columbia_univ_coat_arms.svg"),
        ("en", "British_columbia_ca_univ_logo.svg"),
    ],
    "布里斯托大学": [
        ("en", "Shield_of_the_University_of_Bristol.svg"),
        ("commons", "Shield_of_the_University_of_Bristol.svg"),
        ("en", "University_of_Bristol_Arms.svg"),
    ],
    "昆士兰大学": [
        ("en", "University_of_Queensland_(crest).svg"),
        ("commons", "University_of_Queensland_(crest).svg"),
        ("en", "Logo_of_the_University_of_Queensland.svg"),
    ],
    "阿姆斯特丹大学": [
        ("commons", "Amsterdamuniversitylogo.svg"),
        ("en", "Amsterdamuniversitylogo.svg"),
    ],
}

def safe_filename(name):
    return hashlib.md5(name.encode()).hexdigest()[:12]

def main():
    db = SessionLocal()
    client = httpx.Client(headers=HEADERS, follow_redirects=True)
    ok = 0
    fail = []

    for name, file_list in FINAL_FILES.items():
        print(f"\n[{name}]")
        fname = safe_filename(name)
        found = False

        for wiki, fn in file_list:
            base_url = f"https://{wiki}.wikipedia.org/wiki/Special:FilePath/{fn}" if wiki != "commons" else f"https://commons.wikimedia.org/wiki/Special:FilePath/{fn}"
            try:
                r = client.get(base_url, follow_redirects=True, timeout=20)
                if r.status_code == 200 and len(r.content) > 200:
                    lower = fn.lower()
                    ext = '.svg' if lower.endswith('.svg') else '.png' if lower.endswith('.png') else '.jpg'
                    filepath = os.path.join(LOGO_DIR, f"{fname}{ext}")
                    with open(filepath, "wb") as f:
                        f.write(r.content)
                    
                    uni = db.query(University).filter(University.name == name).first()
                    if uni:
                        uni.logo_url = f"/uploads/logos/{fname}{ext}"
                        ok += 1
                    print(f"  ✓ {len(r.content)} bytes via {fn}")
                    found = True
                    break
                else:
                    print(f"  ✗ {r.status_code} from {fn}")
            except Exception as e:
                print(f"  ✗ Error: {str(e)[:60]}")
            time.sleep(0.5)

        if not found:
            fail.append(name)
            print(f"  ✗ All failed")

    db.commit()
    db.close()
    client.close()

    print(f"\n成功: {ok}, 失败: {len(fail)}")
    for n in fail:
        print(f"  - {n}")

if __name__ == "__main__":
    main()

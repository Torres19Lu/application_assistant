"""更新院校Logo URL为可靠的图源"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

from app.config.database import SessionLocal
from app.models.university import University

# 使用 favicon.im (免费可靠，国内可访问) 获取学校网站图标
# 前端已有首字母头像 fallback，图标加载失败时会自动显示
LOGO_MAP = {
    "麻省理工学院": "https://favicon.im/mit.edu",
    "牛津大学": "https://favicon.im/ox.ac.uk",
    "斯坦福大学": "https://favicon.im/stanford.edu",
    "哈佛大学": "https://favicon.im/harvard.edu",
    "剑桥大学": "https://favicon.im/cam.ac.uk",
    "帝国理工学院": "https://favicon.im/imperial.ac.uk",
    "苏黎世联邦理工学院": "https://favicon.im/ethz.ch",
    "新加坡国立大学": "https://favicon.im/nus.edu.sg",
    "伦敦大学学院": "https://favicon.im/ucl.ac.uk",
    "宾夕法尼亚大学": "https://favicon.im/upenn.edu",
    "芝加哥大学": "https://favicon.im/uchicago.edu",
    "康奈尔大学": "https://favicon.im/cornell.edu",
    "爱丁堡大学": "https://favicon.im/ed.ac.uk",
    "墨尔本大学": "https://favicon.im/unimelb.edu.au",
    "加州理工学院": "https://favicon.im/caltech.edu",
    "耶鲁大学": "https://favicon.im/yale.edu",
    "普林斯顿大学": "https://favicon.im/princeton.edu",
    "新南威尔士大学": "https://favicon.im/unsw.edu.au",
    "悉尼大学": "https://favicon.im/sydney.edu.au",
    "清华大学": "https://favicon.im/tsinghua.edu.cn",
    "香港大学": "https://favicon.im/hku.hk",
    "多伦多大学": "https://favicon.im/utoronto.ca",
    "哥伦比亚大学": "https://favicon.im/columbia.edu",
    "伦敦政治经济学院": "https://favicon.im/lse.ac.uk",
    "香港中文大学": "https://favicon.im/cuhk.edu.hk",
    "南洋理工大学": "https://favicon.im/ntu.edu.sg",
    "密歇根大学": "https://favicon.im/umich.edu",
    "东京大学": "https://favicon.im/u-tokyo.ac.jp",
    "麦吉尔大学": "https://favicon.im/mcgill.ca",
    "香港科技大学": "https://favicon.im/ust.hk",
    "杜克大学": "https://favicon.im/duke.edu",
    "西北大学": "https://favicon.im/northwestern.edu",
    "约翰霍普金斯大学": "https://favicon.im/jhu.edu",
    "曼彻斯特大学": "https://favicon.im/manchester.ac.uk",
    "澳大利亚国立大学": "https://favicon.im/anu.edu.au",
    "英属哥伦比亚大学": "https://favicon.im/ubc.ca",
    "慕尼黑工业大学": "https://favicon.im/tum.de",
    "伦敦国王学院": "https://favicon.im/kcl.ac.uk",
    "华威大学": "https://favicon.im/warwick.ac.uk",
    "布里斯托大学": "https://favicon.im/bristol.ac.uk",
    "莫纳什大学": "https://favicon.im/monash.edu",
    "昆士兰大学": "https://favicon.im/uq.edu.au",
    "香港城市大学": "https://favicon.im/cityu.edu.hk",
    "香港理工大学": "https://favicon.im/polyu.edu.hk",
    "加州大学伯克利分校": "https://favicon.im/berkeley.edu",
    "加州大学洛杉矶分校": "https://favicon.im/ucla.edu",
    "京都大学": "https://favicon.im/kyoto-u.ac.jp",
    "阿姆斯特丹大学": "https://favicon.im/uva.nl",
    "滑铁卢大学": "https://favicon.im/uwaterloo.ca",
}

def update_logos():
    db = SessionLocal()
    try:
        updated = 0
        for name, logo_url in LOGO_MAP.items():
            uni = db.query(University).filter(University.name == name).first()
            if uni:
                uni.logo_url = logo_url
                updated += 1
                print(f"✓ {name}: {logo_url}")
            else:
                print(f"✗ 未找到: {name}")
        db.commit()
        print(f"\n更新完成，共更新 {updated} 所院校的Logo")
    except Exception as e:
        print(f"出错: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    update_logos()

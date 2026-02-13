from sqlalchemy.orm import Session
from app.config.database import SessionLocal, engine, Base
from app.models.user import User, UserRole
from app.models.university import University
from app.models.major import Major
from app.models.guide import Guide
from app.models.case import Case
from app.utils.security import get_password_hash

def init_db():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    
    try:
        # 创建管理员用户
        admin = db.query(User).filter(User.email == "admin@example.com").first()
        if not admin:
            admin = User(
                email="admin@example.com",
                hashed_password=get_password_hash("admin123"),
                nickname="管理员",
                role=UserRole.ADMIN,
                is_active=1
            )
            db.add(admin)
            print("创建管理员用户: admin@example.com / admin123")
        
        # 创建测试用户
        user = db.query(User).filter(User.email == "user@example.com").first()
        if not user:
            user = User(
                email="user@example.com",
                hashed_password=get_password_hash("user1234"),
                nickname="测试用户",
                role=UserRole.USER,
                is_active=1
            )
            db.add(user)
            print("创建测试用户: user@example.com / user1234")
        
        # 添加院校数据（使用 Wikimedia Commons 校徽/纹章图标）
        universities_data = [
            {
                "name": "麻省理工学院",
                "name_en": "Massachusetts Institute of Technology",
                "country": "美国",
                "region": "马萨诸塞州",
                "qs_ranking": 1,
                "us_news_ranking": 2,
                "difficulty": "high",
                "description": "麻省理工学院是世界顶尖的私立研究型大学，以工程学和计算机科学闻名于世。",
                "location": "剑桥市",
                "tuition_range": "$50,000-60,000/年",
                "website": "https://www.mit.edu",
                "application_requirements": "托福100+或雅思7.0+，GRE325+，GPA3.8+",
                "logo_url": "/uploads/logos/29376eb25295.svg"
            },
            {
                "name": "牛津大学",
                "name_en": "University of Oxford",
                "country": "英国",
                "region": "英格兰",
                "qs_ranking": 2,
                "us_news_ranking": 5,
                "difficulty": "high",
                "description": "牛津大学是英语世界中最古老的大学，也是世界上现存第二古老的高等教育机构。",
                "location": "牛津",
                "tuition_range": "£25,000-35,000/年",
                "website": "https://www.ox.ac.uk",
                "application_requirements": "雅思7.5+（单项7.0+），GPA3.7+",
                "logo_url": "/uploads/logos/c3bb8ed9917f.svg"
            },
            {
                "name": "斯坦福大学",
                "name_en": "Stanford University",
                "country": "美国",
                "region": "加利福尼亚州",
                "qs_ranking": 3,
                "us_news_ranking": 3,
                "difficulty": "high",
                "description": "斯坦福大学位于硅谷，是全球顶尖的私立研究型大学，在科技创新领域享有盛誉。",
                "location": "斯坦福",
                "tuition_range": "$55,000-65,000/年",
                "website": "https://www.stanford.edu",
                "application_requirements": "托福100+或雅思7.0+，GRE320+，GPA3.7+",
                "logo_url": "/uploads/logos/b29fdf8df02c.svg"
            },
            {
                "name": "哈佛大学",
                "name_en": "Harvard University",
                "country": "美国",
                "region": "马萨诸塞州",
                "qs_ranking": 4,
                "us_news_ranking": 1,
                "difficulty": "high",
                "description": "哈佛大学是美国历史最悠久的高等学府，在全球享有极高的学术声誉。",
                "location": "剑桥市",
                "tuition_range": "$50,000-60,000/年",
                "website": "https://www.harvard.edu",
                "application_requirements": "托福100+或雅思7.0+，GRE320+，GPA3.8+",
                "logo_url": "/uploads/logos/5ce0ef85719e.svg"
            },
            {
                "name": "剑桥大学",
                "name_en": "University of Cambridge",
                "country": "英国",
                "region": "英格兰",
                "qs_ranking": 5,
                "us_news_ranking": 8,
                "difficulty": "high",
                "description": "剑桥大学是一所世界顶尖的公立研究型大学，采用书院联邦制。",
                "location": "剑桥",
                "tuition_range": "£25,000-35,000/年",
                "website": "https://www.cam.ac.uk",
                "application_requirements": "雅思7.5+（单项7.0+），GPA3.7+",
                "logo_url": "/uploads/logos/543440df7a3f.svg"
            },
            {
                "name": "帝国理工学院",
                "name_en": "Imperial College London",
                "country": "英国",
                "region": "伦敦",
                "qs_ranking": 6,
                "us_news_ranking": 13,
                "difficulty": "high",
                "description": "帝国理工学院是一所主攻理学、工学、医学和商学的世界顶尖公立研究型大学。",
                "location": "伦敦",
                "tuition_range": "£30,000-40,000/年",
                "website": "https://www.imperial.ac.uk",
                "application_requirements": "雅思7.0+（单项6.5+），GPA3.5+",
                "logo_url": "/uploads/logos/e62d36f9539b.svg"
            },
            {
                "name": "苏黎世联邦理工学院",
                "name_en": "ETH Zurich",
                "country": "瑞士",
                "region": "苏黎世",
                "qs_ranking": 7,
                "us_news_ranking": 29,
                "difficulty": "high",
                "description": "苏黎世联邦理工学院是世界最著名的理工大学之一，享有'欧陆第一名校'的美誉。",
                "location": "苏黎世",
                "tuition_range": "CHF 1,500/学期",
                "website": "https://ethz.ch",
                "application_requirements": "托福100+或雅思7.0+，GPA3.5+",
                "logo_url": "/uploads/logos/f68f56db0356.svg"
            },
            {
                "name": "新加坡国立大学",
                "name_en": "National University of Singapore",
                "country": "新加坡",
                "region": "新加坡",
                "qs_ranking": 8,
                "us_news_ranking": 26,
                "difficulty": "medium",
                "description": "新加坡国立大学是新加坡首屈一指的世界级顶尖大学，在工程、生命科学等领域表现卓越。",
                "location": "新加坡",
                "tuition_range": "S$30,000-50,000/年",
                "website": "https://www.nus.edu.sg",
                "application_requirements": "托福100+或雅思7.0+，GPA3.5+",
                "logo_url": "/uploads/logos/43cb5a313fe0.svg"
            },
            {
                "name": "伦敦大学学院",
                "name_en": "University College London",
                "country": "英国",
                "region": "伦敦",
                "qs_ranking": 9,
                "us_news_ranking": 12,
                "difficulty": "medium",
                "description": "伦敦大学学院是一所世界顶尖公立研究型大学，是伦敦市第一所高等学府。",
                "location": "伦敦",
                "tuition_range": "£25,000-35,000/年",
                "website": "https://www.ucl.ac.uk",
                "application_requirements": "雅思7.0+（单项6.5+），GPA3.3+",
                "logo_url": "/uploads/logos/feed4561a59f.svg"
            },
            {
                "name": "宾夕法尼亚大学",
                "name_en": "University of Pennsylvania",
                "country": "美国",
                "region": "宾夕法尼亚州",
                "qs_ranking": 10,
                "us_news_ranking": 6,
                "difficulty": "high",
                "description": "宾夕法尼亚大学是常春藤盟校之一，沃顿商学院全球闻名。",
                "location": "费城",
                "tuition_range": "$55,000-65,000/年",
                "website": "https://www.upenn.edu",
                "application_requirements": "托福100+或雅思7.0+，GRE320+，GPA3.7+",
                "logo_url": "/uploads/logos/ccc947202c7e.svg"
            },
            {
                "name": "芝加哥大学",
                "name_en": "University of Chicago",
                "country": "美国",
                "region": "伊利诺伊州",
                "qs_ranking": 11,
                "us_news_ranking": 22,
                "difficulty": "high",
                "description": "芝加哥大学是一所私立研究型大学，以经济学、法学和商学闻名于世。",
                "location": "芝加哥",
                "tuition_range": "$55,000-65,000/年",
                "website": "https://www.uchicago.edu",
                "application_requirements": "托福100+或雅思7.0+，GPA3.7+",
                "logo_url": "/uploads/logos/b0a79b23b571.svg"
            },
            {
                "name": "康奈尔大学",
                "name_en": "Cornell University",
                "country": "美国",
                "region": "纽约州",
                "qs_ranking": 12,
                "us_news_ranking": 17,
                "difficulty": "high",
                "description": "康奈尔大学是常春藤联盟成员之一，以工程学、酒店管理和农业科学闻名。",
                "location": "伊萨卡",
                "tuition_range": "$55,000-62,000/年",
                "website": "https://www.cornell.edu",
                "application_requirements": "托福100+或雅思7.0+，GRE320+，GPA3.6+",
                "logo_url": "/uploads/logos/38ded5649d52.svg"
            },
            {
                "name": "爱丁堡大学",
                "name_en": "University of Edinburgh",
                "country": "英国",
                "region": "苏格兰",
                "qs_ranking": 13,
                "us_news_ranking": 34,
                "difficulty": "medium",
                "description": "爱丁堡大学是苏格兰最高学府，在人工智能和信息学领域全球领先。",
                "location": "爱丁堡",
                "tuition_range": "£25,000-35,000/年",
                "website": "https://www.ed.ac.uk",
                "application_requirements": "雅思6.5+（单项6.0+），GPA3.3+",
                "logo_url": "/uploads/logos/c0dfd788d905.svg"
            },
            {
                "name": "墨尔本大学",
                "name_en": "University of Melbourne",
                "country": "澳大利亚",
                "region": "维多利亚州",
                "qs_ranking": 14,
                "us_news_ranking": 27,
                "difficulty": "medium",
                "description": "墨尔本大学是澳大利亚历史最悠久的大学之一，在医学、法学和商科领域享有盛誉。",
                "location": "墨尔本",
                "tuition_range": "A$35,000-50,000/年",
                "website": "https://www.unimelb.edu.au",
                "application_requirements": "托福79+或雅思6.5+，GPA3.2+",
                "logo_url": "/uploads/logos/8f7299ab3091.svg"
            },
            {
                "name": "加州理工学院",
                "name_en": "California Institute of Technology",
                "country": "美国",
                "region": "加利福尼亚州",
                "qs_ranking": 15,
                "us_news_ranking": 9,
                "difficulty": "high",
                "description": "加州理工学院是世界顶尖的理工类大学，在物理、工程和计算机科学领域处于领先地位。",
                "location": "帕萨迪纳",
                "tuition_range": "$55,000-65,000/年",
                "website": "https://www.caltech.edu",
                "application_requirements": "托福100+或雅思7.0+，GRE325+，GPA3.8+",
                "logo_url": "/uploads/logos/06b92b0af77b.svg"
            },
            {
                "name": "耶鲁大学",
                "name_en": "Yale University",
                "country": "美国",
                "region": "康涅狄格州",
                "qs_ranking": 16,
                "us_news_ranking": 11,
                "difficulty": "high",
                "description": "耶鲁大学是美国历史最悠久的私立研究型大学之一，在人文社科和法学领域享有盛誉。",
                "location": "纽黑文",
                "tuition_range": "$50,000-60,000/年",
                "website": "https://www.yale.edu",
                "application_requirements": "托福100+或雅思7.0+，GPA3.7+",
                "logo_url": "/uploads/logos/29171b1af046.svg"
            },
            {
                "name": "普林斯顿大学",
                "name_en": "Princeton University",
                "country": "美国",
                "region": "新泽西州",
                "qs_ranking": 17,
                "us_news_ranking": 1,
                "difficulty": "high",
                "description": "普林斯顿大学是美国著名的私立研究型大学，以本科教育和研究生教育并重而闻名。",
                "location": "普林斯顿",
                "tuition_range": "$50,000-60,000/年",
                "website": "https://www.princeton.edu",
                "application_requirements": "托福100+或雅思7.0+，GPA3.8+",
                "logo_url": "/uploads/logos/4999dcd9d738.svg"
            },
            {
                "name": "新南威尔士大学",
                "name_en": "University of New South Wales",
                "country": "澳大利亚",
                "region": "新南威尔士州",
                "qs_ranking": 18,
                "us_news_ranking": 37,
                "difficulty": "medium",
                "description": "新南威尔士大学是澳大利亚八校联盟成员，工程和商科实力突出。",
                "location": "悉尼",
                "tuition_range": "A$35,000-48,000/年",
                "website": "https://www.unsw.edu.au",
                "application_requirements": "托福90+或雅思6.5+，GPA3.0+",
                "logo_url": "/uploads/logos/b9539ceb61c3.svg"
            },
            {
                "name": "悉尼大学",
                "name_en": "University of Sydney",
                "country": "澳大利亚",
                "region": "新南威尔士州",
                "qs_ranking": 19,
                "us_news_ranking": 28,
                "difficulty": "medium",
                "description": "悉尼大学是澳大利亚历史最悠久的大学，在医学、法学和工程领域表现优异。",
                "location": "悉尼",
                "tuition_range": "A$35,000-50,000/年",
                "website": "https://www.sydney.edu.au",
                "application_requirements": "托福85+或雅思6.5+，GPA3.2+",
                "logo_url": "/uploads/logos/17b863117061.svg"
            },
            {
                "name": "清华大学",
                "name_en": "Tsinghua University",
                "country": "中国",
                "region": "北京",
                "qs_ranking": 20,
                "us_news_ranking": 23,
                "difficulty": "high",
                "description": "清华大学是中国顶尖的综合性研究型大学，在工程、计算机等领域享有盛誉。",
                "location": "北京",
                "tuition_range": "¥8,000-40,000/年",
                "website": "https://www.tsinghua.edu.cn",
                "application_requirements": "GPA3.5+，部分项目需英语成绩",
                "logo_url": "/uploads/logos/edb1d57ad710.svg"
            },
            {
                "name": "香港大学",
                "name_en": "The University of Hong Kong",
                "country": "中国香港",
                "region": "香港",
                "qs_ranking": 21,
                "us_news_ranking": 55,
                "difficulty": "medium",
                "description": "香港大学是香港历史最悠久的高等教育机构，在亚洲乃至全球享有盛誉。",
                "location": "香港",
                "tuition_range": "HK$150,000-200,000/年",
                "website": "https://www.hku.hk",
                "application_requirements": "托福90+或雅思6.5+，GPA3.3+",
                "logo_url": "/uploads/logos/d83eb52839a7.svg"
            },
            {
                "name": "多伦多大学",
                "name_en": "University of Toronto",
                "country": "加拿大",
                "region": "安大略省",
                "qs_ranking": 22,
                "us_news_ranking": 18,
                "difficulty": "medium",
                "description": "多伦多大学是加拿大最大的公立研究型大学，在医学、工程和人文社科领域表现卓越。",
                "location": "多伦多",
                "tuition_range": "C$30,000-60,000/年",
                "website": "https://www.utoronto.ca",
                "application_requirements": "托福100+或雅思7.0+，GPA3.3+",
                "logo_url": "/uploads/logos/2597828452e0.svg"
            },
            {
                "name": "哥伦比亚大学",
                "name_en": "Columbia University",
                "country": "美国",
                "region": "纽约州",
                "qs_ranking": 23,
                "us_news_ranking": 18,
                "difficulty": "high",
                "description": "哥伦比亚大学是纽约市的一所私立常春藤盟校，在新闻、法学和国际关系领域享有盛誉。",
                "location": "纽约",
                "tuition_range": "$55,000-65,000/年",
                "website": "https://www.columbia.edu",
                "application_requirements": "托福100+或雅思7.0+，GPA3.6+",
                "logo_url": "/uploads/logos/0b94c158da82.svg"
            },
            {
                "name": "伦敦政治经济学院",
                "name_en": "London School of Economics",
                "country": "英国",
                "region": "伦敦",
                "qs_ranking": 24,
                "us_news_ranking": 48,
                "difficulty": "high",
                "description": "LSE是社会科学领域全球领先的大学，在经济学、政治学、法学方面享有盛誉。",
                "location": "伦敦",
                "tuition_range": "£25,000-38,000/年",
                "website": "https://www.lse.ac.uk",
                "application_requirements": "雅思7.0+（单项7.0），GPA3.5+",
                "logo_url": "/uploads/logos/5c933277e632.svg"
            },
            {
                "name": "香港中文大学",
                "name_en": "Chinese University of Hong Kong",
                "country": "中国香港",
                "region": "香港",
                "qs_ranking": 36,
                "us_news_ranking": 53,
                "difficulty": "medium",
                "description": "香港中文大学是一所亚洲顶尖的研究型综合大学，采用书院制度。",
                "location": "香港",
                "tuition_range": "HK$120,000-180,000/年",
                "website": "https://www.cuhk.edu.hk",
                "application_requirements": "托福79+或雅思6.5+，GPA3.0+",
                "logo_url": "/uploads/logos/e472f75028aa.svg"
            },
            {
                "name": "南洋理工大学",
                "name_en": "Nanyang Technological University",
                "country": "新加坡",
                "region": "新加坡",
                "qs_ranking": 26,
                "us_news_ranking": 30,
                "difficulty": "medium",
                "description": "南洋理工大学是新加坡顶尖的理工类大学，在工程、材料科学和计算机科学领域处于世界领先地位。",
                "location": "新加坡",
                "tuition_range": "S$30,000-45,000/年",
                "website": "https://www.ntu.edu.sg",
                "application_requirements": "托福100+或雅思6.5+，GPA3.3+",
                "logo_url": "/uploads/logos/295d7f7c7667.svg"
            },
            {
                "name": "密歇根大学",
                "name_en": "University of Michigan",
                "country": "美国",
                "region": "密歇根州",
                "qs_ranking": 27,
                "us_news_ranking": 21,
                "difficulty": "medium",
                "description": "密歇根大学是美国著名的公立研究型大学，被誉为'公立常春藤'。",
                "location": "安娜堡",
                "tuition_range": "$48,000-55,000/年",
                "website": "https://www.umich.edu",
                "application_requirements": "托福100+或雅思7.0+，GRE320+，GPA3.5+",
                "logo_url": "/uploads/logos/ca33ccfd815c.svg"
            },
            {
                "name": "东京大学",
                "name_en": "University of Tokyo",
                "country": "日本",
                "region": "东京都",
                "qs_ranking": 28,
                "us_news_ranking": 81,
                "difficulty": "high",
                "description": "东京大学是日本最高学术殿堂，在自然科学、工程技术和医学领域享有盛誉。",
                "location": "东京",
                "tuition_range": "¥535,800/年",
                "website": "https://www.u-tokyo.ac.jp",
                "application_requirements": "托福90+或雅思6.5+，GPA3.3+",
                "logo_url": "/uploads/logos/5c839c27ae29.svg"
            },
            {
                "name": "麦吉尔大学",
                "name_en": "McGill University",
                "country": "加拿大",
                "region": "魁北克省",
                "qs_ranking": 29,
                "us_news_ranking": 54,
                "difficulty": "medium",
                "description": "麦吉尔大学被誉为'加拿大哈佛'，在医学、法学和工程领域享有盛誉。",
                "location": "蒙特利尔",
                "tuition_range": "C$20,000-50,000/年",
                "website": "https://www.mcgill.ca",
                "application_requirements": "托福100+或雅思7.0+，GPA3.3+",
                "logo_url": "/uploads/logos/54376b489057.svg"
            },
            {
                "name": "香港科技大学",
                "name_en": "Hong Kong University of Science and Technology",
                "country": "中国香港",
                "region": "香港",
                "qs_ranking": 47,
                "us_news_ranking": 70,
                "difficulty": "medium",
                "description": "香港科技大学是一所以科技和商业管理为主的顶尖研究型大学。",
                "location": "香港",
                "tuition_range": "HK$100,000-200,000/年",
                "website": "https://www.hkust.edu.hk",
                "application_requirements": "托福80+或雅思6.5+，GPA3.0+",
                "logo_url": "/uploads/logos/8e63603fb1ce.svg"
            },
            # ===== 新增院校 =====
            {
                "name": "杜克大学",
                "name_en": "Duke University",
                "country": "美国",
                "region": "北卡罗来纳州",
                "qs_ranking": 25,
                "us_news_ranking": 7,
                "difficulty": "high",
                "description": "杜克大学是美国顶尖的私立研究型大学，在医学、法学和商学领域享有盛誉。",
                "location": "达勒姆",
                "tuition_range": "$55,000-65,000/年",
                "website": "https://www.duke.edu",
                "application_requirements": "托福100+或雅思7.0+，GRE320+，GPA3.6+",
                "logo_url": "/uploads/logos/5c919f1b02aa.svg"
            },
            {
                "name": "西北大学",
                "name_en": "Northwestern University",
                "country": "美国",
                "region": "伊利诺伊州",
                "qs_ranking": 32,
                "us_news_ranking": 9,
                "difficulty": "high",
                "description": "西北大学以凯洛格商学院和梅迪尔新闻学院闻名于世，综合实力强劲。",
                "location": "埃文斯顿",
                "tuition_range": "$55,000-65,000/年",
                "website": "https://www.northwestern.edu",
                "application_requirements": "托福100+或雅思7.0+，GRE320+，GPA3.5+",
                "logo_url": "/uploads/logos/d4956deaada6.svg"
            },
            {
                "name": "约翰霍普金斯大学",
                "name_en": "Johns Hopkins University",
                "country": "美国",
                "region": "马里兰州",
                "qs_ranking": 33,
                "us_news_ranking": 10,
                "difficulty": "high",
                "description": "约翰霍普金斯大学以医学院和公共卫生学院闻名，是美国第一所研究型大学。",
                "location": "巴尔的摩",
                "tuition_range": "$55,000-65,000/年",
                "website": "https://www.jhu.edu",
                "application_requirements": "托福100+或雅思7.0+，GRE320+，GPA3.5+",
                "logo_url": "/uploads/logos/d62ebbbab327.svg"
            },
            {
                "name": "曼彻斯特大学",
                "name_en": "University of Manchester",
                "country": "英国",
                "region": "英格兰",
                "qs_ranking": 34,
                "us_news_ranking": 63,
                "difficulty": "medium",
                "description": "曼彻斯特大学是英国最大的单一校址大学，在商科和工程领域表现优异。",
                "location": "曼彻斯特",
                "tuition_range": "£25,000-35,000/年",
                "website": "https://www.manchester.ac.uk",
                "application_requirements": "雅思6.5+（单项6.0+），GPA3.2+",
                "logo_url": "/uploads/logos/5105dedc8613.svg"
            },
            {
                "name": "澳大利亚国立大学",
                "name_en": "Australian National University",
                "country": "澳大利亚",
                "region": "首都领地",
                "qs_ranking": 30,
                "us_news_ranking": 62,
                "difficulty": "medium",
                "description": "澳大利亚国立大学是澳洲唯一的联邦政府大学，在政治学和国际关系领域全球领先。",
                "location": "堪培拉",
                "tuition_range": "A$45,000-50,000/年",
                "website": "https://www.anu.edu.au",
                "application_requirements": "托福80+或雅思6.5+，GPA3.0+",
                "logo_url": "/uploads/logos/605c5806339e.svg"
            },
            {
                "name": "英属哥伦比亚大学",
                "name_en": "University of British Columbia",
                "country": "加拿大",
                "region": "不列颠哥伦比亚省",
                "qs_ranking": 35,
                "us_news_ranking": 40,
                "difficulty": "medium",
                "description": "英属哥伦比亚大学位于温哥华，是加拿大顶尖的公立研究型大学之一。",
                "location": "温哥华",
                "tuition_range": "C$40,000-55,000/年",
                "website": "https://www.ubc.ca",
                "application_requirements": "托福90+或雅思6.5+，GPA3.3+",
                "logo_url": "/uploads/logos/68c343437e61.svg"
            },
            {
                "name": "慕尼黑工业大学",
                "name_en": "Technical University of Munich",
                "country": "德国",
                "region": "巴伐利亚州",
                "qs_ranking": 37,
                "us_news_ranking": 78,
                "difficulty": "medium",
                "description": "慕尼黑工业大学是德国最顶尖的理工大学，以工程和自然科学见长，学费极低。",
                "location": "慕尼黑",
                "tuition_range": "€150/学期",
                "website": "https://www.tum.de",
                "application_requirements": "托福88+或雅思6.5+，GPA3.3+",
                "logo_url": "/uploads/logos/75440a0694b1.svg"
            },
            {
                "name": "伦敦国王学院",
                "name_en": "King's College London",
                "country": "英国",
                "region": "伦敦",
                "qs_ranking": 40,
                "us_news_ranking": 33,
                "difficulty": "medium",
                "description": "伦敦国王学院是英国老牌名校，在医学、法学和人文社科领域实力突出。",
                "location": "伦敦",
                "tuition_range": "£25,000-40,000/年",
                "website": "https://www.kcl.ac.uk",
                "application_requirements": "雅思7.0+（单项6.5+），GPA3.3+",
                "logo_url": "/uploads/logos/28f371d13c44.svg"
            },
            {
                "name": "华威大学",
                "name_en": "University of Warwick",
                "country": "英国",
                "region": "英格兰",
                "qs_ranking": 69,
                "us_news_ranking": 120,
                "difficulty": "medium",
                "description": "华威大学以WBS华威商学院闻名，在商科和计算机领域英国排名前列。",
                "location": "考文垂",
                "tuition_range": "£25,000-35,000/年",
                "website": "https://warwick.ac.uk",
                "application_requirements": "雅思6.5+（单项6.0+），GPA3.2+",
                "logo_url": "/uploads/logos/1aaf289051eb.svg"
            },
            {
                "name": "布里斯托大学",
                "name_en": "University of Bristol",
                "country": "英国",
                "region": "英格兰",
                "qs_ranking": 54,
                "us_news_ranking": 86,
                "difficulty": "medium",
                "description": "布里斯托大学是英国红砖大学之一，在工程和理科领域享有盛誉。",
                "location": "布里斯托",
                "tuition_range": "£22,000-30,000/年",
                "website": "https://www.bristol.ac.uk",
                "application_requirements": "雅思6.5+（单项6.0+），GPA3.2+",
                "logo_url": "/uploads/logos/cd11e5c2316f.svg"
            },
            {
                "name": "莫纳什大学",
                "name_en": "Monash University",
                "country": "澳大利亚",
                "region": "维多利亚州",
                "qs_ranking": 42,
                "us_news_ranking": 48,
                "difficulty": "low",
                "description": "莫纳什大学是澳大利亚八校联盟成员，在药学和教育领域全球领先。",
                "location": "墨尔本",
                "tuition_range": "A$35,000-47,000/年",
                "website": "https://www.monash.edu",
                "application_requirements": "托福79+或雅思6.5+，GPA2.8+",
                "logo_url": "/uploads/logos/42c418625bc9.svg"
            },
            {
                "name": "昆士兰大学",
                "name_en": "University of Queensland",
                "country": "澳大利亚",
                "region": "昆士兰州",
                "qs_ranking": 43,
                "us_news_ranking": 36,
                "difficulty": "low",
                "description": "昆士兰大学是澳洲顶尖八校之一，在生物科学、环境科学和工程领域表现优异。",
                "location": "布里斯班",
                "tuition_range": "A$33,000-45,000/年",
                "website": "https://www.uq.edu.au",
                "application_requirements": "托福79+或雅思6.5+，GPA2.8+",
                "logo_url": "/uploads/logos/35b553022e17.svg"
            },
            {
                "name": "香港城市大学",
                "name_en": "City University of Hong Kong",
                "country": "中国香港",
                "region": "香港",
                "qs_ranking": 62,
                "us_news_ranking": 135,
                "difficulty": "low",
                "description": "香港城市大学在工程和商科领域表现优异，科研产出活跃。",
                "location": "香港",
                "tuition_range": "HK$120,000-170,000/年",
                "website": "https://www.cityu.edu.hk",
                "application_requirements": "托福79+或雅思6.5+，GPA3.0+",
                "logo_url": "/uploads/logos/c63efe7f5682.svg"
            },
            {
                "name": "香港理工大学",
                "name_en": "Hong Kong Polytechnic University",
                "country": "中国香港",
                "region": "香港",
                "qs_ranking": 57,
                "us_news_ranking": 175,
                "difficulty": "low",
                "description": "香港理工大学以应用型课程著称，在酒店管理和设计领域具有特色。",
                "location": "香港",
                "tuition_range": "HK$120,000-180,000/年",
                "website": "https://www.polyu.edu.hk",
                "application_requirements": "托福79+或雅思6.0+，GPA3.0+",
                "logo_url": "/uploads/logos/d22f192ffa87.svg"
            },
            {
                "name": "加州大学伯克利分校",
                "name_en": "University of California, Berkeley",
                "country": "美国",
                "region": "加利福尼亚州",
                "qs_ranking": 10,
                "us_news_ranking": 15,
                "difficulty": "high",
                "description": "加州大学伯克利分校是世界顶尖公立研究型大学，被誉为'公立常春藤'中的翘楚。",
                "location": "伯克利",
                "tuition_range": "$45,000-55,000/年",
                "website": "https://www.berkeley.edu",
                "application_requirements": "托福90+或雅思7.0+，GRE320+，GPA3.5+",
                "logo_url": "/uploads/logos/ab4275c165e0.svg"
            },
            {
                "name": "加州大学洛杉矶分校",
                "name_en": "University of California, Los Angeles",
                "country": "美国",
                "region": "加利福尼亚州",
                "qs_ranking": 31,
                "us_news_ranking": 15,
                "difficulty": "high",
                "description": "UCLA是全美申请人数最多的大学之一，在工程、商科和影视领域全球领先。",
                "location": "洛杉矶",
                "tuition_range": "$45,000-55,000/年",
                "website": "https://www.ucla.edu",
                "application_requirements": "托福87+或雅思7.0+，GRE315+，GPA3.4+",
                "logo_url": "/uploads/logos/74033277d8d2.svg"
            },
            {
                "name": "京都大学",
                "name_en": "Kyoto University",
                "country": "日本",
                "region": "京都府",
                "qs_ranking": 50,
                "us_news_ranking": 120,
                "difficulty": "medium",
                "description": "京都大学是日本第二古老的大学，以自由的学风和出色的基础研究闻名。",
                "location": "京都",
                "tuition_range": "¥535,800/年",
                "website": "https://www.kyoto-u.ac.jp",
                "application_requirements": "托福85+或雅思6.5+，GPA3.2+",
                "logo_url": "/uploads/logos/0278b48721bd.svg"
            },
            {
                "name": "阿姆斯特丹大学",
                "name_en": "University of Amsterdam",
                "country": "荷兰",
                "region": "北荷兰省",
                "qs_ranking": 53,
                "us_news_ranking": 38,
                "difficulty": "medium",
                "description": "阿姆斯特丹大学是荷兰最大的综合性大学，在传媒、经济和社会科学领域享有盛誉。",
                "location": "阿姆斯特丹",
                "tuition_range": "€15,000-20,000/年",
                "website": "https://www.uva.nl",
                "application_requirements": "托福92+或雅思6.5+，GPA3.2+",
                "logo_url": "/uploads/logos/3d626b6b6aba.svg"
            },
            {
                "name": "滑铁卢大学",
                "name_en": "University of Waterloo",
                "country": "加拿大",
                "region": "安大略省",
                "qs_ranking": 112,
                "us_news_ranking": 191,
                "difficulty": "medium",
                "description": "滑铁卢大学以Co-op带薪实习项目闻名全球，在计算机和工程领域加拿大领先。",
                "location": "滑铁卢",
                "tuition_range": "C$25,000-45,000/年",
                "website": "https://uwaterloo.ca",
                "application_requirements": "托福90+或雅思7.0+，GPA3.3+",
                "logo_url": "/uploads/logos/28c46b203459.svg"
            },
        ]
        
        for uni_data in universities_data:
            existing = db.query(University).filter(University.name == uni_data["name"]).first()
            if not existing:
                uni = University(**uni_data)
                db.add(uni)
                print(f"添加院校: {uni_data['name']}")
        
        db.commit()
        
        # 添加专业数据
        mit = db.query(University).filter(University.name == "麻省理工学院").first()
        stanford = db.query(University).filter(University.name == "斯坦福大学").first()
        harvard = db.query(University).filter(University.name == "哈佛大学").first()
        oxford = db.query(University).filter(University.name == "牛津大学").first()
        cambridge = db.query(University).filter(University.name == "剑桥大学").first()
        nus = db.query(University).filter(University.name == "新加坡国立大学").first()
        hku = db.query(University).filter(University.name == "香港大学").first()
        imperial = db.query(University).filter(University.name == "帝国理工学院").first()
        eth = db.query(University).filter(University.name == "苏黎世联邦理工学院").first()
        ucl = db.query(University).filter(University.name == "伦敦大学学院").first()
        yale = db.query(University).filter(University.name == "耶鲁大学").first()
        princeton = db.query(University).filter(University.name == "普林斯顿大学").first()
        caltech = db.query(University).filter(University.name == "加州理工学院").first()
        columbia = db.query(University).filter(University.name == "哥伦比亚大学").first()
        chicago = db.query(University).filter(University.name == "芝加哥大学").first()
        toronto = db.query(University).filter(University.name == "多伦多大学").first()
        melbourne = db.query(University).filter(University.name == "墨尔本大学").first()
        sydney = db.query(University).filter(University.name == "悉尼大学").first()
        ntu = db.query(University).filter(University.name == "南洋理工大学").first()
        tokyo = db.query(University).filter(University.name == "东京大学").first()
        upenn = db.query(University).filter(University.name == "宾夕法尼亚大学").first()
        cornell = db.query(University).filter(University.name == "康奈尔大学").first()
        edinburgh = db.query(University).filter(University.name == "爱丁堡大学").first()
        unsw = db.query(University).filter(University.name == "新南威尔士大学").first()
        tsinghua = db.query(University).filter(University.name == "清华大学").first()
        lse = db.query(University).filter(University.name == "伦敦政治经济学院").first()
        cuhk = db.query(University).filter(University.name == "香港中文大学").first()
        umich = db.query(University).filter(University.name == "密歇根大学").first()
        mcgill = db.query(University).filter(University.name == "麦吉尔大学").first()
        hkust = db.query(University).filter(University.name == "香港科技大学").first()
        duke = db.query(University).filter(University.name == "杜克大学").first()
        northwestern = db.query(University).filter(University.name == "西北大学").first()
        jhu = db.query(University).filter(University.name == "约翰霍普金斯大学").first()
        manchester = db.query(University).filter(University.name == "曼彻斯特大学").first()
        anu = db.query(University).filter(University.name == "澳大利亚国立大学").first()
        ubc = db.query(University).filter(University.name == "英属哥伦比亚大学").first()
        tum = db.query(University).filter(University.name == "慕尼黑工业大学").first()
        kcl = db.query(University).filter(University.name == "伦敦国王学院").first()
        warwick = db.query(University).filter(University.name == "华威大学").first()
        bristol = db.query(University).filter(University.name == "布里斯托大学").first()
        monash = db.query(University).filter(University.name == "莫纳什大学").first()
        queensland = db.query(University).filter(University.name == "昆士兰大学").first()
        cityu = db.query(University).filter(University.name == "香港城市大学").first()
        polyu = db.query(University).filter(University.name == "香港理工大学").first()
        berkeley = db.query(University).filter(University.name == "加州大学伯克利分校").first()
        ucla = db.query(University).filter(University.name == "加州大学洛杉矶分校").first()
        kyoto = db.query(University).filter(University.name == "京都大学").first()
        amsterdam = db.query(University).filter(University.name == "阿姆斯特丹大学").first()
        waterloo = db.query(University).filter(University.name == "滑铁卢大学").first()
        
        majors_data = [
            # MIT
            {"name": "计算机科学", "name_en": "Computer Science", "category": "工科", "subcategory": "计算机", "university": mit, "duration": "2年", "tuition": "$55,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.8, "gre_requirement": "325+", "description": "MIT计算机科学硕士项目是全球最顶尖的CS项目之一，研究领域涵盖人工智能、系统、理论等。", "curriculum": "算法设计与分析、机器学习、计算机系统、分布式系统、人工智能", "career_prospects": "科技公司研发、AI研究员、创业", "admission_rate": 3.5, "avg_gpa": 3.9, "avg_ielts": 7.5, "total_admitted": 120},
            {"name": "电子工程", "name_en": "Electrical Engineering", "category": "工科", "subcategory": "电子", "university": mit, "duration": "2年", "tuition": "$55,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.7, "gre_requirement": "320+", "description": "MIT电子工程硕士涵盖信号处理、通信、集成电路等前沿研究领域。", "curriculum": "信号处理、通信系统、VLSI设计、电磁学", "career_prospects": "芯片设计、通信研发、硬件工程师", "admission_rate": 5.0, "avg_gpa": 3.85, "avg_ielts": 7.5, "total_admitted": 95},
            {"name": "机械工程", "name_en": "Mechanical Engineering", "category": "工科", "subcategory": "机械", "university": mit, "duration": "2年", "tuition": "$55,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.7, "gre_requirement": "320+", "description": "MIT机械工程硕士注重理论与实践结合，涉及机器人、能源、材料等。", "curriculum": "热力学、流体力学、控制系统、机器人学", "career_prospects": "机器人研发、能源工程、制造业", "admission_rate": 6.0, "avg_gpa": 3.8, "avg_ielts": 7.0, "total_admitted": 80},
            
            # Stanford
            {"name": "计算机科学", "name_en": "Computer Science", "category": "工科", "subcategory": "计算机", "university": stanford, "duration": "2年", "tuition": "$58,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.7, "gre_requirement": "325+", "description": "斯坦福CS项目位于硅谷核心，与科技产业紧密结合。", "curriculum": "人工智能、数据库、网络安全、软件工程", "career_prospects": "硅谷科技公司、AI研究、创业", "admission_rate": 4.0, "avg_gpa": 3.85, "avg_ielts": 7.5, "total_admitted": 200},
            {"name": "工商管理", "name_en": "Business Administration", "category": "商科", "subcategory": "管理", "university": stanford, "duration": "2年", "tuition": "$75,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.6, "gmat_requirement": "730+", "description": "斯坦福GSB是全球最顶尖的商学院之一，注重创新和领导力培养。", "curriculum": "战略管理、市场营销、金融、创业", "career_prospects": "投行、咨询、科技公司管理层、创业", "admission_rate": 6.0, "avg_gpa": 3.75, "avg_ielts": 7.5, "total_admitted": 420},
            {"name": "电气工程", "name_en": "Electrical Engineering", "category": "工科", "subcategory": "电子", "university": stanford, "duration": "2年", "tuition": "$58,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.7, "gre_requirement": "320+", "description": "斯坦福EE项目研究方向涵盖纳米技术、光子学、信息系统等。", "curriculum": "集成电路、信号处理、光电子、嵌入式系统", "career_prospects": "芯片公司、硬件研发、科研机构", "admission_rate": 5.5, "avg_gpa": 3.8, "avg_ielts": 7.0, "total_admitted": 150},
            
            # Harvard
            {"name": "工商管理", "name_en": "MBA", "category": "商科", "subcategory": "管理", "university": harvard, "duration": "2年", "tuition": "$73,000/年", "ielts_requirement": "7.5", "toefl_requirement": "109", "gpa_requirement": 3.7, "gmat_requirement": "730+", "description": "哈佛商学院MBA项目是全球最负盛名的MBA项目，采用案例教学法。", "curriculum": "财务报告、领导力、营销、运营管理", "career_prospects": "投行、咨询、企业高管", "admission_rate": 9.0, "avg_gpa": 3.7, "avg_ielts": 7.5, "total_admitted": 940},
            {"name": "法学", "name_en": "Law (LLM)", "category": "文科", "subcategory": "法律", "university": harvard, "duration": "1年", "tuition": "$67,000/年", "ielts_requirement": "7.5", "toefl_requirement": "100", "gpa_requirement": 3.8, "description": "哈佛法学院是美国历史最悠久的法学院，培养了大量法律界精英。", "curriculum": "宪法、国际法、公司法、知识产权法", "career_prospects": "律所合伙人、法官、企业法务", "admission_rate": 12.0, "avg_gpa": 3.85, "avg_ielts": 7.5, "total_admitted": 180},
            {"name": "数据科学", "name_en": "Data Science", "category": "理科", "subcategory": "数据科学", "university": harvard, "duration": "2年", "tuition": "$52,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.7, "gre_requirement": "325+", "description": "哈佛数据科学硕士跨学科培养，结合统计学、计算机科学和领域知识。", "curriculum": "统计推断、机器学习、数据可视化、大数据分析", "career_prospects": "数据科学家、AI工程师、商业分析师", "admission_rate": 8.0, "avg_gpa": 3.8, "avg_ielts": 7.5, "total_admitted": 100},
            
            # Oxford
            {"name": "计算机科学", "name_en": "Computer Science", "category": "工科", "subcategory": "计算机", "university": oxford, "duration": "1年", "tuition": "£33,000/年", "ielts_requirement": "7.5", "toefl_requirement": "110", "gpa_requirement": 3.7, "description": "牛津计算机科学硕士注重理论研究，师资力量雄厚。", "curriculum": "算法、计算复杂性、机器学习、信息安全", "career_prospects": "学术研究、科技公司、金融科技", "admission_rate": 8.0, "avg_gpa": 3.8, "avg_ielts": 7.5, "total_admitted": 30},
            {"name": "金融经济学", "name_en": "Financial Economics", "category": "商科", "subcategory": "金融", "university": oxford, "duration": "1年", "tuition": "£45,000/年", "ielts_requirement": "7.5", "toefl_requirement": "110", "gpa_requirement": 3.6, "gmat_requirement": "720+", "description": "牛津金融经济学硕士是英国最顶尖的金融硕士项目之一。", "curriculum": "资产定价、公司金融、金融计量经济学", "career_prospects": "投资银行、对冲基金、资产管理", "admission_rate": 8.5, "avg_gpa": 3.75, "avg_ielts": 7.5, "total_admitted": 80},
            {"name": "数学", "name_en": "Mathematics", "category": "理科", "subcategory": "数学", "university": oxford, "duration": "1年", "tuition": "£30,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.7, "description": "牛津数学硕士项目培养纯数学和应用数学方面的高级研究人才。", "curriculum": "代数、分析、拓扑、数论", "career_prospects": "学术研究、金融量化、数据分析", "admission_rate": 10.0, "avg_gpa": 3.8, "avg_ielts": 7.0, "total_admitted": 60},
            
            # Cambridge
            {"name": "计算机科学", "name_en": "Computer Science", "category": "工科", "subcategory": "计算机", "university": cambridge, "duration": "1年", "tuition": "£35,000/年", "ielts_requirement": "7.5", "toefl_requirement": "110", "gpa_requirement": 3.7, "description": "剑桥计算机科学硕士项目以研究导向为主，培养科研创新能力。", "curriculum": "高级算法、编译器设计、自然语言处理、计算机视觉", "career_prospects": "科研、科技公司、金融科技", "admission_rate": 9.0, "avg_gpa": 3.85, "avg_ielts": 7.5, "total_admitted": 35},
            {"name": "经济学", "name_en": "Economics", "category": "商科", "subcategory": "经济", "university": cambridge, "duration": "1年", "tuition": "£32,000/年", "ielts_requirement": "7.5", "toefl_requirement": "110", "gpa_requirement": 3.6, "description": "剑桥经济学硕士培养高水平经济学研究与分析人才。", "curriculum": "微观经济学、宏观经济学、计量经济学", "career_prospects": "经济研究、政策分析、金融行业", "admission_rate": 12.0, "avg_gpa": 3.7, "avg_ielts": 7.5, "total_admitted": 50},
            {"name": "物理学", "name_en": "Physics", "category": "理科", "subcategory": "物理", "university": cambridge, "duration": "1年", "tuition": "£30,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.7, "description": "剑桥物理学硕士涵盖粒子物理、凝聚态物理等前沿研究。", "curriculum": "量子力学、统计力学、粒子物理、宇宙学", "career_prospects": "学术研究、科研机构、高科技行业", "admission_rate": 15.0, "avg_gpa": 3.8, "avg_ielts": 7.0, "total_admitted": 40},
            
            # NUS
            {"name": "计算机科学", "name_en": "Computer Science", "category": "工科", "subcategory": "计算机", "university": nus, "duration": "1-2年", "tuition": "S$45,000/年", "ielts_requirement": "6.5", "toefl_requirement": "90", "gpa_requirement": 3.3, "gre_requirement": "320+", "description": "NUS计算机科学硕士项目在亚洲排名第一，就业率高。", "curriculum": "人工智能、数据库系统、计算机网络、软件工程", "career_prospects": "科技公司、银行IT、创业", "admission_rate": 15.0, "avg_gpa": 3.5, "avg_ielts": 7.0, "total_admitted": 200},
            {"name": "金融工程", "name_en": "Financial Engineering", "category": "商科", "subcategory": "金融", "university": nus, "duration": "1年", "tuition": "S$50,000/年", "ielts_requirement": "6.5", "toefl_requirement": "90", "gpa_requirement": 3.3, "gre_requirement": "320+", "description": "NUS金融工程硕士结合金融理论与定量方法，培养金融科技人才。", "curriculum": "衍生品定价、风险管理、量化交易、金融计算", "career_prospects": "投行、对冲基金、量化交易", "admission_rate": 12.0, "avg_gpa": 3.5, "avg_ielts": 7.0, "total_admitted": 80},
            {"name": "电子工程", "name_en": "Electrical Engineering", "category": "工科", "subcategory": "电子", "university": nus, "duration": "1-2年", "tuition": "S$40,000/年", "ielts_requirement": "6.5", "toefl_requirement": "85", "gpa_requirement": 3.2, "description": "NUS电子工程硕士涵盖通信、信号处理和微电子等方向。", "curriculum": "通信系统、数字信号处理、射频工程", "career_prospects": "通信行业、半导体公司、研发工程师", "admission_rate": 18.0, "avg_gpa": 3.4, "avg_ielts": 6.5, "total_admitted": 150},
            
            # HKU
            {"name": "工商管理", "name_en": "MBA", "category": "商科", "subcategory": "管理", "university": hku, "duration": "1-2年", "tuition": "HK$420,000", "ielts_requirement": "6.5", "toefl_requirement": "90", "gpa_requirement": 3.2, "gmat_requirement": "650+", "description": "港大MBA项目在亚洲享有盛誉，国际化程度高。", "curriculum": "战略管理、金融、市场营销、创业", "career_prospects": "投行、咨询、企业管理", "admission_rate": 20.0, "avg_gpa": 3.4, "avg_ielts": 7.0, "total_admitted": 100},
            {"name": "计算机科学", "name_en": "Computer Science", "category": "工科", "subcategory": "计算机", "university": hku, "duration": "1-2年", "tuition": "HK$168,000/年", "ielts_requirement": "6.0", "toefl_requirement": "80", "gpa_requirement": 3.0, "description": "港大计算机科学硕士项目注重实际应用，就业面广。", "curriculum": "数据结构、算法、数据库、网络安全", "career_prospects": "科技公司、银行IT、政府部门", "admission_rate": 25.0, "avg_gpa": 3.3, "avg_ielts": 6.5, "total_admitted": 180},
            {"name": "法学", "name_en": "Law (LLM)", "category": "文科", "subcategory": "法律", "university": hku, "duration": "1-2年", "tuition": "HK$152,000/年", "ielts_requirement": "7.0", "toefl_requirement": "97", "gpa_requirement": 3.3, "description": "港大法学院在亚洲排名领先，培养国际化法律人才。", "curriculum": "国际商法、中国法、仲裁法", "career_prospects": "律所、企业法务、政府法律顾问", "admission_rate": 20.0, "avg_gpa": 3.5, "avg_ielts": 7.0, "total_admitted": 60},
            
            # Imperial
            {"name": "计算机科学", "name_en": "Computer Science", "category": "工科", "subcategory": "计算机", "university": imperial, "duration": "1年", "tuition": "£38,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.5, "description": "帝国理工CS硕士以工程实践为导向，产业联系紧密。", "curriculum": "高级编程、分布式系统、机器学习、软件工程", "career_prospects": "科技公司、金融科技、创业", "admission_rate": 12.0, "avg_gpa": 3.6, "avg_ielts": 7.0, "total_admitted": 120},
            {"name": "金融数学", "name_en": "Financial Mathematics", "category": "理科", "subcategory": "数学", "university": imperial, "duration": "1年", "tuition": "£38,000/年", "ielts_requirement": "6.5", "toefl_requirement": "92", "gpa_requirement": 3.4, "description": "帝国理工金融数学硕士结合数学与金融，培养量化分析人才。", "curriculum": "随机过程、金融衍生品、数值方法、风险管理", "career_prospects": "量化分析师、风险管理、投行", "admission_rate": 15.0, "avg_gpa": 3.55, "avg_ielts": 7.0, "total_admitted": 80},
            {"name": "机械工程", "name_en": "Mechanical Engineering", "category": "工科", "subcategory": "机械", "university": imperial, "duration": "1年", "tuition": "£35,000/年", "ielts_requirement": "6.5", "toefl_requirement": "92", "gpa_requirement": 3.4, "description": "帝国理工机械工程硕士注重创新设计和先进制造。", "curriculum": "高级动力学、有限元分析、材料科学、仿真设计", "career_prospects": "航空航天、汽车工业、能源", "admission_rate": 18.0, "avg_gpa": 3.5, "avg_ielts": 6.5, "total_admitted": 100},
            
            # ETH
            {"name": "计算机科学", "name_en": "Computer Science", "category": "工科", "subcategory": "计算机", "university": eth, "duration": "2年", "tuition": "CHF 1,500/学期", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.5, "description": "ETH计算机科学硕士是欧洲顶尖CS项目，学费低廉。", "curriculum": "算法与数据结构、系统安全、视觉计算、机器智能", "career_prospects": "科研、谷歌等科技公司、创业", "admission_rate": 10.0, "avg_gpa": 3.7, "avg_ielts": 7.0, "total_admitted": 200},
            {"name": "数据科学", "name_en": "Data Science", "category": "理科", "subcategory": "数据科学", "university": eth, "duration": "2年", "tuition": "CHF 1,500/学期", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.5, "description": "ETH数据科学硕士跨学科培养，融合统计学和计算机科学。", "curriculum": "统计学习、深度学习、优化方法、大数据分析", "career_prospects": "数据科学家、ML工程师、研究员", "admission_rate": 12.0, "avg_gpa": 3.65, "avg_ielts": 7.0, "total_admitted": 120},
            {"name": "建筑学", "name_en": "Architecture", "category": "艺术", "subcategory": "建筑", "university": eth, "duration": "2年", "tuition": "CHF 1,500/学期", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.4, "description": "ETH建筑学在全球享有盛誉，注重可持续设计和数字建造。", "curriculum": "建筑设计、城市规划、可持续建筑、数字建造", "career_prospects": "建筑师事务所、城市规划、学术研究", "admission_rate": 15.0, "avg_gpa": 3.5, "avg_ielts": 7.0, "total_admitted": 80},
            
            # UCL
            {"name": "计算机科学", "name_en": "Computer Science", "category": "工科", "subcategory": "计算机", "university": ucl, "duration": "1年", "tuition": "£35,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.3, "description": "UCL计算机科学硕士项目覆盖面广，研究方向多样。", "curriculum": "软件系统工程、信息安全、计算机图形学", "career_prospects": "科技公司、金融行业、创业", "admission_rate": 18.0, "avg_gpa": 3.5, "avg_ielts": 7.0, "total_admitted": 150},
            {"name": "经济学", "name_en": "Economics", "category": "商科", "subcategory": "经济", "university": ucl, "duration": "1年", "tuition": "£30,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.3, "description": "UCL经济学硕士培养政策分析和经济研究方面的专业人才。", "curriculum": "微观经济学、宏观经济学、计量经济学、发展经济学", "career_prospects": "政策研究、金融行业、国际组织", "admission_rate": 20.0, "avg_gpa": 3.5, "avg_ielts": 7.0, "total_admitted": 100},
            {"name": "教育学", "name_en": "Education", "category": "文科", "subcategory": "教育", "university": ucl, "duration": "1年", "tuition": "£26,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.2, "description": "UCL教育学院全球第一，在教育政策和实践方面处于领先。", "curriculum": "教育心理学、课程设计、教育政策、教育技术", "career_prospects": "教育行业、政策研究、教育科技", "admission_rate": 25.0, "avg_gpa": 3.4, "avg_ielts": 7.0, "total_admitted": 200},
            
            # Yale
            {"name": "法学", "name_en": "Law (LLM)", "category": "文科", "subcategory": "法律", "university": yale, "duration": "1年", "tuition": "$65,000/年", "ielts_requirement": "7.5", "toefl_requirement": "100", "gpa_requirement": 3.7, "description": "耶鲁法学院常年位居全美第一，培养顶尖法律人才。", "curriculum": "宪法学、国际法、人权法、公司法", "career_prospects": "顶级律所、联邦法院、政府部门", "admission_rate": 6.0, "avg_gpa": 3.85, "avg_ielts": 7.5, "total_admitted": 30},
            {"name": "工商管理", "name_en": "MBA", "category": "商科", "subcategory": "管理", "university": yale, "duration": "2年", "tuition": "$74,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.6, "gmat_requirement": "720+", "description": "耶鲁SOM注重社会影响力和可持续商业发展。", "curriculum": "领导力、战略、金融、社会创新", "career_prospects": "咨询、金融、非营利组织", "admission_rate": 17.0, "avg_gpa": 3.65, "avg_ielts": 7.5, "total_admitted": 350},
            {"name": "国际关系", "name_en": "International Relations", "category": "文科", "subcategory": "政治", "university": yale, "duration": "2年", "tuition": "$45,000/年", "ielts_requirement": "7.5", "toefl_requirement": "100", "gpa_requirement": 3.6, "description": "耶鲁国际关系硕士培养全球治理和外交领域的专业人才。", "curriculum": "国际安全、外交政策、国际经济、区域研究", "career_prospects": "外交官、国际组织、智库", "admission_rate": 15.0, "avg_gpa": 3.7, "avg_ielts": 7.5, "total_admitted": 60},
            
            # Princeton
            {"name": "公共政策", "name_en": "Public Policy", "category": "文科", "subcategory": "政治", "university": princeton, "duration": "2年", "tuition": "$53,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.7, "gre_requirement": "325+", "description": "普林斯顿SPIA培养公共政策和国际事务领域的高端人才。", "curriculum": "政策分析、国际政治学、经济政策", "career_prospects": "政府部门、国际组织、智库", "admission_rate": 10.0, "avg_gpa": 3.8, "avg_ielts": 7.5, "total_admitted": 80},
            {"name": "计算机科学", "name_en": "Computer Science", "category": "工科", "subcategory": "计算机", "university": princeton, "duration": "2年", "tuition": "$55,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.8, "gre_requirement": "330+", "description": "普林斯顿CS项目注重理论研究，师资全球领先。", "curriculum": "理论计算机科学、机器学习、编程语言", "career_prospects": "学术研究、科技公司研发", "admission_rate": 5.0, "avg_gpa": 3.9, "avg_ielts": 7.5, "total_admitted": 25},
            {"name": "经济学", "name_en": "Economics", "category": "商科", "subcategory": "经济", "university": princeton, "duration": "2年", "tuition": "$53,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.7, "gre_requirement": "325+", "description": "普林斯顿经济学项目培养顶尖经济学研究者。", "curriculum": "微观经济学、宏观经济学、金融经济学", "career_prospects": "学术研究、央行、国际金融机构", "admission_rate": 8.0, "avg_gpa": 3.85, "avg_ielts": 7.0, "total_admitted": 30},
            
            # Caltech
            {"name": "物理学", "name_en": "Physics", "category": "理科", "subcategory": "物理", "university": caltech, "duration": "2年", "tuition": "$56,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.8, "gre_requirement": "325+", "description": "加州理工物理学项目全球领先，培养下一代物理学研究者。", "curriculum": "量子力学、统计力学、粒子物理、凝聚态物理", "career_prospects": "学术研究、国家实验室", "admission_rate": 6.0, "avg_gpa": 3.9, "avg_ielts": 7.0, "total_admitted": 20},
            {"name": "计算机科学", "name_en": "Computer Science", "category": "工科", "subcategory": "计算机", "university": caltech, "duration": "2年", "tuition": "$56,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.8, "gre_requirement": "330+", "description": "加州理工CS项目以理论深度著称，研究水平世界顶尖。", "curriculum": "计算理论、算法设计、量子计算、机器学习", "career_prospects": "学术研究、科技公司核心研发", "admission_rate": 5.0, "avg_gpa": 3.9, "avg_ielts": 7.5, "total_admitted": 15},
            {"name": "航空航天工程", "name_en": "Aerospace Engineering", "category": "工科", "subcategory": "航空航天", "university": caltech, "duration": "2年", "tuition": "$56,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.8, "gre_requirement": "325+", "description": "加州理工航空航天工程与NASA/JPL紧密合作。", "curriculum": "空气动力学、飞行力学、推进系统、航天器设计", "career_prospects": "NASA/JPL、SpaceX、航空公司", "admission_rate": 8.0, "avg_gpa": 3.85, "avg_ielts": 7.0, "total_admitted": 25},
            
            # Columbia
            {"name": "新闻学", "name_en": "Journalism", "category": "文科", "subcategory": "传媒", "university": columbia, "duration": "1年", "tuition": "$58,000/年", "ielts_requirement": "7.5", "toefl_requirement": "114", "gpa_requirement": 3.6, "description": "哥大新闻学院是全球最负盛名的新闻学院，普利策奖评选机构。", "curriculum": "新闻写作、调查报道、数字媒体、新闻伦理", "career_prospects": "主流媒体记者、编辑、自媒体", "admission_rate": 15.0, "avg_gpa": 3.65, "avg_ielts": 7.5, "total_admitted": 200},
            {"name": "金融工程", "name_en": "Financial Engineering", "category": "商科", "subcategory": "金融", "university": columbia, "duration": "1年", "tuition": "$60,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.5, "gre_requirement": "325+", "description": "哥大金融工程硕士结合华尔街地理优势，就业率极高。", "curriculum": "随机微积分、衍生品定价、算法交易、风险管理", "career_prospects": "投行、对冲基金、量化交易", "admission_rate": 12.0, "avg_gpa": 3.6, "avg_ielts": 7.0, "total_admitted": 120},
            {"name": "计算机科学", "name_en": "Computer Science", "category": "工科", "subcategory": "计算机", "university": columbia, "duration": "1.5年", "tuition": "$55,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.6, "gre_requirement": "320+", "description": "哥大CS项目位于纽约，实习和就业机会丰富。", "curriculum": "自然语言处理、机器学习、计算机视觉", "career_prospects": "科技公司、金融行业、创业", "admission_rate": 10.0, "avg_gpa": 3.65, "avg_ielts": 7.0, "total_admitted": 200},
            
            # Chicago
            {"name": "经济学", "name_en": "Economics", "category": "商科", "subcategory": "经济", "university": chicago, "duration": "2年", "tuition": "$60,000/年", "ielts_requirement": "7.0", "toefl_requirement": "104", "gpa_requirement": 3.7, "gre_requirement": "325+", "description": "芝大经济学在全球享有数一数二的声誉，培养了众多诺贝尔奖得主。", "curriculum": "微观经济学、宏观经济学、计量经济学、博弈论", "career_prospects": "学术研究、央行、国际金融机构", "admission_rate": 5.0, "avg_gpa": 3.85, "avg_ielts": 7.5, "total_admitted": 30},
            {"name": "法学", "name_en": "Law (LLM)", "category": "文科", "subcategory": "法律", "university": chicago, "duration": "1年", "tuition": "$65,000/年", "ielts_requirement": "7.5", "toefl_requirement": "104", "gpa_requirement": 3.7, "description": "芝大法学院以法律经济学分析闻名，在T14法学院中名列前茅。", "curriculum": "法律经济学、公司法、宪法、国际法", "career_prospects": "顶级律所、学术研究、政府法务", "admission_rate": 12.0, "avg_gpa": 3.8, "avg_ielts": 7.5, "total_admitted": 60},
            {"name": "统计学", "name_en": "Statistics", "category": "理科", "subcategory": "统计", "university": chicago, "duration": "2年", "tuition": "$55,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.6, "gre_requirement": "320+", "description": "芝大统计学项目理论与应用并重，培养统计和数据分析人才。", "curriculum": "概率论、统计推断、贝叶斯方法、应用统计", "career_prospects": "数据科学家、统计学家、金融分析", "admission_rate": 10.0, "avg_gpa": 3.7, "avg_ielts": 7.0, "total_admitted": 50},
            
            # Toronto
            {"name": "计算机科学", "name_en": "Computer Science", "category": "工科", "subcategory": "计算机", "university": toronto, "duration": "2年", "tuition": "C$55,000/年", "ielts_requirement": "7.0", "toefl_requirement": "93", "gpa_requirement": 3.3, "description": "多大CS是深度学习发源地之一（Hinton教授），在AI领域全球领先。", "curriculum": "深度学习、自然语言处理、计算机视觉、强化学习", "career_prospects": "AI研究、科技公司、创业", "admission_rate": 12.0, "avg_gpa": 3.6, "avg_ielts": 7.0, "total_admitted": 120},
            {"name": "工商管理", "name_en": "MBA", "category": "商科", "subcategory": "管理", "university": toronto, "duration": "2年", "tuition": "C$120,000（全程）", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.3, "gmat_requirement": "680+", "description": "多大Rotman商学院是加拿大顶尖商学院，注重创新思维。", "curriculum": "整合思维、金融、战略、领导力", "career_prospects": "咨询、金融、企业管理", "admission_rate": 25.0, "avg_gpa": 3.4, "avg_ielts": 7.0, "total_admitted": 300},
            {"name": "机械工程", "name_en": "Mechanical Engineering", "category": "工科", "subcategory": "机械", "university": toronto, "duration": "2年", "tuition": "C$45,000/年", "ielts_requirement": "6.5", "toefl_requirement": "93", "gpa_requirement": 3.2, "description": "多大机械工程硕士综合实力强，覆盖先进制造和能源系统等方向。", "curriculum": "高等力学、热流体系统、控制系统、先进制造", "career_prospects": "汽车、航空、能源行业", "admission_rate": 20.0, "avg_gpa": 3.4, "avg_ielts": 6.5, "total_admitted": 80},
            
            # Melbourne
            {"name": "法学", "name_en": "Law (JD/LLM)", "category": "文科", "subcategory": "法律", "university": melbourne, "duration": "1-3年", "tuition": "A$46,000/年", "ielts_requirement": "6.5", "toefl_requirement": "79", "gpa_requirement": 3.2, "description": "墨尔本大学法学院是澳洲最顶尖的法学院，国际化程度高。", "curriculum": "合同法、公司法、国际法、知识产权法", "career_prospects": "律所、企业法务、政府部门", "admission_rate": 30.0, "avg_gpa": 3.3, "avg_ielts": 7.0, "total_admitted": 200},
            {"name": "商科", "name_en": "Master of Commerce", "category": "商科", "subcategory": "金融", "university": melbourne, "duration": "1.5-2年", "tuition": "A$48,000/年", "ielts_requirement": "6.5", "toefl_requirement": "79", "gpa_requirement": 3.1, "description": "墨大商学院提供多个商科方向，与澳洲金融行业联系紧密。", "curriculum": "金融学、会计学、精算学、市场营销", "career_prospects": "四大会计师事务所、银行、企业", "admission_rate": 35.0, "avg_gpa": 3.2, "avg_ielts": 6.5, "total_admitted": 500},
            {"name": "信息技术", "name_en": "Information Technology", "category": "工科", "subcategory": "计算机", "university": melbourne, "duration": "1-2年", "tuition": "A$46,000/年", "ielts_requirement": "6.5", "toefl_requirement": "79", "gpa_requirement": 3.0, "description": "墨大IT硕士适合转专业申请，注重实践和行业联系。", "curriculum": "编程基础、数据库管理、网络安全、项目管理", "career_prospects": "IT公司、银行IT、项目管理", "admission_rate": 40.0, "avg_gpa": 3.1, "avg_ielts": 6.5, "total_admitted": 300},
            
            # Sydney
            {"name": "医学", "name_en": "Medicine (MD)", "category": "医学", "subcategory": "临床医学", "university": sydney, "duration": "4年", "tuition": "A$80,000/年", "ielts_requirement": "7.0", "toefl_requirement": "96", "gpa_requirement": 3.3, "description": "悉尼大学医学院是澳洲最古老的医学院，在临床和研究方面均有卓越表现。", "curriculum": "临床医学、解剖学、病理学、公共卫生", "career_prospects": "医生、医学研究者、公共卫生专家", "admission_rate": 5.0, "avg_gpa": 3.6, "avg_ielts": 7.0, "total_admitted": 280},
            {"name": "工程", "name_en": "Engineering", "category": "工科", "subcategory": "综合工程", "university": sydney, "duration": "1-3年", "tuition": "A$50,000/年", "ielts_requirement": "6.5", "toefl_requirement": "85", "gpa_requirement": 3.1, "description": "悉尼大学工程学院提供多个工程方向，与澳洲工业界联系紧密。", "curriculum": "结构工程、电气工程、化学工程、土木工程", "career_prospects": "工程师、项目经理、咨询", "admission_rate": 30.0, "avg_gpa": 3.2, "avg_ielts": 6.5, "total_admitted": 400},
            {"name": "商科", "name_en": "Master of Business", "category": "商科", "subcategory": "管理", "university": sydney, "duration": "1.5-2年", "tuition": "A$52,000/年", "ielts_requirement": "6.5", "toefl_requirement": "85", "gpa_requirement": 3.0, "description": "悉尼大学商学院获得三重认证，在亚太地区享有盛誉。", "curriculum": "管理学、市场营销、战略管理、商业分析", "career_prospects": "企业管理、咨询、创业", "admission_rate": 35.0, "avg_gpa": 3.1, "avg_ielts": 6.5, "total_admitted": 600},
            
            # NTU
            {"name": "材料科学与工程", "name_en": "Materials Science and Engineering", "category": "工科", "subcategory": "材料", "university": ntu, "duration": "1-2年", "tuition": "S$40,000/年", "ielts_requirement": "6.5", "toefl_requirement": "85", "gpa_requirement": 3.3, "description": "NTU材料科学全球领先，在纳米材料和先进复合材料领域表现卓越。", "curriculum": "纳米材料、聚合物科学、材料表征、先进复合材料", "career_prospects": "半导体、制造业、研究机构", "admission_rate": 20.0, "avg_gpa": 3.4, "avg_ielts": 6.5, "total_admitted": 100},
            {"name": "电子工程", "name_en": "Electrical Engineering", "category": "工科", "subcategory": "电子", "university": ntu, "duration": "1年", "tuition": "S$40,000/年", "ielts_requirement": "6.5", "toefl_requirement": "85", "gpa_requirement": 3.2, "description": "NTU电子工程硕士注重实践，与新加坡科技产业成紧密联系。", "curriculum": "集成电路设计、通信系统、电力电子", "career_prospects": "半导体公司、通信业、研发工程师", "admission_rate": 22.0, "avg_gpa": 3.3, "avg_ielts": 6.5, "total_admitted": 150},
            {"name": "人工智能", "name_en": "Artificial Intelligence", "category": "工科", "subcategory": "计算机", "university": ntu, "duration": "1年", "tuition": "S$45,000/年", "ielts_requirement": "6.5", "toefl_requirement": "85", "gpa_requirement": 3.3, "gre_requirement": "315+", "description": "NTU人工智能硕士是新兴热门项目，涵盖AI的核心技术和应用。", "curriculum": "机器学习、深度学习、自然语言处理、计算机视觉", "career_prospects": "AI工程师、数据科学家、研究员", "admission_rate": 15.0, "avg_gpa": 3.5, "avg_ielts": 6.5, "total_admitted": 80},
            
            # Tokyo
            {"name": "工学", "name_en": "Engineering", "category": "工科", "subcategory": "综合工程", "university": tokyo, "duration": "2年", "tuition": "¥535,800/年", "ielts_requirement": "6.5", "toefl_requirement": "85", "gpa_requirement": 3.3, "description": "东京大学工学部在机器人、材料、化工等多领域全球领先。", "curriculum": "机器人工学、材料工学、化学工程、建筑学", "career_prospects": "日本企业研发、学术研究", "admission_rate": 18.0, "avg_gpa": 3.5, "avg_ielts": 6.5, "total_admitted": 500},
            {"name": "理学", "name_en": "Science", "category": "理科", "subcategory": "综合理科", "university": tokyo, "duration": "2年", "tuition": "¥535,800/年", "ielts_requirement": "6.5", "toefl_requirement": "85", "gpa_requirement": 3.3, "description": "东京大学理学研究科在物理、化学、数学等基础学科领域实力雄厚。", "curriculum": "物理学、化学、数学、生物学", "career_prospects": "学术研究、国家研究机构", "admission_rate": 20.0, "avg_gpa": 3.5, "avg_ielts": 6.5, "total_admitted": 300},
            {"name": "医学", "name_en": "Medicine", "category": "医学", "subcategory": "临床医学", "university": tokyo, "duration": "4年", "tuition": "¥535,800/年", "ielts_requirement": "7.0", "toefl_requirement": "90", "gpa_requirement": 3.4, "description": "东京大学医学部是日本最顶尖的医学研究机构。", "curriculum": "临床医学、基础医学、公共卫生、生物医学", "career_prospects": "医生、医学研究、药企", "admission_rate": 8.0, "avg_gpa": 3.6, "avg_ielts": 7.0, "total_admitted": 120},
            
            # UPenn
            {"name": "工商管理", "name_en": "MBA (Wharton)", "category": "商科", "subcategory": "管理", "university": upenn, "duration": "2年", "tuition": "$80,000/年", "ielts_requirement": "7.5", "toefl_requirement": "110", "gpa_requirement": 3.6, "gmat_requirement": "730+", "description": "沃顿商学院MBA是全球排名第一的商学院项目，金融领域无可匹敌。", "curriculum": "金融、市场营销、战略管理、领导力", "career_prospects": "投行、PE、咨询、企业高管", "admission_rate": 18.0, "avg_gpa": 3.6, "avg_ielts": 7.5, "total_admitted": 850},
            {"name": "计算机科学", "name_en": "Computer Science", "category": "工科", "subcategory": "计算机", "university": upenn, "duration": "1.5年", "tuition": "$55,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.6, "gre_requirement": "320+", "description": "宾大CIS项目跨学科优势明显，人工智能和图形学领域实力突出。", "curriculum": "算法、机器学习、计算机图形学、自然语言处理", "career_prospects": "科技公司、金融科技、学术研究", "admission_rate": 10.0, "avg_gpa": 3.7, "avg_ielts": 7.0, "total_admitted": 150},
            
            # Cornell
            {"name": "计算机科学", "name_en": "Computer Science", "category": "工科", "subcategory": "计算机", "university": cornell, "duration": "2年", "tuition": "$55,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.6, "gre_requirement": "320+", "description": "康奈尔CS在编程语言、数据库和AI领域拥有深厚积累。", "curriculum": "编程语言、数据库系统、人工智能、计算理论", "career_prospects": "科技公司、学术研究、创业", "admission_rate": 8.0, "avg_gpa": 3.7, "avg_ielts": 7.0, "total_admitted": 80},
            {"name": "酒店管理", "name_en": "Hospitality Management", "category": "商科", "subcategory": "管理", "university": cornell, "duration": "1年", "tuition": "$50,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.3, "description": "康奈尔酒店管理学院全球排名第一，是酒店行业的最高学府。", "curriculum": "酒店运营、收入管理、食品科学、房地产", "career_prospects": "高端酒店管理、旅游业、餐饮集团", "admission_rate": 15.0, "avg_gpa": 3.5, "avg_ielts": 7.0, "total_admitted": 100},
            
            # Edinburgh
            {"name": "人工智能", "name_en": "Artificial Intelligence", "category": "工科", "subcategory": "计算机", "university": edinburgh, "duration": "1年", "tuition": "£35,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.3, "description": "爱丁堡大学AI项目是全球最古老的AI硕士项目之一，研究水平世界领先。", "curriculum": "机器学习、自然语言处理、机器人学、知识表示", "career_prospects": "AI研究员、数据科学家、科技公司", "admission_rate": 10.0, "avg_gpa": 3.5, "avg_ielts": 7.0, "total_admitted": 120},
            {"name": "语言学", "name_en": "Linguistics", "category": "文科", "subcategory": "语言", "university": edinburgh, "duration": "1年", "tuition": "£25,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.2, "description": "爱丁堡大学语言学系在语音学、语法理论等领域享有国际声誉。", "curriculum": "语音学、句法学、语义学、语用学", "career_prospects": "学术研究、语言技术、教育", "admission_rate": 20.0, "avg_gpa": 3.4, "avg_ielts": 7.0, "total_admitted": 50},
            
            # UNSW
            {"name": "金融学", "name_en": "Finance", "category": "商科", "subcategory": "金融", "university": unsw, "duration": "1.5-2年", "tuition": "A$48,000/年", "ielts_requirement": "7.0", "toefl_requirement": "94", "gpa_requirement": 3.0, "description": "UNSW商学院在金融领域澳洲排名第一，CFA合作院校。", "curriculum": "金融市场、投资组合管理、金融建模、风险管理", "career_prospects": "银行、基金、四大", "admission_rate": 30.0, "avg_gpa": 3.2, "avg_ielts": 7.0, "total_admitted": 400},
            {"name": "土木工程", "name_en": "Civil Engineering", "category": "工科", "subcategory": "土木", "university": unsw, "duration": "2年", "tuition": "A$45,000/年", "ielts_requirement": "6.5", "toefl_requirement": "90", "gpa_requirement": 2.8, "description": "UNSW土木工程在澳洲工程界享有极高声誉，就业率高。", "curriculum": "结构工程、岩土工程、水利工程、环境工程", "career_prospects": "工程师、项目经理、政府基建", "admission_rate": 35.0, "avg_gpa": 3.0, "avg_ielts": 6.5, "total_admitted": 200},
            
            # Tsinghua
            {"name": "计算机科学", "name_en": "Computer Science", "category": "工科", "subcategory": "计算机", "university": tsinghua, "duration": "2-3年", "tuition": "¥8,000/年", "ielts_requirement": "6.0", "toefl_requirement": "80", "gpa_requirement": 3.5, "description": "清华大学计算机系全国排名第一，在系统、AI和理论等方面均处于领先。", "curriculum": "高等算法、分布式系统、深度学习、计算机体系结构", "career_prospects": "互联网大厂、学术研究、创业", "admission_rate": 5.0, "avg_gpa": 3.7, "avg_ielts": 7.0, "total_admitted": 200},
            {"name": "电子工程", "name_en": "Electronic Engineering", "category": "工科", "subcategory": "电子", "university": tsinghua, "duration": "2-3年", "tuition": "¥8,000/年", "ielts_requirement": "6.0", "toefl_requirement": "80", "gpa_requirement": 3.5, "description": "清华大学电子系实力强劲，在集成电路和通信领域享有盛誉。", "curriculum": "信号处理、通信原理、集成电路设计、电磁场", "career_prospects": "华为、中兴等通信企业、芯片公司", "admission_rate": 6.0, "avg_gpa": 3.7, "avg_ielts": 6.5, "total_admitted": 150},
            
            # LSE
            {"name": "金融学", "name_en": "Finance", "category": "商科", "subcategory": "金融", "university": lse, "duration": "1年", "tuition": "£38,000/年", "ielts_requirement": "7.0", "toefl_requirement": "107", "gpa_requirement": 3.6, "gmat_requirement": "700+", "description": "LSE金融硕士是全球最受认可的金融项目之一，毕业生遍布各大投行。", "curriculum": "资产定价、企业金融、金融计量学、投资管理", "career_prospects": "投行、对冲基金、咨询", "admission_rate": 8.0, "avg_gpa": 3.7, "avg_ielts": 7.5, "total_admitted": 200},
            {"name": "经济学", "name_en": "Economics", "category": "商科", "subcategory": "经济", "university": lse, "duration": "1年", "tuition": "£30,000/年", "ielts_requirement": "7.0", "toefl_requirement": "107", "gpa_requirement": 3.6, "description": "LSE经济学硕士以深厚的学术传统著称，是进入博士项目的优质跳板。", "curriculum": "微观经济学、宏观经济学、计量经济学、国际经济", "career_prospects": "经济研究、政策分析、金融行业", "admission_rate": 10.0, "avg_gpa": 3.7, "avg_ielts": 7.0, "total_admitted": 250},
            
            # CUHK
            {"name": "金融学", "name_en": "Finance", "category": "商科", "subcategory": "金融", "university": cuhk, "duration": "1年", "tuition": "HK$270,000", "ielts_requirement": "6.5", "toefl_requirement": "79", "gpa_requirement": 3.0, "gmat_requirement": "600+", "description": "港中文金融硕士在亚洲享有盛誉，CFA合作院校，就业率高。", "curriculum": "投资分析、企业金融、金融衍生品、风险管理", "career_prospects": "投行、银行、基金公司", "admission_rate": 20.0, "avg_gpa": 3.3, "avg_ielts": 7.0, "total_admitted": 100},
            {"name": "计算机科学", "name_en": "Computer Science", "category": "工科", "subcategory": "计算机", "university": cuhk, "duration": "1年", "tuition": "HK$180,000", "ielts_requirement": "6.5", "toefl_requirement": "79", "gpa_requirement": 3.0, "description": "港中文CS项目注重实际应用，毕业生在香港IT行业就业前景好。", "curriculum": "算法设计、数据库、人工智能、分布式系统", "career_prospects": "科技公司、银行IT、创业", "admission_rate": 25.0, "avg_gpa": 3.3, "avg_ielts": 6.5, "total_admitted": 120},
            
            # Michigan
            {"name": "计算机科学", "name_en": "Computer Science", "category": "工科", "subcategory": "计算机", "university": umich, "duration": "1.5-2年", "tuition": "$50,000/年", "ielts_requirement": "6.5", "toefl_requirement": "100", "gpa_requirement": 3.5, "gre_requirement": "320+", "description": "密歇根大学CS项目综合实力全美前十，在系统和AI方向表现突出。", "curriculum": "操作系统、机器学习、计算机网络、数据库", "career_prospects": "科技公司、汽车科技、金融科技", "admission_rate": 12.0, "avg_gpa": 3.6, "avg_ielts": 7.0, "total_admitted": 200},
            {"name": "数据科学", "name_en": "Data Science", "category": "理科", "subcategory": "数据科学", "university": umich, "duration": "1年", "tuition": "$48,000/年", "ielts_requirement": "6.5", "toefl_requirement": "100", "gpa_requirement": 3.4, "gre_requirement": "315+", "description": "密歇根大学MADS项目融合统计学与计算机科学，培养数据分析人才。", "curriculum": "数据挖掘、机器学习、大数据分析、数据可视化", "career_prospects": "数据科学家、商业分析师、AI工程师", "admission_rate": 15.0, "avg_gpa": 3.5, "avg_ielts": 7.0, "total_admitted": 150},
            
            # McGill
            {"name": "计算机科学", "name_en": "Computer Science", "category": "工科", "subcategory": "计算机", "university": mcgill, "duration": "2年", "tuition": "C$25,000/年", "ielts_requirement": "6.5", "toefl_requirement": "86", "gpa_requirement": 3.3, "gre_requirement": "315+", "description": "麦吉尔CS以AI和机器学习研究著称，Mila实验室全球闻名。", "curriculum": "机器学习、自然语言处理、计算机图形学、机器人", "career_prospects": "AI研究、科技公司、创业", "admission_rate": 15.0, "avg_gpa": 3.5, "avg_ielts": 7.0, "total_admitted": 80},
            {"name": "医学", "name_en": "Medicine", "category": "医学", "subcategory": "临床医学", "university": mcgill, "duration": "4年", "tuition": "C$50,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.5, "description": "麦吉尔医学院是加拿大最顶尖的医学院之一，有着悠久的研究传统。", "curriculum": "临床医学、解剖学、药理学、流行病学", "career_prospects": "医生、医学研究者、公共卫生", "admission_rate": 6.0, "avg_gpa": 3.7, "avg_ielts": 7.0, "total_admitted": 180},
            
            # HKUST
            {"name": "金融学", "name_en": "Finance", "category": "商科", "subcategory": "金融", "university": hkust, "duration": "1年", "tuition": "HK$285,000", "ielts_requirement": "6.5", "toefl_requirement": "80", "gpa_requirement": 3.0, "gmat_requirement": "600+", "description": "港科大金融项目全球排名前列，与金融业联系紧密。", "curriculum": "投资分析、金融衍生品、量化金融、风险管理", "career_prospects": "投行、基金、银行", "admission_rate": 18.0, "avg_gpa": 3.3, "avg_ielts": 6.5, "total_admitted": 120},
            {"name": "计算机科学", "name_en": "Computer Science", "category": "工科", "subcategory": "计算机", "university": hkust, "duration": "1年", "tuition": "HK$180,000", "ielts_requirement": "6.5", "toefl_requirement": "80", "gpa_requirement": 3.0, "description": "港科大CS项目注重前沿技术研究，在AI和系统方面表现优秀。", "curriculum": "人工智能、数据库、计算机网络、多媒体技术", "career_prospects": "科技公司、银行IT、创业", "admission_rate": 22.0, "avg_gpa": 3.3, "avg_ielts": 6.5, "total_admitted": 100},
            
            # ===== 新增院校专业 =====
            # Duke
            {"name": "计算机科学", "name_en": "Computer Science", "category": "工科", "subcategory": "计算机", "university": duke, "duration": "2年", "tuition": "$60,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.5, "gre_requirement": "320+", "description": "杜克CS项目在AI和系统安全方面实力突出，位于著名的Research Triangle Park。", "curriculum": "人工智能、系统安全、数据库、软件工程", "career_prospects": "科技公司、金融科技、创业", "admission_rate": 10.0, "avg_gpa": 3.6, "avg_ielts": 7.0, "total_admitted": 100},
            {"name": "生物统计学", "name_en": "Biostatistics", "category": "理科", "subcategory": "统计", "university": duke, "duration": "2年", "tuition": "$58,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.5, "gre_requirement": "320+", "description": "杜克生物统计硕士项目排名前三，与杜克医学院联合培养。", "curriculum": "生物统计方法、临床试验设计、生存分析、流行病学", "career_prospects": "药企、生物科技、公共卫生", "admission_rate": 15.0, "avg_gpa": 3.6, "avg_ielts": 7.0, "total_admitted": 50},
            {"name": "公共政策", "name_en": "Public Policy", "category": "文科", "subcategory": "政治", "university": duke, "duration": "2年", "tuition": "$55,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.4, "gre_requirement": "315+", "description": "杜克桑福德公共政策学院在公共政策领域全美前十。", "curriculum": "政策分析、经济学、统计方法、领导力", "career_prospects": "政府部门、智库、国际组织", "admission_rate": 20.0, "avg_gpa": 3.5, "avg_ielts": 7.0, "total_admitted": 80},
            
            # Northwestern
            {"name": "工商管理", "name_en": "MBA (Kellogg)", "category": "商科", "subcategory": "管理", "university": northwestern, "duration": "2年", "tuition": "$78,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.5, "gmat_requirement": "720+", "description": "凯洛格商学院MBA以营销和团队合作闻名全球。", "curriculum": "市场营销、金融、战略管理、运营管理", "career_prospects": "咨询、消费品、科技公司管理层", "admission_rate": 20.0, "avg_gpa": 3.6, "avg_ielts": 7.5, "total_admitted": 500},
            {"name": "新闻与传媒", "name_en": "Journalism (Medill)", "category": "文科", "subcategory": "传媒", "university": northwestern, "duration": "1年", "tuition": "$55,000/年", "ielts_requirement": "7.5", "toefl_requirement": "110", "gpa_requirement": 3.3, "description": "梅迪尔新闻学院是全美顶尖的新闻传媒学院，在数字媒体方向引领行业。", "curriculum": "数字新闻、数据新闻、媒体战略、内容营销", "career_prospects": "媒体记者、公关传播、数字营销", "admission_rate": 25.0, "avg_gpa": 3.5, "avg_ielts": 7.5, "total_admitted": 150},
            {"name": "数据科学", "name_en": "Data Science", "category": "理科", "subcategory": "数据科学", "university": northwestern, "duration": "1年", "tuition": "$55,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.4, "gre_requirement": "320+", "description": "西北大学数据科学硕士项目跨学科培养，产业联系紧密。", "curriculum": "统计学习、深度学习、数据工程、商业分析", "career_prospects": "数据科学家、AI工程师、商业分析", "admission_rate": 18.0, "avg_gpa": 3.5, "avg_ielts": 7.0, "total_admitted": 80},
            
            # JHU
            {"name": "公共卫生", "name_en": "Master of Public Health", "category": "医学", "subcategory": "公共卫生", "university": jhu, "duration": "2年", "tuition": "$65,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.4, "gre_requirement": "315+", "description": "约翰霍普金斯彭博公共卫生学院全球排名第一，培养顶尖公共卫生人才。", "curriculum": "流行病学、生物统计、环境卫生、卫生政策", "career_prospects": "WHO、CDC、药企、学术研究", "admission_rate": 20.0, "avg_gpa": 3.5, "avg_ielts": 7.0, "total_admitted": 700},
            {"name": "金融数学", "name_en": "Financial Mathematics", "category": "理科", "subcategory": "数学", "university": jhu, "duration": "1年", "tuition": "$55,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.4, "gre_requirement": "320+", "description": "JHU金融数学硕士结合应用数学与金融理论，就业前景好。", "curriculum": "随机过程、金融衍生品、蒙特卡洛方法、时间序列", "career_prospects": "量化分析、风险管理、投行", "admission_rate": 25.0, "avg_gpa": 3.5, "avg_ielts": 7.0, "total_admitted": 100},
            {"name": "计算机科学", "name_en": "Computer Science", "category": "工科", "subcategory": "计算机", "university": jhu, "duration": "2年", "tuition": "$58,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.4, "gre_requirement": "320+", "description": "JHU计算机科学在NLP和机器学习领域实力突出。", "curriculum": "自然语言处理、机器学习、计算机视觉、语音识别", "career_prospects": "科技公司、医学AI、学术研究", "admission_rate": 15.0, "avg_gpa": 3.6, "avg_ielts": 7.0, "total_admitted": 120},
            
            # Manchester
            {"name": "计算机科学", "name_en": "Computer Science", "category": "工科", "subcategory": "计算机", "university": manchester, "duration": "1年", "tuition": "£30,000/年", "ielts_requirement": "6.5", "toefl_requirement": "90", "gpa_requirement": 3.2, "description": "曼大CS在AI、数据科学和网络安全方向实力突出。", "curriculum": "人工智能、数据工程、网络安全、软件架构", "career_prospects": "科技公司、金融IT、咨询", "admission_rate": 25.0, "avg_gpa": 3.3, "avg_ielts": 6.5, "total_admitted": 200},
            {"name": "商业分析", "name_en": "Business Analytics", "category": "商科", "subcategory": "商业分析", "university": manchester, "duration": "1年", "tuition": "£32,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.2, "gmat_requirement": "650+", "description": "曼彻斯特联合商学院BA项目注重数据驱动决策能力培养。", "curriculum": "数据分析、机器学习应用、商业模型、决策科学", "career_prospects": "咨询、大数据、商业分析师", "admission_rate": 30.0, "avg_gpa": 3.3, "avg_ielts": 7.0, "total_admitted": 120},
            {"name": "电气与电子工程", "name_en": "Electrical and Electronic Engineering", "category": "工科", "subcategory": "电子", "university": manchester, "duration": "1年", "tuition": "£28,000/年", "ielts_requirement": "6.5", "toefl_requirement": "90", "gpa_requirement": 3.0, "description": "曼大EEE在通信和电力系统领域享有声誉。", "curriculum": "通信系统、数字信号处理、电力电子、控制工程", "career_prospects": "通信公司、电力行业、半导体", "admission_rate": 35.0, "avg_gpa": 3.2, "avg_ielts": 6.5, "total_admitted": 150},
            
            # ANU
            {"name": "计算机科学", "name_en": "Computer Science", "category": "工科", "subcategory": "计算机", "university": anu, "duration": "2年", "tuition": "A$47,000/年", "ielts_requirement": "6.5", "toefl_requirement": "80", "gpa_requirement": 3.0, "description": "ANU计算机科学硕士在人工智能和安全方向表现优秀。", "curriculum": "人工智能、算法设计、信息安全、数据科学", "career_prospects": "科技公司、政府IT、研究机构", "admission_rate": 30.0, "avg_gpa": 3.2, "avg_ielts": 6.5, "total_admitted": 120},
            {"name": "国际关系", "name_en": "International Relations", "category": "文科", "subcategory": "政治", "university": anu, "duration": "2年", "tuition": "A$45,000/年", "ielts_requirement": "6.5", "toefl_requirement": "80", "gpa_requirement": 3.0, "description": "ANU国际关系在亚太地区排名第一，距离澳洲国会仅数百米。", "curriculum": "国际安全、外交政策、亚太政治、全球治理", "career_prospects": "外交官、国际组织、智库", "admission_rate": 25.0, "avg_gpa": 3.3, "avg_ielts": 7.0, "total_admitted": 80},
            
            # UBC
            {"name": "计算机科学", "name_en": "Computer Science", "category": "工科", "subcategory": "计算机", "university": ubc, "duration": "2年", "tuition": "C$50,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.3, "description": "UBC CS在人机交互和视觉计算领域全球领先。", "curriculum": "人机交互、计算机图形学、机器学习、软件工程", "career_prospects": "科技公司、游戏公司、创业", "admission_rate": 15.0, "avg_gpa": 3.5, "avg_ielts": 7.0, "total_admitted": 80},
            {"name": "商业分析", "name_en": "Business Analytics", "category": "商科", "subcategory": "商业分析", "university": ubc, "duration": "1年", "tuition": "C$55,000", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.2, "gmat_requirement": "650+", "description": "UBC尚德商学院BA项目注重数据分析和商业决策。", "curriculum": "预测分析、数据可视化、运营分析、营销分析", "career_prospects": "商业分析师、咨询、科技公司", "admission_rate": 25.0, "avg_gpa": 3.3, "avg_ielts": 7.0, "total_admitted": 70},
            
            # TU Munich
            {"name": "计算机科学", "name_en": "Computer Science", "category": "工科", "subcategory": "计算机", "university": tum, "duration": "2年", "tuition": "€150/学期", "ielts_requirement": "6.5", "toefl_requirement": "88", "gpa_requirement": 3.3, "description": "TUM CS项目免学费，在自动驾驶和工业4.0领域处于前沿。", "curriculum": "自动驾驶、机器人学、人工智能、分布式系统", "career_prospects": "BMW/西门子/SAP等德企、创业", "admission_rate": 20.0, "avg_gpa": 3.4, "avg_ielts": 6.5, "total_admitted": 300},
            {"name": "机械工程", "name_en": "Mechanical Engineering", "category": "工科", "subcategory": "机械", "university": tum, "duration": "2年", "tuition": "€150/学期", "ielts_requirement": "6.5", "toefl_requirement": "88", "gpa_requirement": 3.3, "description": "TUM机械工程在欧洲首屈一指，与德国制造业紧密结合。", "curriculum": "汽车工程、制造技术、热流体力学、材料力学", "career_prospects": "BMW、戴姆勒、博世等德企", "admission_rate": 25.0, "avg_gpa": 3.4, "avg_ielts": 6.5, "total_admitted": 250},
            {"name": "电气与计算机工程", "name_en": "Electrical and Computer Engineering", "category": "工科", "subcategory": "电子", "university": tum, "duration": "2年", "tuition": "€150/学期", "ielts_requirement": "6.5", "toefl_requirement": "88", "gpa_requirement": 3.2, "description": "TUM电气工程以工业自动化和电力系统研究见长。", "curriculum": "自动控制、电力系统、嵌入式系统、信号处理", "career_prospects": "西门子、英飞凌等企业", "admission_rate": 28.0, "avg_gpa": 3.3, "avg_ielts": 6.5, "total_admitted": 200},
            
            # KCL
            {"name": "国际关系", "name_en": "International Relations", "category": "文科", "subcategory": "政治", "university": kcl, "duration": "1年", "tuition": "£25,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.3, "description": "KCL战争研究系全球第一，国际关系专业享誉世界。", "curriculum": "国际安全、战争与冲突、外交政策、恐怖主义研究", "career_prospects": "外交官、智库、国际组织", "admission_rate": 20.0, "avg_gpa": 3.4, "avg_ielts": 7.0, "total_admitted": 100},
            {"name": "法学", "name_en": "Law (LLM)", "category": "文科", "subcategory": "法律", "university": kcl, "duration": "1年", "tuition": "£28,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.3, "description": "KCL法学院Dickson Poon小区是伦敦法律教育和研究的中心。", "curriculum": "国际商法、知识产权、竞争法、欧盟法", "career_prospects": "律所、企业法务、政府法律顾问", "admission_rate": 22.0, "avg_gpa": 3.4, "avg_ielts": 7.0, "total_admitted": 150},
            {"name": "数据科学", "name_en": "Data Science", "category": "理科", "subcategory": "数据科学", "university": kcl, "duration": "1年", "tuition": "£30,000/年", "ielts_requirement": "6.5", "toefl_requirement": "92", "gpa_requirement": 3.2, "description": "KCL数据科学硕士位于伦敦核心区，就业资源丰富。", "curriculum": "机器学习、数据挖掘、大数据技术、统计建模", "career_prospects": "数据科学家、AI工程师、金融分析", "admission_rate": 28.0, "avg_gpa": 3.3, "avg_ielts": 7.0, "total_admitted": 80},
            
            # Warwick
            {"name": "工商管理", "name_en": "MBA", "category": "商科", "subcategory": "管理", "university": warwick, "duration": "1年", "tuition": "£45,000", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.3, "gmat_requirement": "680+", "description": "华威商学院WBS是英国顶尖商学院，三重认证MBA项目。", "curriculum": "战略管理、金融、领导力、创新", "career_prospects": "咨询、金融、企业管理", "admission_rate": 25.0, "avg_gpa": 3.4, "avg_ielts": 7.0, "total_admitted": 120},
            {"name": "计算机科学", "name_en": "Computer Science", "category": "工科", "subcategory": "计算机", "university": warwick, "duration": "1年", "tuition": "£30,000/年", "ielts_requirement": "6.5", "toefl_requirement": "92", "gpa_requirement": 3.2, "description": "华威CS在理论计算机和离散数学方向表现优异。", "curriculum": "算法设计、形式方法、机器学习、网络安全", "career_prospects": "科技公司、金融IT、学术研究", "admission_rate": 22.0, "avg_gpa": 3.4, "avg_ielts": 7.0, "total_admitted": 80},
            {"name": "经济学", "name_en": "Economics", "category": "商科", "subcategory": "经济", "university": warwick, "duration": "1年", "tuition": "£28,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.3, "description": "华威经济学在英国排名前五，培养经济研究和政策分析人才。", "curriculum": "微观经济学、宏观经济学、计量经济学、发展经济学", "career_prospects": "经济研究、政策分析、金融行业", "admission_rate": 20.0, "avg_gpa": 3.5, "avg_ielts": 7.0, "total_admitted": 100},
            
            # Bristol
            {"name": "机器人学", "name_en": "Robotics", "category": "工科", "subcategory": "机械", "university": bristol, "duration": "1年", "tuition": "£28,000/年", "ielts_requirement": "6.5", "toefl_requirement": "90", "gpa_requirement": 3.2, "description": "布里斯托大学机器人学是英国最强项目之一，布里斯托机器人实验室全球闻名。", "curriculum": "机器人控制、计算机视觉、人工智能、传感器技术", "career_prospects": "机器人公司、自动驾驶、航空航天", "admission_rate": 25.0, "avg_gpa": 3.3, "avg_ielts": 6.5, "total_admitted": 60},
            {"name": "计算机科学", "name_en": "Computer Science", "category": "工科", "subcategory": "计算机", "university": bristol, "duration": "1年", "tuition": "£28,000/年", "ielts_requirement": "6.5", "toefl_requirement": "90", "gpa_requirement": 3.2, "description": "布里斯托CS项目在高性能计算和AI方面具特色。", "curriculum": "高性能计算、人工智能、网络安全、云计算", "career_prospects": "科技公司、国防、金融IT", "admission_rate": 28.0, "avg_gpa": 3.3, "avg_ielts": 6.5, "total_admitted": 100},
            
            # Monash
            {"name": "商业分析", "name_en": "Business Analytics", "category": "商科", "subcategory": "商业分析", "university": monash, "duration": "1.5-2年", "tuition": "A$45,000/年", "ielts_requirement": "6.5", "toefl_requirement": "79", "gpa_requirement": 2.8, "description": "莫纳什商学院BA项目注重实践，与澳洲企业联系紧密。", "curriculum": "数据分析、统计建模、商业智能、决策分析", "career_prospects": "商业分析师、咨询、数据分析", "admission_rate": 40.0, "avg_gpa": 3.0, "avg_ielts": 6.5, "total_admitted": 150},
            {"name": "教育学", "name_en": "Education", "category": "文科", "subcategory": "教育", "university": monash, "duration": "1-2年", "tuition": "A$36,000/年", "ielts_requirement": "6.5", "toefl_requirement": "79", "gpa_requirement": 2.8, "description": "莫纳什教育学院全球排名前20，提供多种教育方向。", "curriculum": "教育心理学、课程设计、教育技术、TESOL", "career_prospects": "教师、教育管理、教育科技", "admission_rate": 45.0, "avg_gpa": 3.0, "avg_ielts": 6.5, "total_admitted": 200},
            {"name": "药学", "name_en": "Pharmacy", "category": "医学", "subcategory": "药学", "university": monash, "duration": "2年", "tuition": "A$45,000/年", "ielts_requirement": "6.5", "toefl_requirement": "79", "gpa_requirement": 3.0, "description": "莫纳什药学全球排名第二，在药理和制药领域实力卓越。", "curriculum": "药理学、药剂学、临床药学、药物化学", "career_prospects": "药企、医院药房、监管机构", "admission_rate": 20.0, "avg_gpa": 3.3, "avg_ielts": 7.0, "total_admitted": 80},
            
            # Queensland
            {"name": "数据科学", "name_en": "Data Science", "category": "理科", "subcategory": "数据科学", "university": queensland, "duration": "2年", "tuition": "A$43,000/年", "ielts_requirement": "6.5", "toefl_requirement": "79", "gpa_requirement": 2.8, "description": "UQ数据科学硕士融合统计学和计算机科学，注重实际应用。", "curriculum": "机器学习、统计建模、大数据技术、数据可视化", "career_prospects": "数据科学家、分析师、AI工程师", "admission_rate": 35.0, "avg_gpa": 3.0, "avg_ielts": 6.5, "total_admitted": 100},
            {"name": "环境科学", "name_en": "Environmental Science", "category": "理科", "subcategory": "环境", "university": queensland, "duration": "2年", "tuition": "A$42,000/年", "ielts_requirement": "6.5", "toefl_requirement": "79", "gpa_requirement": 2.8, "description": "UQ环境科学依托大堡礁研究资源，在海洋和生态领域全球领先。", "curriculum": "生态学、保护生物学、环境评估、气候变化", "career_prospects": "环保机构、政府、研究机构", "admission_rate": 35.0, "avg_gpa": 3.0, "avg_ielts": 6.5, "total_admitted": 80},
            
            # CityU HK
            {"name": "电子信息工程", "name_en": "Electronic Information Engineering", "category": "工科", "subcategory": "电子", "university": cityu, "duration": "1年", "tuition": "HK$150,000", "ielts_requirement": "6.5", "toefl_requirement": "79", "gpa_requirement": 3.0, "description": "城大电子工程在通信和集成电路方向有较强实力。", "curriculum": "无线通信、信号处理、集成电路、物联网", "career_prospects": "华为、中兴、通信运营商", "admission_rate": 30.0, "avg_gpa": 3.1, "avg_ielts": 6.5, "total_admitted": 100},
            {"name": "商业分析", "name_en": "Business Analytics", "category": "商科", "subcategory": "商业分析", "university": cityu, "duration": "1年", "tuition": "HK$200,000", "ielts_requirement": "6.5", "toefl_requirement": "79", "gpa_requirement": 3.0, "description": "城大商学院BA项目注重数据驱动商业洞察。", "curriculum": "数据分析、商业智能、营销分析、财务分析", "career_prospects": "商业分析师、咨询、银行", "admission_rate": 30.0, "avg_gpa": 3.2, "avg_ielts": 6.5, "total_admitted": 80},
            {"name": "创意媒体", "name_en": "Creative Media", "category": "艺术", "subcategory": "媒体艺术", "university": cityu, "duration": "1年", "tuition": "HK$150,000", "ielts_requirement": "6.5", "toefl_requirement": "79", "gpa_requirement": 2.8, "description": "城大创意媒体学院在媒体艺术和科技融合领域独具特色。", "curriculum": "数字媒体、交互设计、动画制作、新媒体艺术", "career_prospects": "媒体公司、游戏公司、广告创意", "admission_rate": 35.0, "avg_gpa": 3.0, "avg_ielts": 6.5, "total_admitted": 60},
            
            # PolyU HK
            {"name": "酒店与旅游管理", "name_en": "Hospitality and Tourism Management", "category": "商科", "subcategory": "管理", "university": polyu, "duration": "1年", "tuition": "HK$180,000", "ielts_requirement": "6.0", "toefl_requirement": "80", "gpa_requirement": 2.8, "description": "理大酒店与旅游管理全球排名第一，行业认可度极高。", "curriculum": "酒店运营、旅游规划、餐饮管理、收入管理", "career_prospects": "高端酒店集团、旅游企业、航空公司", "admission_rate": 25.0, "avg_gpa": 3.0, "avg_ielts": 6.5, "total_admitted": 120},
            {"name": "设计学", "name_en": "Design", "category": "艺术", "subcategory": "设计", "university": polyu, "duration": "1年", "tuition": "HK$160,000", "ielts_requirement": "6.0", "toefl_requirement": "80", "gpa_requirement": 2.8, "description": "理大设计学院在亚洲名列前茅，以产品和交互设计见长。", "curriculum": "产品设计、交互设计、服务设计、设计思维", "career_prospects": "设计公司、科技公司UX、品牌设计", "admission_rate": 30.0, "avg_gpa": 3.0, "avg_ielts": 6.5, "total_admitted": 80},
            {"name": "土木工程", "name_en": "Civil Engineering", "category": "工科", "subcategory": "土木", "university": polyu, "duration": "1年", "tuition": "HK$150,000", "ielts_requirement": "6.0", "toefl_requirement": "80", "gpa_requirement": 2.8, "description": "理大土木工程在结构工程和建造管理方面享有声誉。", "curriculum": "结构工程、建造管理、岩土工程、环境工程", "career_prospects": "工程师、项目经理、建筑公司", "admission_rate": 35.0, "avg_gpa": 3.0, "avg_ielts": 6.5, "total_admitted": 100},
            
            # UC Berkeley
            {"name": "电气工程与计算机科学", "name_en": "EECS", "category": "工科", "subcategory": "计算机", "university": berkeley, "duration": "2年", "tuition": "$50,000/年", "ielts_requirement": "7.0", "toefl_requirement": "90", "gpa_requirement": 3.7, "gre_requirement": "325+", "description": "伯克利EECS是全球最强的EECS项目之一，培养了无数科技领袖。", "curriculum": "操作系统、计算机体系结构、人工智能、集成电路", "career_prospects": "硅谷科技公司、创业、学术研究", "admission_rate": 5.0, "avg_gpa": 3.85, "avg_ielts": 7.5, "total_admitted": 100},
            {"name": "统计学", "name_en": "Statistics", "category": "理科", "subcategory": "统计", "university": berkeley, "duration": "2年", "tuition": "$48,000/年", "ielts_requirement": "7.0", "toefl_requirement": "90", "gpa_requirement": 3.6, "gre_requirement": "320+", "description": "伯克利统计系在理论统计和应用统计领域均全球领先。", "curriculum": "概率论、统计推断、贝叶斯方法、高维统计", "career_prospects": "数据科学家、统计学家、学术研究", "admission_rate": 8.0, "avg_gpa": 3.75, "avg_ielts": 7.0, "total_admitted": 40},
            {"name": "公共政策", "name_en": "Public Policy", "category": "文科", "subcategory": "政治", "university": berkeley, "duration": "2年", "tuition": "$45,000/年", "ielts_requirement": "7.0", "toefl_requirement": "90", "gpa_requirement": 3.4, "gre_requirement": "315+", "description": "伯克利高盛公共政策学院在公共政策和社会政策领域享有盛名。", "curriculum": "政策分析、经济学、统计方法、公共管理", "career_prospects": "政府部门、国际组织、非营利机构", "admission_rate": 15.0, "avg_gpa": 3.6, "avg_ielts": 7.0, "total_admitted": 50},
            
            # UCLA
            {"name": "计算机科学", "name_en": "Computer Science", "category": "工科", "subcategory": "计算机", "university": ucla, "duration": "2年", "tuition": "$50,000/年", "ielts_requirement": "7.0", "toefl_requirement": "87", "gpa_requirement": 3.5, "gre_requirement": "320+", "description": "UCLA CS在网络安全和系统方向全美领先，地处洛杉矶就业资源丰富。", "curriculum": "网络安全、系统编程、人工智能、数据库", "career_prospects": "科技公司、娱乐科技、创业", "admission_rate": 8.0, "avg_gpa": 3.7, "avg_ielts": 7.0, "total_admitted": 80},
            {"name": "影视制作", "name_en": "Film and Television", "category": "艺术", "subcategory": "影视", "university": ucla, "duration": "3年", "tuition": "$55,000/年", "ielts_requirement": "7.0", "toefl_requirement": "100", "gpa_requirement": 3.3, "description": "UCLA影视学院是好莱坞人才的摇篮，全美排名前三。", "curriculum": "电影制作、编剧、导演、动画制作", "career_prospects": "好莱坞制片、导演、编剧", "admission_rate": 5.0, "avg_gpa": 3.5, "avg_ielts": 7.0, "total_admitted": 30},
            {"name": "公共卫生", "name_en": "Public Health", "category": "医学", "subcategory": "公共卫生", "university": ucla, "duration": "2年", "tuition": "$45,000/年", "ielts_requirement": "7.0", "toefl_requirement": "87", "gpa_requirement": 3.3, "gre_requirement": "310+", "description": "UCLA公共卫生学院在流行病学和社区卫生领域表现出色。", "curriculum": "流行病学、生物统计、环境卫生、卫生行为学", "career_prospects": "CDC、WHO、医院、药企", "admission_rate": 18.0, "avg_gpa": 3.5, "avg_ielts": 7.0, "total_admitted": 200},
            
            # Kyoto
            {"name": "情报学", "name_en": "Informatics", "category": "工科", "subcategory": "计算机", "university": kyoto, "duration": "2年", "tuition": "¥535,800/年", "ielts_requirement": "6.5", "toefl_requirement": "85", "gpa_requirement": 3.2, "description": "京都大学情报学研究科在智能系统和社会信息学方向有深厚积累。", "curriculum": "人工智能、社会信息学、通信系统、数据科学", "career_prospects": "日本科技企业、学术研究", "admission_rate": 20.0, "avg_gpa": 3.4, "avg_ielts": 6.5, "total_admitted": 100},
            {"name": "化学", "name_en": "Chemistry", "category": "理科", "subcategory": "化学", "university": kyoto, "duration": "2年", "tuition": "¥535,800/年", "ielts_requirement": "6.0", "toefl_requirement": "80", "gpa_requirement": 3.2, "description": "京都大学化学系培养了多位诺贝尔化学奖获得者，研究实力世界一流。", "curriculum": "有机化学、无机化学、物理化学、高分子化学", "career_prospects": "化工企业、药企、学术研究", "admission_rate": 22.0, "avg_gpa": 3.4, "avg_ielts": 6.5, "total_admitted": 80},
            
            # Amsterdam
            {"name": "人工智能", "name_en": "Artificial Intelligence", "category": "工科", "subcategory": "计算机", "university": amsterdam, "duration": "2年", "tuition": "€16,000/年", "ielts_requirement": "7.0", "toefl_requirement": "92", "gpa_requirement": 3.2, "description": "阿姆斯特丹大学AI项目在欧洲享有盛誉，学费相对较低。", "curriculum": "机器学习、自然语言处理、计算机视觉、多智能体", "career_prospects": "AI研究员、科技公司、创业", "admission_rate": 25.0, "avg_gpa": 3.4, "avg_ielts": 7.0, "total_admitted": 100},
            {"name": "传播学", "name_en": "Communication Science", "category": "文科", "subcategory": "传媒", "university": amsterdam, "duration": "1年", "tuition": "€16,000/年", "ielts_requirement": "7.0", "toefl_requirement": "92", "gpa_requirement": 3.0, "description": "阿姆斯特丹大学传播学全球排名第一，在媒体效果和政治传播领域领先。", "curriculum": "媒体效果、政治传播、企业传播、新媒体", "career_prospects": "媒体公司、公关、学术研究", "admission_rate": 30.0, "avg_gpa": 3.3, "avg_ielts": 7.0, "total_admitted": 80},
            
            # Waterloo
            {"name": "计算机科学", "name_en": "Computer Science", "category": "工科", "subcategory": "计算机", "university": waterloo, "duration": "2年", "tuition": "C$25,000/年", "ielts_requirement": "7.0", "toefl_requirement": "90", "gpa_requirement": 3.3, "gre_requirement": "315+", "description": "滑铁卢CS以强大的Co-op项目闻名，毕业生备受硅谷青睐。", "curriculum": "算法设计、人工智能、数据库、软件工程", "career_prospects": "硅谷科技公司、加拿大科技业、创业", "admission_rate": 15.0, "avg_gpa": 3.5, "avg_ielts": 7.0, "total_admitted": 60},
            {"name": "精算学", "name_en": "Actuarial Science", "category": "理科", "subcategory": "统计", "university": waterloo, "duration": "2年", "tuition": "C$20,000/年", "ielts_requirement": "7.0", "toefl_requirement": "90", "gpa_requirement": 3.3, "description": "滑铁卢精算学全球第一，SOA和CAS考试通过率极高。", "curriculum": "精算数学、风险理论、生命精算、非寿险精算", "career_prospects": "保险公司、咨询公司、银行", "admission_rate": 18.0, "avg_gpa": 3.5, "avg_ielts": 7.0, "total_admitted": 40},
        ]
        
        for major_data in majors_data:
            if major_data["university"]:
                existing = db.query(Major).filter(
                    Major.name == major_data["name"],
                    Major.university_id == major_data["university"].id
                ).first()
                if not existing:
                    uni = major_data.pop("university")
                    major = Major(**major_data, university_id=uni.id)
                    db.add(major)
                    print(f"添加专业: {major_data['name']} - {uni.name}")
        
        db.commit()
        
        # 添加攻略数据
        admin_user = db.query(User).filter(User.role == UserRole.ADMIN).first()
        admin_id = admin_user.id if admin_user else 1
        test_user = db.query(User).filter(User.email == "user@example.com").first()
        user_id = test_user.id if test_user else 2
        
        guides_data = [
            {
                "title": "2026年美国硕士申请时间规划",
                "category": "申请规划",
                "summary": "美国硕士申请通常需要提前1-2年开始准备，本文详细规划各阶段要做的事情。",
                "content": "美国硕士申请通常需要提前1-2年开始准备。以下是一个详细的时间规划：\n\n大一-大二：\n- 保持高GPA\n- 开始准备托福/雅思\n- 参加科研项目或实习\n\n大三：\n- 参加GRE/GMAT考试\n- 确定目标院校和专业\n- 开始准备推荐信\n\n大四上学期（9-12月）：\n- 提交申请材料\n- 准备面试\n\n大四下学期（1-4月）：\n- 等待录取结果\n- 办理签证",
                "author_id": admin_id,
                "views": 1250
            },
            {
                "title": "如何写出优秀的个人陈述（PS）",
                "category": "文书写作",
                "summary": "个人陈述是申请材料中最重要的部分之一，本文分享PS写作的核心要点。",
                "content": "个人陈述是申请材料中最重要的部分之一。以下是写作要点：\n\n1. 开头要吸引人\n- 用一个具体的故事或经历开篇\n- 避免陈词滥调\n\n2. 展示你的独特性\n- 突出你的学术背景和研究兴趣\n- 说明为什么选择这个专业\n\n3. 体现与项目的匹配度\n- 研究目标院校的课程设置\n- 说明为什么适合这个项目\n\n4. 结尾要有力\n- 总结你的优势\n- 表达对未来学习的期待",
                "author_id": admin_id,
                "views": 980
            },
            {
                "title": "GRE备考攻略：三个月冲刺330+",
                "category": "考试准备",
                "summary": "GRE考试是申请美国研究生的重要考试，本文提供三个月高效备考计划。",
                "content": "GRE考试是申请美国研究生的重要考试。以下是三个月备考计划：\n\n第一个月：基础阶段\n- 背诵GRE核心词汇\n- 学习数学基础知识点\n- 了解考试题型\n\n第二个月：强化阶段\n- 每天做阅读练习\n- 刷数学题，总结错题\n- 练习写作模板\n\n第三个月：冲刺阶段\n- 做模拟题，控制时间\n- 复习错题\n- 调整考试状态",
                "author_id": admin_id,
                "views": 1500
            },
            {
                "title": "英国G5院校申请全攻略",
                "category": "申请规划",
                "summary": "英国G5院校包括牛津、剑桥、帝国理工、LSE和UCL，本文全面解析申请要点。",
                "content": "英国G5院校包括牛津、剑桥、帝国理工、LSE和UCL。申请要点如下：\n\n1. 学术要求\n- 985/211院校均分85+\n- 双非院校均分90+\n- 相关专业背景\n\n2. 语言要求\n- 雅思7.0-7.5\n- 部分专业需要GMAT/GRE\n\n3. 申请材料\n- 个人陈述（重点突出学术能力）\n- 两封学术推荐信\n- 研究计划（研究型硕士）\n\n4. 申请时间\n- 通常在10月开放申请\n- 建议尽早提交",
                "author_id": admin_id,
                "views": 1100,
                "is_pinned": 1
            },
            {
                "title": "面试技巧：如何应对名校面试",
                "category": "面试准备",
                "summary": "名校面试是申请过程中的重要环节，本文分享应对面试的实用技巧。",
                "content": "名校面试是申请过程中的重要环节。以下是应对技巧：\n\n面试前准备：\n- 深入了解项目和教授\n- 准备常见问题的回答\n- 模拟面试练习\n\n常见面试问题：\n1. 自我介绍\n2. 为什么选择我们学校？\n3. 你的研究兴趣是什么？\n4. 你的职业规划是什么？\n5. 你有什么问题要问我们？\n\n面试技巧：\n- 保持自信和真诚\n- 用具体例子支撑观点\n- 注意仪表和礼仪\n- 准备2-3个反问问题",
                "author_id": admin_id,
                "views": 850
            },
            # ===== 新增攻略 =====
            {
                "title": "雅思7.0+高分备考经验分享",
                "category": "考试准备",
                "summary": "雅思考试是留学申请的重要语言门槛，本文分享从5.5到7.5的高效备考方法。",
                "content": "雅思考试是留学申请的重要语言门槛。以下是高分备考经验：\n\n一、听力（目标7.5+）\n- 精听BBC/TED，每天30分钟\n- 做剑桥真题，整理同义替换\n- 注意拼写和单复数\n\n二、阅读（目标8.0+）\n- 练习定位和快速阅读技巧\n- 学会识别题型（判断题、匹配题等）\n- 积累学术词汇\n\n三、写作（目标6.5+）\n- 学习高分范文结构\n- 练习图表描述（Task 1）\n- 议论文论点展开逻辑\n\n四、口语（目标7.0+）\n- 日常练习口语表达\n- 准备话题素材库\n- 注意流利度和发音",
                "author_id": admin_id,
                "views": 2100
            },
            {
                "title": "托福100+一个月冲刺计划",
                "category": "考试准备",
                "summary": "针对基础较好的考生，如何在一个月内冲刺托福100分以上。",
                "content": "针对已有85分基础的考生，一个月冲刺100+的计划：\n\n第一周：题型熟悉与弱项分析\n- 做一套完整模考\n- 分析各科弱项\n- 制定个性化计划\n\n第二周：专项突破\n- 听力：TPO精听+跟读\n- 阅读：重点练习推断题和词汇题\n- 口语：整理独立口语模板\n- 写作：积累论据素材\n\n第三周：强化训练\n- 每天模拟一套完整考试\n- 总结错误类型\n- 调整应试策略\n\n第四周：考前冲刺\n- 模考+回顾\n- 保持题感\n- 注意休息和心态调整",
                "author_id": admin_id,
                "views": 1800
            },
            {
                "title": "推荐信：如何选择推荐人和沟通",
                "category": "文书写作",
                "summary": "推荐信是申请材料的重要组成部分，本文教你如何选择合适的推荐人。",
                "content": "推荐信通常需要2-3封，选择合适的推荐人至关重要：\n\n一、推荐人选择原则\n1. 了解你的人：选择与你有密切学术交流的教授\n2. 学术地位：知名教授的推荐更有说服力\n3. 多样性：学术推荐人+实习/工作推荐人\n\n二、如何与推荐人沟通\n1. 提前2-3个月预约\n2. 提供你的CV、PS和申请学校列表\n3. 告知推荐截止日期\n4. 适时提醒，态度诚恳\n\n三、注意事项\n- 不要选择不太了解你的教授\n- 避免所有推荐信内容雷同\n- 申请后及时感谢推荐人",
                "author_id": admin_id,
                "views": 920
            },
            {
                "title": "留学签证申请全流程指南",
                "category": "签证办理",
                "summary": "拿到offer后如何顺利办理留学签证？本文涵盖美英澳加签证全流程。",
                "content": "拿到offer后，签证是最关键的一步。以下是主要留学国家签证指南：\n\n一、美国F-1签证\n1. 收到I-20表格\n2. 缴纳SEVIS Fee\n3. 预约签证面试\n4. 准备材料：护照、I-20、DS-160确认页、照片、财力证明\n5. 面签Tips：自信回答，展示回国意愿\n\n二、英国Tier 4签证\n1. 收到CAS\n2. 在线申请\n3. 预约签证中心\n4. 提交生物信息\n5. 等待结果（通常3周）\n\n三、澳大利亚学生签证（Subclass 500）\n1. 收到CoE\n2. 在线递交申请\n3. 体检\n4. 等待审批\n\n四、加拿大学习许可\n1. 收到录取信\n2. 在线申请Study Permit\n3. 提交生物信息\n4. 等待获批",
                "author_id": admin_id,
                "views": 1600
            },
            {
                "title": "留学生活：出国前必须准备的10件事",
                "category": "留学生活",
                "summary": "即将出国留学？这10件事你必须提前准备好。",
                "content": "出国留学前的10件必做准备：\n\n1. 机票预订\n- 提前1-2个月预订\n- 关注行李额度要求\n\n2. 住宿安排\n- 校内宿舍 vs 校外租房\n- 提前了解周边环境\n\n3. 银行卡与汇款\n- 办理Visa/Mastercard信用卡\n- 了解当地银行开户流程\n\n4. 保险购买\n- 学校要求的医疗保险\n- 财产保险（可选）\n\n5. 行李准备\n- 重要证件复印件\n- 常用药品\n- 适当的衣物\n\n6. 手机通讯\n- 当地SIM卡或国际套餐\n\n7. 接机安排\n- 学校接机服务\n- 公共交通路线\n\n8. 文化准备\n- 了解当地文化习俗\n- 学习基本日常用语\n\n9. 体检与疫苗\n- 学校要求的疫苗接种\n- 出国体检证明\n\n10. 重要文件备份\n- 护照、签证、offer等电子版",
                "author_id": admin_id,
                "views": 2500
            },
            {
                "title": "如何选校：匹配度比排名更重要",
                "category": "申请规划",
                "summary": "选校不只看排名，本文教你如何找到最适合自己的学校和项目。",
                "content": "选校是申请中最重要的决策之一，切勿只看排名：\n\n一、评估维度\n1. 项目匹配度\n- 课程设置是否符合兴趣\n- 研究方向是否对口\n- 是否有心仪的导师\n\n2. 地理位置\n- 实习和就业机会\n- 生活成本\n- 安全程度\n\n3. 录取概率\n- 建立冲刺/匹配/保底梯度\n- 冲刺(2-3所) + 匹配(3-4所) + 保底(2所)\n\n二、信息获取渠道\n- 学校官网和项目主页\n- 学长学姐经验分享\n- 留学论坛和社群\n- 专业排名（US News, QS等）\n\n三、常见误区\n- 不要过度追求综排\n- 不要忽视专业排名\n- 不要只申请同一难度的学校",
                "author_id": admin_id,
                "views": 1350,
                "is_pinned": 1
            },
            {
                "title": "GMAT备考全攻略：从650到720",
                "category": "考试准备",
                "summary": "GMAT是商科申请的重要考试，本文分享从650提升到720+的备考策略。",
                "content": "GMAT是商科硕士和MBA申请的关键考试，以下是高效备考策略：\n\n一、考试概述\n- 总分200-800\n- 主要考查Verbal和Quantitative\n- 2024年起改版为GMAT Focus Edition\n\n二、备考阶段\n\n基础阶段（1-2周）：\n- 了解题型和评分标准\n- 做一套诊断题\n- 识别薄弱环节\n\n强化阶段（4-6周）：\n- Verbal：句子改错(SC)是重中之重\n- Quant：刷OG和Prep，注意数据充分性\n- 坚持做错题分析\n\n冲刺阶段（2周）：\n- 模考练速度\n- 复习错题本\n- 调整考试状态\n\n三、备考资源\n- OG（Official Guide）\n- Manhattan GMAT\n- GWD真题\n- GMAT Club论坛",
                "author_id": admin_id,
                "views": 1200
            },
            {
                "title": "简历CV写作：留学申请版",
                "category": "文书写作",
                "summary": "留学申请CV与求职简历有所不同，本文教你写出打动招生官的CV。",
                "content": "留学申请CV需要突出学术和研究能力：\n\n一、CV结构\n1. 教育背景（Education）\n- 学校、专业、GPA、排名\n- 相关课程\n\n2. 研究经历（Research Experience）\n- 实验室名称和导师\n- 具体工作和成果\n\n3. 实习/工作经历（Work Experience）\n- 公司名称和职位\n- 具体职责和成就\n\n4. 发表论文（Publications）\n- 按标准学术格式列出\n\n5. 荣誉奖项（Awards）\n- 学术和竞赛获奖\n\n6. 技能（Skills）\n- 编程语言、工具、语言能力\n\n二、注意事项\n- 控制在1-2页\n- 使用动词开头描述经历\n- 量化成果（如提升了30%效率）\n- 保持格式统一整洁",
                "author_id": admin_id,
                "views": 760
            },
            {
                "title": "留学租房避坑指南",
                "category": "留学生活",
                "summary": "在海外租房有哪些注意事项？如何避免常见的租房陷阱？",
                "content": "海外租房是留学生活的第一步，以下是实用建议：\n\n一、租房类型\n1. 校内宿舍：安全方便，但名额有限\n2. 合租公寓：性价比高，可以分摊费用\n3. 独立公寓：隐私好，费用较高\n4. 寄宿家庭：适合语言提升，文化融入\n\n二、租房流程\n1. 确定预算和区域\n2. 浏览房源网站\n3. 实地看房/视频看房\n4. 签订合同，注意条款\n5. 缴纳押金和首月房租\n\n三、避坑指南\n- 不要提前支付大额定金\n- 仔细阅读合同中的退租条款\n- 确认水电网费是否包含\n- 检查房屋设施并拍照存证\n- 了解当地租房法律保护\n\n四、常用租房网站\n- 美国：Zillow, Apartments.com\n- 英国：Rightmove, SpareRoom\n- 澳洲：Domain, Flatmates",
                "author_id": user_id,
                "views": 680
            },
            {
                "title": "港校申请全攻略：香港八大详解",
                "category": "申请规划",
                "summary": "香港院校申请流程、要求和热门专业全面解析。",
                "content": "香港是内地学生留学的热门目的地，以下是港校申请全解析：\n\n一、香港八大院校\n- 香港大学（HKU）：综合实力最强\n- 香港科技大学（HKUST）：理工科强劲\n- 香港中文大学（CUHK）：人文社科突出\n- 香港城市大学（CityU）：商科和工程\n- 香港理工大学（PolyU）：酒店管理第一\n- 香港浸会大学（HKBU）：传媒和文科\n- 香港岭南大学（LU）：博雅教育\n- 香港教育大学（EdUHK）：教育专业\n\n二、申请要求\n- 本科背景：985/211有优势\n- GPA：3.0+（热门专业3.5+）\n- 语言：雅思6.0-7.0或托福80-100\n- 工作经验：部分商科项目要求\n\n三、申请时间线\n- 9-11月：第一轮申请\n- 12-次年2月：第二轮\n- 3-5月：补录\n\n四、优势\n- 距离近，方便回家\n- 学制短（1年授课型）\n- 国际化环境\n- 就业市场活跃",
                "author_id": admin_id,
                "views": 3200,
                "is_pinned": 1
            }
        ]
        
        for guide_data in guides_data:
            existing = db.query(Guide).filter(Guide.title == guide_data["title"]).first()
            if not existing:
                guide = Guide(**guide_data)
                db.add(guide)
                print(f"添加攻略: {guide_data['title']}")
        
        db.commit()
        
        # ===== 录取案例数据 =====
        # 获取院校和专业ID映射
        all_unis = {u.name: u.id for u in db.query(University).all()}
        all_majors = {}
        for m in db.query(Major).all():
            all_majors[(m.name, m.university_id)] = m.id
        
        def get_major_id(major_name_part, uni_name):
            """通过专业名关键字和院校名查找 major_id"""
            uid = all_unis.get(uni_name)
            if not uid:
                return None
            for (mname, muid), mid in all_majors.items():
                if muid == uid and major_name_part in mname:
                    return mid
            return None
        
        cases_data = [
            # 案例1: 录取 MIT
            {
                "applicant_name": "张同学",
                "undergraduate_university_id": all_unis.get("清华大学"),
                "undergraduate_university_name": "清华大学",
                "undergraduate_major": "计算机科学与技术",
                "graduation_year": 2025,
                "gpa": 3.9, "gpa_scale": 4.0, "ranking": "3/120",
                "toefl_total": 112, "toefl_reading": 29, "toefl_listening": 28, "toefl_speaking": 26, "toefl_writing": 29,
                "gre_total": 332, "gre_verbal": 162, "gre_quant": 170, "gre_writing": 4.5,
                "internship_count": 3, "internship_experience": "微软亚洲研究院实习、字节跳动算法实习、Google Summer of Code",
                "research_count": 2, "research_experience": "NLP方向论文研究、计算机视觉实验室助研",
                "publication_count": 1, "publications": "ACL 2024 一篇一作论文",
                "awards": "ACM-ICPC亚洲区域赛金奖",
                "recommendation_strength": "strong",
                "admitted_university_id": all_unis.get("麻省理工学院"),
                "admitted_major_id": get_major_id("计算机", "麻省理工学院"),
                "admission_year": 2026, "admission_semester": "秋季",
                "result": "录取", "scholarship": "全额奖学金+RA",
                "submitter_id": admin_id, "is_verified": 1
            },
            # 案例2: 录取 Stanford
            {
                "applicant_name": "李同学",
                "undergraduate_university_id": all_unis.get("北京大学"),
                "undergraduate_university_name": "北京大学",
                "undergraduate_major": "电子信息工程",
                "graduation_year": 2025,
                "gpa": 3.85, "gpa_scale": 4.0, "ranking": "5/150",
                "ielts_overall": 7.5, "ielts_listening": 8.0, "ielts_reading": 8.5, "ielts_writing": 7.0, "ielts_speaking": 7.0,
                "gre_total": 328, "gre_verbal": 158, "gre_quant": 170, "gre_writing": 4.0,
                "internship_count": 2, "internship_experience": "华为2012实验室、旷视科技",
                "research_count": 3, "research_experience": "视觉感知实验室、MIT CSAIL远程科研、机器人方向研究",
                "publication_count": 2, "publications": "CVPR 2024 一篇一作, NeurIPS 2024 一篇二作",
                "recommendation_strength": "strong",
                "admitted_university_id": all_unis.get("斯坦福大学"),
                "admitted_major_id": get_major_id("电气工程", "斯坦福大学"),
                "admission_year": 2026, "admission_semester": "秋季",
                "result": "录取", "scholarship": "半额奖学金",
                "submitter_id": admin_id, "is_verified": 1
            },
            # 案例3: 录取 NUS
            {
                "applicant_name": "王同学",
                "undergraduate_university_id": all_unis.get("浙江大学"),
                "undergraduate_university_name": "浙江大学",
                "undergraduate_major": "金融学",
                "graduation_year": 2025,
                "gpa": 3.7, "gpa_scale": 4.0, "ranking": "15/200",
                "ielts_overall": 7.0, "ielts_listening": 7.5, "ielts_reading": 7.5, "ielts_writing": 6.5, "ielts_speaking": 6.5,
                "gmat_total": 720,
                "internship_count": 3, "internship_experience": "中金公司投行部、高盛暑期实习、腾讯投资部",
                "research_count": 1, "research_experience": "金融工程方向量化策略研究",
                "work_years": 0, "work_experience": "",
                "awards": "全国大学生数学建模竞赛一等奖",
                "recommendation_strength": "strong",
                "admitted_university_id": all_unis.get("新加坡国立大学"),
                "admitted_major_id": get_major_id("金融", "新加坡国立大学"),
                "admission_year": 2026, "admission_semester": "秋季",
                "result": "录取", "scholarship": "",
                "submitter_id": admin_id, "is_verified": 1
            },
            # 案例4: 录取 NTU
            {
                "applicant_name": "陈同学",
                "undergraduate_university_name": "南京大学",
                "undergraduate_major": "人工智能",
                "graduation_year": 2025,
                "gpa": 88.5, "gpa_scale": 100, "ranking": "10/100",
                "ielts_overall": 7.0, "ielts_listening": 7.0, "ielts_reading": 8.0, "ielts_writing": 6.5, "ielts_speaking": 6.0,
                "gre_total": 322, "gre_verbal": 155, "gre_quant": 167, "gre_writing": 3.5,
                "internship_count": 2, "internship_experience": "百度AI Lab、商汤科技",
                "research_count": 2, "research_experience": "自然语言处理实验室、强化学习方向研究",
                "publication_count": 1, "publications": "AAAI 2025 一篇共一作",
                "recommendation_strength": "medium",
                "admitted_university_id": all_unis.get("南洋理工大学"),
                "admitted_major_id": get_major_id("人工智能", "南洋理工大学"),
                "admission_year": 2026, "admission_semester": "秋季",
                "result": "录取", "scholarship": "助研奖学金",
                "submitter_id": user_id, "is_verified": 1
            },
            # 案例5: 录取 UCL
            {
                "applicant_name": "赵同学",
                "undergraduate_university_name": "中山大学",
                "undergraduate_major": "传播学",
                "graduation_year": 2025,
                "gpa": 3.6, "gpa_scale": 4.0,
                "ielts_overall": 7.5, "ielts_listening": 8.0, "ielts_reading": 7.5, "ielts_writing": 7.0, "ielts_speaking": 7.0,
                "internship_count": 2, "internship_experience": "新华社实习记者、BBC中文网",
                "research_count": 1, "research_experience": "新媒体传播效果研究",
                "extracurricular": "校辩论队队长、学生会宣传部长",
                "awards": "全国大学生英语演讲比赛二等奖",
                "recommendation_strength": "medium",
                "admitted_university_id": all_unis.get("伦敦大学学院"),
                "admitted_major_id": get_major_id("教育", "伦敦大学学院"),
                "admission_year": 2026, "admission_semester": "秋季",
                "result": "录取", "scholarship": "",
                "submitter_id": user_id, "is_verified": 1
            },
            # 案例6: 拒绝 Oxford
            {
                "applicant_name": "刘同学",
                "undergraduate_university_name": "复旦大学",
                "undergraduate_major": "经济学",
                "graduation_year": 2025,
                "gpa": 3.5, "gpa_scale": 4.0,
                "ielts_overall": 7.0, "ielts_listening": 7.5, "ielts_reading": 7.5, "ielts_writing": 6.5, "ielts_speaking": 6.5,
                "gre_total": 320, "gre_verbal": 155, "gre_quant": 165, "gre_writing": 4.0,
                "internship_count": 2, "internship_experience": "国泰君安、普华永道",
                "research_count": 0,
                "recommendation_strength": "medium",
                "admitted_university_id": all_unis.get("牛津大学"),
                "admitted_major_id": get_major_id("经济", "牛津大学"),
                "admission_year": 2026, "admission_semester": "秋季",
                "result": "拒绝",
                "remarks": "面试表现一般，科研经历不足",
                "submitter_id": admin_id, "is_verified": 1
            },
            # 案例7: 录取 HKU
            {
                "applicant_name": "吴同学",
                "undergraduate_university_name": "武汉大学",
                "undergraduate_major": "法学",
                "graduation_year": 2025,
                "gpa": 3.65, "gpa_scale": 4.0,
                "ielts_overall": 7.5, "ielts_listening": 7.5, "ielts_reading": 8.0, "ielts_writing": 7.0, "ielts_speaking": 7.0,
                "internship_count": 2, "internship_experience": "金杜律师事务所、联合国实习",
                "research_count": 1, "research_experience": "国际商法方向研究",
                "publication_count": 0,
                "awards": "Jessup国际法模拟法庭中国赛区最佳辩手",
                "recommendation_strength": "strong",
                "admitted_university_id": all_unis.get("香港大学"),
                "admitted_major_id": get_major_id("法学", "香港大学"),
                "admission_year": 2026, "admission_semester": "秋季",
                "result": "录取", "scholarship": "入学奖学金5万港币",
                "submitter_id": user_id, "is_verified": 1
            },
            # 案例8: 录取 Imperial College
            {
                "applicant_name": "周同学",
                "undergraduate_university_id": all_unis.get("上海交通大学"),
                "undergraduate_university_name": "上海交通大学",
                "undergraduate_major": "机械工程",
                "graduation_year": 2025,
                "gpa": 87.2, "gpa_scale": 100, "ranking": "8/150",
                "ielts_overall": 7.0, "ielts_listening": 7.5, "ielts_reading": 7.0, "ielts_writing": 6.5, "ielts_speaking": 7.0,
                "internship_count": 2, "internship_experience": "西门子工程实习、宝马研发中心",
                "research_count": 2, "research_experience": "机器人控制方向、3D打印材料研究",
                "publication_count": 1, "publications": "IEEE Robotics 一篇合作论文",
                "recommendation_strength": "strong",
                "admitted_university_id": all_unis.get("帝国理工学院"),
                "admitted_major_id": get_major_id("机械", "帝国理工学院"),
                "admission_year": 2026, "admission_semester": "秋季",
                "result": "录取", "scholarship": "",
                "submitter_id": admin_id, "is_verified": 1
            },
            # 案例9: 录取 University of Melbourne
            {
                "applicant_name": "郑同学",
                "undergraduate_university_name": "华中科技大学",
                "undergraduate_major": "会计学",
                "graduation_year": 2025,
                "gpa": 3.4, "gpa_scale": 4.0,
                "ielts_overall": 6.5, "ielts_listening": 7.0, "ielts_reading": 7.0, "ielts_writing": 6.0, "ielts_speaking": 6.0,
                "gmat_total": 690,
                "internship_count": 2, "internship_experience": "德勤审计、毕马威咨询",
                "research_count": 0,
                "recommendation_strength": "medium",
                "admitted_university_id": all_unis.get("墨尔本大学"),
                "admitted_major_id": get_major_id("商", "墨尔本大学"),
                "admission_year": 2026, "admission_semester": "秋季",
                "result": "录取", "scholarship": "",
                "submitter_id": user_id, "is_verified": 1
            },
            # 案例10: 录取 Columbia
            {
                "applicant_name": "孙同学",
                "undergraduate_university_id": all_unis.get("北京大学"),
                "undergraduate_university_name": "北京大学",
                "undergraduate_major": "统计学",
                "graduation_year": 2025,
                "gpa": 3.8, "gpa_scale": 4.0, "ranking": "8/80",
                "toefl_total": 108, "toefl_reading": 28, "toefl_listening": 27, "toefl_speaking": 24, "toefl_writing": 29,
                "gre_total": 330, "gre_verbal": 160, "gre_quant": 170, "gre_writing": 4.0,
                "internship_count": 2, "internship_experience": "摩根士丹利量化分析、两西格玛暑期实习",
                "research_count": 1, "research_experience": "统计机器学习方向研究",
                "publication_count": 1, "publications": "统计学期刊一篇合作论文",
                "recommendation_strength": "strong",
                "admitted_university_id": all_unis.get("哥伦比亚大学"),
                "admitted_major_id": get_major_id("计算机", "哥伦比亚大学"),
                "admission_year": 2026, "admission_semester": "秋季",
                "result": "录取", "scholarship": "半奖",
                "submitter_id": admin_id, "is_verified": 1
            },
            # 案例11: 候补 Cambridge
            {
                "applicant_name": "黄同学",
                "undergraduate_university_name": "同济大学",
                "undergraduate_major": "建筑学",
                "graduation_year": 2025,
                "gpa": 3.55, "gpa_scale": 4.0,
                "ielts_overall": 7.0, "ielts_listening": 7.0, "ielts_reading": 7.5, "ielts_writing": 6.5, "ielts_speaking": 6.5,
                "internship_count": 1, "internship_experience": "Gensler建筑事务所",
                "research_count": 1, "research_experience": "绿色建筑方向设计研究",
                "awards": "全国高校建筑设计竞赛银奖",
                "recommendation_strength": "medium",
                "admitted_university_id": all_unis.get("剑桥大学"),
                "admitted_major_id": get_major_id("物理", "剑桥大学"),
                "admission_year": 2026, "admission_semester": "秋季",
                "result": "候补",
                "remarks": "作品集评价较高，但GPA稍低",
                "submitter_id": user_id, "is_verified": 1
            },
            # 案例12: 录取 ETH Zurich
            {
                "applicant_name": "林同学",
                "undergraduate_university_id": all_unis.get("清华大学"),
                "undergraduate_university_name": "清华大学",
                "undergraduate_major": "电子工程",
                "graduation_year": 2025,
                "gpa": 3.88, "gpa_scale": 4.0, "ranking": "5/130",
                "toefl_total": 105, "toefl_reading": 28, "toefl_listening": 26, "toefl_speaking": 23, "toefl_writing": 28,
                "gre_total": 325, "gre_verbal": 155, "gre_quant": 170, "gre_writing": 3.5,
                "internship_count": 1, "internship_experience": "CERN暑期实习",
                "research_count": 3, "research_experience": "量子计算方向、半导体物理研究、信号处理研究",
                "publication_count": 2, "publications": "IEEE两篇合作论文",
                "recommendation_strength": "strong",
                "admitted_university_id": all_unis.get("苏黎世联邦理工学院"),
                "admitted_major_id": get_major_id("计算机", "苏黎世联邦理工学院"),
                "admission_year": 2026, "admission_semester": "秋季",
                "result": "录取", "scholarship": "全额奖学金",
                "submitter_id": admin_id, "is_verified": 1
            },
            # 案例13: 录取 Toronto
            {
                "applicant_name": "杨同学",
                "undergraduate_university_name": "西安交通大学",
                "undergraduate_major": "软件工程",
                "graduation_year": 2025,
                "gpa": 3.5, "gpa_scale": 4.0,
                "ielts_overall": 7.0, "ielts_listening": 7.5, "ielts_reading": 7.5, "ielts_writing": 6.5, "ielts_speaking": 6.0,
                "gre_total": 318, "gre_verbal": 150, "gre_quant": 168, "gre_writing": 3.5,
                "internship_count": 2, "internship_experience": "阿里巴巴达摩院、亚马逊AWS",
                "research_count": 1, "research_experience": "分布式系统方向",
                "publication_count": 0,
                "recommendation_strength": "medium",
                "admitted_university_id": all_unis.get("多伦多大学"),
                "admitted_major_id": get_major_id("计算机", "多伦多大学"),
                "admission_year": 2026, "admission_semester": "秋季",
                "result": "录取", "scholarship": "",
                "submitter_id": user_id, "is_verified": 1
            },
            # 案例14: 录取 NUS 计算机
            {
                "applicant_name": "何同学",
                "undergraduate_university_name": "哈尔滨工业大学",
                "undergraduate_major": "计算机科学",
                "graduation_year": 2025,
                "gpa": 85.8, "gpa_scale": 100, "ranking": "20/180",
                "ielts_overall": 6.5, "ielts_listening": 7.0, "ielts_reading": 7.0, "ielts_writing": 6.0, "ielts_speaking": 6.0,
                "gre_total": 315, "gre_verbal": 148, "gre_quant": 167, "gre_writing": 3.0,
                "internship_count": 2, "internship_experience": "腾讯微信团队、美团",
                "research_count": 1, "research_experience": "推荐系统方向",
                "recommendation_strength": "medium",
                "admitted_university_id": all_unis.get("新加坡国立大学"),
                "admitted_major_id": get_major_id("计算机", "新加坡国立大学"),
                "admission_year": 2026, "admission_semester": "秋季",
                "result": "录取", "scholarship": "",
                "submitter_id": admin_id, "is_verified": 1
            },
            # 案例15: 录取 LSE
            {
                "applicant_name": "许同学",
                "undergraduate_university_name": "中国人民大学",
                "undergraduate_major": "经济学",
                "graduation_year": 2025,
                "gpa": 3.75, "gpa_scale": 4.0,
                "ielts_overall": 7.5, "ielts_listening": 8.0, "ielts_reading": 8.0, "ielts_writing": 7.0, "ielts_speaking": 7.0,
                "gmat_total": 740,
                "internship_count": 3, "internship_experience": "高盛、中信证券、BCG咨询",
                "research_count": 1, "research_experience": "发展经济学方向研究",
                "publication_count": 0,
                "awards": "CFA一级通过",
                "recommendation_strength": "strong",
                "admitted_university_id": all_unis.get("伦敦政治经济学院"),
                "admitted_major_id": get_major_id("经济", "伦敦政治经济学院"),
                "admission_year": 2026, "admission_semester": "秋季",
                "result": "录取", "scholarship": "",
                "submitter_id": admin_id, "is_verified": 1
            },
            # 案例16: 拒绝 Harvard
            {
                "applicant_name": "马同学",
                "undergraduate_university_name": "复旦大学",
                "undergraduate_major": "生物科学",
                "graduation_year": 2025,
                "gpa": 3.6, "gpa_scale": 4.0,
                "toefl_total": 105, "toefl_reading": 28, "toefl_listening": 27, "toefl_speaking": 23, "toefl_writing": 27,
                "gre_total": 322, "gre_verbal": 156, "gre_quant": 166, "gre_writing": 4.0,
                "internship_count": 1, "internship_experience": "药企研发实习",
                "research_count": 2, "research_experience": "基因编辑方向、干细胞研究",
                "publication_count": 1, "publications": "Nature子刊一篇合作论文",
                "recommendation_strength": "medium",
                "admitted_university_id": all_unis.get("哈佛大学"),
                "admitted_major_id": get_major_id("数据科学", "哈佛大学"),
                "admission_year": 2026, "admission_semester": "秋季",
                "result": "拒绝",
                "remarks": "竞争激烈，GPA和语言成绩偏低",
                "submitter_id": user_id, "is_verified": 1
            },
            # 案例17: 录取 HKUST
            {
                "applicant_name": "朱同学",
                "undergraduate_university_name": "东南大学",
                "undergraduate_major": "电气工程",
                "graduation_year": 2025,
                "gpa": 3.45, "gpa_scale": 4.0,
                "ielts_overall": 6.5, "ielts_listening": 7.0, "ielts_reading": 6.5, "ielts_writing": 6.0, "ielts_speaking": 6.5,
                "internship_count": 1, "internship_experience": "国家电网研究院",
                "research_count": 1, "research_experience": "电力系统优化研究",
                "recommendation_strength": "medium",
                "admitted_university_id": all_unis.get("香港科技大学"),
                "admitted_major_id": get_major_id("计算机", "香港科技大学"),
                "admission_year": 2026, "admission_semester": "秋季",
                "result": "录取", "scholarship": "",
                "submitter_id": admin_id, "is_verified": 1
            },
            # 案例18: 录取 University of Sydney
            {
                "applicant_name": "田同学",
                "undergraduate_university_name": "厦门大学",
                "undergraduate_major": "市场营销",
                "graduation_year": 2025,
                "gpa": 3.3, "gpa_scale": 4.0,
                "ielts_overall": 6.5, "ielts_listening": 6.5, "ielts_reading": 7.0, "ielts_writing": 6.0, "ielts_speaking": 6.0,
                "internship_count": 2, "internship_experience": "宝洁品牌管理实习、联合利华",
                "research_count": 0,
                "extracurricular": "校园营销策划大赛冠军队",
                "recommendation_strength": "medium",
                "admitted_university_id": all_unis.get("悉尼大学"),
                "admitted_major_id": get_major_id("商", "悉尼大学"),
                "admission_year": 2026, "admission_semester": "秋季",
                "result": "录取", "scholarship": "",
                "submitter_id": user_id, "is_verified": 1
            },
            # 案例19: 录取 Kyoto University
            {
                "applicant_name": "高同学",
                "undergraduate_university_name": "中国科学技术大学",
                "undergraduate_major": "物理学",
                "graduation_year": 2025,
                "gpa": 3.7, "gpa_scale": 4.0,
                "toefl_total": 95, "toefl_reading": 26, "toefl_listening": 24, "toefl_speaking": 21, "toefl_writing": 24,
                "gre_total": 325, "gre_verbal": 156, "gre_quant": 169, "gre_writing": 3.5,
                "research_count": 2, "research_experience": "凝聚态物理实验室、量子光学研究",
                "publication_count": 1, "publications": "Physical Review B一篇合作论文",
                "recommendation_strength": "strong",
                "admitted_university_id": all_unis.get("东京大学"),
                "admitted_major_id": get_major_id("理学", "东京大学"),
                "admission_year": 2026, "admission_semester": "秋季",
                "result": "录取", "scholarship": "MEXT奖学金",
                "submitter_id": admin_id, "is_verified": 1
            },
            # 案例20: 录取 Edinburgh
            {
                "applicant_name": "沈同学",
                "undergraduate_university_name": "北京师范大学",
                "undergraduate_major": "心理学",
                "graduation_year": 2025,
                "gpa": 3.6, "gpa_scale": 4.0,
                "ielts_overall": 7.0, "ielts_listening": 7.5, "ielts_reading": 7.0, "ielts_writing": 6.5, "ielts_speaking": 7.0,
                "internship_count": 1, "internship_experience": "北京安定医院临床心理科实习",
                "research_count": 2, "research_experience": "认知神经科学实验室、发展心理学研究",
                "publication_count": 0,
                "extracurricular": "心理咨询志愿者协会会长",
                "recommendation_strength": "medium",
                "admitted_university_id": all_unis.get("爱丁堡大学"),
                "admitted_major_id": get_major_id("语言", "爱丁堡大学"),
                "admission_year": 2026, "admission_semester": "秋季",
                "result": "录取", "scholarship": "",
                "submitter_id": user_id, "is_verified": 1
            },
            # ===== 新增案例 =====
            # 案例21: 录取 Duke 生物统计
            {
                "applicant_name": "罗同学",
                "undergraduate_university_name": "南开大学",
                "undergraduate_major": "统计学",
                "graduation_year": 2025,
                "gpa": 3.7, "gpa_scale": 4.0, "ranking": "8/90",
                "toefl_total": 105, "toefl_reading": 28, "toefl_listening": 26, "toefl_speaking": 23, "toefl_writing": 28,
                "gre_total": 325, "gre_verbal": 155, "gre_quant": 170, "gre_writing": 3.5,
                "internship_count": 2, "internship_experience": "辉瑞制药数据分析实习、中国CDC统计分析",
                "research_count": 2, "research_experience": "生存分析方法研究、临床试验数据分析",
                "publication_count": 1, "publications": "生物统计学期刊一篇合作论文",
                "recommendation_strength": "strong",
                "admitted_university_id": all_unis.get("杜克大学"),
                "admitted_major_id": get_major_id("生物统计", "杜克大学"),
                "admission_year": 2026, "admission_semester": "秋季",
                "result": "录取", "scholarship": "25%学费减免",
                "submitter_id": admin_id, "is_verified": 1
            },
            # 案例22: 录取 Northwestern MBA
            {
                "applicant_name": "谢同学",
                "undergraduate_university_name": "上海财经大学",
                "undergraduate_major": "工商管理",
                "graduation_year": 2022,
                "gpa": 3.5, "gpa_scale": 4.0,
                "ielts_overall": 7.5, "ielts_listening": 8.0, "ielts_reading": 8.0, "ielts_writing": 7.0, "ielts_speaking": 7.0,
                "gmat_total": 730,
                "internship_count": 1, "internship_experience": "麦肯锡暑期实习",
                "work_years": 3, "work_experience": "贝恩咨询3年工作经验，Associate Consultant",
                "awards": "公司年度最佳新人奖",
                "recommendation_strength": "strong",
                "admitted_university_id": all_unis.get("西北大学"),
                "admitted_major_id": get_major_id("工商管理", "西北大学"),
                "admission_year": 2026, "admission_semester": "秋季",
                "result": "录取", "scholarship": "Merit Scholarship $20,000",
                "submitter_id": admin_id, "is_verified": 1
            },
            # 案例23: 录取 JHU 公共卫生
            {
                "applicant_name": "唐同学",
                "undergraduate_university_name": "北京大学医学部",
                "undergraduate_major": "预防医学",
                "graduation_year": 2025,
                "gpa": 3.65, "gpa_scale": 4.0,
                "toefl_total": 102, "toefl_reading": 27, "toefl_listening": 26, "toefl_speaking": 22, "toefl_writing": 27,
                "gre_total": 318, "gre_verbal": 150, "gre_quant": 168, "gre_writing": 3.5,
                "internship_count": 2, "internship_experience": "中国CDC流行病学调查、世卫组织北京办事处",
                "research_count": 2, "research_experience": "传染病流行病学研究、全球健康方向",
                "publication_count": 1, "publications": "Lancet Public Health一篇合作论文",
                "recommendation_strength": "strong",
                "admitted_university_id": all_unis.get("约翰霍普金斯大学"),
                "admitted_major_id": get_major_id("公共卫生", "约翰霍普金斯大学"),
                "admission_year": 2026, "admission_semester": "秋季",
                "result": "录取", "scholarship": "Tuition Fellowship",
                "submitter_id": admin_id, "is_verified": 1
            },
            # 案例24: 录取 Manchester 商业分析
            {
                "applicant_name": "曹同学",
                "undergraduate_university_name": "对外经济贸易大学",
                "undergraduate_major": "金融工程",
                "graduation_year": 2025,
                "gpa": 3.4, "gpa_scale": 4.0,
                "ielts_overall": 7.0, "ielts_listening": 7.0, "ielts_reading": 7.5, "ielts_writing": 6.5, "ielts_speaking": 6.5,
                "gmat_total": 680,
                "internship_count": 2, "internship_experience": "安永咨询、京东数据分析",
                "research_count": 0,
                "recommendation_strength": "medium",
                "admitted_university_id": all_unis.get("曼彻斯特大学"),
                "admitted_major_id": get_major_id("商业分析", "曼彻斯特大学"),
                "admission_year": 2026, "admission_semester": "秋季",
                "result": "录取", "scholarship": "",
                "submitter_id": user_id, "is_verified": 1
            },
            # 案例25: 拒绝 Berkeley
            {
                "applicant_name": "韩同学",
                "undergraduate_university_name": "北京航空航天大学",
                "undergraduate_major": "计算机科学",
                "graduation_year": 2025,
                "gpa": 3.6, "gpa_scale": 4.0,
                "toefl_total": 100, "toefl_reading": 27, "toefl_listening": 25, "toefl_speaking": 22, "toefl_writing": 26,
                "gre_total": 322, "gre_verbal": 155, "gre_quant": 167, "gre_writing": 3.5,
                "internship_count": 2, "internship_experience": "微软苏州、网易游戏",
                "research_count": 1, "research_experience": "软件工程方向研究",
                "recommendation_strength": "medium",
                "admitted_university_id": all_unis.get("加州大学伯克利分校"),
                "admitted_major_id": get_major_id("电气工程", "加州大学伯克利分校"),
                "admission_year": 2026, "admission_semester": "秋季",
                "result": "拒绝",
                "remarks": "GPA和科研经历不够突出，Berkeley EECS竞争极为激烈",
                "submitter_id": user_id, "is_verified": 1
            },
            # 案例26: 录取 UBC 商业分析
            {
                "applicant_name": "冯同学",
                "undergraduate_university_name": "山东大学",
                "undergraduate_major": "信息管理与信息系统",
                "graduation_year": 2025,
                "gpa": 3.5, "gpa_scale": 4.0,
                "ielts_overall": 7.0, "ielts_listening": 7.0, "ielts_reading": 7.5, "ielts_writing": 6.5, "ielts_speaking": 6.5,
                "gmat_total": 700,
                "internship_count": 2, "internship_experience": "普华永道数据咨询、字节跳动产品分析",
                "research_count": 1, "research_experience": "商业智能方向研究",
                "recommendation_strength": "medium",
                "admitted_university_id": all_unis.get("英属哥伦比亚大学"),
                "admitted_major_id": get_major_id("商业分析", "英属哥伦比亚大学"),
                "admission_year": 2026, "admission_semester": "秋季",
                "result": "录取", "scholarship": "",
                "submitter_id": user_id, "is_verified": 1
            },
            # 案例27: 录取 TU Munich 计算机
            {
                "applicant_name": "邓同学",
                "undergraduate_university_name": "同济大学",
                "undergraduate_major": "车辆工程",
                "graduation_year": 2025,
                "gpa": 3.55, "gpa_scale": 4.0,
                "ielts_overall": 6.5, "ielts_listening": 7.0, "ielts_reading": 7.0, "ielts_writing": 6.0, "ielts_speaking": 6.0,
                "gre_total": 318, "gre_verbal": 150, "gre_quant": 168, "gre_writing": 3.0,
                "internship_count": 2, "internship_experience": "大众汽车研发中心、博世中国",
                "research_count": 1, "research_experience": "自动驾驶感知算法研究",
                "recommendation_strength": "medium",
                "admitted_university_id": all_unis.get("慕尼黑工业大学"),
                "admitted_major_id": get_major_id("计算机", "慕尼黑工业大学"),
                "admission_year": 2026, "admission_semester": "冬季",
                "result": "录取", "scholarship": "DAAD奖学金",
                "submitter_id": admin_id, "is_verified": 1
            },
            # 案例28: 录取 KCL 国际关系
            {
                "applicant_name": "程同学",
                "undergraduate_university_name": "外交学院",
                "undergraduate_major": "国际关系",
                "graduation_year": 2025,
                "gpa": 3.6, "gpa_scale": 4.0,
                "ielts_overall": 7.5, "ielts_listening": 7.5, "ielts_reading": 8.0, "ielts_writing": 7.0, "ielts_speaking": 7.0,
                "internship_count": 2, "internship_experience": "中国外交部实习、联合国日内瓦办事处",
                "research_count": 1, "research_experience": "中东地区安全问题研究",
                "publication_count": 0,
                "extracurricular": "模拟联合国全国最佳代表",
                "awards": "全国大学生英语辩论赛冠军",
                "recommendation_strength": "strong",
                "admitted_university_id": all_unis.get("伦敦国王学院"),
                "admitted_major_id": get_major_id("国际关系", "伦敦国王学院"),
                "admission_year": 2026, "admission_semester": "秋季",
                "result": "录取", "scholarship": "",
                "submitter_id": admin_id, "is_verified": 1
            },
            # 案例29: 候补 Warwick MBA
            {
                "applicant_name": "蒋同学",
                "undergraduate_university_name": "中南财经政法大学",
                "undergraduate_major": "会计学",
                "graduation_year": 2023,
                "gpa": 3.3, "gpa_scale": 4.0,
                "ielts_overall": 7.0, "ielts_listening": 7.0, "ielts_reading": 7.5, "ielts_writing": 6.5, "ielts_speaking": 6.5,
                "gmat_total": 680,
                "work_years": 2, "work_experience": "德勤审计部2年",
                "internship_count": 0,
                "recommendation_strength": "medium",
                "admitted_university_id": all_unis.get("华威大学"),
                "admitted_major_id": get_major_id("工商管理", "华威大学"),
                "admission_year": 2026, "admission_semester": "秋季",
                "result": "候补",
                "remarks": "GPA偏低，工作年限不足，GMAT可以再刷高",
                "submitter_id": user_id, "is_verified": 1
            },
            # 案例30: 录取 CityU 创意媒体
            {
                "applicant_name": "彭同学",
                "undergraduate_university_name": "中国传媒大学",
                "undergraduate_major": "数字媒体艺术",
                "graduation_year": 2025,
                "gpa": 3.4, "gpa_scale": 4.0,
                "ielts_overall": 6.5, "ielts_listening": 7.0, "ielts_reading": 6.5, "ielts_writing": 6.0, "ielts_speaking": 6.0,
                "internship_count": 2, "internship_experience": "光线影业后期制作、网易游戏美术实习",
                "research_count": 0,
                "awards": "全国大学生新媒体创意大赛金奖",
                "extracurricular": "独立短片导演，作品入围大学生电影节",
                "recommendation_strength": "medium",
                "admitted_university_id": all_unis.get("香港城市大学"),
                "admitted_major_id": get_major_id("创意媒体", "香港城市大学"),
                "admission_year": 2026, "admission_semester": "秋季",
                "result": "录取", "scholarship": "入学奖学金3万港币",
                "submitter_id": user_id, "is_verified": 1
            },
            # 案例31: 录取 PolyU 酒店管理
            {
                "applicant_name": "魏同学",
                "undergraduate_university_name": "四川大学",
                "undergraduate_major": "旅游管理",
                "graduation_year": 2025,
                "gpa": 3.3, "gpa_scale": 4.0,
                "ielts_overall": 6.5, "ielts_listening": 6.5, "ielts_reading": 7.0, "ielts_writing": 6.0, "ielts_speaking": 6.0,
                "internship_count": 3, "internship_experience": "丽思卡尔顿前台管理实习、万豪集团运营管理、携程产品运营",
                "research_count": 0,
                "extracurricular": "校酒店管理协会会长",
                "recommendation_strength": "medium",
                "admitted_university_id": all_unis.get("香港理工大学"),
                "admitted_major_id": get_major_id("酒店", "香港理工大学"),
                "admission_year": 2026, "admission_semester": "秋季",
                "result": "录取", "scholarship": "",
                "submitter_id": admin_id, "is_verified": 1
            },
            # 案例32: 录取 Monash 药学
            {
                "applicant_name": "叶同学",
                "undergraduate_university_name": "中国药科大学",
                "undergraduate_major": "药学",
                "graduation_year": 2025,
                "gpa": 3.5, "gpa_scale": 4.0,
                "ielts_overall": 6.5, "ielts_listening": 7.0, "ielts_reading": 6.5, "ielts_writing": 6.0, "ielts_speaking": 6.0,
                "internship_count": 1, "internship_experience": "恒瑞医药研发实习",
                "research_count": 2, "research_experience": "药物化学实验室、临床药学研究",
                "publication_count": 1, "publications": "Pharmaceutical Research一篇合作论文",
                "recommendation_strength": "medium",
                "admitted_university_id": all_unis.get("莫纳什大学"),
                "admitted_major_id": get_major_id("药学", "莫纳什大学"),
                "admission_year": 2026, "admission_semester": "秋季",
                "result": "录取", "scholarship": "",
                "submitter_id": admin_id, "is_verified": 1
            },
            # 案例33: 录取 UCLA 公共卫生
            {
                "applicant_name": "潘同学",
                "undergraduate_university_name": "华中科技大学同济医学院",
                "undergraduate_major": "公共卫生",
                "graduation_year": 2025,
                "gpa": 3.55, "gpa_scale": 4.0,
                "toefl_total": 100, "toefl_reading": 27, "toefl_listening": 25, "toefl_speaking": 22, "toefl_writing": 26,
                "gre_total": 315, "gre_verbal": 148, "gre_quant": 167, "gre_writing": 3.5,
                "internship_count": 2, "internship_experience": "湖北省疾控中心、强生医疗",
                "research_count": 1, "research_experience": "慢性病流行病学研究",
                "recommendation_strength": "medium",
                "admitted_university_id": all_unis.get("加州大学洛杉矶分校"),
                "admitted_major_id": get_major_id("公共卫生", "加州大学洛杉矶分校"),
                "admission_year": 2026, "admission_semester": "秋季",
                "result": "录取", "scholarship": "",
                "submitter_id": user_id, "is_verified": 1
            },
            # 案例34: 拒绝 Stanford CS
            {
                "applicant_name": "范同学",
                "undergraduate_university_name": "上海交通大学",
                "undergraduate_major": "计算机科学",
                "graduation_year": 2025,
                "gpa": 3.7, "gpa_scale": 4.0,
                "toefl_total": 108, "toefl_reading": 28, "toefl_listening": 28, "toefl_speaking": 24, "toefl_writing": 28,
                "gre_total": 326, "gre_verbal": 158, "gre_quant": 168, "gre_writing": 4.0,
                "internship_count": 2, "internship_experience": "Google暑期实习、阿里巴巴达摩院",
                "research_count": 1, "research_experience": "NLP方向研究",
                "publication_count": 0,
                "recommendation_strength": "medium",
                "admitted_university_id": all_unis.get("斯坦福大学"),
                "admitted_major_id": get_major_id("计算机", "斯坦福大学"),
                "admission_year": 2026, "admission_semester": "秋季",
                "result": "拒绝",
                "remarks": "缺少顶会论文，Stanford CS竞争激烈需要更强科研背景",
                "submitter_id": admin_id, "is_verified": 1
            },
            # 案例35: 录取 Waterloo CS
            {
                "applicant_name": "方同学",
                "undergraduate_university_name": "电子科技大学",
                "undergraduate_major": "软件工程",
                "graduation_year": 2025,
                "gpa": 3.5, "gpa_scale": 4.0,
                "ielts_overall": 7.0, "ielts_listening": 7.0, "ielts_reading": 7.5, "ielts_writing": 6.5, "ielts_speaking": 6.5,
                "gre_total": 320, "gre_verbal": 152, "gre_quant": 168, "gre_writing": 3.5,
                "internship_count": 2, "internship_experience": "华为云计算实习、美团后端开发",
                "research_count": 1, "research_experience": "分布式计算方向",
                "recommendation_strength": "medium",
                "admitted_university_id": all_unis.get("滑铁卢大学"),
                "admitted_major_id": get_major_id("计算机", "滑铁卢大学"),
                "admission_year": 2026, "admission_semester": "秋季",
                "result": "录取", "scholarship": "",
                "submitter_id": user_id, "is_verified": 1
            },
            # 案例36: 录取 ANU 国际关系
            {
                "applicant_name": "任同学",
                "undergraduate_university_name": "北京外国语大学",
                "undergraduate_major": "国际政治",
                "graduation_year": 2025,
                "gpa": 3.55, "gpa_scale": 4.0,
                "ielts_overall": 7.5, "ielts_listening": 7.5, "ielts_reading": 8.0, "ielts_writing": 7.0, "ielts_speaking": 7.0,
                "internship_count": 2, "internship_experience": "新华社国际部实习、中国国际问题研究院",
                "research_count": 1, "research_experience": "亚太安全格局研究",
                "publication_count": 0,
                "extracurricular": "全国大学生国际模拟法庭辩论赛参赛",
                "recommendation_strength": "strong",
                "admitted_university_id": all_unis.get("澳大利亚国立大学"),
                "admitted_major_id": get_major_id("国际关系", "澳大利亚国立大学"),
                "admission_year": 2026, "admission_semester": "秋季",
                "result": "录取", "scholarship": "ANU Merit Scholarship A$10,000",
                "submitter_id": admin_id, "is_verified": 1
            },
            # 案例37: 录取 Amsterdam 传播学
            {
                "applicant_name": "姚同学",
                "undergraduate_university_name": "暨南大学",
                "undergraduate_major": "新闻传播学",
                "graduation_year": 2025,
                "gpa": 3.45, "gpa_scale": 4.0,
                "ielts_overall": 7.0, "ielts_listening": 7.0, "ielts_reading": 7.5, "ielts_writing": 6.5, "ielts_speaking": 6.5,
                "internship_count": 2, "internship_experience": "南方都市报、腾讯新闻内容运营",
                "research_count": 1, "research_experience": "新媒体传播效果研究",
                "publication_count": 0,
                "recommendation_strength": "medium",
                "admitted_university_id": all_unis.get("阿姆斯特丹大学"),
                "admitted_major_id": get_major_id("传播", "阿姆斯特丹大学"),
                "admission_year": 2026, "admission_semester": "秋季",
                "result": "录取", "scholarship": "",
                "submitter_id": user_id, "is_verified": 1
            },
            # 案例38: 拒绝 Columbia 金融工程
            {
                "applicant_name": "段同学",
                "undergraduate_university_name": "中央财经大学",
                "undergraduate_major": "金融数学",
                "graduation_year": 2025,
                "gpa": 3.5, "gpa_scale": 4.0,
                "toefl_total": 100, "toefl_reading": 27, "toefl_listening": 25, "toefl_speaking": 22, "toefl_writing": 26,
                "gre_total": 320, "gre_verbal": 152, "gre_quant": 168, "gre_writing": 3.5,
                "internship_count": 2, "internship_experience": "中信证券量化研究、券商实习",
                "research_count": 0,
                "recommendation_strength": "medium",
                "admitted_university_id": all_unis.get("哥伦比亚大学"),
                "admitted_major_id": get_major_id("金融工程", "哥伦比亚大学"),
                "admission_year": 2026, "admission_semester": "秋季",
                "result": "拒绝",
                "remarks": "本科背景不够top，缺少科研和竞赛经历",
                "submitter_id": admin_id, "is_verified": 1
            },
            # 案例39: 录取 Queensland 环境科学
            {
                "applicant_name": "钟同学",
                "undergraduate_university_name": "中国海洋大学",
                "undergraduate_major": "海洋科学",
                "graduation_year": 2025,
                "gpa": 3.4, "gpa_scale": 4.0,
                "ielts_overall": 6.5, "ielts_listening": 6.5, "ielts_reading": 7.0, "ielts_writing": 6.0, "ielts_speaking": 6.0,
                "internship_count": 1, "internship_experience": "中科院海洋研究所暑期实习",
                "research_count": 2, "research_experience": "海洋生态调查、珊瑚礁保护研究",
                "publication_count": 0,
                "extracurricular": "海洋环保志愿者协会创始人",
                "recommendation_strength": "medium",
                "admitted_university_id": all_unis.get("昆士兰大学"),
                "admitted_major_id": get_major_id("环境", "昆士兰大学"),
                "admission_year": 2026, "admission_semester": "秋季",
                "result": "录取", "scholarship": "UQ Excellence Scholarship A$5,000",
                "submitter_id": user_id, "is_verified": 1
            },
            # 案例40: 录取 Bristol 机器人
            {
                "applicant_name": "贾同学",
                "undergraduate_university_name": "哈尔滨工业大学",
                "undergraduate_major": "自动化",
                "graduation_year": 2025,
                "gpa": 3.55, "gpa_scale": 4.0,
                "ielts_overall": 6.5, "ielts_listening": 7.0, "ielts_reading": 7.0, "ielts_writing": 6.0, "ielts_speaking": 6.0,
                "internship_count": 1, "internship_experience": "大疆创新机器视觉实习",
                "research_count": 2, "research_experience": "移动机器人导航、SLAM方向研究",
                "publication_count": 1, "publications": "IROS 2024一篇合作论文",
                "recommendation_strength": "medium",
                "admitted_university_id": all_unis.get("布里斯托大学"),
                "admitted_major_id": get_major_id("机器人", "布里斯托大学"),
                "admission_year": 2026, "admission_semester": "秋季",
                "result": "录取", "scholarship": "",
                "submitter_id": admin_id, "is_verified": 1
            },
        ]
        
        for cdata in cases_data:
            # 跳过 admitted_university_id 或 admitted_major_id 为 None 的
            if not cdata.get("admitted_university_id") or not cdata.get("admitted_major_id"):
                print(f"跳过案例（缺少院校/专业ID）: {cdata.get('applicant_name')}")
                continue
            existing = db.query(Case).filter(
                Case.applicant_name == cdata["applicant_name"],
                Case.admitted_university_id == cdata["admitted_university_id"],
                Case.admitted_major_id == cdata["admitted_major_id"]
            ).first()
            if not existing:
                case = Case(**cdata)
                db.add(case)
                print(f"添加案例: {cdata['applicant_name']} → {cdata.get('result')}")
        
        db.commit()
        print("\n数据初始化完成！")
        
    except Exception as e:
        print(f"初始化数据时出错: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    init_db()

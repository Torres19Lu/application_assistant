"""查找剩余学校的 Wikipedia 图片文件名"""
import httpx
import time

HEADERS = {'User-Agent': 'MasterApp/1.0'}
client = httpx.Client(headers=HEADERS, follow_redirects=True)

articles = {
    '墨尔本大学': 'University_of_Melbourne',
    '新南威尔士大学': 'University_of_New_South_Wales',
    '香港中文大学': 'Chinese_University_of_Hong_Kong',
    '香港科技大学': 'Hong_Kong_University_of_Science_and_Technology',
    '约翰霍普金斯大学': 'Johns_Hopkins_University',
    '英属哥伦比亚大学': 'University_of_British_Columbia',
    '布里斯托大学': 'University_of_Bristol',
    '昆士兰大学': 'University_of_Queensland',
    '阿姆斯特丹大学': 'University_of_Amsterdam',
}

for name, art in articles.items():
    url = f'https://en.wikipedia.org/w/api.php?action=query&titles={art}&prop=images&imlimit=30&format=json'
    r = client.get(url, timeout=15)
    data = r.json()
    pages = data.get('query', {}).get('pages', {})
    for pid, pdata in pages.items():
        images = pdata.get('images', [])
        keywords = ['seal', 'coat', 'crest', 'shield', 'logo', 'emblem', 'arms']
        svgs = [img['title'] for img in images if any(kw in img['title'].lower() for kw in keywords)]
        print(f'\n{name}:')
        for s in svgs[:5]:
            print(f'  {s}')
        if not svgs:
            all_imgs = [img['title'] for img in images[:8]]
            print(f'  No matching. All images:')
            for a in all_imgs:
                print(f'    {a}')
    time.sleep(0.5)

client.close()

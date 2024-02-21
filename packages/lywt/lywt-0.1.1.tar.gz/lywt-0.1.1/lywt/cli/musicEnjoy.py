import re
import requests
from bs4 import BeautifulSoup
import json

DEFAULT_USER_AGENT = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:108.0) Gecko/20100101 Firefox/108.0'


def getPage(url, encoding='utf-8') -> str:
    headers = {'User-Agent': DEFAULT_USER_AGENT}
    response = requests.get(url=url, headers=headers)
    print(response.status_code)
    content = response.content.decode(encoding=encoding)
    return content


def savePage(url: str, dest: str = './page.html', encoding='utf-8'):
    page = getPage(url=url, encoding=encoding)
    with open(dest, 'w', encoding=encoding) as fw:
        fw.write(page)


def download(url: str, dest: str, headers: dict):
    try:
        response = requests.get(url=url, headers=headers,
                                stream=True, verify=True)
        print(response.status_code)
        with open(dest, 'wb') as fw:
            for chunk in response.iter_content(1024):
                fw.write(chunk)
                fw.flush()  # 清空缓存
    except Exception as e:
        print("url下载错误: %s" % url)
        print(e)
    return


def bilibili(url: str, dest: str, audio_or_video: str):
    headers = {
        'User-Agent': DEFAULT_USER_AGENT,
        "Origin": 'https://www.bilibili.com/',
        "Referer": 'https://www.bilibili.com/',
    }
    response = requests.get(url=url, headers=headers)
    soup = BeautifulSoup(response.text, 'lxml')
    video_url = ''
    audio_url = ''
    for i in range(len(soup('script'))):
        pattern = 'window.__playinfo__='
        if str(soup('script')[i].string)[:len(pattern)] == pattern:
            info = str(soup('script')[i].string)[len(pattern):]
            info_dict = json.loads(info)
            video_url = info_dict['data']['dash']['video'][0]['baseUrl']
            audio_url = info_dict['data']['dash']['audio'][0]['baseUrl']
            break
    if audio_or_video == 'audio':
        download(url=audio_url, dest=dest, headers=headers)
    if audio_or_video == 'video':
        download(url=video_url, dest=dest, headers=headers)
    return


def kugou(url, dest):
    """
        url = 'https://www.kugou.com/mixsong/49zyubb7.html?frombaidu#hash=04BBC1EC0A36C36457541588F0A6B337&album_id=3771
        4499&album_audio_id=258659363'
        address:
            https://wwwapi.kugou.com/yy/index.php?r=play/getdata&callback=jQuery19106392951916303002_1654082244006 // 固定
            &hash=13C62DD9569E717335EC282F8A38D837  // 可得
            &dfid=0R7vvH0Zd9bG4fCYat0Ad5ge&appid=1014&mid=c25d7ff99a965e5755984d727fccd663&platid=4   // 固定
            &album_id=970232    // 可得
            &album_audio_id=32130860  // 可得
    """
    # hashCode = 'hash=.*?&'
    # hashCode = re.findall(hashCode, url)[0]
    # album_id = 'album_id=[0-9]*'
    # album_id = re.findall(album_id, url)[0]
    # album_audio_id = 'album_audio_id.*?$'
    # album_audio_id = re.findall(album_audio_id, url)[0]

    hashCode = 'EBCCDE59F97BC06183F3B1A8502B7479'
    album_id = '2nc3vnfe'

    address = 'https://wwwapi.kugou.com/yy/index.php?r=play/getdata&callback=jQuery191063929519' \
              '16303002_1654082244006&' + hashCode + 'dfid=0R7vvH0Zd9bG4fCYat0Ad5ge&appid=1014&mid' \
                                                     '=c25d7ff99a965e5755984d727fccd663&platid=4&' + album_id
    print(address)

    headers = {
        'User-Agent': DEFAULT_USER_AGENT,
        "Origin": 'https://www.kugou.com/',
        "Referer": 'https://www.kugou.com/',
    }
    mp3 = "\"play_url\":\"https:.*?\""
    page = getPage(url=address)
    print(page)
    mp3 = re.findall("\"play_url\":\"https:.*?\"", page)[0][11:]
    print(mp3)
    mp3 = mp3.replace('\\', '')
    mp3 = mp3.replace('"', '')
    # print(mp3)
    download(url=mp3, dest=dest, headers=headers)
    return


if __name__ == '__main__':
    # print('hello world')
    # m = "https://www.bilibili.com/video/BV15841137Ge/"
    # bilibili(m, '1.mp3', 'audio')
    pass

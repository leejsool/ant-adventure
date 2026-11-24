"""index.html(원본)에서 배포용 파일을 한 번에 다시 만든다. 게임을 고친 뒤에는 이 명령 하나만 실행하면 된다.

  python make-single.py

만드는 것
  1) ant-adventure.html   : 파일 하나로 열리는 판 (앱 설치용 연결을 뺌)
  2) ../ant-adventure.zip : 인터넷에 올리는 판 (index.html + 앱 설정 + 아이콘 + 서비스 워커)
항상 index.html 기준이라 세 가지가 서로 어긋나지 않는다.
"""
import re, pathlib, zipfile

root = pathlib.Path(__file__).resolve().parent
import datetime
stamp = datetime.datetime.now().strftime('%Y-%m-%d %H:%M')
src = (root / 'index.html').read_text(encoding='utf-8')
src = re.sub(r"const BUILD = '[^']*';", "const BUILD = '%s';" % stamp, src)   # 버전 표시(시각)를 새로 찍는다
with open(root / 'index.html', 'w', encoding='utf-8', newline='\n') as f:
    f.write(src)
print('버전 표시:', stamp)

# 1) 파일 하나짜리
drop_lines = ('rel="manifest"', 'name="theme-color"', 'rel="apple-touch-icon"', 'apple-mobile-web-app')
text = '\n'.join(ln for ln in src.split('\n') if not any(k in ln for k in drop_lines))
text, n = re.subn(r"try \{ if \('serviceWorker' in navigator.*?\} catch \(e\) \{\}\n", '', text, flags=re.S)
(root / 'ant-adventure.html').write_text(text, encoding='utf-8')
print('ant-adventure.html 만듦 (서비스 워커 줄 제거: %d개)' % n)

# 2) 올리기용 zip (파일 6개)
files = ['index.html', 'manifest.webmanifest', 'sw.js', 'icon-192.png', 'icon-512.png', 'apple-touch-icon.png']
zpath = root.parent / 'ant-adventure.zip'
with zipfile.ZipFile(zpath, 'w', zipfile.ZIP_DEFLATED) as z:
    for f in files:
        z.write(root / f, f)
print('ant-adventure.zip 만듦:', zpath, '(%d bytes)' % zpath.stat().st_size)

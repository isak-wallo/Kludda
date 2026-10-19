"""Bygger Kludda som Android-app (APK) med Capacitor.

Appens filer (ASSETS i sw.js, utom sw.js) kopieras från arbetskopian till
app-webb/ och läggs in i Android-projektet (android/), som byggs och signeras
med keIWs nyckel (keiwsNycklar i ~/.gradle/gradle.properties, utanför repot).
APK:n hamnar i Claude\\apk\\Kludda-vNN.apk (i Dropbox, så att den kan öppnas på
plattan). versionCode är numret i VERSION i sw.js (v33 -> 33), så en ny APK
installeras över den gamla och teckningen finns kvar.

    python verktyg/bygg_apk.py               # bygger APK:n
    python verktyg/bygg_apk.py --installera  # och installerar den med adb (USB)

Kräver Node, Java 21 och Android SDK (ANDROID_HOME, annars
%LOCALAPPDATA%\\Android\\Sdk). Första gången: npm install.
"""
import argparse
import os
import re
import shutil
import subprocess
import sys

ROT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
WEBB = os.path.join(ROT, 'app-webb')
UT = os.path.join(os.path.dirname(ROT), 'apk')
SDK = os.environ.get('ANDROID_HOME') or os.path.join(os.environ['LOCALAPPDATA'], 'Android', 'Sdk')


def kor(kommando, cwd=ROT):
    subprocess.run(kommando, shell=True, cwd=cwd, check=True,
                   env={**os.environ, 'ANDROID_HOME': SDK})


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--installera', action='store_true')
    arg = ap.parse_args()

    sw = open(os.path.join(ROT, 'sw.js'), encoding='utf-8').read()
    version = re.search(r"const VERSION = '([^']*)'", sw).group(1)
    nr = int(re.search(r'\d+', version).group(0))
    assets = re.findall(r"'\./([^']*)'", re.search(r'const ASSETS = \[(.*?)\];', sw, re.S).group(1))

    # app-webb/ töms men tas inte bort (den är Dropbox-ignorerad).
    os.makedirs(WEBB, exist_ok=True)
    for f in os.listdir(WEBB):
        p = os.path.join(WEBB, f)
        shutil.rmtree(p) if os.path.isdir(p) else os.remove(p)
    for fil in [f for f in assets if f]:
        mal = os.path.join(WEBB, fil)
        os.makedirs(os.path.dirname(mal), exist_ok=True)
        shutil.copyfile(os.path.join(ROT, fil), mal)

    kor('npx cap sync android')
    kor(os.path.join(ROT, 'android', 'gradlew.bat') + ' assembleRelease -q -PversionCode=%d -PversionName=%s' % (nr, version),
        cwd=os.path.join(ROT, 'android'))

    os.makedirs(UT, exist_ok=True)
    apk = os.path.join(UT, 'Kludda-%s.apk' % version)
    shutil.copyfile(os.path.join(ROT, 'android', 'app', 'build', 'outputs', 'apk', 'release',
                                 'app-release.apk'), apk)
    print('Klar:', apk)
    if arg.installera:
        kor('"%s" install -r "%s"' % (os.path.join(SDK, 'platform-tools', 'adb.exe'), apk))


if __name__ == '__main__':
    sys.stdout.reconfigure(encoding='utf-8')
    main()

#!/usr/bin/python

#un obscuro script de ajolo

from random import randrange
import pprint
from datetime import datetime

EQUIPOS = [
            "AIX",
            "CentOS",
            "CrunchBang",
            "DragonFly",
            "FreeBSD",
            "Funtoo",
            "Gentoo",
            "gNewSense",
            "HP-UX",
            "Kali",
            "Mac OS X",
            "Manjaro",
            "NetBSD",
            "OpenBSD",
            "OpenIndiana",
            "PCLinuxOS",
            "Puppy",
            "ReactOS",
            "Red Hat",
            "Sabayon",
            "Slackware",
            "Solaris",
            "SteamOS",
            "Windows",
        ]

elegidos = []

GRUPOS = {
            "A": ["Mint", ],
            "B": ["Ubuntu", ],
            "C": ["Debian", ],
            "D": ["Mageia", ],
            "E": ["Fedora", ],
            "F": ["OpenSUSE", ],
            "G": ["elementary OS", ],
            "H": ["Arch", ],
        }


for grupo in GRUPOS.keys():
    i = 0
    while i < 3:
        sorteado = randrange(24)
        while EQUIPOS[sorteado] in elegidos or EQUIPOS[sorteado] in GRUPOS[grupo]:
            sorteado = randrange(24)
        GRUPOS[grupo].append(EQUIPOS[sorteado])
        elegidos.append(EQUIPOS[sorteado])
        i += 1

rightnow = datetime.now()
print "Sorteo realizado el " + rightnow.strftime("%Y/%m/%d") + " a las " + rightnow.strftime("%H:%M") + "\n"
pprint.pprint(GRUPOS)

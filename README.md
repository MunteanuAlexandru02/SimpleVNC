# Proiect IA4 - SimpleVNC

Ne-am propus să implememtăm un server și un client în Python pentru o aplicație
stil TeamViewer, mult simplificată, dar care să își păstreze funcționalitatea
de bază, de control la distanță. Am realizat aplicația folosind biblioteci care
implementează protocolul VNC: `asyncvnc` pentru client și `pyVNCs` pentru server.

Am început prin a crea o interfață grafică de bază; pentru acest lucru am ales
biblioteca `PySimpleGUI`, care oferă funcționalitate de bază pentru crearea unei
interfețe grafice simple, dar funcționale. Întrucât scopul ei este doar de a
primi de la utilizator parametrii necesari realizării conexiunii între client
și server, câteva căsuțe de text și butoane sunt suficiente pentru a ne atinge
scopul.

În continuare, am avut de integrat funcționalitatea de backend cu acest
frontend; după câteva încercări nereușite de a apela funcționalitatea de server
în interiorul fișierului ce conține interfața grafică, am ajuns la concluzia că
cea mai simplă metodă de a rula serverul, fără a „îngheța” interfața grafică
este să creem un nou proces, care să fie pornit și oprit de către interfața
grafică.

Odată ce acesta accepta conexiuni și comenzi de la un client de VNC comercial,
ne-am îndreptat atenția spre crearea propriului client, o sarcină considerabil
mai dificilă, întrucât, pe lăngă interfața de introducere a parametrilor de
conectare (care, de altfel, este foarte asemănătoare cu cea a serverului), este
necesară și crearea ferestrei care să afișeze ecranul calculatorului controlat
și primirea tastelor și poziția cursorului de la utilizator.

Primul pas a fost cel de a alege o bibliotecă de VNC pe care clientul să o
folosească. Comparativ cu serverul, am avut mai multe opțiuni, dar, spre
surprinderea noastră, cu excepția unor clienți de VNC compleți (la care nu aveam
cum să contribuim în vreun fel semnificativ), nu am reușit să ne conectăm la
server, indiferent dacă era al nostru sau unul comercial. După o cercetare mai
amănunțită, am decoperit, în repository-ul de pe GitHub a uneia dintre acestea
(`asyncvnc`, cea pe care am folosit-o într-un final), un Issue care descria exact
problemele pe care le întâmpinam și noi, anume o eroare de autentificare.
Astfel, cu ajutorul unei modificări în codul bibliotecii pusă la dispoziție de
utilizatorul care a semnalat problema, am reușit să ne conectăm cu succes la
server. Din acest motiv a trebuit să includem cu aplicația noastră o clonă a
repo-ului cu pricina, astfel încât să putem include versiunea modificată și
funcțională a acesteia.

Având acum o metodă de a ne conecta la server, a mai rămas doar fereastra
efectivă de control. După câteva teste cu sample code-ul oferit de creatorul
bibliotecii, am realizat că, din păcate, operațiunea de primire a ecranului
de la server este una care durează destul de mult, ceea ce, dacă am realiza-o
direct în bucla de execuție a interfeței grafice, ar duce la blocarea acesteia,
o așa-zisă „înghețare” periodică supărătoare. Din acest motiv, am decis să
separăm aceste două funcționalități prin utilizarea unui thread, care să se
ocupe de comunicarea cu serverul, în timp ce main thread-ul se ocupă de
interfața grafică și colectarea input-ului de la utilizator.

După câteva teste cu biblioteca pe care am folosit-o până acum (`PySimpleGUI`), am
ajuns la concluzia că aceasta (care este practic un wrapper peste alte
biblioteci de GUI mai puțin intuitive)	nu ar fi capabilă să actualizeze în mod
rapid și eficient capturile de ecran primite de client. Din această cauză, am
optat pentru a utiliza biblioteca pe care `PySimpleGUI` se bazează: `tkinter`.
Deși a avut un learning curve ceva mai mare decât prima interfață grafică, s-a
dovedit o alegere mai bună pentru operațiile ceva mai granulare pe care le-am
avut de făcut asupra fluxului de imagini primit de la server: acestea trebuie
redimensionate și afișate la poziția corectă în fereastra de control.

În final, a mai rămas de realizat partea de transmitere a comenzilor, care
constă practic în realizarea unei bijecții între input-ul primit de fereastra
de control și metodele de transmitere a acestora din biblioteca de VNC.

Până în acest punct, lucrul la acest proiect s-a realizat în Linux (Python deja
instalat, toți lucram pe aceeași mașină virtuală). Odată ce am vrut să testăm
aplicația și bare-metal (și, mai ales, pe Windows), ne-am lovit de o problemă
neașteptată: coordonatele de la mouse nu erau interpretate corespunzător de
către server. Inițial am renunțat la a încerca să găsim problema, întrucât pe
Linux serverul funcționează satisfăcător, dar, printr-o întâmplare, am testat
serverul și pe un laptop cu Windows cu un display de rezoluție mai mică
(1366x768), unde problema nu avea loc. Experimentând cu setările display-ului
din Windows 10, am constatat că problema de bază provenea de la setarea scalării
ecranului (utilă pentru a face elementele sistemului de operare mai mari pe
ecrane cu rezoluție mare - laptopul cu rezoluție mică avea scalarea setată la
100%, deci coordonatele nu erau afectate). O căutare pe internet a dezvăluit
faptul că problema provine din faptul că această setare este ignorată de pynput,
biblioteca folosită de server pentru a transmite comenzile primite de la client.
Soluția finală constă în pre-procesarea coordonatelor înainte de a fi transmise
metodelor din pynput, prin împărțirea lor la scala pe care Windows o folosește
pentru ecranul curent.

Astfel, programul nostru este testat, într-o destul de bună măsură, pe Windows
și Ubuntu, pe versiuni de Python>=3.7 (cerința minimă a bibliotecilor folosite).

## Instalare

Atât pentru server, cât și pentru client am pus la dispoziție câte un fișier
`requirements.txt`, care conține dependințele programului. Acestea pot fi
instalate cu `pip`; cea mai simplă metodă pentru a face acest lucru este
utilizarea unuia dintre fișierele Makefile puse la dispoziție, folosind comanda:
```
make setup
```

## Rulare

Pornirea oricăreia dintre aplicații se face din linia de comandă, în folderul
corespunzător acesteia, fie rulând cu Python fișierul corespunzător, adică
`python ./simplevncserver.py`,
respectiv
`python ./simplevncclient.py`,
fie folosind regulile de run existente în fișierele Makefile furnizate.

## Contribuții individuale la proiect

* Patricia Octavia SÎRBOIU: interfața grafică în `PySimpleGUI` a celor două aplicații
* Cristian-Alexandru CHIRIAC: realizarea conectării clientului la server și integrarea cu interfața grafică
* Mihai-Lucian PANDELICĂ: interfața grafică in `tkinter` și scalarea corespunzătoare a screenshot-urilor primite de la server; documentarea procesului de scriere a aplicației
* Alexandru-Constantin MUNTEANU: primirea comenzilor de la utilizator și translatarea coordonatelor mouse-ului primite de interfața grafică pentru a fi trimise mai departe serverului; curățare și comentare finală a codului

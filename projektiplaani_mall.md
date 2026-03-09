# Tehisintellekti rakendamise projektiplaani mall (CRISP-DM)

<br>
<br>


## 🔴 1. Äritegevuse mõistmine
*Fookus: mis on probleem ja milline on hea tulemus?*


### 🔴 1.1 Kasutaja kirjeldus ja eesmärgid
Kellel on probleem ja miks see lahendamist vajab? Mis on lahenduse oodatud kasu? Milline on hetkel eksisteeriv lahendus?

> Probleem on see, et toode võib olla mitte ettenähtud vormis. Vaja on, et tehisintellekt tuvastaks kõiksuguseid vigu. Sildid puudu, kuupäev õige, toode üldse olemas, õige toode pakis. Kasu on see, et tarbijani jõuab õige toode, mis on värske ja korraliku kvaliteediga. Hetkel olev lahendus on see, et inimene kontrollib, aga see on tihti vigane erinevate põhjuste tõttu, motovatsioon, väsimus jne. Peamine eesmärk on saada pikaajalist statistikat, et monitoorida paremini kulusi, materjali kulu ja toodete kvaliteeti suuremas pildis. Kui miski on valesti, siis liin panna ajutiselt seisma, et lahendada probleem. Oluliseim on see, et kuupäev oleks õige ja toode samuti õige. Inimesel on palju lihtsam märgata seda, kui sildid on puudu. Aga see liini seisma panemine sõltub kohalolevast IT tiimist, meie ülesanne on luua tuvastussüsteem.

### 🔴 1.2 Edukuse mõõdikud
Kuidas mõõdame rakenduse edukust? Mida peab rakendus teha suutma?

> Rakendus peab suutma tuvastada 2 sildi olemasolu, toote aegumiskuupäeva koos triipkoodiga. Toode ise peab ka pakis olemas olema, mis peab olema vastavuses sildil oleva tootega. See info tuleb triipkoodil olevast inforst. Ideaalis on kõik need komponendid olemas ja pakis vastav toode. Seda saaks hinnata protsentuaalselt kogu toodangust ja tuvastada, kus tekib kõige rohkem vigu.

### 🔴 1.3 Ressursid ja piirangud
Millised on ressursipiirangud (nt aeg, eelarve, tööjõud, arvutusvõimsus)? Millised on tehnilised ja juriidilised piirangud (GDPR, turvanõuded, platvorm)? Millised on piirangud tasuliste tehisintellekti mudelite kasutamisele?

> Peamine piirang on süsteemi arendamiseks kuluv aeg ja tööjõud. Eeldame, et vajalik kaamera koos muu riistvara ja tarkvaraga on paigaldatud eelnevalt. Meie ülesanne on kaameravogu töödelda. 

<br>
<br>


## 🟠 2. Andmete mõistmine
*Fookus: millised on meie andmed?*

### 🟠 2.1 Andmevajadus ja andmeallikad
Milliseid andmeid (ning kui palju) on lahenduse toimimiseks vaja? Kust andmed pärinevad ja kas on tagatud andmetele ligipääs?

> Andmeteks on videod päris tooteliini kohta. Ehk videoandmed. Andmeid on vaja erinevate toodete kohta (neid on mitukümmend). Andmetele ligipääs on tagatud piisavas mahus, et lahendada probleemi. Andmed kuupäeva kohta on keerulisemalt, kuna alati ei olegi võimalik tuvastada seda. Saame ära kasutada teadmist, et samad tooted, mis jõrjest tulevad on sama kuupäevaga. 

### 🟠 2.2 Andmete kasutuspiirangud
Kas andmete kasutamine (sh ärilisel eesmärgil) on lubatud? Kas andmestik sisaldab tundlikku informatsiooni?

> Andmete kasutamine on lubatud selle ülesande lahendamiseks. Andmestik sisaldab informatsiooni NÕO lihatootmise eravara kohta. 

### 🟠 2.3 Andmete kvaliteet ja maht
Millises formaadis andmeid hoiustatakse? Mis on andmete maht ja andmestiku suurus? Kas andmete kvaliteet on piisav (struktureeritus, puhtus, andmete kogus) või on vaja märkimisväärset eeltööd?

> Andmed on live-voona, aga meile antakse ligipääs salvestatud videotele. 

### 🟠 2.4 Andmete kirjeldamise vajadus
Milliseid samme on vaja teha, et kirjeldada olemasolevaid andmeid ja nende kvaliteeti.

> Andmeanalüüs

<br>
<br>


## 🟡 3. Andmete ettevalmistamine
Fookus: Toordokumentide viimine tehisintellekti jaoks sobivasse formaati.

### 🟡 3.1 Puhastamise strateegia
Milliseid samme on vaja teha andmete puhastamiseks ja standardiseerimiseks? Kui suur on ettevalmistusele kuluv aja- või rahaline ressurss?

> ...

### 🟡 3.2 Tehisintellektispetsiifiline ettevalmistus
Kuidas andmed tehisintellekti mudelile sobivaks tehakse (nt tükeldamine, vektoriseerimine, metaandmete lisamine)?

> ...

<br>
<br>

## 🟢 4. Tehisintellekti rakendamine
Fookus: Tehisintellekti rakendamise süsteemi komponentide ja disaini kirjeldamine.

### 🟢 4.1 Komponentide valik ja koostöö
Millist tüüpi tehisintellekti komponente on vaja rakenduses kasutada? Kas on vaja ka komponente, mis ei sisalda tehisintellekti? Kas komponendid on eraldiseisvad või sõltuvad üksteisest (keerulisem agentsem disan)?

> OpticalFlow kaardimuutuse tuvastamiseks. Videost on vaja võtta kaader. Ideaalis liigub konveier iga 7 sekundi tagant. Pätast liikumist võtad kaadri ja lõikad seda, kuna siis töötlemine arvutusvõimsuse poolest palju parem. tehisintellekt on kuupäevade tuvastus, siltide tuvastus ...

### 🟢 4.2 Tehisintellekti lahenduste valik
Milliseid mudeleid on plaanis kasutada? Kas kasutada valmis teenust (API) või arendada/majutada mudelid ise?

> ...

### 🟢 4.3 Kuidas hinnata rakenduse headust?
Kuidas rakenduse arenduse käigus hinnata rakenduse headust?

> ...

### 🟢 4.4 Rakenduse arendus
Milliste sammude abil on plaanis/on võimalik rakendust järk-järgult parandada (viibadisain, erinevte mudelite testimine jne)?

> ...


### 🟢 4.5 Riskijuhtimine
Kuidas maandatakse tehisintellektispetsiifilisi riske (hallutsinatsioonid, kallutatus, turvalisus)?

> ...

<br>
<br>

## 🔵 5. Tulemuste hindamine
Fookus: kuidas hinnata loodud lahenduse rakendatavust ettevõttes/probleemilahendusel?

### 🔵 5.1 Vastavus eesmärkidele
Kuidas hinnata, kas rakendus vastab seatud eesmärkidele?

> ...

<br>
<br>

## 🟣 6. Juurutamine
Fookus: kuidas hinnata loodud lahenduse rakendatavust ettevõttes/probleemilahendusel?

### 🟣 6.1 Integratsioon
Kuidas ja millise liidese kaudu lõppkasutaja rakendust kasutab? Kuidas rakendus olemasolevasse töövoogu integreeritakse (juhul kui see on vajalik)?

> ...

### 🟣 6.2 Rakenduse elutsükkel ja hooldus
Kes vastutab süsteemi tööshoidmise ja jooksvate kulude eest? Kuidas toimub rakenduse uuendamine tulevikus?

> ...
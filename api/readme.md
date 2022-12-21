# Assignment 4 -- Databases

## Introduction

In this assignment, we will get the first introduction into databases in MySQL (with SQL) and MongoDB (with NoSQL).
We will also explore how to connect these databases to our Python API. By structuring our project well, we will allow our Database connection to be easily replaced by a different database, with little to no code-changes!

## Objective

### Knowledge
- SQL
- MySQL Databases
- MongoDB Databases
- Python libraries
    - SQLAlchemy (Relational databases)
    - PyMongo (MongoDB)
- Python API structure

### Skills
- Working with databases
- Extending Docker knowledge
- Structuring Python API's using patterns and Dependency Injection

## Assignment explanation
As our FastAPI project already has a well structured baseline, we can easily extend on this one to continue adding a database instead of working with the default JSON file I gave.
You might have also noticed that we currently only "add" information into memory and not into a persistent storage.

This will be something we can perfectly explore in this assignment.

## First steps

The first steps will be to explore SQL on our own a little bit, before we dive into the details of connecting everything to Python.

You can ignore the previous project where we have worked with nginx and a frontend project for now.
If you wish to explore this further by adding some functionalities later, you'll be able to do so as you please.

Create a new `docker-compose.yml` file, you can even call it `docker-compose.db.yml` for convenience. That way you can keep a clean slate on your previous project.

This `docker-compose.db.yml` should contain at least this already:

```yaml=
services:
    mariadb:
      image: mariadb:10.9.4
      restart: always
      ports:
        - 3306:3306
      environment:
        MYSQL_USER: user
        MYSQL_PASSWORD: password
        MYSQL_DATABASE: api
        MYSQL_ROOT_PASSWORD: password
      volumes:
        - db:/var/lib/mysql

volumes:
    db:
        # Don't write anything here, I didn't forget anything, but this is the default part!
```

When you boot up this Compose project, you'll get a new database that gets spun up.
Using the volume mapping, we will create a persistent storage volume somewhere on our PC, in a location that Docker will manage for us.

The Environment variables are your own choice, but don't forget to edit them if you want something different!

For now, it's not yet the most secure, but that's beside the point for this first exploration.

### Adding a GUI
You might be wondering how we will be putting something into our database for now, and what the structure of our database might look like?
Well, we can explore our database using the `adminer` Docker image.

:::warning
**TASK**
1. Add the Adminer service into the Docker image
Use the documentation for more help.
2. Try to connect to the database using the Adminer service in your browser
:::success
**QUESTION**
Paste the YAML you used below here.
Also answer what connection data you filled in into the fields to get your connection up and running.
```yaml
services:
    # Adminer service
```

```text
server: <>
username: <>
password: <>
database: <>
```
:::

#### Creating tables and injecting some data

When creating tables in a database, you first have to determine if you're working **database-first** or **code-first**.
When you're not really the programming specialist, you'll probably work with the database first.
You might also have a specific database developer in your team or company that already created the database before you even joined in on the project.

If this is the case, you'll need to structure your code to suit your database the best.
In the scenario where there is not database yet, you have more flexibility to create the database using Python libraries (or the equivalent in other languages!)

In our first exploration, we will go with a **database-first** approach. Then, we will later add some extra tables using the **code-first** approach.

To create our first table, we will use the Adminer GUI.

:::warning
**TASK**
1. Try to copy the information provided in the screenshot below which you can get after pressing the **`Create table`** button in Adminer.
![Create a table in Adminer](https://i.imgur.com/oDRNBB8.png)

3. Answer the questions below
4. Insert some dummy data, which you can find below.

:::success
**QUESTION**
1. Can you find the equivalent SQL command? It's somewhere on Adminer too. Please try to understand this command and adapt if necessary.
```sql
 -- Answer here, comments are added using `--` in SQL.
```
2. Why are we using this specific `text` type instead of `varchar` for the `description` column ?
```
Answer here
```
:::

:::spoiler Find the dummy data for this table here!

**Use the GUI or SQL to insert this information in the database**.

```json
[
    {
        "title": "Smart XR Developer",
        "description": "Welkom in het tijdperk van spatial computing. Waar de echte en de virtuele wereld versmelten tot een rijkere en betere ervaring voor iedereen. Als eerste profiel in Vlaanderen word je klaargestoomd voor het tijdperk waarin innovatieve Extended Reality (XR) interfaces on-the-job-training, medische interventies en mobiliteit naar een ander niveau zullen brengen.",
        "weight": 10
    },
    {
        "title": "Next Web Developer",
        "description": "Hoe laat je een drone vliegen met enkel code? Hoe kan je gebruikers razendsnel realtime laten communiceren? Zit web development ook in jouw DNA? Zie jij het potentieel in smartwatches en smartphones? Dat gevoel kennen we. We gaan aan de slag met zo veel meer dan een simpele klik of swipe. Een hartslag die verhoogt, een wenkbrauw die omhooggaat, een nieuwe houding of de toon van je stem: voor ons is het input.",
        "weight": 20
    },
    {
        "title": "AI Engineer",
        "description": "Het verkeer slimmer aansturen, kanker sneller opsporen, misdaden oplossen door het verbeteren van lage resolutie beelden en robots aansturen. Supervised learning en Neurale netwerken doen jou dromen van het ontwikkelen van AI software die zelf leert patronen ontdekken, voorspellingen maken of objecten herkennen. Software die net dat beetje slimmer is en nieuwe inzichten vindt in de immer streamende data.",
        "weight": 30
    },
    {
        "title": "IoT Infrastructure Engineer",
        "description": "Als gepassioneerd IoT Infrastructure Engineer sta je in het kloppend hart van de onderneming. Je onderhoudt het netwerk en servers met aandacht voor bedrijfscontinuïteit. Je hebt daarbij oog voor de modernste beveiliging tegen externe en interne bedreigingen.",
        "weight": 40
    }
]
```
:::

### Setting up a second table with a relationship to the first one.

We have set up a first table that contained the information of the different tracks we have in MCT. The second table we will want to add (and later fill in using Code), will be the `Courses` table.

:::warning
**TASK**
1. Use this SQL command to create the table.
```sql
-- Creating the Table
CREATE TABLE `courses` (
  `id` int NOT NULL AUTO_INCREMENT PRIMARY KEY,
  `title` varchar(255) NOT NULL,
  `tools` text NULL,
  `semester` int NOT NULL,
  `weight` int NOT NULL,
  `pillar` varchar(255) NOT NULL,
  `track_id` int(11) NULL,
  `content` longtext NOT NULL,
  FOREIGN KEY (`track_id`) REFERENCES `tracks` (`id`) ON DELETE NO ACTION
);
```
2. Use this SQL command to insert some data into the table.
:::spoiler Use this data
```sql
-- Inserting some data
INSERT INTO courses(title,tools,semester,weight,pillar,track_id,content) VALUES
('Basic Programming','Python, Visual Studio Code',1,10,'code',NULL,'<p>In deze module leren we de basisprincipes van programmeren aan via de programmeertaal <strong>Python</strong>. In het eerste deel leren we de syntax aan waarbij we uitgebreid stilstaan bij variabelen, deelproblemen, collectiestructuren, lusstructuren, enumerations &amp; arrays, enz. Dit laat ons toe om kleine applicaties te ontwikkelen die lezen en schrijven naar databestanden te verzorgen. Ondertussen hebben we ook aandacht voor een <strong>goede en consequente codestijl</strong>. In het tweede deel focust zich op <strong>OOP (Object Oriented Programming)</strong>, een techniek die in elke programeertaal aanwezig is.</p>'),
('Frontend Foundations','Visual Studio Code',1,20,'code',NULL,'<p>In deze korte module kan je leren hoe een webpagina technisch opgebouwd wordt. Dit doen we niet aan de hand van ellenlange theorie, maar we pakken deze module onmiddellijk hand-on aan.
Je leert werken met Hypertext Markup Language <strong>(HTML)</strong> en (Sassy) Cascading Style Sheets <strong>(SCSS)</strong> om web interfaces technisch uit te werken vanaf een voorontwerp.</p>
<p>Volgende topics komen aan bod:</p>
<ul>
<li>HTML (Hypertext Markup Language)</li>
<li>(S)CSS (Cascading Style Sheets)</li>
<li>De combinatie van deze talen</li>
<li>(S)CSS-frameworks</li>
<li>Responsiveness</li>
<li>Gebruik van best practices</li>
<li>Voorontwerpen omzetten naar (deel)assets en/of volledige webinterfaces</li>
</ul>'),
('User Experience Design','Adobe XD, pen & papier',1,25,'design',NULL,'<p>In deze module leren we <strong>designen voor de eindgebruiker</strong>. We bekijken <strong>verschillende technieken</strong> om een product te maken dat precies <strong>op maat van de doelgroep</strong> is. Het eerste onderdeel in onze workflow is <strong>research</strong>. Nadat we een onderzoek gedaan hebben, gaan we met deze kennis aan de slag om een eerste prototype te maken. Een <strong>eerste prototype</strong> kan op papier gebeuren. Heel snel gaan we met Adobe XD aan de slag. Adobe XD is gemaakt voor ontwerpers en het is de snelste manier om gebruikerservaringen te ontwerpen, te prototypen en te delen of het nu gaat over websites of mobiele apps of over spraakinteracties.</p>
<p>Uiteindelijk <strong>testen</strong> we of alles op een logische plaats staat, of gebruikers onze app of website goed kunnen gebruiken en hoe we de <strong>eerste stappen naar</strong> een <strong>afgewerkt design</strong> kunnen zetten.
In deze eerste design module ga je ook zorgen dat je je basisbouwstenen voor webdevelopment beheerst: <strong>HTML</strong> en <strong>CSS</strong> leer je zelfstandig met behulp van blended learning.</p>
<p>Patterns, usability heuristics, design thinking en Gestalt theorie komen aan bod in de uitlegsessies. Elke editie nodigen we professionals uit om hun expertise op het gebied van User Experience te delen. Zo kwamen bijvoorbeeld al knappe casussen van Skinn Branding Agency uitgebreid aan bod.</p>
<p>In de werkcolleges oefenen we de verschillende aspecten van de workflow. De verschillende challenges maken het uitdagend om je te verdiepen in User Experience.</p>'),
('Computer Networks','Windows 10/11, Debian Linux, Raspberry Pi, SOHO router, VMware virtualisatie',1,30,'connect',NULL,'<p>Tegenwoordig is elke computer verbonden met de wereld. Het internet heb je aan je vingers op je smartphone. Maar hoe komt dat eigenlijk? Hoe hangt alles aan elkaar?</p>
<p>In Computer Networks lopen we stap voor stap door een <strong>Small Office / Home Office (SOHO)</strong> netwerk om inzicht te krijgen in de <strong>opbouw</strong>, <strong>werking</strong> en <strong>beveiliging</strong> ervan. Je hoeft geen expert te zijn, want de basiskennis wordt stapsgewijs uitgelegd in praktische labo’s, ondersteund met de nodige theorie.</p>
<p>We beginnen bij de client met <strong>besturingssysteem Windows 10/11</strong> en vervolgens <strong>Linux</strong>, zowel <strong>Debian</strong> als <strong>Raspberry Pi OS</strong> op jouw persoonlijke Raspberry Pi. We bekijken een aantal basis- en beheerscommando’s om een basis server op te bouwen, uiteraard met de nodige achtergrondkennis.
Om je klaar te stomen voor de andere modules zal je op je Raspberry Pi een volledig geconfigureerde <strong>webserver</strong> en <strong>database</strong> kunnen opstarten.</p>
<p>Daarna gaan we deze toestellen integreren in een netwerk en gaan zo over de bekabeling naar centrale netwerkcomponenten zoals <strong>switches</strong>, <strong>draadloze access points</strong>, <strong>routers</strong> en <strong>firewalls</strong>.
De kennis over deze componenten gebruiken we om verschillende netwerken op te bouwen en te configureren om uiteindelijk een compleet netwerk vanaf nul op te zetten, zowel bekabeld als draadloos. Hier speelt de integratie van alle theoretische én de praktische kennis een belangrijke rol. Je installeert, configureert én beveiligt een netwerk vanaf de grond op, waarna je de servers en clients ermee koppelt.</p>
<p>Een goeie basis van <strong>IP subnetting</strong> en <strong>routing</strong> komt hier ook aan bod. Als <strong>Cisco Networking Academy</strong> gebruiken we de module &lsquo;Introduction to Networking&rsquo; als ondersteunend materiaal. In latere modules komen de andere delen van de Cisco opleiding aan bod.</p>'),
('Data Science & AI','Excel, Jupyter Notebook, Python',1,30,'analysis',NULL,'<p>In data science bestaat de <strong>uitdaging</strong> erin om <strong>uit</strong> (grote hoeveelheden) <strong>data zinvolle informatie</strong> te halen.<!-- raw HTML omitted -->Data science biedt een zodanige <strong>economische meerwaarde</strong> dat er niet meer aan te ontkomen valt. Het drijft zelfs de vierde industriële revolutie in een razend tempo vooruit. De meest succesvolle bedrijven ter wereld zijn heel dikwijls ook koploper op het vlak van data science en artificiële intelligentie. Denk maar aan Google en Facebook die gebruikersprofielen analyseren en advertenties op maat aanbieden, Tesla die aan de hand van sensordata hun wagens zelfrijdend maakt, luchtvaarmaatschappijen die optimale vliegroutes bepalen, banken die beurkoersen voorspellen of risico’s voorspellen of fraude detecteren.</p>
<p>In deze module leg je de basis om <strong>data om te zetten naar bruikbare inzichten</strong>. Dit begint bij het evalueren van de <strong>bruikbaarheid van de data</strong> en de <strong>preprocessing</strong> van een <strong>dataset</strong>. Vervolgens leer je <strong>statistische analyses</strong> toe te passen, <strong>data te visualiseren</strong>, conclusies te trekken en <strong>gefundeerde keuzes</strong> te maken. Je leert kennis maken met kansverdeling, regressie en zet zelfs je eerste stapjes in <strong>Machine learning en AI</strong>.</p>'),
('Prototyping','Arduino, ESP32',1,50,'project',NULL,'<p>Met behulp van een microcontrollerboard (bv.: Arduino UNO, ESP32) en enkele elektronica componenten bouwen we een tof idee uit tot een werkend prototype. We starten met de basis, dus voorkennis is niet vereist. Elektrische schakelingen en componenten worden stap per stap verkend. We leren werken met de multimeter zodat we zelf fouten kunnen opsporen en indien nodig de fouten opsporen en oplossen. De software code om het controller bordje aan te sturen leren we ook stap per stap opbouwen. We schrijven de software code op de laptop en sturen deze dan door naar ons controllerboard.</p>
<p>Voorbeelden van enkele leuke oefeningen zijn o.a.: met enkele kleuren ledjes een patroon weergeven, de intensiteit van licht inlezen en daaraan enkele acties koppelen of met een temperatuur sensor, een transistor en de nodige software een motortje als ventilator aansturen &hellip;</p>
<p>We gebruiken voor de meeste schakelingen een breadboard (oefen prikbord), maar we leren ook kleine schakelingen solderen, om kleine herstellingen (draadje losgekomen &hellip;) te kunnen uitvoeren of om kleine proefopstellingen te kunnen maken.</p>
<p>We bouwen een eigen spelletje met knopjes en ledjes. Dit kan bijvoorbeeld een &ldquo;Simon Says&rdquo; of een &ldquo;stay-in-the-box&rdquo; game zijn. Al deze oefeningen vormen de basis om in het volgend semester sensoren met een Raspberry Pi in te kunnen lezen om verder de IoT wereld te kunnen verkennen.</p>'),
('Full Stack Web Development','Visual Studio Code, Postman',2,10,'code',NULL,'<p><strong>In deze module kan je leren hoe je een volledig API-driven website kan maken en van A tot Z coderen.
Omdat je als bachelor MCT kan kiezen voor de specialisatie Next Web Developer moet je in staat zijn om volledige (full stack) websites te bouwen.</strong></p>
<p>In deze module maken wij vanaf het begin een duidelijke splitsing tussen de kant van de website die voor de gebruiker bestemd is (de frontend) en de kant waar de gegevens opgehaald en verwerkt worden (de backend).</p>
<p>Om deze beide zijdes te kunnen programmeren of te scripten maken we gebruik van twee programmeertalen: Javascript voor de frontend ontwikkeling en Python voor de backend ontwikkeling.</p>
<p>Het uitzicht van de website bepalen en ontwikkelen enerzijds en hoe je databanken manipuleert anderzijds zal je aanleren in de modules <a href="/programma/user-interface-design">User Interface Design</a> en <a href="/programma/datamanagement">Datamanagement</a><!-- raw HTML omitted -->.</p>
<p>Het ultieme doel van deze module is ervoor zorgen dat er een real-time tweewegs-communicatie ontstaat tussen sensoren en actuatoren op je Raspberry Pi en je zelfgemaakte website.</p>'),
('User Interface Design','Adobe XD, Photoshop en Atom',2,20,'design',NULL,'<p>Een goede User Interface draagt bij tot een betere <!-- raw HTML omitted -->User experience<!-- raw HTML omitted -->.
In deze module leer je hoe je de principes van visual design zoals typgrafie, kleur, layout en vertical rhythm kan toepassen om een aantrekkelijke, uitnodigende en gebruiksvriendelijke interface te ontwerpen.
Je leert werken met <strong>Adobe XD</strong> om interfaces te ontwerpen. <strong>Photoshop</strong> gebruiken we om foto&rsquo;s te bewerken en assets aan te maken.</p>
<p>User Interface design is niet enkel in een grafische tool schermen uitwerken. Voor het web zijn er tal van design beslissingen die je veel beter kan nemen rechtstreeks in de natuurlijke omgeving van het web: de browser. Responsive webdesign, hover effecten, kleine animaties… allemaal zaken die je het best kan doen met <strong>CSS</strong>. Daarom leren we in deze module al snel hoe je de principes van visual design kan toepassen met CSS. Je leert werken met de handige text editor <strong>Atom</strong>.</p>
<p>Op het einde zien we hoe we <strong>Javascript en CSS</strong> kunnen combineren om kleine interacties zoals een mobiele navigatie mogelijk te maken. Javascript leer je in <a href="/programma/full-stack-web-development">Full Stack Web Development</a>.</p>'),
('Sensors & Interfacing','Arduino, ESP32, Raspberry Pi, I2C, SPI Bus, One-Wire',2,30,'connect',NULL,'<p>Met behulp van een single board computer (bv.: Raspberry Pi) en enkele elektronica componenten en sensoren verkennen we verschillende protocollen om data uit te wisselen tussen verschillende devices. We leren werken met seriële protocollen, <strong>I2C bussen</strong>, de <strong>SPI bus</strong>, de <strong>One-Wire bus</strong> en andere seriële en parallelle communicatie tussen componenten onderling of naar de buitenwereld. We gebruiken daarvoor onder andere displays, sensoren (temperatuur, licht, acceleratormeter &hellip;), microcontrollers, motoren &hellip;</p>
<p>We bespreken ook <strong>dataoverdracht</strong> en <strong>datacompressie</strong>, om op een snelle, efficiënte en veilige manier data van het ene toestel naar het andere toestel over te brengen. Communicatie door de lucht of toch over een kabel? Wat zijn de voor- en nadelen en waar moeten we rekening mee houden?</p>
<p>We leren ook werken met <strong>bits</strong>, <strong>bytes</strong> en <strong>bit-operatoren</strong>. Een bit uit een byte halen? Enkele bits samenvoegen tot een byte? Na deze lessen spelen we daar mee, zodat je vlot allerlei controllers en boards kan aansturen. Data uit bijvoorbeeld een game controller ontleden heeft geen enkel geheim meer voor jou.</p>
<p>Dit alles komt dan later terug in het opleidingsprogramma, o.a. in de project modules. In die modules kan je dan de aangeleerde communicatie, software en componenten toepassen voor jouw eigen of een door een klant gevraagd project.</p>'),
('Datamanagement','MySQL Workbench',2,40,'analysis',NULL,'<p>Data en databases zijn niet weg te denken uit onze hedendaagse leefwereld. Je leert het juiste <strong>databasemanagementsysteem</strong> (DBMS) te kiezen. Meeste aandacht gaat hierbij naar <strong>relationele databases</strong> om een <strong>genormaliseerd model</strong> te bouwen met <strong>T-SQL</strong>.</p>
<p>Je <strong>manipuleert</strong> en <strong>bevraagt</strong> de <strong>gestockeerde data</strong>. Je programmeert <strong>procedurele databaseobjecten</strong> om <strong>beveiliging</strong>, <strong>onderhoud</strong> en <strong>foutcontrole</strong> te <strong>optimaliseren</strong>.</p>'),
('Project One','Raspberry Pi, Webserver, Database, 3D-printer, Lasercutting, Toggl',2,50,'project',NULL,'<p><strong>Project One</strong> is je <strong>eerste integratiemodule</strong>: je bewijst door <strong>zelfstandig</strong> (waterfall) binnen de gegeven richtlijnen (maar met veel ruimte voor je eigen creatieve invulling) een persoonlijke case volledig uit te werken, te documenteren en te presenteren tijdens de projectweken. Je verdiept hiermee je eerder verworven technische competenties en bewijst je <strong>project skills</strong>: (Project Management, TimeManagement, leren reflecteren, product prototyping technieken, presentatietechnieken &hellip; ) die je in verschillende sessies met medewerking van gastsprekers uit de industrie hebt aangeleerd gekregen.</p>
<p>De module Project One scherpt je schriftelijke communicatie aan, biedt een inleidende sessie over leren presenteren en leert je op een kritische manier omgaan met bronnen.
Behoorlijk wat aandacht gaat ook naar leren reflecteren: naast de basics leer je meer over het hoe en waarom van reflecteren van professionals uit the field; stagegevers en alumni komen graag getuigen over ze groeien als professional door stil te staan bij wat goed werkte en wat misschien wat minder goed ging.</p>
<p>Een viertal sessies gaat naar maker skills: je wil je projectwerk immers ook graag een functionele behuizing geven. Op een pragmatische manier komen 3D printing, lasercutting, basis verbindingstechnieken en andere vaardigheden aan bod die je in staat stellen om in een makerspace (Bv. in Budafabriek) of Industrial Design Center (IDC) zonder koudwatervrees aan de slag te gaan.</p>
<p>Benieuwd naar wat je voorgangers al hebben gemaakt? Aan het eind van de projectweken is er een toonmoment voor mensen uit de industrie.
Bekijk zeker ons <a href="https://www.youtube.com/channel/UC6lyX8GadHRNPo7FTzrQtow">Youtube kanaal</a> om meer filmpjes te zien van de projecten, en laat je inspireren! <a href="https://www.youtube.com/watch?v=bsGKQyBfyUs">In dit filmpje</a> zie je hoe je een boekenkast slim kan maken!</p>'),
('Device Programming','Xamarin.Forms, .NET MAUI, Visual Studio',3,10,'code',NULL,'<p>Het doel van deze module is om <strong>C#.NET</strong> te leren en de concepten van <strong>object georiënteerd programmeren</strong> verder uit te diepen. Deze kennis wordt ingezet om mobiele Xamarin.Forms/.NET MAUI applicaties te ontwikkelen die data manipuleren van bestaande <strong>bronnen in de cloud</strong>. Hoewel Xamarin.Forms/.NET MAUI toelaat op verschillende platformen te draaien, ligt de focus van het testen voornamelijk op Android.
Deze module bouwt verder op de kennis die opgedaan werd in <a href="/programma/user-experience-design">User Experience Design</a>, <a href="/programma/basic-programming">Basic Programming</a> en <a href="/programma/full-stack-web-development">Full Stack Web Development</a>, en <strong>loopt parallel met de module <a href="/programma/iot-cloud/">IoT Cloud</a></strong>. Naast het verder uitdiepen van programmeerprincipes die toegepast kunnen worden in alle specialisaties, bereidt het tevens voor op meer specifieke modules zoals <strong><a href="/programma/smart-app-development">Smart App Development</a></strong>, <strong><a href="/programma/backend-development">Backend Development</a></strong> en <strong><a href="/programma/mixed-reality">Mixed Reality</a></strong></p>
<p>Algemene doelen voor deze module:</p>
<ul>
<li>Je zal de kennis die je opgedaan hebt in Basic Programming (object geörienteerd programmeren in <strong>Python</strong>) kunnen omzetten naar <strong>C#.NET (Xamarin/.NET MAUI)</strong>, aangevuld door <strong>extra concepten</strong> van <strong>object geörienteerd programmeren</strong>.</li>
<li>Je zal weten waar Xamarin/.NET MAUI gesitueerd wordt in het <strong>.NET landschap</strong>, en wat het <strong>basis verschil</strong> is tussen Xamarin.Forms en .NET MAUI.</li>
<li>Je zal <strong>data asynchroon kunnen lezen en/of manipuleren</strong>, door bestaande <strong>data sources</strong> in de <strong>cloud</strong> te gebruiken die data in <strong>verschillende formaten</strong> kunnen aanleveren (zoals CSV, JSON).</li>
<li>Je zal <strong>sneller en efficiënter</strong> leren coderen door gebruik te maken van specifieke principes in zowel <strong>C# .NET</strong> als <strong>Visual Studio</strong>. Deze tool zal je ook helpen om je code efficienter te leren <strong>debuggen</strong>.</li>
<li>Je doet een basis kennis op van <strong>XAML</strong> in <strong>Xamarin Forms/.NET MAUI</strong> zodat je in staat bent om een gebruiksvriendelijke UI te bouwen met <strong>controls en containers</strong> die best passend zijn voor de applicatie. Ook het <strong>navigatiesysteem</strong> komt aan bod.</li>
<li>Je leert <strong>platform specifieke code en XAML</strong> schrijven in <strong>Xamarin Forms en .NET MAUI (Android, iOS, UWP)</strong>.</li>
</ul>'),
('Interaction Design','Adobe',3,20,'design',NULL,'<p>In deze module integreren we kennis uit het eerste jaar (<a href="/programma/full-stack-web-development">Full Stack Web Development</a>, <a href="/programma/user-experience-design/">User Experience Design</a> en <a href="/programma/user-interface-design/">User Interface Design</a>) tot een goed werkend geheel. De focus van de module ligt op het creeëren van een functioneel design met een goede interactie. Van <strong>microinteracties</strong> tot een goed overzicht in een <strong>dashboard</strong> wordt bekeken hoe je jouw applicatie beter kan maken. We grijpen ook nog even terug naar de UX basis en kijken hoe je door details de interactie tussen jouw applicatie en de gebruikers nog beter kan maken!</p>
<p>Technisch werken we met HTML, CSS en JS om vorm te geven aan de ideeën en keuzes die we maken voor ons ontwerp.</p>'),
('Security','Kali, Wireshark, OWASP ZAP',3,30,'connect',NULL,'<p>Studenten worden bewust gemaakt van de mogelijke bedreigingen die de <strong>beschikbaarheid</strong>, de <strong>vertrouwelijkheid</strong> of de <strong>integriteit</strong> van een systeem <strong>kunnen compromitteren</strong>
Er worden diverse tegenmaatregelen besproken die de kwetsbaarheid tegenover deze bedreigingen kunnen verminderen of minimaliseren.</p>
<p>Aan de hand van <strong>praktische voorbeelden</strong> wordt getracht een inzicht te verwerven in het <strong>brede en complexe veld van de ICT-beveiliging</strong>, zowel op het gebied van WEB-technologie, netwerk-infrastructuur, hardware en software applicaties. In het bijzonder daar waar deze technologieën worden geïntegreerd <strong>in moderne Cloud en IoT toepassingen</strong>.<br>
Er wordt een zeer summiere inleiding gegeven in de bestaande methodieken en in de ter zake doende wetgeving.</p>
<p><strong>Praktische labo-sessies</strong> laten de studenten zelf aan de slag gaan met een aantal tools om de <strong>effectiviteit van beveiligingen</strong> te <strong>testen</strong>. Een opgezette afgeschermde omgeving laat de studenten toe zelf een aantal <strong>kwetsbaarheden in applicaties uit te buiten</strong> zodat men zich een goed beeld kan vormen van de impact van het falen van een beveiliging.</p>'),
('IoT Cloud','Azure Portal, Azure IoT-Hub',3,40,'analysis',NULL,'<p>IoT zonder cloud is onmogelijk. Deze module bevat 3 grote delen. We gaan dieper in op opslag van data in de cloud. Daarnaast is , connectiviteit  van de devices naar de cloud zeer belangrijk. Als laatste moeten we de devices voorzien van de nodige software. Om dit alles te realiseren maken we gebruik van de <strong>Microsoft Azure Cloud</strong>. We schrijven onze eerste <strong>webservices</strong>. De <strong>hosting van de services</strong> zal gebeuren <strong>via het Serverless Platform van Azure</strong>, namelijk <strong>Azure Functions</strong>. Voor het opslaan van data maken we zowel gebruik van relationele opslag als nosql opslag. Relatione opslag van data zal gebeuren in de cloud via Azure SQL Database. Als het gaat om Nosql opslag kiezen we voor Azure Cosmos DB. Naast het opslaan van data leren we ook hoe we devices kunnen connecteren aan het Internet. Met behulp van de Raspberry Pi gaan we berichten versturen naar de Cloud. Daarnaast moeten we ook berichten ontvangen uit de Cloud. Voor beide scenario’s maken we gebruik van <strong>Azure IoT Hub</strong> en <strong>MQTT</strong>. Deze managed services zal een full end to end secure verbinding opzetten waarover we berichten kunnen versturen. Als laatste zien we <strong>Azure IoT Edge</strong>. Deze oplossing laat ons toe om op een beheer  manier software te deployen naar toestellen zoals de Raspberry Pi. Cruciaal is hier het gebruik van Docker</p>'),
('Team Project','Trello, Toggl',3,50,'project',NULL,'<p>Na alle modules en examens uit Semester 3 (<a href="/programma/device-programming">Device Programming</a>, <a href="/programma/security">Security</a>, <a href="/programma/iot-cloud">IoT Cloud</a> en <a href="/programma/interaction-design">Interaction Design</a>), volgt het Team Project, een traject van 3 à 4 weken. De opgedane kennis uit de vorige modules wordt tijdens deze projectweken in de praktijk omgezet in een <strong>interne case</strong>.</p>
<p>Het voornaamste doel van deze module is om de <strong>rollen &amp; werkmethodes</strong> in <strong>projectmanagement</strong> te leren kennen en deze ook te integreren in een <strong>project van begin tot einde</strong>. Deze case wordt binnen een <strong>team</strong> uitgewerkt en gepresenteerd.</p>
<p>Aan de hand van de <strong>agile methode</strong>, leer je voor het eerst samenwerken en communiceren in een team en met interne klanten van een andere opleiding (<strong>Sport en Bewegen</strong>). Elke week presenteer je een stand van zaken bij de docenten en word je gecoacht om het project bij te sturen en tot een goed einde te brengen.</p>'),
('Backend Development','Visual Studio Code, .NET Core, MongoDB, Docker, Azure',4,10,'code',2,'<p>Hoe bouw je een API die je host in een public cloud plaform zoals Azure, AWS of GCP en dit met behulp van ASP.NET Core Web API</p>
<p>In deze module gaan we dieper in op de ontwikkeling van <strong>API&rsquo;s</strong> die gebruikt worden door frontend applicaties of later in een <strong>microservice architectuur</strong>. We starten met het opzetten van een basis API in ASP.NET Core Web API met behulp van C#. Daarna bouwen we stap voor stap verder en gaan we dieper in op zaken zoals <strong>Entity Framework</strong>, <strong>Unit Testing</strong>, <strong>Integration Testing</strong>. We leren ook hoe we applicatie hosten in <strong>Docker</strong> omgevingen. Op deze manier kan de student de module volgen zowel op Windows, Linux als Mac en kunnen de gemaakte containers op elk platform gehost worden.</p>'),
('Network Infrastructure','Cisco, HP, CCNA',4,10,'connect',4,'<p>Je hebt gekozen voor het afstudeerprofiel &lsquo;IoT Infrastructure Engineer&rsquo;. Hier zetten we bedrijfsnetwerken op in het klein, ondersteund met algemene theorie:</p>
<ul>
<li>IP subnetting</li>
<li>DNS</li>
<li>DHCP</li>
<li>NAT</li>
<li>Port Forwarding</li>
<li>VPN</li>
<li>bekabeling</li>
<li>troubleshooting, &hellip;</li>
</ul>
<p>Dit kan je opnieuw toepassen in de <a href="/programma/windows-os/">Windows OS</a> en de <a href="/programma/linux-os">Linux OS</a> modules. Je gaat aan de slag met professioneel netwerkmateriaal (Cisco, HP, &hellip;) In het labo wordt real-life netwerken opgezet met de meest gebruikte netwerktechnologiën (VLANs, static &amp; dynamic routing, QOS, VoIP, …) Je legt de module 1 &amp; 2 van <strong>Cisco Certified Network Associate</strong> (CCNA) op eigen tempo af (= deelnamecertificaten). <strong>Hands-on</strong> is het sleutelwoord!</p>'),
('Unity','Unity',4,10,'code',1,'<p>Een Extended Reality applicatie bouwen begint bij het ontwikkelen van een programma.
Met behulp van Unity, een 3D engine, maken we krachtige applicaties die in staat zijn om 3D assets en animaties weer te geven.</p>
<p>In deze samenwerking met Digital Arts &amp; Entertainment (DAE) worden jullie klaargestoomd om te werken met de technologie achter tal van games.</p>'),
('3D1','Maya, Blender',4,20,'design',1,'<p><strong>Onder voorbehoud</strong></p>
<p>In de module 3D1 werken we samen met de opleiding Digital Arts &amp; Entertainment (DAE).
We leren de basis concepten van 3D design om assets te ontwikkelen en aan te passen naar wens.</p>
<p>Op het einde van het semester ben je in staat om zelfgemaakte assets vorm te geven en naar jouw hand te zetten.
Zo bouw je mee aan de 3D-modellen voor je eigen Extended Reality applicaties.</p>'),
('Advanced Programming & Maths','Python, Matplotlib, Pandas, Numpy, SciPy',4,20,'analysis',3,'<p>Deze module ondersteunt rechtstreeks de modules <a href="/programma/machine-learning">Machine learning</a> en <a href="/programma/deep-learning/">Deep learning</a> binnen AI Engineer en <a href="/programma/iot-devices-robotics">IoT Devices &amp; Robotics</a> en <a href="/programma/unity">Unity</a> voor de Smart XR Developers. Beide tracks zijn immers gebouwd op de programmering van afleidende logica-systemen en systemen voor kansberekening en statistiek. &ldquo;Intelligente&rdquo; algoritmes zijn in staat om van enorme hoeveelheden input te leren en dit om te zetten naar praktische output, al dan niet naar aanleiding van een nieuwe specifieke dataset die verbonden moet worden aan een bepaalde output. Dergelijke algoritmes kunnen zo uiteindelijk voorspellingen doen of beslissingen nemen, gebaseerd op de verzamelde data en de analyse hiervan.</p>
<p>In deze module verdiepen we onze programmeervaardigheden in Python met <strong>threading/networking</strong>. We verkennen verschillende belangrijke library’s zoals Pandas, Matplot, SciPy, Numpy &hellip; Deze Python pakketten maken van de simpele programmeertaal een krachtig gereedschap voor het maken van software voor data analyse en -verwerking. We verkennen reïnforcement learning en bijhorende algoritmes.
Tegelijkertijd worden volgende wiskunde onderdelen aangeleerd zoals:</p>
<ul>
<li>Herkennen van basis wiskunde functies (<strong>gaussian function</strong>, de <strong>sigmoid</strong> function, <strong>cross-entropy</strong>, etc)</li>
<li>Werken met exponenten en logaritmes</li>
<li>Rekenen met matrices</li>
<li>Kansenberekening om finaal tot de stelling van Bayes praktisch toe te gaan passen</li>
<li>Convoluties</li>
<li>&hellip;</li>
</ul>
<p>Doorheen de module is er veel tijd om alle onderdelen begeleid zelf in te oefenen.</p>'),
('Big Data','Elasticsearch, Kafka, InfluxDB, AWS, MySQL, PySpark',4,20,'analysis',3,'<p>Met <strong>IoT sensor data</strong> problemen voorspellen, transacties op een veilige manier laten gebeuren of met text search intelligent informatie ophalen: <strong>data intensieve applicaties steunen op een complexe data architectuur!</strong> Je duikt diept in schema flexibility, isolation levels, index structures, partitioning en nog veel meer zodat je gefundeerde keuzes kan maken als data architect. Je zal begrijpen dat het <strong>CAP Theoreum</strong> (Consistency, Availability and Partioning, choose 2) een sterke vereenvoudiging is. Je leert hoe je (architecturale) keuzes van databaseontwikkelaars kan doorgronden en hoe je deze kan gebruiken voor jouw applicatie.</p>
<p>Je slaat je data op in een relationele database, time series database of document store. We gaan aan de slag met o.a. de <strong>relationele database MySQL, de time series database InfluxDB en het gedistribueerde Elasticsearch</strong>, dat je zowel voor search, document store, analytics als geospatiale data kan inzetten. Steevast werken we met <strong>Docker</strong>, dit is nu eenmaal de snelste en populairste containertechnolgie om met complexe (Big Data) softwarearchitecturen aan de slag te gaan!</p>
<p>Deze uitdagende module bouwt eveneens de data lake die ervoor zorgt dat de machine &amp; deep learning modellen die je bouwt van data voorzien worden. Afhankelijk van de situatie bouw je een <strong>stream processing architectuur</strong> met een message queue (zoals Apache Kafka) of een batch processing met frameworks zoals Apache Hadoop of Apache Spark (PySpark). Je leert ook gebruik maken van o.a. <strong>AWS cloud services</strong> zodat je kan inschatten wanneer je beroep doet op de kracht van het Amazon of Azure cloud platform en wanneer je toch beter aan de slag gaat met open source componenten. In staat zijn hardware &amp; software keuzes te maken om een <strong>Reliable, Available, Maintainable &amp; Scalable (RAMS) data intensieve applicatie</strong> te ontwerpen is de <strong>doelstelling</strong> van deze module.</p>'),
('Linux OS','Debian GNU/Linux, Apache httpd, haproxy, bash, ssh',4,20,'connect',4,'<p>Linux is alomtegenwoordig. Alleen weten veel mensen dat niet. Gebruik je soms Facebook? Of Instagram? Of Spotify? Of Twitter? Of Android? Dan <strong>gebruik je onbewust Linux</strong>. Want al deze diensten gebruiken achterliggend Linux.</p>
<p>We starten vanaf de basis met de installatie van een linux-gebaseerd operating system. We kiezen hierbij voor <strong>Debian GNU/Linux</strong> omdat het aan de basis staat van heel vele andere bekende linux distributies zoals onder andere Ubuntu, Kali Linux, Knoppix, Element en Linux Mint.</p>
<p>Je leert er je weg vinden in een Linux-gebaseerd Operating System, basis beheerstaken uitvoeren, servers opzetten, een volwaardig Linux-gebaseerd netwerk uitbouwen &hellip;</p>
<p>Je leert er over backup, over <strong>loadbalancing</strong>, over <strong>high availability</strong>, over <strong>monitoring</strong>, etc. Ook is er veel ruimte voor vragen en eigen inbreng om de lessen nog interessanter te maken.</p>'),
('Smart App Development','Expo, webpack, JS, ReactNative, Lottie',4,20,'code',2,'<p><strong>Smart App Development — Hoe maken we performante en mooie apps die een zo veel mogelijk gedeelde codebase hebben tussen iOS &amp; Android?</strong></p>
<p>We bekijken hoe we met React Native een hybride mobile app kunnen maken met een zo veel mogelijk shared codebase. Aan de hand van Expo zetten we een vlotte development structuur op. We bekijken welke device-API&rsquo;s we kunnen gebruiken, hoe we met data werken en hoe we platform specifieke logica toevoegen.</p>
<p>Ook komen animaties aan bod, basis microinteracties en het gestructureerd werken met Javascript.</p>
<p>Deze module is ook een aanzet naar de web-based <a href="/programma/advanced-full-stack-development/">JS-frameworks en patterns</a>.</p>'),
('Virtualisation & Cloud Computing Infrastructure','VMware, HyperV, Docker, KVM',4,30,'connect',4,'<p>In datacenteromgevingen is virtualisatie niet meer weg te denken. Door de <strong>verlaging</strong> van de <strong>Total Cost of Ownership</strong> (TCO), de <strong>verhoging van de schaalbaarheid</strong>, de <strong>verbetering van de beschikbaarheid</strong>, en het <strong>vereenvoudigen van complexe beheerstaken</strong> overtreffen gevirtualiseerde infrastructuren de klassieke modellen in vrijwel elk opzicht. In deze module maken we jou vertrouwd met de concepten en technologieën die gebruikt worden in <strong>moderne geconvergeerde en geïntegreerde datacenters</strong>.</p>
<p>De basistaken die noodzakelijk zijn voor het opzetten en beheren van een infrastructuur op basis van <strong>VMware vSphere, Microsoft HyperV</strong> en <strong>KVM</strong> worden praktisch ingeoefend. Het uitrollen en beheren van applicaties met behulp van op containers gebaseerde virtualisatie technieken zoals <strong>LXC</strong> en <strong>Docker</strong> komt tevens aan bod.</p>'),
('Applied AI','Python, Jupyter Notebook',4,40,'analysis',1,'<p>Artificiële intelligentie (AI) is een onderwerp dat momenteel sterk tot de verbeelding spreekt. <strong>Zelfrijdende auto&rsquo;s</strong>, interactie met robots en slimme camera&rsquo;s zijn maar enkele van de mogelijke toepassingen van AI. Ook als Smart XR Developer is het belangrijk dat je in staat bent om een applicatie te verrijken met AI. Zo maak je jouw extended reality apps nog <strong>slimmer</strong>, waardoor het gemakkelijker is om in te spelen op wat de gebruiker wilt.</p>
<p>In deze module maak je kennis met de basis van AI en Machine Learning, waarna je dieper in gaat op thema&rsquo;s zoals data labeling, classificatie, object detectie, segmentatie en <strong>spraaktechnologie</strong>.</p>
<p>In deze module krijg je een overzicht krijgt van wat AI is en hoe je dit efficiënt en praktisch kan toepassen in jouw applicaties.</p>'),
('Machine Learning','Support Vector Machines, Random Forest Trees, Naive Bayes, Logistic Regression, Ensemble Learning',4,40,'analysis',3,'<p>IoT en machine learning zijn de drijvende krachten van de vierde industriële revolutie die de wereld zoals we deze nu kennen <strong>in een razend tempo transformeert</strong>. Dit zal onvermijdelijk leiden tot een (aard)verschuiving op de arbeidsmarkt.</p>
<p>Veel (repetitieve jobs) zullen door AI-toepassingen worden overgenomen.</p>
<p>Echter zullen er enorme <strong>opportuniteiten</strong> zijn voor IT’ers met kennis van machine learning die slimme algoritmes en system kunnen integreren.</p>
<p>Er wordt vooral nadruk gelegd op het <strong>conceptueel begrijpen van hoe bepaalde algoritmes werken</strong>. Belangrijk is om de <strong>juiste machine learning algoritmes te kunnen kiezen, trainen, correct evalueren</strong> en de prestaties ervan te verbeteren via <strong>hyperparameter tuning</strong>. We bekijken de meest courante machine learning technieken waarmee je in de praktijk onmiddellijk aan de slag kunt:</p>
<ol>
<li>Supervised learning waarbij je leert uit gelabelde data:
<ul>
<li>Lineaire (meervoudige) regressie waarmee je continue outputs kunt voorspellen. Voorbeelden zijn het voorspellen van beurskoersen, het schatten van de leeftijd van een persoon op basis van een foto van het gezicht, risico’s voorspellen, predicties doen van verkoopsaantallen, etc.</li>
<li>Classificatie laat je toe om data in categorieën onder te verdelen. Gezichtsherkenning, handschriftherkenning, kankerdetectie, voorspellen of iemand op een advertentie of link zal klikken zijn maar enkele voorbeelden. Topics en algoritmes die aan bod komen zijn <strong>logistic regression, Support Vector Machines, Naive Bayes, Random Forest Trees en Ensemble learning</strong>.</li>
</ul>
</li>
<li>Unsupervised learning waarbij je informatie haalt uit niet gelabelde data.
<ul>
<li><strong>Clustering technieken</strong> waarbij je op zoek gaat naar gelijksoortige data. Op deze manier kan je patronen, verbanden en gelijkenissen ontdekken in complexe multi-dimensionele data.</li>
<li><strong>Dimensionality reduction</strong> laat ons toe om data te transformeren naar de essentie. Zo kan data compacter voorgesteld worden of kan de performantie van machine learning voorspellingstechnieken verhoogd worden.</li>
</ul>
</li>
<li><strong>Neurale netwerken</strong>, geïnspireerd op de werking van de hersenen laten ons toe om inzichten uit data te halen die tot voor kort niet mogelijk maken. In de module machine learning bekijken we de conceptuele werking ervan en bouwen we neurale netwerken voor regressie en classificatie. Daarmee wordt de basis gelegd voor de module deep learning die hier verder op bouwt.</li>
</ol>
<p>Vandaag de dag al zijn <strong>data scientists en AI experts bij de meest gegeerde profielen op de arbeidsmarkt</strong>. De meest succesvolle bedrijven ter wereld zijn dikwijls degene die ook koploper zijn op het vlak van data science en artificiële intelligentie. Denk maar aan Google en Facebook die gebruikersprofielen analyseren en advertenties op maat aanbieden, Tesla die aan de hand van sensordata hun wagens zelfrijdend maakt, luchtvaarmaatschappijen die optimale vliegroutes uitstippelen, banken die beurskoersen voorspellen, risico’s inschatten of fraude detecteren.</p>
<p>In deze module leer je de <strong>concepten</strong> van een aantal <strong>machine learning algoritmes</strong> en vooral hoe je ze <strong>praktisch</strong> kunt <strong>toepassen</strong> om ML problemen op te lossen.</p>
<p>Tevens wordt de basis gelegd voor de module <a href="/programma/deep-learning/">Deep Learning</a> die hierop aansluit.</p>'),
('Motion Design','Adobe After Effects, Lottie',4,40,'design',2,'<p>Naast een goede User Interface (UI), is <strong>User Experience</strong> (UX) misschien wel het belangrijkste onderdeel van een web, app of andere interface. Om een succesvolle UX te garanderen hanteren we binnen deze module <strong>motion design</strong>. Dat helpt de gebruiker onder andere bij het navigeren: via kleine onderdelen van je UI te animeren wordt de aandacht getrokken. Deze <strong>subtiele animaties</strong> helpen bij de oriëntatie op je platform. Zo wordt de gebruiker naar de juiste plaats op de site of app begeleid.
Daarnaast kan motion design ook dienen om een <strong>actie te bevestigen</strong>. Een gebruiker krijgt feedback na een klik, scroll, upload of na het verzenden van een e-mail. Dat gaat over <strong>micro-animaties</strong>, met een simpele maar effectieve respons.
Tot slot kan motion design ook een meerwaarde zijn voor de esthetische functionaliteit van een website of applicatie. Een micro-animatie die goed getimed is, kan bijdragen tot een <strong>aangename ervaring</strong> op je platform. Denk bijvoorbeeld aan een leuke animatie in plaats van een klassiek laadicoontje tijdens het wachten. Zo is de gebruiker geneigd om je web / app sneller opnieuw te gebruiken.</p>'),
('Windows OS','Microsoft Windows Server 2019, Active Directory',4,40,'connect',4,'<p>In heel veel bedrijven wordt <strong>Microsoft Windows Server 2019</strong> gebruikt voor authenticatie en het beveiligen van resources. <strong>Active Directory</strong> is één van de pijlers. Je krijgt een volledige virtuele omgeving ter beschikking (zelfs van thuis/kot bereikbaar) om een Windows gebaseerd KMO netwerk op te zetten. Aan de hand van een ‘best practice’ ben je in staat snel een goed beveiligde omgeving op te zetten. Op basis van heel wat praktijkervaring werden deze best practices samengesteld. Opnieuw wordt de labo-inhoud gerealiseerd op basis van <strong>tal van praktijkvoorbeelden</strong>.</p>'),
('Industry Project',NULL,4,50,'project',NULL,'<p><strong>Na alle modules en examens uit Semester 4, volgt het Industry Project, een traject van 4 à 5 weken. De opgedane kennis uit de vorige modules wordt tijdens deze projectweken in de praktijk omgezet in een externe case.</strong></p>
<p>Deze module werkt verder op de <a href="/programma/team-project">Team Project</a> module. In deze module zal er een project uitgewerkt worden voor een <strong>bedrijf</strong>. Hierbij worden alle rollen en werkmethodes in projectmanagement vlot toegepast. De druk en verwachtingen liggen hier een stuk hoger. Hierbij is een goede communicatie met <strong>externe partijen</strong> dus van groot belang. De projecten situeren zich in de context van <strong>web development</strong>, <strong>AI &amp; machine learning</strong>, <strong>XR Development</strong> en <strong>infrastructure</strong>.</p>
<p>Bedrijven waar we reeds mee samenwerken zijn onder andere <a href="https://www.tvh.com">TVH</a>, <a href="https://www.smappee.com">Smappee</a>, <a href="https://www.barco.com">Barco</a>, [Ordina](<a href="https://www.ordina.be/">https://www.ordina.be/</a>, <a href="https://www.kinepolis.com">Kinepolis</a>, <a href="https://www.delaware.pro">Delaware</a>.</p>'),
('Cloud Services','File storage, Object storage, Docker, VPC, DDoS',5,10,'connect',4,'<p>Cloud Computing is niet meer hip, Cloud Computing is gemeengoed. Daarom is het niet meer dan logisch dat we in MCT aan de slag gaan met <strong>de twee grootste public cloud platformen: Amazon Web Services (AWS) en Microsoft Azure</strong>.</p>
<p>We gaan van start met Microsoft Azure. We analyseren hoe Microsoft hun datacenters over de wereld verspreid heeft, hoe ze de connectiviteit tussen de datacenters inrichten en hoe wij daar optimaal gebruik kunnen van maken. We <strong>leren hoe storage in de hyper-cloud omgeving van Azure</strong> opgezet is en hoe die te gebruiken. Wanneer je diensten afneemt uit de public cloud, ben je erg afhankelijk van de netwerkverbinding naar deze diensten en tussen de diensten onderling. Daarom gaan we dieper in op <strong>Azure networking</strong>.</p>
<p>In de tweede helft van deze module gaan we aan de slag met die ander grote public cloud: Amazon Web Services. We analyseren dezelfde onderwerpen die we bij Azure hebben gekeken, maar ditmaal in AWS: <strong>datacenter opbouw, storage, networking, IaaS</strong>.</p>
<p>De wekelijkse lessen zijn opgebouwd uit een stuk theorie en een groot stuk labo. We vinden het <strong>in onze praktijkgerichte opleiding belangrijk om vooral hands-on aan de slag te gaan</strong>.</p>'),
('Experimental XR',NULL,5,10,'code',1,'<p><strong>Onder voorbehoud</strong></p>
<p>Extended Reality applicaties gaan koppelen aan menselijke interactie ? Het kan!
In deze module experimenteren we met de mogelijkheden van Eye-tracking devices en hersengolf activiteiten.</p>
<p>Met tal van sensoren meten we de gemoedstoestand van een gebruiker, en passen hiervoor onze applicatie live aan.
Door middel van data verzameling en AI capteren we deze gegevens en leren we wat onze applicatie met een gebruiker doet.</p>
<p>Deze unieke samenwerking van IoT devices, Mixed en Augmented Reality interfaces maakt ons een echte Smart XR Developer.</p>'),
('Future Technologies','Cool new technologies!',5,10,'code',2,'<p>In deze modules dompelen we je onder in de nieuwste en relevantste cutting edge technologie. We beginnen het semester met wekelijkse sessies van gast-sprekers uit het werkveld en lectoren. Vanuit deze inspiratie en technische kennis werk je in groep of individueel aan een veelbelovende technologie die nog in de kinderschoenen staat. Op deze manier kom jij straks als expert in het werkveld terecht.</p>'),
('MLOps','Azure ML, Vertex AI, GitHub Actions, Kubernetes, Kubeflow',5,10,'code',3,'<p>In de module MLOps leren we AI modellen, ontwikkeld in <a href="/programma/deep-learning/">Deep Learning</a> en <a href="/programma/advanced-ai/">Advanced AI</a>, in productie te brengen.
Getrainde AI modellen moeten namelijk uit de ontwikkelingsfase richting een productie omgeving komen.
Ze worden in een applicatie geintegreerd op allerlei manieren. Wij leren de best practices rond deployment.
Hiervoor werken we met de laatste nieuwe technologieen op vlak van Web API&rsquo;s, Docker en Kubernetes, op cloud en lokale servers.</p>
<p>Daarnaast is het ook belangrijk dat een AI-ontwikkelaar hun modellen constant verbeteren en hertrainen.
In deze module stellen we een pipeline op die het hele trainingsproces zal automatiseren.
Aan de hand van een <strong>Continuous Integration pipeline</strong> wordt het trainingsproces deel van het deployment proces van je software applicatie.
Gebruik makend van Cloud AI oplossingen, en krachtige GPU machines is het trainingsproces nu in handen van geautomatiseerde machines.
De automatisatie gebeurt d.m.v. Python en CLI tools binnen <strong>Azure Machine Learning Service</strong> en <strong>Google Cloud Platform (Vertex AI)</strong>.</p>
<p>Met een diepgaand onderzoek naar <strong>Kubeflow en MLflow</strong>, twee bekende MLOps tools, wordt deze pipeline in een mum van tijd opgestart.
Zo wordt een volledige data pipeline, AI pipeline en deployment pipeline opgezet, beheerd en onderhouden.</p>
<p>Samenwerken in een team met een MLOps-Engineer was nog nooit zo eenvoudig!</p>'),
('Advanced Full Stack Development',NULL,5,20,'code',2,'<p>In deze module werken we aan full stack projecten die we bouwen op verschillende PaaS-oplossingen. We kijken naar de beste koppeling tussen de frontend en de backend met alle tools die momenteel interessant zijn.</p>'),
('Deep Learning','Convolutional Neural Networks (CNN), Generative Adversarial Networks (GAN), Long-Short Term Memory (LSTM), Recurrent Neural Networks (RNN)',5,20,'analysis',3,'<p><strong>Opgelet: Deze module kan je ook volgen als &lsquo;AI for Healthcare&rsquo;, een unieke samenwerking tussen Howest MCT en Howest BIT. Je leert er toegepaste praktijk toepassingen voor de medische wereld.</strong></p>
<p>De module deep learning gaat verder waar de module <a href="/programma/machine-learning/">Machine Learning</a> is gestopt, namelijk bij de neurale netwerken.</p>
<ul>
<li>Herhaling <strong>neurale netwerken</strong> en introductie tot deep learing.</li>
<li><strong>Convolutional Neural Networks (CNN)</strong> die vooral gebruikt worden bij image recogntion.</li>
<li><strong>Auto encoders en restricted Bolzmann machines</strong>: kunnen verloren of beschadigde data reconstrueren maar ook gebruikt worden om muziek te genereren of suggesties te doen.</li>
<li><strong>Generative Adversarial Networks (GAN)</strong>. Worden gebruikt voor bijvoorbeeld generatatie van afbeeldingen, voorspellen van welk geneesmiddel zal werken bij bepaalde symptomen &hellip;</li>
<li><strong>Recommendation systems</strong> voor het genereren van gepersonaliseerde aanbevelingen.</li>
<li><strong>Neurale netwerken met geheugen</strong>: Recursive Neural Networks (RNN) en Long Short-term memory networks (LSTM): toepassingen zijn bijvoorbeeld natural language processing en sentiment analysis.</li>
<li><strong>Reinforcement learning</strong>: het algoritme leert door interactie met de omgeving.</li>
</ul>'),
('Network Scripting','Powershell, Bash, Terraform, Ansible, Git, VMware',5,20,'connect',4,'<p>Om administratieve taken binnen een (netwerk)infrastructuur <strong>snel, geautomatiseerd en efficiënt</strong> te realiseren, kan je niet zonder <strong>scripting</strong>.
Configureren van DNS en DHCP, aanmaken van gebruikers en groepen, beveiligen van resources, installatie en configuratie van software, aanmaken en beheren van virtuele machines zijn maar een paar voorbeelden.</p>
<p>Je gaat aan de slag met <strong>Microsoft Windows</strong>, verschillende <strong>Linux</strong> distributies en een virtualisatieomgeving steunend op <strong>VMware</strong>. Er wordt dus zowel aandacht besteed aan commerciële evenals open source omgevingen en tools.</p>
<p>Aan het einde van deze module zou <strong>Infrastructure as Code</strong> (IaC) en <strong>Configuration as Code</strong> (CaC) geen geheimen meer voor jou mogen hebben! Hiervoor maken we gebruik van een breed scala aan oplossingen, waaronder Microsoft Powershell, Bash, Python, Terraform, Ansible, Git &hellip;</p>'),
('Advanced AI','Deep Reinforcement Learning models',5,30,'analysis',3,'<p>In deze hands-on module bestuderen en implementeren we Reinforcement Learning en Deep Reinforcement Learning systemen. In plaats van te leren uit data gaan deze zelflerende systemen aan de hand van <strong>trial &amp; error</strong> een optimale strategie zoeken die hen een maximale reward oplevert. Deze (Deep) Reinforcement Leerstrategieën vinden vooral toepassingen bij zelflerende robots, optimalisatie van industriële processen, computer games, self-driving cars en gepersonaliseerde aanbevelingen. Aanvullend gaan we dieper in op een aantal populaire optimalisatie- en simulatietechnieken die de performantie van jouw gebruikte leeralgoritme gevoelig kunnen verbeteren.</p>'),
('Mixed Reality','Unity, Vuforia, Hololens',5,30,'design',1,'<p>Het doel van deze module is om kennis te maken met Augmented Reality en Mixed Reality. Je maakt kennis met de verschillende mogelijkheden naar <strong>interactie en visualisatie</strong>. In het praktische luik van de module worden hiervoor business toepassingen uitgewerkt, in hoofdzaak a.d.h.v. <strong>Microsoft Hololens</strong> maar ook via <strong>mobile devices</strong> en alternatieven zoals <strong>MagicLeap</strong>.</p>
<p>De kennis die opgedaan werd in UX-design, UI-design en <a href="/programma/interaction-design/">Interaction Design</a> wordt aangehaald om User Experience om te zetten naar een volledig nieuwe <strong>augmented/mixed reality omgeving</strong>. Daarnaast wordt je kennis C#.NET uit de module <a href="/programma/device-programming/">Device Programming</a> ingezet voor het programmeergedeelte in <strong>Unity en UWP</strong>.</p>
<ul>
<li>Je leert de <strong>User Experience</strong> te optimaliseren voor Augmented/Mixed Reality omgevingen.</li>
<li>Je wordt ondergedompeld in de mogelijkheden die reeds op de markt zijn voor <strong>interactie en visualisatie</strong> van Augmented en Mixed Reality.</li>
<li>Het gebruik van de game engine <strong>Unity</strong> wordt verder bekeken om een 3D augmented reality omgeving op te zetten en te programmeren.</li>
</ul>'),
('New Interface Design','Wearables',5,30,'design',2,'<p>Aan de slag met nieuwe interfaces! We bouwen verder op eerdere design-modules die je al gekregen hebt in de voorgaande semesters. Alles wat je maakt kan technische nog zo goed zijn, als je geen goede UI of UX hebt, dan gaan jouw gebruikers hier niet mee aan de slag kunnen.</p>
<p>We kijken naar de nieuwe interacties tussen mensen en machines via voice, nieuwe mobile devices en met minder gangbare devices.
Je wordt ondergedompeld in de mogelijkheden die reeds op de markt zijn voor interactie en visualisatie van onder andere Augmented en Mixed Reality.</p>
<p>Deze module hangt ook nauw samen met de <a href="/programma/future-technologies">Future technologies</a> module, waar we vooral de technologie-kant bekijken.</p>'),
('IoT Devices & Robotics','InfluxDB, Grafana, MQTT, Reachy',5,40,'analysis',1,'<p>Robots bestaan al lang: zware industriële robots werden reeds geproduceerd sinds 1956. Sinds een paar jaar zijn huishoudelijke robots zoals een grasmaairobot en stofzuigerbot gemeengoed aan het worden.</p>
<p>De echte robot revolutie moet echter nog beginnen! Robots zullen enorme sprongen vooruit maken dankzij internet of things en geavanceerde AI software. Eenmaal een robot ook een &ldquo;Thing&rdquo; is dat geconnecteerd is aan het <strong>Internet of Things</strong>, kan men AI toe passen op de data geproduceerd door de sensors van duizenden robots <strong>(= Big Data)</strong>. Robots leren dus van elkaars &ldquo;ervaringen&rdquo; dankzij Internet of Things zoals wij leren van filmpjes en websites op het Web. In Sci-Fi taal: een Skynet geconnecteerde terminator leert sneller bij dan een alleenstaande voorgeprogrammeerde R2D2.</p>
<p>De huidige generatie van autonome robots kunnen dus met behulp van IoT en <strong>AI</strong> veel slimmer en flexibeler worden. En IoT-applicaties dringen ook door in industriële omgevingen. Een revolutie dat <strong>Industry 4.0</strong> wordt genoemd.</p>
<p>In de module &ldquo;IoT Devices &amp; Robotics&rdquo; wordt de huidige stand van moderne commerciële en industriële robotica verkend. Je wordt uitgedaagd een visie te ontwikkelen op de mogelijkheden van de producten van de toekomst.</p>
<p>Maar daar blijft het niet bij. In de practica ga je zelf aan de slag met bestaande robots, die je slimmer maakt en uitbreidt met baanbrekende nieuwe functionaliteiten dankzij wat je geleerd hebt in de modules <a href="/programma/iot-cloud/">IoT Cloud</a>, <a href="/programma/big-data/">Big Data</a>, <a href="/programma/machine-learning/">Machine Learning</a> en <a href="/programma/deep-learning/">Deep Learning</a> of <a href="/programma/applied-ai">Applied AI</a>.</p>
<p>Inzichten in robotica, sensoren, dataverwerking, AI en Computer vision worden aangebracht met technologieën zoals MQTT, ESP32, LoraWAN, OpenCV en Nvidia Jetson GPU processing.</p>'),
('The Collective','Miro',5,40,'project',NULL,'<p>The Collective is a module that requires <strong>international</strong> and / or <strong>interdisciplinary</strong> teamwork: you get the chance to work together with Communication Management, Occupational Therapy, Network Economy, Tourism &amp; Recreation Management, DAE and Industrial Product Design students.</p>
<p>You have already a ton of project work experience but it is a whole different ball game when you team up with people with another background. For the first time more aspects than the mere technical ones deserve your attention: finance, marketing, sales &hellip;
Sometimes these aspects will need you to kill your darling ideas(s) and move forward. Agile working will lead to success.</p>
<p>As a technical expert (IoT Infrastructure Engineer, Next Web Developer, AI Engineer or Smart XR Developer) you need to do research and work out of your comfort zone and seek for help. Luckily a multitude of people are ready to help you if you can explain what you are doing and in what manner you need their help.
You and your team are all but alone in this endeavour: experts and teacher-coaches help you all the way.</p>'),
('Research Project','IEEE, Zotero, Mendeley',5,50,'project',NULL,'<p>In deze module zal er een research project uitgewerkt worden. De projecten situeren zich in de context van <strong>web development, IoT, XR, AI en (cloud) infrastructure</strong>. Dit project vormt de basis van de bachelorproef.</p>'),
('Stage in binnen- of buitenland',NULL,6,10,'project',NULL,'<p>Als sluitstuk van de opleiding komt de <strong>reële ervaring</strong> met het <strong>werkveld</strong>: de stage. Hierbij is het de bedoeling om verschillende leerresultaten in werksituaties te gaan toepassen. Niet alleen door zijn omvang in duur en studiepunten maar ook als <strong>ideale instap in het werkveld</strong>, is de stage een <strong>ideale werkvorm</strong> om te functioneren als MCT&rsquo;er in een complexe authentieke situatie.</p>'),
('Bachelorproef',NULL,6,20,'project',NULL,'<p>De opleiding MCT wordt afgesloten met een stage in het werkveld én een individuele bachelorproef. De bachelorproef is de ideale gelegenheid voor de toekomstige bachelor om zich te verdiepen in een aantal essentiële technische competenties. Daarnaast is de bachelorproef ook de manier om heel wat algemene competenties verder te ontwikkelen. Zo dient een student</p>
<ul>
<li>in staat zijn om gedurende korte periode een specifiek aspect te onderzoeken;</li>
<li>hiervoor de nodige denk- als redeneervaardigheid aan te wenden;</li>
<li>de resultaten van zijn/haar onderzoek kritisch te bekijken;</li>
<li>gestructureerd te werk gaan;</li>
<li>de juiste conclusies uit eigen verkregen resultaten te trekken;</li>
<li>zijn bachelorproef voor een vakjury te verdedigen;</li>
<li>een attitude tot levenslang leren zich eigen maken.</li>
</ul>
<p>Hoe komt een bachelorproef tot stand?</p>
<ol>
<li>De bachelorproef vertrekt van een concrete onderzoeksvraag, al dan niet afkomstig vanuit het stagewerkveld. De opleiding bewaakt het eindniveau ervan.</li>
<li>Het onderzoek gebeurt op school: de onderzoeksvraag wordt in een afzonderlijke projectmodule (‘project 4’) in team gedurende 6 weken volledig technisch uitgewerkt. Hierbij bedenkt/creëert/onderzoekt het team studenten een eigen oplossing/ontwerp/prototype (al dan niet vooraf in specifieke richting gestuurd).</li>
<li>In de bachelorproef gaat de student individueel het behaalde resultaat aftoetsen met bedrijfswereld &amp; community.</li>
</ol>
<p>De bachelorproef moet een valorisatiewaarde/meerwaarde voor het werkveld hebben.</p>
<p>De student is projectverantwoordelijk en documenteert, rapporteert en presenteert zowel m.b.t. het proces als het product van de bachelorproef. De eindpresentatie gebeurt voor een jury (van interne en externe leden) al dan niet vakdeskundigen.</p>
<p>De bekomen technische competenties zijn afhankelijk van de gekozen onderzoeksvraag.
De bachelorproef wordt praktisch georganiseerd gedurende de stageperiode. De voorbereidingen gebeuren in het voorgaande semester.
De onderzoeksvraag wordt door het werkveld in samenwerking met het lectorenteam opgesteld.</p>')
```
:::

#### Test the relationship

When you request all the courses in the database, you will have the option to click on the `track_id` which will automatically show the result of a `SELECT` query into the Adminer GUI.
You can, of course, also write this query yourself, with a `JOIN` which we will focus on in a little bit.

### Query the information

Now that we have all of this information into our database, we can start writing our first queries.
I know that this assignment is not supposed to be a class of SQL, but I think it will help you writing the queries in Python later on.

#### Query 1. Fetching the elements which contains "Engineer" in the title.

As we currently have about 4 rows in our database, which consist of two of our tracks that contain "Engineer": `IoT Infrastructure Engineer` and `AI Engineer`.

:::warning
**TASK**
1. Write a query to fetch the two tracks, `IoT Infrastructure Engineer` and `AI Engineer`. Use `WHERE ... LIKE ...`
2. Make sure they are NOT sorted alphabetically. Use `ORDER BY`.
3. Then fetch the second element. Use `LIMIT`.
4. Hopefully, you'll get `AI Engineer`

:::success
**QUESTION**
Which query did you use to search for this item?
```sql
```
:::

#### Query 2. Fetching the track which contains the "Unity" course.

This time, we will have to write a JOIN query, where we want all the information of the track which contains the `Unity` course.

:::warning
**TASK**
Use these steps to create the query
1. Find the course named Unity.
2. Fetch **at least** the `track_id` from that Record.
3. Join the `track_id` with the `tracks` table on the common field (using the **FK** and **PK**)
4. Fetch the information you want from the `tracks` table (for example the title).

NOTE: You can use an `AS` alias when using `FROM courses AS c` so it's easier to access the table using `c.title`.
You will need to specify which `title` column you want if they exist in both 

:::success
**QUESTION**
Which query did you use to search for this item?
```sql
```
:::

:::success
**QUESTION**
We've got a small problem now, which we will not solve right away this time ...
What if we have a course that is taught in multiple tracks? Backend Development is currently taught in `Next Web Developer` as well as `AI Engineer`. (I have only specified it for one track in the dummy data) Currently, we do not allow that to happen in our database, because the `track_id` only contains one `integer`.
Any suggestions?

```text
I would suggest to ...
```
:::

#### Query 3. Counting courses

In MCT, all our courses are split up into 5 different "pillars", one of them is `Code`, where `Backend@Home` also belongs to. Our goal is to find how many of them are labelled under each of these pillars.
In the theory class we didn't discuss the methods like `Count()` and `GROUP BY` much, but you can figure it out yourselves!

:::warning
**TASK**
Use these steps to create the query which **returns the amount of courses for each pillar**.
1. Use the `Count(*)` method to return all records. Rename this column as `Number of courses`
2. Group them using the `GROUP BY` option.
3. You should have this result

![GROUP by and Count](https://i.imgur.com/gI1RWqd.png)

:::success
**QUESTION**
Which query did you use to search for this view?
```sql
```
:::

## Python connection now

Enough with writing these SQL queries manually, or using the GUI. Let's go on and connect the database using Python and FastAPI.

:::info
Before you proceed, it's important that you read this.

**Database security**

Currently, our database is open to everyone who can access our laptop's IP address. It's exposed to `localhost:3306` on our laptop. This is not the security we want eventually, but will be the easiest way to connect to the database for now.

In one of the later steps, in the things you will be able to explore yourselves, you can build a Docker Image for your API, and let Docker Compose create a Container for it, in the same Docker Network (I.e.: The same file) as the Database.
That way, you can simply use `expose` instead of `ports` and your database will not be accessible "publicly" anymore.
The only way you want to give access to the database is by exposing and letting users use the API. By doing it like this, you can add some extra authentication, authorization and security checks into your API. You'll want to remove the Adminer GUI too, then!
:::

### Preparing the Python environment

We will continue from the Python API from the previous assignments, where you already worked with the Courses and Lecturers objects. We will extend this to work with the database this time.
It's advised to create a completely new project this time, as we will gradually add some features, but the structure of our application might look different.

When it's time to copy things, I'll let you know and I'll give you some more pointers to additional features later on.

#### Installing the packages
As noted earlier on in this course, I like to use Poetry to install my packages, but if you feel more confident with other package installers, feel free to use them instead. 
The packages we need are:
- `sqlalchemy`
- `pymysql`
- `fastapi`
- `strawberry-graphql[debug-server]=0.144.3`, Currently, the latest version doesn't work well with Docker. I'll let you know when it's fixed.
- `python-dotenv` to read the environment variables from a `.env` file to fetch the database connection information.

The sub-packages `pydantic` and `uvicorn` are automatically installed as well.

Make sure to install these packages first.

#### Getting our folder structure ready

Get a basic FastAPI project running again, and create a `Router` for the `Tracks` and `Courses` objects we will be working with. Later on, we will add the Lecturers as well.

Create a `main.py` file in your top directory, if it's not already there.
(If you used `poetry new api`, it will be under `api > api`. (api is an example name!))

It's advised to create a seperate folder for both of these objects `tracks` and `course`
Inside this folder create the files:
- `router.py` which will contain all the endpoints specific for the API objects.
- `repository.py` which will contain the database request code.
- `schema.py` which will contain a code-representation of the Database Schema we will connect to.
- `models.py` which will contain all our Pydantic (Base)Models that we will use inside our Routers.
- `graphql.py` for the GraphQL Queries and Mutations we are working with.

We will go into more detail on each of these files in a bit, but you should already have most of it somewhere in your project.

**Database connection**
In order to work with our database, we will need to create a `database.py` script in our top-level directory (i.e.: Next to `main.py`).

Copy this in there, this will allow you to connect to the MySQL database from either a Docker-environment or the local-environment, depending on a variable that can be toggled.

:::info
In order for the following script to work, you need to create a `.env` file containing the same values as those you entered for the `docker-compose.yml` file.
You can also reuse the same `.env` file in the Docker Compose project.

**TASK**
1. Create a `.env` file in the directory next to your `docker-compose.yml`
2. Enter the following content:
```text
MYSQL_ROOT_PASSWORD=password
MYSQL_USER=user
MYSQL_PASSWORD=password
MYSQL_PORT=3306
MYSQL_HOST=mariadb
MYSQL_DATABASE=database
```
3. Change the `docker-compose.yml` to this:
```yaml
services:
  # mariadb database
  mariadb:
    image: mariadb:10.9.4
    # environment:
    #   MYSQL_USER: user
    #   MYSQL_PASSWORD: password
    #   MYSQL_DATABASE: database
    #   MYSQL_ROOT_PASSWORD: password
    env_file:
      - .env
      
     # Leave the rest untouched
```
:::

```python=
# database.py

import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, scoped_session

# Package is `python-dotenv`
from dotenv import load_dotenv

load_dotenv() # Make sure we have our .env values

MYSQL_USER = os.getenv('MYSQL_USER')
if (os.getenv("ENVIRONMENT") == "DOCKER"):
    MYSQL_HOST = os.getenv('MYSQL_HOST')
else:
    MYSQL_HOST = "127.0.0.1"

MYSQL_PORT = os.getenv('MYSQL_PORT')
MYSQL_DATABASE = os.getenv('MYSQL_DATABASE')
MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD')


engine = create_engine(
    f'mysql+pymysql://{MYSQL_USER}:{MYSQL_PASSWORD}@{MYSQL_HOST}:{MYSQL_PORT}/{MYSQL_DATABASE}'
)
session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine) )

db = session()
Base = declarative_base()

def start_db():
    Base.metadata.create_all(engine)
```

### Filling in the scripts now

I'll give you the examples for the scripts of the Course object, which, at first, is not going to contain a relationship with the `Tracks` object, just yet.

Our Course's Schema will look something like this. This makes sure it takes the `Base` object from the `database.py` script, and then inherits the `CourseTable()` class with that: `CourseTable(Base)`.
This is needed, so that our 

```python=
from database import Base

from sqlalchemy import Column, String, Text, Integer


class CourseTable(Base):
    __tablename__ = 'courses'

    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    tools = Column(Text)
    semester = Column(Integer)
    weight = Column(Integer)
    pillar = Column(String(255))
    track_id = Column(Integer)
    content = Column(Text)

```

Now, let's define the `models.py` in such a way that we use Pydantic with the `orm_mode` configured.

```python=
# models.py
from pydantic import BaseModel
from typing import Optional

class Course(BaseModel):
    id: Optional[int]
    title: str
    tools: Optional[str] # Nullable, so optional
    semester: int
    weight: int
    pillar: str # This can be converted to an ENUM if you want to!
    track_id: Optional[int] # Nullable, so optional Currently only one track, no list of tracks in the database!
    content: str
    
    class Config:
        orm_mode = True
```

In our `repository.py`, add the following first database operations, using SQLAlchemy:

```python=
# Repository.py
# Repository.py
from database import db
from .schema import CourseTable
from .models import Course

class CourseRepository(): # Eventually, you can create a BaseRepository and make this one inherit from that!
    
    @staticmethod
    def get_all():
        db_objects = db.query(CourseTable).all()
        return [Course(**obj) for obj in db_objects] # Convert to the Pydantic objects here
    
    @staticmethod
    def insert(new_course: Course):
        try:
            db_object = CourseTable(**new_course.dict())
            db.add(db_object)
            db.commit()
            db.refresh(db_object)
            return db_object
        except Exception as err:
            import traceback
            traceback.print_tb(err.__traceback__)
            db.rollback()
    
    # Implement these ones yourselves!
    @staticmethod
    def get_one():
        raise Exception("Not yet implemented")
        
    @staticmethod
    def update():
        raise Exception("Not yet implemented")
        
    @staticmethod
    def delete():
        raise Exception("Not yet implemented")
        
```

Finally, we need to use the database in our router endpoints...

```python
# router.py

from fastapi import APIRouter
from .repository import CourseRepository
from .models import Course
from typings import List
router = APIRouter()

# Very basic, up to you to add some more documentation to it!
@router.get("/", response_model=List[Course])
def get_all():
    # Currently there is no error handling on this API, but that's up to you!
    return CourseRepository.get_all()

# Add some more functionalities later on ...

```

#### Test if it works!
1. Link your Course Router into `main.py`
```python=
from courses.router import router as courses_router
# ...
app.include_router(courses_router, prefix="/authors")
```
2. Make sure your database is still started up.
3. Place this piece of code in the top of your `main.py` after all the other imports:
```python
import database as db
db.start_db()
```
4. Run your `main.py` using `poetry run python main.py` (or enter a `poetry shell` and simply execute `python main.py`)
Make sure your `main.py` contains this, in order to run it from terminal without any other commands.
```python
if __name__ == "__main__":
    # Run the app with uvicorn and autoreload
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
```
5. Go to your browser on [localhost:8000/docs](http://localhost:8000/docs) and test it out in the `/docs` endpoint!

### Adding the Tracks objects

:::warning
**TASK**
1. Try to copy the same functionalities for the Tracks objects now.
2. Follow these steps
    - Create the Schema
    - Create the Model
    - Create the Repository
    - Create the Router
    - Add the Router to the API in `main.py`

:::

### Defining the relation between Tracks and Courses using SQLAlchemy

In order to get the relation configured, we need to use SQLAlchemy and modify a few of our scripts.

1. `courses > schema.py`
```python
from sqlalchemy import Column, String, Text, Integer, ForeignKey
from sqlalchemy.orm import relationship
class CoursesTable(Base):
    # Keep the rest untouched
    
    # track_id = Column(Integer)
    track_id = Column(Integer, ForeignKey("tracks.id"))
    track = relationship("TracksTable", back_populates="courses")
```
2. `tracks > schema.py`
```python
from sqlalchemy.orm import relationship
class TracksTable(Base):
    # Keep the rest untouched
    
    courses = relationship("CoursesTable", back_populates="track")
```

:::danger
**NOTE**
Because of circular dependencies, we cannot import `Track` in `course > models.py` and the other way around for `Course` in `tracks > models.py`
That way, it's easier to create a different file in the top-level directory called `viewmodels.py`
:::
3. `viewmodels.py`
```python
from courses.models import Course
from tracks.models import Track
from typing import Optional, List

class CourseWithTrack(Course):
    track: Optional[Track] # Optional in case it is null...

class TrackWithCourses(Track):
    courses: Optional[List[Course]]
```
4. `course > repository.py`
    This now needs to return a `TrackWithCourses`.
```python
from viewmodels import CourseWithTrack
class CourseRepository():
    
    @staticmethod
    def get_all():
        db_objects = db.query(CoursesTable).all()
        return [CourseWithTrack.from_orm(obj) for obj in db_objects] # Convert to the Pydantic objects here
    
```
5. `track > repository.py`
    This now needs to return a `TrackWithCourses`.
```python
from viewmodels import TrackWithCourses

class TrackRepository
    @staticmethod
    def get_all():
        db_objects = db.query(TracksTable).all()
        return [TrackWithCourses.from_orm(obj) for obj in db_objects] # Convert to the Pydantic objects here
```
5. Change the `response_model` in your `router.py` files as well, for both the `tracks` as the `courses`.

### Extending the API

We are now more or less finished with the first parts of accessing databases.
There are a few things you can still work out on your own to practice some more:
- Working out the **Get One**, **Update** or **Delete** routes
- Adding GraphQL
- Adding proper error handling

All of those things can also be found in the demonstration.
Some more information is written below as well.

### Working out the Docker part
Remember that we can place our FastAPI into a Docker container?
If we do it that way, we can place the API inside the same network as the database, which will be beneficial for the communication between these microservices.
We are also preparing to place it online eventually!

:::warning
**TASK**
1. Create a `Dockerfile` in the root of your project.
2. Add the following code to it:
```dockerfile
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-alpine3.14 as build-image

# python
ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100 \
    # poetry
    # https://python-poetry.org/docs/configuration/#using-environment-variables
    POETRY_VERSION=1.1.13 \
    # make poetry install to this location
    POETRY_HOME="/opt/poetry" \
    # make poetry create the virtual environment in the project's root
    # it gets named `.venv`
    POETRY_VIRTUALENVS_IN_PROJECT=true \
    # do not ask any interactive question
    POETRY_NO_INTERACTION=1 \
    # paths
    # this is where our requirements + virtual environment will live
    PYSETUP_PATH="/opt/pysetup" \
    VENV_PATH="/opt/pysetup/.venv"

# prepend poetry and venv to path
ENV PATH="$POETRY_HOME/bin:$VENV_PATH/bin:$PATH"

WORKDIR '/app'

RUN apk add --no-cache g++ curl libffi-dev

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | python

# Copy poetry.lock* in case it doesn't exist in the repo
COPY ./pyproject.toml ./poetry.lock* /app/

RUN poetry export --without-hashes -f requirements.txt > requirements.txt \
        && pip wheel --wheel-dir=/root/wheels -r requirements.txt



FROM tiangolo/uvicorn-gunicorn-fastapi:python3.9-alpine3.14 as production-image

ENV PYTHONUNBUFFERED=1 \
    # prevents python creating .pyc files
    PYTHONDONTWRITEBYTECODE=1 \
    # pip
    PIP_NO_CACHE_DIR=off \
    PIP_DISABLE_PIP_VERSION_CHECK=on \
    PIP_DEFAULT_TIMEOUT=100

WORKDIR '/app'

COPY --from=build-image /root/wheels /root/wheels

COPY --from=build-image /app/requirements.txt ./

RUN pip install --no-index --find-links=/root/wheels -r requirements.txt

# Change this line to your own project name
COPY ./api ./

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```
3. Add the following service to the `docker-compose.yml` file.
```yaml
api:
    # Replace with the image name of your choice.
    # Follow this format: <your-username>/<your-project-name>:<tag>
    image: nathansegers/backend-at-home-04-api:latest
    build:
        context: .
        dockerfile: Dockerfile
    restart: always
    ports:
        - 8000:8000
    env_file:
        - .env
    # This should be set seperately, not in the `.env` file, because you're also using the `.env` file in local development and in your database container.
    # By adding this seperate environment variable, we define that the ENVIRONMENT we are working with is in DOCKER. This will use other settings than the local development settings.
    environment:
        ENVIRONMENT: DOCKER
```
4. Turn off your local running `python main.py` script.
5. Run `docker compose up -d --build` to build the image and start the container. 
6. Test out in your browser again if everything works as it should.
:::

## Time to add in a second database, because... why not?

So far, we have explored the possibilities of a MySQL database, which is best suited for relational objects, which is the case in this scenario where we have the Lecturers combined with the Courses.

### Explanation of the non-relational data

As an addition to our project, I want to add some more information regarding the class syllabus for a specific course.

This will be in a object called `Subject`.
As courses may cover a wide range of subjects, it may be useful to store information about these subjects in a database. One way to do this in MongoDB would be to create a collection for these `Subjects` and include a document for each Subject, with fields for the name, description, programming languages, the MCT pillar and also the courses that cover this subject.

This component may not fit well in a relational database because it does not have a strict one-to-one relationship with courses. A course may cover multiple subjects, and a subject may be covered in multiple courses. In a relational database, this type of relationship would typically be represented using a join table, which can be cumbersome to work with and may not be as efficient as using a document-based data model like MongoDB.

Additionally, storing course subjects in a MongoDB database allows for more flexible querying and updating of the data. For example, you can easily retrieve a list of all subjects covered in a particular course by querying the course subjects collection and filtering by the course id. You can also easily update a subject document to add or remove courses that cover the subject, without having to update multiple related tables.

Finally, MongoDB has the flexibility of dynamic objects. This means that you are not bound to the fixed nature of a MySQL database scheme. Some might find this rather difficult to work with, on the contrary. If you do not know the structure of your application upfront, but you already wish to retrieve some data, then MongoDB can help for that.

### Setting up MongoDB in the same Docker Compose project

:::warning
**TASK**

1. Set up a MongoDB service into docker-compose and create a new volume for it.
```yaml
mongodb:
    image: mongo:6.0 # 6.0 is currently the latest version
    restart: always
    env_file:
      - .env
    volumes:
      - mongodb:/data/db # Data storage path
```
2. Add the Mongo-express service.
```yaml
mongo-express:
    image: mongo-express:1.0.0-alpha.4
    restart: always
    env_file:
      - .env
```
3. Add these Environment variables to the `.env` file
```text
MONGO_INITDB_ROOT_USERNAME=user
MONGO_INITDB_ROOT_PASSWORD=password

ME_CONFIG_MONGODB_ADMINUSERNAME=user
ME_CONFIG_MONGODB_ADMINPASSWORD=password
ME_CONFIG_MONGODB_URL=mongodb://user:password@mongodb:27017/

MONGO_HOST=mongodb
MONGO_PORT=27017
MONGO_USER=user
MONGO_PASSWORD=password
MONGO_DATABASE=database
```
4. Map the port 27017:27017 for MongoDB to your localhost. It can be public for now.
5. Map the mongo-express service to port 8081:8081, as it's the default for the mongo express.
6. Launch your Docker-Compose project.
7. Test out that you can surf to `8081`
:::

### Connecting to MongoDB from Python

:::warning
**TASK**
1. Install the `pymongo[srv]` package using Poetry.
2. create a second database.py script, this time call it `nosql_database.py` which will contain the following script
```python
# database.py

import os
from pymongo import MongoClient

# Package is `python-dotenv`
from dotenv import load_dotenv

load_dotenv() # Make sure we have our .env values


MONGO_USER = os.getenv('MONGO_USER')
if (os.getenv("ENVIRONMENT") == "DOCKER"):
    MONGO_HOST = os.getenv('MONGO_HOST')
else:
    MONGO_HOST = "localhost"

MONGO_PORT = os.getenv('MONGO_PORT')
MONGO_DATABASE = os.getenv('MONGO_DATABASE')
MONGO_PASSWORD = os.getenv('MONGO_PASSWORD')

def get_database(collection_name: str):

    CONNECTION_STRING = f"mongodb://{MONGO_USER}:{MONGO_PASSWORD}@{MONGO_HOST}/{MONGO_DATABASE}?authSource=admin"
    client = MongoClient(CONNECTION_STRING)
    db = client[MONGO_DATABASE]
    return db[collection_name]
```

3. You don't need to import this `nosql_database.py` in your `main.py`, but we will use it in the repository.
4. Create a folder for the `subjects` and create these files:
    - `router.py`
    - `models.py`
    - `repository.py`
5. Add this into your `models.py` and try to understand the structure of the components. It will become clearer when we're adding our first dataobjects.
```python
# models.py
from pydantic import BaseModel
from typing import Optional, List

class Document(BaseModel):
    _type: Optional[str] # E.g.: "SubjectResource", "SubjectTopic", "SubjectCourse", "Subject" ... Useful for structuring your json

class SubjectResource(Document):
    title: str
    link: str
    description: Optional[str] # You don't have to add a description

class SubjectTopic(Document):
    title: str # E.g.: Classes, Staticmethods ...
    week: int
    description: Optional[str] # You don't have to add a description
    resources: Optional[List[SubjectResource]] # The list of resources for this specific subjectcourse

class SubjectCourse(Document):
    title: str
    description: Optional[str]
    topics: List[SubjectTopic] # The list of topics we're handling: E.g.: Classes, Staticmethods ...
    resources: Optional[List[SubjectResource]] # The list of resources for this specific subjectcourse

class Subject(Document):
    _id: Optional[int] # Randomly generated ID by MongoDB
    title: str # E.g.: Object Oriented Programming
    weight: int # Used to sort the order of the subjects
    description: str # A short description what this subject is about
    courses: List[SubjectCourse] # The list of courses where this subject is being taught, 
    resources: Optional[List[SubjectResource]] # The list of resources
```
6. Add this into your `repository.py` and try to understand the structure of the components. We're now doing a different connection to the database, so we need to import the `nosql_database.py` file.
As you'll notice, it looks a little different this time, as it's a different connector. We're using the `collection` object to insert and find data.
```python
from typing import List
from uuid import uuid4
from nosql_database import (
    get_database
)
from .models import Subject
import traceback
collection = get_database('subjects')

class SubjectRepository():

    @staticmethod
    def get_all() -> List[Subject]:
        try:
            subjects = collection.find()
            return [Subject(**document) for document in subjects]
        except Exception as err:
            print(traceback.format_exc())
            print(err)
            return []

    @staticmethod
    def create(subject: Subject) -> str:
        """Create a new book"""
        document = subject.dict()
        document["_id"] = str(uuid4())
        result = collection.insert_one(document)
        assert result.acknowledged
        return "Created"
```
7. Finally, fill in the Router like you're used to! And add it to the `main.py` file.
This time, we'll also create the `add` route using a `POST` request.
```python
@router.post("/", name="Create a subject", response_model=str)
def create_subject(subject: Subject):
    result = SubjectRepository.create(subject)
    return result
```
:::

:::spoiler Test if you can add a subject to the database using this example
```json
{
    "_type": "Subject",
    "title": "Object Oriented Programming",
    "weight": 10,
    "description": "Object Oriented Programming is a concept that's often used when working in bigger applications to structure your code in a way that's easy to understand and maintain. It's a way of thinking about your code and how it's structured. It's not a language, but a concept that can be applied to any language.",
    "courses": [
        {
            "_type": "SubjectCourse",
            "title": "Object Oriented Programming in C#",
            "description": "This course will teach you the basics of Object Oriented Programming in C#.",
            "topics": [
                {
                    "_type": "SubjectTopic",
                    "title": "Classes",
                    "week": 1,
                    "description": "Classes are the building blocks of Object Oriented Programming. They are the blueprints for objects. They define the properties and methods that an object has.",
                    "resources": [
                        {
                            "_type": "SubjectResource",
                            "title": "C# Classes",
                            "description": "This is a great resource for learning about classes in C#.",
                            "link": "https://www.w3schools.com/cs/cs_classes.asp"
                        }
                    ]
                },
                {
                    "_type": "SubjectTopic",
                    "title": "Objects",
                    "week": 2,
                    "description": "Objects are the instances of a class. They are the actual things that you create from a class. They have the properties and methods that are defined in the class.",
                    "resources": [
                        {
                            "_type": "SubjectResource",
                            "title": "C# Objects",
                            "description": "This is a great resource for learning about objects in C#.",
                            "link": "https://www.w3schools.com/cs/cs_classes.asp"
                        }
                    ]
                },
                {
                    "_type": "SubjectTopic",
                    "title": "Inheritance",
                    "week": 3,
                    "description": "Inheritance is a way of creating a new class from an existing class. The new class will have all the properties and methods of the existing class, and can add new properties and methods of its own.",
                    "resources": [
                        {
                            "_type": "SubjectResource",
                            "title": "C# Inheritance",
                            "description": "This is a great resource for learning about inheritance in C#.",
                            "link": "https://www.w3schools.com/cs/cs_inheritance.asp"
                        }
                    ]
                }
            ],
            "resources": [
                {
                    "_type": "SubjectResource",
                    "title": "C# Object Oriented Programming",
                    "description": "This is a great resource for learning Object Oriented Programming in C#.",
                    "link": "https://www.w3schools.com/cs/cs_oop.asp"
                }
            ]
        },
        {
            "_type": "SubjectCourse",
            "title": "Object Oriented Programming in Python",
            "description": "This course will teach you the basics of Object Oriented Programming in Python.",
            "topics": [
                {
                    "_type": "SubjectTopic",
                    "title": "Classes",
                    "week": 1,
                    "description": "Classes are the building blocks of Object Oriented Programming. They are the blueprints for objects. They define the properties and methods that an object has.",
                    "resources": [
                        {
                            "_type": "SubjectResource",
                            "title": "Python Classes",
                            "description": "This is a great resource for learning about classes in Python.",
                            "link": "https://www.w3schools.com/python/python_classes.asp"
                        }
                    ]
                },
                {
                    "_type": "SubjectTopic",
                    "title": "Objects",
                    "week": 2,
                    "description": "Objects are the instances of a class. They are the actual things that you create from a class. They have the properties and methods that are defined in the class.",
                    "resources": [
                        {
                            "_type": "SubjectResource",
                            "title": "Python Objects",
                            "description": "This is a great resource for learning about objects in Python.",
                            "link": "https://www.w3schools.com/python/python_classes.asp"
                        }
                    ]
                },
                {
                    "_type": "SubjectTopic",
                    "title": "Inheritance",
                    "week": 3,
                    "description": "Inheritance is a way of creating a new class from an existing class. The new class will have all the properties and methods of the existing class, and can add new properties and methods of its own.",
                    "resources": [
                        {
                            "_type": "SubjectResource",
                            "title": "Python Inheritance",
                            "description": "This is a great resource for learning about inheritance in Python.",
                            "link": "https://www.w3schools.com/python/python_inheritance.asp"
                        }
                    ]
                }
            ],
            "resources": [
                {
                    "_type": "SubjectResource",
                    "title": "Python Object Oriented Programming",
                    "description": "This is a great resource for learning Object Oriented Programming in Python.",
                    "link": "https://www.w3schools.com/python/python_classes.asp"
                }
            ]
        }
    ]
}
```
:::

#### Explore in the MongoExpress

Now that you have an object in your database, you can explore it in the MongoExpress view.
Surf to `http://localhost:8081` and you should see the database `database` with the collection `subjects` in it.
If you want to, you can even edit the object directly from the MongoExpress GUI.
Then you might notice why we didn't create a full relational database to put all of this information in.


## Extending the project

### More routes

As I mentioned earlier, there's still some room for improvement on adding more functionalities regarding the database queries.
So far, we have only focussed on **Getting all** or **adding** one item.

In order to have all benefits of your application, you could allow your users to query some more information and add some more endpoints with some database operations linked to it.

Whether that is to the MongoDB or the MySQL one is your choice, of course!

### GraphQL

Check out the Demo's to find out how you can extend your project by using GraphQL instead of the classical REST endpoints.

### Proper error handling
:::warning
**TASK**
1. Write clean error handling options using `raise` and `try ... except`
2. You can raise errors from the Repository and "catch" them from the Router, there you can format a nice error.
3. You can also use the error handling to show different responses based on the error.
- **404** when there is nothing to be found, for example.
- **400** when there is something wrong with the request.
- **200** when everything went well.
- **201** when something was created.
- ...
:::
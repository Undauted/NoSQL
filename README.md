## Piotr Kacprowicz
Informacje o komputerze na którym były wykonywane obliczenia:

| Nazwa                 | Wartosć    |
|-----------------------|------------|
| System operacyjny     | Win 10 Pro x64 |
| Procesor              | Intel Core i7-4710HQ |
| Ilość rdzeni          | 4 |
| Pamięć                | 12GB |
| Dysk                  | Hitachi Travelstar 7K1000 1TB |
| Baza danych           | TODO |

Rozwiązania zadań z przedmiotu *Bazy NoSQL*:

Wybrany zbiór danych - [Jester](http://www.ieor.berkeley.edu/~goldberg/jester-data/)

# Zaliczenie:

## Zadanie GEO
[Zadanie GEO](https://undauted.github.io/NoSQL/)

Instrukcja do skryptów znajduje się [tutaj]()

Zbiór danych: [Offshore wells on the UKCS](http://data.ogauthority.opendata.arcgis.com/datasets/40b80e75b8004fab8c87218ae1664d91_0.csv). 
 
Dane jakie zostały wykorzystane w tym zadaniu zawierają zbiór odwiertów morskich wokół Wielkiej Brytanii. Mamy tutaj plik csv zajmujący 3.9 MB, który zawiera najważniejsze informacje dotyczące odwiertów morskich.

Plik csv został skonwertowany za pomocą strony [MyGeodata](https://mygeodata.cloud/converter/csv-to-geojson). Po konwersji plik zajmuje 12.9 MB.

<h6>Liczba rekordów</h6>

```
Imported 11832 documents
```     
	
<h6>Przykładowy rekord</h6>

```
{
	"type" : "Feature",
        "properties" : {
                "X" : 1.312231,
                "Y" : 58.791347,
                "OBJECTID" : "2001",
                "WELLREGNO" : "16/07a- 14",
                "DENNO" : "1493",
                "TOPHOLEYDD" : "58.791944",
                "TOPHOLEXDD" : "1.313861",
                "TOPHOLEYGE" : "058 47 31.000N",
                "TOPHOLEXGE" : "001 18 49.900E",
                "TOPHOLEYNG" : "",
                "TOPHOLEXNG" : "",
                "COUNTRYCOD" : "SEAWARD",
                "QUADRANTNO" : "16",
                "BLOCKNO" : "7",
                "BLOCKSUFFI" : "a",
                "PLATFORM" : "",
                "SLOTNO" : "",
                "DRILLSEQNO" : "14",
                "WELLSUFFIX" : "",
                "ORIGINTENT" : "A",
                "DATUMELEV" : "82",
                "DATUMTYPE" : "KB",
                "GROUNDELEV" : "0",
                "WATERDEPTH" : "343",
                "SPUDDATE" : "1980-04-09T00:00:00.000Z",
                "DATETDREAC" : "1980-07-08T00:00:00.000Z",
                "COMPLEDATE" : "1980-08-10T00:00:00.000Z",
                "ORIGUNITS" : "F",
                "OPERATOR" : "MARATHON OIL U.K. LLC",
                "WELLSYMBOL" : "13",
                "PRIMARYTAR" : "N",
                "COMPLESTAT" : "AB3",
                "FLOWCLASS" : "GCW",
                "TVDSSDRILL" : "0",
                "TOTALMDDRI" : "13178",
                "PARENTROLE" : "",
                "WELLINFO" : "http://data.ogauthority.opendata.arcgis.com/",
                "NAME" : "",
                "TOPHOLEDTM" : "ED 50",
                "DEVTYPE" : "",
                "OTHERCLASS" : ""
        },
        "geometry" : {
                "type" : "Point",
                "coordinates" : [
                        1.312231390246396,
                        58.79134657742885
                ]
        }
}
```

<h6>Wyjaśnienie najistotniejszych pól</h6>
<br>
<table>
  <thead>
    <tr>
      <th>Pole</th>
      <th>Wyjaśnienie</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>COUNTRYCOD</td>
      <td>Kod należenie do konkretnego państwa </td>
    </tr>
	<tr>
      <td>DENNO</td>
      <td>Głębokość wiercenie</td>
    </tr>
    <tr>
      <td>SPUDDATE</td>
      <td>Data rozpoczęcia budowy</td>
    </tr>
    <tr>
      <td>COMPLEDATE</td>
      <td>Data zakończenia budowy</td>
    </tr>
     <tr>
      <td>OPERATOR</td>
      <td>Firma do której należy odwiert</td>       
    </tr>
	</tr>
     <tr>
      <td>coordinater</td>
      <td>Długośc i szerokość geograficzna odwiertu</td>       
    </tr>
 </tbody>
</table>

### MongoDb

<h6>Stworzenie bazy ORG</h6>

```
use ORG
```

<h6>Stworzenie kolekcji Wells</h6>	

```
db.createCollection("Wells")
```

<h6>Import danych do bazy</h6>	

```
mongoimport --db ORG --collection Wells --file OGA_Wells_WGS84.geojson --jsonArray
```

### Zapytania

<h6>Odwierty położone 5km od odwiertu własności CONOCOPHILLIPS o koordynatach (53.44106130104489, 2.393602625903736)</h6>

```
db.Wells.find({
	geometry:{
		$near:{
			$geometry:{ 
				"type" : "Point", 
				"coordinates" : [ 2.393602625903736,53.44106130104489 ] },
				$maxDistance:5000
				}
			}
});

```

[Mapa 1](https://github.com/Undauted/NoSQL/blob/master/mapa1.geojson)

<h6>Odwiert operatora ENERGY RESOURCE TECHNOLOGY jest położony w centrum, a pozostałe odwierty sa w promieniu 0.1(52.94598756402161, 2.1531123182033376)</h6>

```
db.Wells.find({
	geometry: { 
		$geoWithin: { 
			$center:  [ [ 2.1531123182033376, 52.94598756402161  ], 0.1 ] 
		} 
	}
});
```

[Mapa 2](https://github.com/Undauted/NoSQL/blob/master/mapa2.geojson)

<h6>Odwierty położone w konkretnym czworokącie</h6>

```
db.Wells.find({
	geometry: {
		$geoWithin: { 
			$geometry: { 
				type : 'Polygon', 
				coordinates: [[[ -4.399991, 60.325 ], [ -4.3080609999999995, 60.319297 ],   [ -4.30, 60.28 ], [ -4.48, 60.26], [ -4.399991, 60.325 ]    ]]
			}
		} 
	}				
});
```

[Mapa 3]((https://github.com/Undauted/NoSQL/blob/master/mapa3.geojson))

## Zadanie 1

### PostgreSQL

Zbiór danych - [Health](https://archive.org/download/stackexchange/health.stackexchange.com.7z)

<h6>Utworzenie tabeli</h6>

<h6>Posts</h6>

```
CREATE TABLE Posts(
	Id BIGINT, 
	PostTypeId INTEGER, 
	AcceptedAnswerId INTEGER, 
	CreationDate VARCHAR, 
	Score INTEGER, 
	ViewCount BIGINT, 
	OwnerUserId INTEGER, 
	LastEditorUserId INTEGER, 
	LastEditDate VARCHAR, 
	LastActivityDate VARCHAR, 
	Title VARCHAR, 
	Tags VARCHAR, 
	AnswerCount 
	INTEGER, 
	CommentCount 
	INTEGER, 
	FavoriteCount INTEGER
);
```

<h6>Users</h6>

```
CREATE TABLE Users(
	Id INTEGER, 
	Reputation INTEGER, 
	CreationDate VARCHAR, 
	DisplayName VARCHAR, 
	LastAccessDate VARCHAR, 
	Location VARCHAR, 
	Views INTEGER, 
	UpVotes INTEGER, 
	DownVotes INTEGER, 
	Age INTEGER, 
	AccountId INTEGER
);
```

<h6>Import danych z pliku CSV</h6>

```
\copy Posts FROM 'E:\MongoDB\Health\CSV\Post.csv' DELIMITER ';' CSV HEADER
\copy Users FROM 'E:\MongoDB\Health\CSV\Users.csv' DELIMITER ';' CSV HEADER
```

<h6>Zliczenie ilości zaimportowanych rekordów</h6>

```
SELECT COUNT(*) FROM Posts;
SELECT COUNT(*) FROM Users;
```

<h6>Liczba rekordów</h6>

```
Posts - 6400
Users - 5990
```

<h6>Obliczenie i czas importu danych</h6>

```
\timing \copy Posts FROM 'E:\MongoDB\Health\CSV\Post.csv' DELIMITER ';' CSV HEADER
Posts - 23,886 ms

\timing \copy Users FROM 'E:\MongoDB\Health\CSV\Users.csv' DELIMITER ';' CSV HEADER
Users - 18,384 ms
```

<h4>Agregacja 1. 5 najwcześniej dodanych postów w 2015</h4>

```
SELECT Title,CreationDate 
FROM Posts 
ORDER BY CreationDate 
ASC LIMIT 5;
```

<h6>Czas wykonania zapytania</h6>

```
5,839 ms
```

<h6>Wynik zapytania</h6>
<br>
<table>
  <thead>
    <tr>
      <th>Tytuł</th>
      <th>Data</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>What are these lines in teeth?</td>
      <td>2015-03-31T19:00:01.793</td>
    </tr>
    <tr>
      <td>Calcium supplements versus \"fortified with calcium\"</td>
      <td>2015-03-31T19:06:32.503</td>
    </tr>
    <tr>
      <td>If human life is so long largely due to modern medicine, does every illness shorten lifespan?</td>
      <td>2015-03-31T19:11:24.947</td>
    </tr>
     <tr>
      <td>Can the immune system break down anything?</td>
      <td>2015-03-31T19:21:14.007</td>       
    </tr>
    <tr>
      <td>What should I consider when deciding to remove a blister or not?</td>
      <td>2015-03-31T19:26:15.727</td>
    </tr>
 </tbody>
</table>

<h4>Agregacja 2. Tytuł i liczba punktów 10 postów którę mają liczbę wyswietleń większa niż 100, ale mniejszą niż 200</h4>

```
SELECT Title, Score, ViewCount 
FROM Posts 
WHERE ViewCount 
BETWEEN 101 AND 200 
ORDER BY Id 
DESC LIMIT 10;
```

<h6>Czas wykonania zapytania</h6>

```
2,502 ms
```

<h6>Wynik zapytania</h6>
<br>
<table>
  <thead>
    <tr>
      <th>Tytuł</th>
      <th>Punkty</th>
      <th>Wyświetlenia</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Suicide with no pain</td>
      <td>1</td>
      <td>112</td>
    </tr>
    <tr>
      <td>Medical professionals referring to 'left' and 'right': are they referring to my relative directions or theirs?</td>
      <td>8</td>
      <td>107</td>
    </tr>
    <tr>
      <td>Can i use parachute hair coconut oil for oil pulling for tooth problem?</td>
      <td>0</td>
      <td>141</td>
    </tr>
     <tr>
      <td>Can you thermoregulate a fever externally with e.g. an ice bath?</td>
      <td>2</td>
      <td>108</td>
    </tr>
    <tr>
      <td>Can sperm fertilize an egg before reaching full maturity?</td>
      <td>3</td>
      <td>130</td>
    </tr>
    <tr>
      <td>Can pre-ejaculate cause pregnancy?</td>
      <td>6</td>
      <td>144</td>
    </tr>
     <tr>
      <td>Bad Brain fog 15 min after eating but sugar test is negative</td>
      <td>2</td>
      <td>106</td>
    </tr>
    <tr>
      <td>Does eyesight significantly vary from day-to-day?</td>
      <td>2</td>
      <td>126</td>
    </tr>
    <tr>
      <td>Is there a difference between anti-anxiety and anti-depression drugs?</td>
      <td>2</td>
      <td>179</td>
    </tr>
    <tr>
      <td>Identical twins have the same DNA and blood-types, right? But different fingerprints? Why is that? Same for clones?</td>
      <td>1</td>
      <td>108</td>
    </tr>
     </tbody>
</table>

<h4>Agregacja 3. Tytuł oraz 8 użytkowników, którzy zdobyli największa liczbę punktów za swój post</h4>

```
SELECT Title, DisplayName, Score 
FROM Posts 
INNER JOIN Users 
ON Users.Id = Posts.OwnerUserId 
ORDER BY Score 
DESC LIMIT 8;
```

<h6>Czas wykonania zapytania</h6>

```
7,151 ms
```

<h6>Wynik zapytania</h6>
<br>
<table>
  <thead>
    <tr>
      <th>Tytuł</th>
      <th>Punkty</th>
      <th>Autor</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>How can I protect my eyesight when using computers?</td>
      <td>69</td>
      <td>Nate Barbettini</td>
    </tr>
    <tr>
      <td>What's the best long-term sitting posture?</td>
      <td>42</td>
      <td>Jez</td>
    </tr>
    <tr>
      <td>Is there any health risk in cellular phones?"</td>
      <td>32</td>
      <td>Shadow Wizard</td>
    </tr>
     <tr>
      <td>Are there any health benefits to male circumcision?</td>
      <td>32</td>
      <td>Jez</td>
    </tr>
    <tr>
      <td>Is food prepared in a microwave oven less healthy?</td>
      <td>29</td>
      <td>Patrick Hoefler</td>
    </tr>
    <tr>
      <td>Can MRI scans be dangerous for one's health?</td>
      <td>28</td>
      <td>Franck Dernoncourt</td>
    </tr>
     <tr>
      <td>How many eggs can one eat per day?</td>
      <td>28</td>
      <td>Franck Dernoncourt</td>
    </tr>
    <tr>
      <td>Does the lack of sleep affect my health?</td>
      <td>27</td>
      <td>Shevliaskovic</td>
    </tr>
     </tbody>
</table>

### MongoDB

Zbiór danych - [Health](https://archive.org/download/stackexchange/health.stackexchange.com.7z)

<h6>Import danych z pliku JSON</h6>

```
mongoimport -d nosql -c post --file E:\MongoDB\health\Json\Post.json --jsonArray
mongoimport -d nosql -c users --file E:\MongoDB\health\Json\Users.json --jsonArray
```

<h6>Zliczenie ilości zaimportowanych rekordów</h6>

```
db.post.count()
db.users.count()
```

<h6>Liczba rekordów</h6>

```
Post - 6400
Users - 5990
```

<h6>Obliczenie czasu importu danych</h6>

```
powershell "Measure-Command{mongoimport -d nosql -c post --file E:\MongoDB\health\Json\Post.json --jsonArray}"
powershell "Measure-Command{mongoimport -d nosql -c users --file E:\MongoDB\health\Json\Users.json --jsonArray}"
```

<h6>Czas importu danych</h6>

```
Post - 628,1095 ms
Users - 344,4309 ms
```

<h6>Parsowanie na inta</h6>

```
db.post.find().forEach( function (x) { x._Score = parseInt(x._Score); db.post.save(x);})
db.post.find().forEach( function (x) { x._ViewCount = parseInt(x._ViewCount); db.post.save(x);})
db.post.find().forEach( function (x) { x._CreationDate = parseInt(x._CreationDate); db.post.save(x);})
```

<h4>Agregacja 1. 5 najwcześniej dodanych postów w 2015</h4>

```
db.post.aggregate([
     {$match:{"_CreationDate":{$gte:2015}}},
     {$project:{_CreationDate:1,_Title:1}},
     {$limit:5},
     {$sort:{_CreationDate:-1}}
]).pretty()
```

<h6>Czas wykonania zapytania</h6>

```
1 ms
```

<h6>Wynik zapytania</h6>
<br>
<table>
  <thead>
    <tr>
      <th>Tytuł</th>
      <th>Data</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>What are these lines in teeth?</td>
      <td>2015-03-31T19:00:01.793</td>
    </tr>
    <tr>
      <td>Calcium supplements versus \"fortified with calcium\"</td>
      <td>2015-03-31T19:06:32.503</td>
    </tr>
    <tr>
      <td>If human life is so long largely due to modern medicine, does every illness shorten lifespan?</td>
      <td>2015-03-31T19:11:24.947</td>
    </tr>
     <tr>
      <td>Can the immune system break down anything?</td>
      <td>2015-03-31T19:21:14.007</td>       
    </tr>
    <tr>
      <td>What should I consider when deciding to remove a blister or not?</td>
      <td>2015-03-31T19:26:15.727</td>
    </tr>
 </tbody>
</table>

<h4>Agregacja 2. Tytuł i liczba punktów 10 postów którę mają liczbę wyswietleń większa niż 100, ale mniejszą niż 200</h4>

```
db.post.aggregate([
     {$match:{"_ViewCount":{$lt:200, $gt:100}}},
     {$group: {_id: {view: "$_ViewCount", score: "$_Score",title: "$_Title"}}},
     {$limit:10}
]).pretty()
```

<h6>Czas wykonania zapytania</h6>

```
32 ms
```

<h6>Wynik zapytania</h6>
<br>
<table>
  <thead>
    <tr>
      <th>Tytuł</th>
      <th>Punkty</th>
      <th>Wyświetlenia</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Suicide with no pain</td>
      <td>1</td>
      <td>112</td>
    </tr>
    <tr>
      <td>Medical professionals referring to 'left' and 'right': are they referring to my relative directions or theirs?</td>
      <td>8</td>
      <td>107</td>
    </tr>
    <tr>
      <td>Can i use parachute hair coconut oil for oil pulling for tooth problem?</td>
      <td>0</td>
      <td>141</td>
    </tr>
     <tr>
      <td>Can you thermoregulate a fever externally with e.g. an ice bath?</td>
      <td>2</td>
      <td>108</td>
    </tr>
    <tr>
      <td>Can sperm fertilize an egg before reaching full maturity?</td>
      <td>3</td>
      <td>130</td>
    </tr>
    <tr>
      <td>Can pre-ejaculate cause pregnancy?</td>
      <td>6</td>
      <td>144</td>
    </tr>
     <tr>
      <td>Bad Brain fog 15 min after eating but sugar test is negative</td>
      <td>2</td>
      <td>106</td>
    </tr>
    <tr>
      <td>Does eyesight significantly vary from day-to-day?</td>
      <td>2</td>
      <td>126</td>
    </tr>
    <tr>
      <td>Is there a difference between anti-anxiety and anti-depression drugs?</td>
      <td>2</td>
      <td>179</td>
    </tr>
    <tr>
      <td>Identical twins have the same DNA and blood-types, right? But different fingerprints? Why is that? Same for clones?</td>
      <td>1</td>
      <td>108</td>
    </tr>
     </tbody>
</table>

<h4>Agregacja 3. Tytuł oraz 8 użytkowników, którzy zdobyli największa liczbę punktów za swój post</h4>

```
db.post.aggregate([{
     $lookup:{from:"users", localField:"_OwnerUserId", foreignField: "_Id", as:"postid"}},
     {$project:{_Score:1,"postid._DisplayName":1,_Title:1}},
     {$group:{_id:{user:"$postid._DisplayName", score:"$_Score", title:"$_Title"}}},
     {$sort: {"_id.score":- 1}},
     {$limit:8}
]).pretty()
```

<h6>Czas wykonania zapytania</h6>

```
60072 ms
```

<h6>Wynik zapytania</h6>
<br>
<table>
  <thead>
    <tr>
      <th>Tytuł</th>
      <th>Punkty</th>
      <th>Autor</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>How can I protect my eyesight when using computers?</td>
      <td>69</td>
      <td>Nate Barbettini</td>
    </tr>
    <tr>
      <td>What's the best long-term sitting posture?</td>
      <td>42</td>
      <td>Jez</td>
    </tr>
    <tr>
      <td>Is there any health risk in cellular phones?"</td>
      <td>32</td>
      <td>Shadow Wizard</td>
    </tr>
     <tr>
      <td>Are there any health benefits to male circumcision?</td>
      <td>32</td>
      <td>Jez</td>
    </tr>
    <tr>
      <td>Is food prepared in a microwave oven less healthy?</td>
      <td>29</td>
      <td>Patrick Hoefler</td>
    </tr>
    <tr>
      <td>Can MRI scans be dangerous for one's health?</td>
      <td>28</td>
      <td>Franck Dernoncourt</td>
    </tr>
     <tr>
      <td>How many eggs can one eat per day?</td>
      <td>28</td>
      <td>Franck Dernoncourt</td>
    </tr>
    <tr>
      <td>Does the lack of sleep affect my health?</td>
      <td>27</td>
      <td>Shevliaskovic</td>
    </tr>
     </tbody>
</table>


### Aggregation Pipeline
 
Egzamin:
 - [ ] MapReduce



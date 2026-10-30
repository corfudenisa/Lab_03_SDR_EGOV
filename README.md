# Lab_03_SDR_EGOV

Laboratorul 2 - Sistem de recomandare cu Recombee (înregistrarea proprietăților)

## Dataset-ul ales

Am ales domeniul **filme**, folosind dataset-ul **IMDB Movies Dataset** (Top 1000 Movies and TV Shows) de pe Kaggle:
https://www.kaggle.com/datasets/harshitshankhdhar/imdb-dataset-of-top-1000-movies-and-tv-shows

Fișierul folosit este `imdb_top_1000.csv` și conține **1000** de filme, adică primele 1000 de filme de pe IMDB în funcție de rating. Pentru fiecare film avem informații precum titlul, anul apariției, genul, regizorul, actorii principali, ratingul IMDB, numărul de voturi și încasările.

Am ales filmele pentru că este un domeniu familiar tuturor, în care sistemele de recomandare sunt folosite des, pe platforme precum Netflix sau HBO Max. Preferințele oamenilor pentru filme sunt destul de variate, așa că un sistem de recomandare chiar poate ajuta utilizatorul să descopere titluri noi pe care altfel nu le-ar fi găsit. În plus, dataset-ul conține suficiente informații despre fiecare film pentru a putea găsi asemănări între ele, iar datele sunt deja organizate și ușor de importat în Recombee.

## Proprietățile folosite în Recombee

Din cele 16 coloane ale fișierului am ales următoarele proprietăți pentru catalog:

| Proprietate Recombee | Coloana din CSV | Tip    | Descriere                              |
| -------------------- | --------------- | ------ | -------------------------------------- |
| `title`              | `Series_Title`  | string | titlul filmului                        |
| `year`               | `Released_Year` | int    | anul în care a apărut filmul           |
| `rating`             | `IMDB_Rating`   | double | ratingul de pe IMDB (ex. 9.3)          |
| `genre`              | `Genre`         | string | genul filmului (ex. „Thriller, Drama”) |
| `director`           | `Director`      | string | regizorul                              |
| `votes`              | `No_of_Votes`   | int    | numărul de voturi de pe IMDB           |

---

Laboratorul 3 - Sistem de recomandare cu Recombee

## Dataset

Am continuat cu dataset-ul din Laboratorul 2, `imdb_top_1000.csv`, care conține **1000** de filme.

## Maparea datelor

| Proprietate Recombee | Coloana din CSV                           | Tip         |
| -------------------- | ----------------------------------------- | ----------- |
| `itemId`             | `item_id` (`movie_0001` ... `movie_1000`) | ID implicit |
| `title`              | `Series_Title`                            | string      |
| `year`               | `Released_Year`                           | int         |
| `rating`             | `IMDB_Rating`                             | double      |
| `genre`              | `Genre`                                   | string      |
| `director`           | `Director`                                | string      |
| `votes`              | `No_of_Votes`                             | int         |

- **ID unic:** dataset-ul original nu are o coloană de ID, iar titlul nu poate fi folosit pentru că nu este unic (_Drishyam_ apare de două ori, cu filme diferite). De aceea, am adăugat în `imdb_top_1000.csv` coloana `item_id`, cu valori generate din poziția filmului în fișier, iar scriptul o leagă la `itemId` din Recombee.
- **Curățare:** filmul _Apollo 13_ are valoarea `PG` în coloana `Released_Year`, așa că scriptul o corectează cu anul real, 1995.

## Trimiterea item-urilor

Scriptul `recombee_items.py` citește fișierul CSV, construiește câte un request `SetItemValues` pentru fiecare film și le trimite în loturi de câte 100, prin cereri `Batch`. Astfel, cele 1000 de filme sunt trimise în doar 10 request-uri HTTP. Rulat din nou, scriptul actualizează filmele existente, fără să creeze duplicate.

## Rezultat

Datele au fost încărcate cu succes în Recombee: toate cele **1000** de filme apar în catalogul bazei de date `denisacorfu-sdr-dev`, cu toate proprietățile completate.

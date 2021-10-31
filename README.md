# Pola Web

Celem tego projektu jest zbudowanie interfejsu Web w technologii React dla aplikacji [Pola. Zabierz ją na zakupy](https://www.pola-app.pl/). W tym celu ściślę współpracuje z [pola-backend](https://github.com/KlubJagiellonski/pola-backend).

Masz dość masówki globalnych koncernów? Szukasz lokalnych firm tworzących unikatowe produkty? Pola pomoże Ci odnaleźć polskie wyroby. Zabierając Polę na zakupy, odnajdujesz produkty „z duszą” i wspierasz polską gospodarkę.

Zeskanuj kod kreskowy z dowolnego produktu i dowiedz się więcej o firmie, która go wyprodukowała. Pola powie Ci, czy dany producent opiera się na polskim kapitale, ma u nas swoją produkcję, tworzy wykwalifikowane miejsca pracy, jest częścią zagranicznego koncernu.

Ten projekt został rozpoczęty wykorzystując starter [https://evaluates2.github.io/Gatsby-Starter-TypeScript-Redux-TDD-BDD](https://evaluates2.github.io/Gatsby-Starter-TypeScript-Redux-TDD-BDD).

Podgląd wersji deweloperskiej: [https://pola-staging.herokuapp.com/](https://pola-staging.herokuapp.com/)

## Dostępne skrypty

W katalogu projektu możesz uruchomić:

### `npm start`

Uruchamia aplikację w trybie programistycznym.
Odtwórz [http://localhost:8000](http://localhost:8000) aby wyświetlić go w przeglądarce.

Strona zostanie załadowana ponownie, jeśli wprowadzisz zmiany.
W konsoli zostaną również wyświetlone wszelkie błędy analizy statycznej (ang. lint).

### `npm test`

Uruchamia test runner w interaktywnym trybie obserwującym zmiany.

### `npm run build`

Kompiluje aplikację do produkcji do folderu `build`.
Prawidłowo buduje aplikacje Reacta w trybie produkcyjnym i optymalizuje ją pod kątem najlepszej wydajności.

```
npm run build
```

Serve local build

```
npm run serve
```

Run Unit Tests (TDD watch-mode style)

```
npm test
```

Run Unit Tests (Single run for CI and with code coverage output)

```
npm run test-once
```

Run BDD / E2e Tests (Locally With UI)

```
npm run e2e
```

Run BDD / E2e Tests (Headless Mode for CI):

```
node_modules/.bin/cypress run
```

Run linting (calls both prettier linting and tslint)

```
npm run lint
```

Deploy

```
npx gatsby deploy
```

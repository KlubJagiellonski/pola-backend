# Pola Web

Celem tego projektu jest zbudowanie interfejsu Web w technologii React dla aplikacji [Pola. Zabierz ją na zakupy](https://www.pola-app.pl/). W tym celu ściślę współpracuje z [pola-backend](https://github.com/KlubJagiellonski/pola-backend).

Masz dość masówki globalnych koncernów? Szukasz lokalnych firm tworzących unikatowe produkty? Pola pomoże Ci odnaleźć polskie wyroby. Zabierając Polę na zakupy, odnajdujesz produkty „z duszą” i wspierasz polską gospodarkę.

Zeskanuj kod kreskowy z dowolnego produktu i dowiedz się więcej o firmie, która go wyprodukowała. Pola powie Ci, czy dany producent opiera się na polskim kapitale, ma u nas swoją produkcję, tworzy wykwalifikowane miejsca pracy, jest częścią zagranicznego koncernu.

Ten projekt został rozpoczęty wykorzystując starter [https://evaluates2.github.io/Gatsby-Starter-TypeScript-Redux-TDD-BDD](https://evaluates2.github.io/Gatsby-Starter-TypeScript-Redux-TDD-BDD).

Podgląd wersji deweloperskiej: [https://klubjagiellonski.github.io/pola-web/](https://klubjagiellonski.github.io/pola-web/)

<img src="./_Gatsby-Starter-TypeScript-Redux-TDD-BDD-Logo.png">

An awesome Gatsby starter template that takes care of the tooling setup, allowing you and your team to dive right into building ultra-fast React applications quickly and deploy them with confidence!

[![Build Status](https://api.travis-ci.org/Evaluates2/Gatsby-Starter-TypeScript-Redux-TDD-BDD.svg?branch=master)](https://travis-ci.org/Evaluates2/Gatsby-Starter-TypeScript-Redux-TDD-BDD)

# Features

- [x] TypeScript pre-installed and all src files have been converted to TypeScript.
- [x] Redux preinstalled and with simple examples of actions, reducers, and types, and custom middlewares.
- [x] Redux-devtools support preinstalled (For usage with Redux Dev Tools Chrome Extension)
- [x] Redux-localstorage-simple preinstalled (For automatic syncing of specified reducers to local storage)
- [x] Unit testing with Jest pre-configured and ready to go.
- [x] End-to-end UI automation testing with Cypress pre-configured.
- [x] Cucumber plugin preinstalled into Cypress to run gherkin features files and steps definitions for outside-in behavior-driven-development.
- [x] Linting pre-configured with Prettier _AND_ TSLint.
- [x] Continuous integration & continuous deploy setup with Travis CI.

### npm i

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

## Adding Travis CI

Now that you have all of these automated tests checking that the application id working properly, wouldn't it be awesome if when you pushed or merged to specific git branches that the tests were run, and if every passed then a fresh build was made and deployed to dev for you? Well, that's basically what adding continuous integration and continuous deployment (CI / CD) is all about! You can use any continuous integration system you like. We chose TravisCI for this project simply because it is extremely easy to use and totally free for public Github repositories. All you need to do to add travis CI to your repo is go to the TravisCI repositories page linked with your GitHub account and click the toggle button on to "activate" the repository. Then simply add a `.travis.yml` file in the root of your project, and you're done! This project contains a sample Travis configuration file with commented sections for you to enter the command for deploying your project. In general, git-triggered deploys should go to your first and most bleeding-edge environment, often named "dev". This will then usually be manually tested and approved to the next environment one or more times. The final environment is often called "prod" or "production" and refers to the one environment that the end-users actually use.

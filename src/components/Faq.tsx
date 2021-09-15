import React from 'react'
import styled from 'styled-components'
import { urls } from '../domain/website'
import { TitleSection } from '../styles/GlobalStyle.css'
import { margin } from '../styles/theme'
import AccordionList from './accordion/AccordionList'

const faq = [
  {
    question: "Mam telefon z systemem operacyjnym Android. Nie mogę znaleźć aplikacji w Google Play. Dlaczego?",
    answer: <p>Aplikacja Pola działa na telefonach wyposażonych w system Android 4.1 lub nowszy. Aktualnie nie planujemy wsparcia dla wcześniejszych wersji.</p>,
    key: 1
  },
  {
    question: "Mam telefon iPhone (iPad). Nie mogę znaleźć aplikacji w App Store. Dlaczego?",
    answer: <p>Aplikacja Pola działa na urządzeniach wyposażonych w system operacyjny iOS w wersji 11.0 lub nowszej. Aktualnie nie planujemy wsparcia dla wcześniejszych wersji.</p>,
    key: 2
  },
  {
    question: "Reprezentuję producenta. Moja firma nie została jeszcze zweryfikowana przez redakcję. Co mam zrobić?",
    answer: <p>W pierwszej kolejności zajmujemy się tymi firmami, których produkty są najczęściej skanowane. Jednak możesz nam pomóc w weryfikacji firmy wypełniając <a href={urls.external.form.href}>formularz</a>.</p>,
    key: 3
  },
  {
    question: "Jak mogę zgłosić uwagi lub błąd w serwisie Pola?",
    answer: <p>Korzystamy z serwisu GitHub do zgłaszania błędów i uwag. Wybierz do jakiej części Poli chcesz zgłosić uwagi: <a href={urls.external.githubAndroid.href}>aplikacja na Androida</a>, <a href={urls.external.githubIos.href}>aplikacja na iPhone'a</a>, <a href={urls.external.githubWeb.href}>strona internetowa</a>.</p>,
    key: 4
  },
  {
    question: "Chcę pomóc w projekcie",
    answer: <p>Zapraszamy do włączenia się w pracę nad serwisem Pola. Dołącz do nas i pracuj nad <a href={urls.external.githubAndroid.href}>aplikacją na Androida</a>, <a href={urls.external.githubIos.href}>aplikacją na iPhone'a</a> lub <a href={urls.external.githubWeb.href}>stroną internetową</a>. Stale poszukujemy też wolontariuszy chcących pomóc nam rozwijać bazę danych o firmach - zachęcamy do kontaktu z Mateuszem Perowiczem (tel. 660 010 034, e-mail: mateusz.perowicz@klubjagiellonski.pl)</p>,
    key: 5
  },
]


const Wrapper = styled.div`
  margin: ${margin.big} 0;
`

const Faq = () => {
  return (
    <Wrapper>
      <TitleSection>
        FAQ
      </TitleSection>
      <AccordionList list={faq} />
    </Wrapper>
  )
}

export default Faq;
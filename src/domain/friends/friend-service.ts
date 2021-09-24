import { graphql, useStaticQuery } from 'gatsby';

export interface IFriendsSuccess {
  results: IFriendsData[];
}

export interface IFriendsError {
  error: unknown;
}

interface IFriendsData {
  id: number;
  photo: string;
  description: string;
}

const friends: IFriendsData[] = [
  {
    id: 1,
    photo: 'Browar-Piwojad.png',
    description:
      'Piwojad to kontraktowy browar rzemieślniczy z Krakowa założony przez Pawła Świdniewicza i Pawła Teodorczyka, którzy przygodę z piwowarstwem zaczęli od domowej produkcji na małą skalę. Piwojad dużą wagę przywiązuje do regionu, w którym warzy piwa. Priorytetem jest zaopatrywanie się w surowce dostępne u lokalnych dostawców i producentów żywności.',
  },
  {
    id: 2,
    photo: 'logo_radziemska.png',
    description:
      'Rodzime przedsiębiorstwo chemiczne powstałe w 1982 roku. Firma specjalizuje się w produkcji chemii gospodarczej, w tym odplamiaczy, proszków do prania czy wybielaczy. Jest laureatem wielu nagród konsumenckich, a jej siedziba znajduje się w Łomiankach pod Warszawą.',
  },
  {
    id: 3,
    photo: 'AmeriPol-Trading.png',
    description:
      'Firma Ameri-Pol Trading Ltd sp. z o.o. jest polską firmą założoną w 1992 r. jako spółka polsko amerykańska, jednak w ciągu lat działalności udziałowiec amerykański został wykupiony przez polskich udziałowców. Firma oferuje szeroki wybór klejów kontaktowych w pojemnikach ciśnieniowych oraz rozpuszczalników mających zastosowanie w różnych branżach, m.in. w meblarstwie, w branży motoryzacyjnej, w produkcji jachtów, w branży budowlanej. Oferowane przez nas kleje są sprzedawane pod własną wspólną marką SPRAY-KON i LEP-KON.',
  },
  {
    id: 4,
    photo: 'AvetPharma.png',
    description:
      'Spółka farmaceutyczna założona 10 lat temu przez magistra farmacji z wieloletnim doświadczeniem w branży leków OTC oraz suplementów diety. Firma zajmuje się produkcją oraz dystrybucją suplementów diety. Przez dekadę wprowadziła na rynek ponad 40 produktów własnych, które są dostępne w aptekach, sklepach zielarsko-medycznych oraz marketach. Siedziba spółki znajduje się w Warszawie.',
  },
];

export const FriendsService = {
  getFriends: async (): Promise<IFriendsSuccess> => {
    return {
      results: friends,
    };
  },
  getAll: () =>
    useStaticQuery(
      graphql`
        {
          allLogosFriendsYaml {
            nodes {
              id
              name
              description
              image {
                base
              }
              page
              slug
            }
          }
        }
      `
    ),
};

export interface IFriendNode {
  id: string;
  name: string;
  description: string;
  image: {
    base: string;
  };
  page: string;
  slug: string;
}

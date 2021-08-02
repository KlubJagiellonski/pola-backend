export enum PageType {
  HOME = 'home',
  NEWS = 'news',
  ARTICLE = 'article',
  ABOUT = 'about',
  SUPPORT = 'support',
  FRIENDS = 'friends',
  TEAM = 'team',
  FAQ = 'faq',
  CONTACT = 'contact',
  PRODUCTS = 'products',
  ERROR_404 = '404',
}

export interface PageLinkData {
  type: PageType;
  label: string;
  url: string;
}

export const urls = {
  pola: {
    home: '/',
    news: '/news',
    about: '/about',
    support: '/support',
    friends: '/friends',
    team: '/join',
    faq: '/faq',
    contact: '/contact',
    products: '/products',
  },
  external: {
    openFoods: new URL('https://pl.openfoodfacts.org/'),
    polaGooglePlay: new URL('https://play.google.com/store/apps/details?id=pl.pola_app'),
    polaAppStore: new URL('https://itunes.apple.com/us/app/pola.-zabierz-ja-na-zakupy/id1038401148?ls=1&amp;mt=8'),
    polaGitHub: new URL('https://github.com/KlubJagiellonski'),
    polaPrivacyPolicy: new URL('https://pola-app.s3.amazonaws.com/docs/polityka_prywatnosci.pdf'),
    klubJagiellonski: new URL('https://klubjagiellonski.pl/projekty/centrum-analiz/'),
    instytutLogistyki: new URL('https://ilim.lukasiewicz.gov.pl/'),
    mojePanstwo: new URL('https://mojepanstwo.pl/'),
    polaSocialMedia: {
      facebook: new URL('https://www.facebook.com/app.pola'),
      twitter: new URL('https://twitter.com/pola_app'),
      instagram: new URL('https://www.instagram.com/pola_skanuj_zakupy/'),
    },
  },
};

export const pageLinks: PageLinkData[] = [
  { type: PageType.HOME, label: 'Home', url: urls.pola.home },
  { type: PageType.NEWS, label: 'Aktualności', url: urls.pola.news },
  { type: PageType.ABOUT, label: 'O Poli', url: urls.pola.about },
  { type: PageType.SUPPORT, label: 'Wesprzyj aplikację', url: urls.pola.support },
  { type: PageType.FRIENDS, label: 'Klub przyjaciół Poli', url: urls.pola.friends },
  { type: PageType.TEAM, label: 'Dołącz do zespołu', url: urls.pola.team },
  { type: PageType.FAQ, label: 'FAQ', url: urls.pola.faq },
  { type: PageType.CONTACT, label: 'Kontakt', url: urls.pola.contact },
];

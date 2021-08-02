import { IPartner } from '.';
import { urls } from '../website';

const partners: IPartner[] = [
  {
    name: 'Klub Jagielloński',
    imageSrc: 'logo_cakjv2_crop.png',
    description: 'Algorytm',
    sourceUrl: urls.external.klubJagiellonski.href,
  },
  {
    name: 'Instytut Logistyki i Magazynowania',
    imageSrc: 'logo_logistyka.png',
    description: 'Baza kodów kreskowych i producentów',
    sourceUrl: urls.external.instytutLogistyki.href,
  },
  {
    name: 'Koduj dla Polski',
    imageSrc: 'logo_kodujdlapolski.png',
    description: 'Otwarte spotkania projektowe dla programistów',
    sourceUrl: urls.external.mojePanstwo.href,
  },
];

export const PartnerService = {
  getAll: (): IPartner[] => partners,
};

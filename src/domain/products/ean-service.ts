import axios from 'axios';
import { IProductEAN, IProductMock } from '.';
import { ApiService } from '../../services/api-service';

export interface IProductEANParams {
  code: string;
}

export interface IProductEANError {
  error: unknown;
}

const MOCK_PRODUCT_EAN_API = 'https://fakestoreapi.com/products';
const PRODUCT_EAN_API =
  'https://www.pola-app.pl/a/v3/get_by_code?code=4006985902304&device_id=WEB-x4815scljgh086gbivo9vd4yytu6tmwm';

export class ProductEANService extends ApiService {
  public static getInstance(): ProductEANService {
    if (!ProductEANService.instance) {
      ProductEANService.instance = new ProductEANService();
    }
    return ProductEANService.instance;
  }
  private static instance: ProductEANService;

  private constructor() {
    super(MOCK_PRODUCT_EAN_API);
  }

  public async getProduct(code: string): Promise<IProductEAN> {
    const response = await axios.get(`${this.apiUrl}/${code}`);
    const product: IProductMock = response.data;

    return {
      product_id: parseInt(product.id),
      code,
      name: product.title,
      plScore: 0,
      report_text: 'Zgłoś',
      report_button_type: 'report button',
      report_button_text: 'Zgłoś informacje o tym produkcie',
      donate: {
        show_button: true,
        title: 'Potrzebujemy 1 zł',
        url: 'https://klubjagiellonski.pl/zbiorka/wspieraj-aplikacje-pola/',
      },
    };
  }
}

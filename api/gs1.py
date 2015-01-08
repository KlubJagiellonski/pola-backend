import json
import logging

import httplib2
from kupujpolskie.settings import GS1_API_KEY


logger = logging.getLogger(__name__)

class GS1Api:
    GS1_HOST = 'http://api3.produktywsieci.pl/PublicService.svc/rest/json/'

    @classmethod
    def get_product_by_gtin(cls, barcode):
        h = httplib2.Http()
        resp, content = h.request(GS1Api.GS1_HOST + "GetProductByGTIN" + "?gs1Key=" + GS1_API_KEY + "&gtin=" + barcode,
                                  "GET")
        logger.info('GS1 resp:' + str(resp) + ", content:" + str(content))
        return json.loads(content)
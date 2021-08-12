from django.core import signing
from django.core.paginator import InvalidPage, Page, Paginator
from django.core.signing import BadSignature


class InvalidPageToken(InvalidPage):
    pass


class TokenizedPage(Page):
    def next_page_token(self):
        return signing.dumps({"page_num": self.next_page_number()}, compress=True, salt=self.paginator.token_salt)


class TokenizedPaginator(Paginator):
    def __init__(self, *args, token_salt='search', **kwargs):
        super().__init__(*args, **kwargs)
        self.token_salt = token_salt

    def _get_page(self, *args, **kwargs):
        return TokenizedPage(*args, **kwargs)

    def get_page_by_token(self, page_token=None):
        return self.get_page(self._page_token_to_page_num(page_token))

    def _page_token_to_page_num(self, page_token):
        if not page_token:
            return 1
        try:
            msg = signing.loads(page_token, salt=self.token_salt)
            if not isinstance(msg, dict):
                return 1
            return msg.get('page_num', 1)
        except BadSignature:
            raise InvalidPageToken("Invalid page token")

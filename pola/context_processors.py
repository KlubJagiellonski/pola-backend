import os

GITHUB_LINK_FORMAT = "https://github.com/KlubJagiellonski/pola-backend/commit/{}"


def release_info(request):
    release_sha = os.environ.get("RELEASE_SHA")
    return {
        'release_sha': release_sha or "unknown",
        'release_link': GITHUB_LINK_FORMAT.format(release_sha) if release_sha else "unknown",
    }

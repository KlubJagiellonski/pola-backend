import re
import reversion
from .models import Report


COMMAND_REGEXP = re.compile(r'(?P<command>\w+)\s?\#(?P<pk>[0-9]+)', re.I)


def on_revision_commit(instances, revision, **kwargs):
    comment = revision.comment
    search = COMMAND_REGEXP.search(comment)
    if not search:
        return

    command = search.group('command')
    pk = search.group('pk')

    if command.lower() == 'close':
        handle_command_close(revision, command, pk)

reversion.post_revision_commit.connect(on_revision_commit)


def handle_command_close(revision, command, pk):
    report = Report.objects.only_open().get(pk=pk)

    if report:
        report.resolve(revision.user)

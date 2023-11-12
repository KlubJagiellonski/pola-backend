from pola.report.models import Report


def create_bot_report(product, description, check_if_already_exists=False):
    if (
        check_if_already_exists
        and Report.objects.filter(product=product, client='krs-bot', description=description).exists()
    ):
        return

    report = Report(description=description)
    report.product = product
    report.client = 'krs-bot'
    report.save()

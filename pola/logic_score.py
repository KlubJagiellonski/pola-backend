def get_pl_score(company):
    if (
        company.plCapital is not None
        and company.plWorkers is not None
        and company.plRnD is not None
        and company.plRegistered is not None
        and company.plNotGlobEnt is not None
    ):
        return int(
            0.35 * company.plCapital
            + 0.30 * company.plWorkers
            + 0.15 * company.plRnD
            + 0.10 * company.plRegistered
            + 0.10 * company.plNotGlobEnt
        )
    else:
        return None

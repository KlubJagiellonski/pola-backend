-- company
select to_char(reversion_revision.date_created, 'YYYY-MM'), username, count(*)
from users_user
join reversion_revision on users_user.id=user_id
join reversion_version on reversion_revision.id = reversion_version.revision_id
where reversion_version.content_type_id=16
group by to_char(reversion_revision.date_created, 'YYYY-MM'), username
order by 1 desc, 3 desc;

-- product
select to_char(reversion_revision.date_created, 'YYYY-MM'), username, count(*)
from users_user
join reversion_revision on users_user.id=user_id
join reversion_version on reversion_revision.id = reversion_version.revision_id
where reversion_version.content_type_id=15
group by to_char(reversion_revision.date_created, 'YYYY-MM'), username
order by 1 desc, 3 desc;

-- report
select to_char(report_report.resolved_at, 'YYYY-MM'), username, count(*)
from users_user
join report_report on users_user.id=report_report.resolved_by_id
group by to_char(report_report.resolved_at, 'YYYY-MM'), username
order by 1 desc, 3 desc;

-- requery ilim
select to_char(ilim_queried_at, 'YYYY-MM-DD'), count(*)
from product_product
group by to_char(ilim_queried_at, 'YYYY-MM-DD')
order by 1 desc;

select name from company_company where "plCapital"=0 and "plNotGlobEnt"=100;

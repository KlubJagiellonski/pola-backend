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

-- look for escaped characters in database
select name, official_name, common_name, address
from company_company
where name like '%&%;%' or
official_name like '%&%;%' or
common_name like '%&%;%' OR
address like '%&%;%'
;

update product_product set query_count = (select count(*) from pola_query where pola_query.product_id=product_product.id);

SELECT "company_company"."id", "company_company"."name", SUM("product_product"."query_count") AS "query_count"
FROM "company_company" JOIN "product_product" ON ( "company_company"."id" = "product_product"."company_id" )
WHERE "company_company"."verified" = false
GROUP BY "company_company"."id", "company_company"."name"
ORDER BY "query_count" DESC LIMIT 10;

update product_product
set query_count = count(query_count.id)
from pola_query
where pola_query.product_id = product_product.id;


select code,query_count,name from product_product where query_count>0 and company_id is null and code like '590%'
order by query_count desc;

select count(*) from company_company;
select count(*) from pola_query;
select count(*) from pola_stats;
select count(*) from product_product;
select count(*) from report_attachment;
select count(*) from report_report;
select count(*) from reversion_revision;
select count(*) from reversion_version;


select to_char(date_created, 'YYYY-MM'), count(*)
from reversion_revision
group by to_char(date_created, 'YYYY-MM')
order by 1 desc;


select to_char(date_created, 'YYYY-MM'), user_id, content_type_id, count(*)
from reversion_version
left outer join reversion_revision on reversion_revision.id = reversion_version.revision_id
group by to_char(reversion_revision.date_created, 'YYYY-MM'), user_id, content_type_id
order by 1 desc, 2 desc, 3 desc;

select user_id, content_type_id, comment, count(*)
from reversion_version
full join reversion_revision on reversion_revision.id = reversion_version.revision_id
group by user_id, content_type_id, comment
order by 4 desc limit 20;


select comment
from reversion_version
join reversion_revision on reversion_revision.id = reversion_version.revision_id
where content_type_id=16 and object_id_int=711
order by date_created desc limit 10;

select count(*) from reversion_revision
where id not in (select revision_id from reversion_version);


select name, query_count from company_company where "plCapital"=100 and "plWorkers"=100 and "plRnD"=100 and "plRegistered"=100 and "plNotGlobEnt"=100
order by query_count desc limit 100;

SELECT relname,n_live_tup
  FROM pg_stat_user_tables where n_Live_tup>250
  ORDER BY n_live_tup DESC;

select sum(n_live_tup) from pg_stat_user_tables;

select product_id,count(*) from report_report
 join report_attachment on report_attachment.report_id = report_report.id
group by product_id order by count(*) desc;

update product_product set query_count = (select count(id)
from pola_query
where pola_query.product_id=product_product.id)


  select count(*) from product_product
  where query_count <4 and company_id is null and (select count(*) from report_report where report_report.product_id=product_product.id)=0;

select date_part('year', created_at) as year, date_part('month', created_at) as month, count(*)
from product_product
group by year, month
order by 1,2;

SELECT schemaname,relname,n_live_tup
  FROM pg_stat_user_tables
  ORDER BY n_live_tup DESC limit 4;

 schemaname |      relname       | n_live_tup
------------+--------------------+------------
 public     | pola_query         |   10772597
 public     | product_product    |    6099783
 public     | reversion_version  |    4880335
 public     | reversion_revision |    4876212
 public     | report_attachment  |     144507
 public     | report_report      |     111171
(6 rows)


SELECT count(*)
FROM product_product
WHERE company_id IS NULL AND name IS NULL
 AND (select count(*) from report_report where product_id=product_product.id)=0
 AND (select count(*) from ai_pics_aipics where product_id=product_product.id)=0
 AND (select count(*) from pola_query where product_id=product_product.id) <
 (12*date_part('year',age(created_at))+ date_part('month',age(created_at)))
limit 10;

SELECT product_product.code, name, count(*) as cnt
FROM product_product
join ai_pics_aipics on product_product.id = product_id
join ai_pics_aiattachment on ai_pics_aipics.id = ai_pics_id
where product_product.name is not null and (is_valid=TRUE OR is_valid is NULL)
group by product_product.code, name
order by cnt desc
limit 10;

select date_part('year', created_at) as year, date_part('week', created_at) as week, count(*)
from ai_pics_aipics
join ai_pics_aiattachment on ai_pics_aipics.id=ai_pics_aiattachment.ai_pics_id
group by year, week
order by 1,2;

select sum(query_count), sum(query_count*enough_ai_pics) from
(
select count(distinct pola_query.id) as query_count,
case when count(distinct ai_pics_aiattachment.id)>20 then 1 else 0 end as enough_ai_pics
from product_product
join pola_query on product_product.id=pola_query.product_id
left outer join ai_pics_aipics on product_product.id = ai_pics_aipics.product_id
left outer join ai_pics_aiattachment on ai_pics_aipics.id = ai_pics_id
where pola_query.timestamp > current_timestamp - interval '1 day'
group by product_product.id, product_product.name
) as sub;

select date_part('year', timestamp) as year, date_part('month', timestamp) as month,
(100.0 * count(CASE WHEN was_590 THEN 1 END)/count(*))::numeric(5,2) as "c590",
(100.0 * count(CASE WHEN "was_plScore" THEN 1 END)/count(*))::numeric(5,2) as "plScore",
(100.0 * count(CASE WHEN was_verified THEN 1 END)/count(*))::numeric(5,2) as "was_verified",
count(*)
from pola_query
where timestamp > '05-01-2018'
group by year, month
order by 1,2;

select date_part('year', created_at) as year, date_part('month', created_at) as month,
--(100.0 * count(CASE WHEN company_id is null THEN 1 END)/count(*))::numeric(5,2) as "null_company",
count(*)
from product_product
where created_at > '05-01-2018'
group by year, month
order by 1,2;

SELECT id, code,
(select count(*) from pola_query where product_id=product_product.id),
(12 * date_part('year', age(created_at)) + date_part('month', age(created_at))),
date_part('year', age(created_at)), date_part('month', age(created_at))
FROM product_product
WHERE company_id IS NULL AND name IS NULL
AND (select count(*) from report_report where product_id=product_product.id) = 0
AND (select count(*) from ai_pics_aipics where product_id=product_product.id)=0
AND created_at > '10-01-2018'
order by 3
limit 100;

                SELECT count(id)
                FROM product_product
                WHERE company_id IS NULL AND name IS NULL
                AND (select count(*) from report_report where product_id=product_product.id) = 0
                AND (select count(*) from ai_pics_aipics where product_id=product_product.id)=0
                AND (
                select count(*) from pola_query where product_id=product_product.id
                ) <
                2* (
                12 * date_part('year', age(created_at)) + date_part('month', age(created_at))
                ) ;

# find duplicate company names

select id, name, common_name, official_name, query_count from company_company ou
where (select count(*) from company_company inr where inr.name = ou.name) > 1
order by name;

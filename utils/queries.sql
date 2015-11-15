select username, count(*) from users_user join reversion_revision
on users_user.id=user_id group by username order by 2 desc;

select name from company_company where "plCapital"=0 and "plNotGlobEnt"=100;
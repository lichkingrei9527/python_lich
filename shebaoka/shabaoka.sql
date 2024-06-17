# 原始表
select * from lich_sbk order by 制卡日期;
#去重日期排序
select distinct 卡号,客户名称,营销机构号,营销人,制卡日期
    from lich_sbk
    where  制卡日期 between "2023-08-01" and "2023-09-01"
    order by 制卡日期 ;
#去重机构号排序
select distinct 卡号,客户名称,营销机构号,营销人,制卡日期
    from lich_sbk
    where  制卡日期 between "2023-08-01" and "2023-09-01"
    order by 营销机构号 ;


select count(*),营销机构号 from lich_sbk where 制卡日期 between "2023-08-01" and "2023-09-01"
    group by 营销机构号
    order by 营销机构号 ;

select count(*),营销机构号,营销人
    from lich_sbk where 制卡日期 between "2023-08-01" and "2023-09-01"
    group by 营销机构号,营销人
    order by 营销机构号;


select  * from lich_base_jgh;

#去重 关联机构号
select a.卡号,a.营销机构号,a.营销人,b.机构名称,a.制卡日期
    from (select distinct 卡号,营销机构号,营销人,制卡日期
        from lich_sbk
        where 制卡日期 between "2023-08-01" and "2023-09-01") a
        left join  lich_base_jgh b
    on a.营销机构号 = b.机构号;

#机构名称 统计
select count(*),b.机构名称,a.营销机构号
    from (select distinct 卡号,营销机构号,营销人,制卡日期
        from lich_sbk
        where 制卡日期 between "2023-08-01" and "2023-09-01") a
        left join  lich_base_jgh b
    on a.营销机构号 = b.机构号
    group by b.机构名称,a.营销机构号;
#营销人 统计
select count(*),b.机构名称,a.营销人
    from (select distinct 卡号,营销机构号,营销人,制卡日期
        from lich_sbk
        where 制卡日期 between "2023-08-01" and "2023-09-01") a
        left join  lich_base_jgh b
    on a.营销机构号 = b.机构号
    group by a.营销人, b.机构名称;



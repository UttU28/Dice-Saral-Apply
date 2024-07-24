-- select * from allData;
-- select * from myQueue;
-- select * from applyQueue;
-- select * from resumeList;

select COUNT(*) from allData;
select COUNT(*) from myQueue;
select COUNT(*) from applyQueue;
select COUNT(*) from resumeList;

-- drop table applyQueue;
-- drop table myQueue;
-- drop table allData;
-- drop table resumeList;

-- select * from resumeList;
-- select * from applyQueue;
-- select * from myQueue;

-- delete from myQueue;
-- select * from myQueue;
-- select * from applyQueue;
-- select count(*) from allData;
-- select count(*) from myQueue;
-- select count(*) from applyQueue;

-- QUERY TO SHOW ALL THE MYQUEUE DATA
-- select allData.id, allData.title, myQueue.timeOfArrival from allData JOIN myQueue ON allData.id = myQueue.id ORDER BY myQueue.timeOfArrival ASC;
-- SELECT COUNT(*) FROM allData JOIN myQueue ON allData.id = myQueue.id;

-- INSERT INTO allData (id, title, location, company, description, datePosted, dateUpdated, myStatus, decisionTime)
-- VALUES ('11111', 'this Is Title', 'location', 'company', 'description', 1721590526, 1721590528, 'pending', NULL);

-- INSERT INTO myQueue (id, title, timeOfArrival)
-- VALUES ('11111', 'this Is Title', 1721590526);


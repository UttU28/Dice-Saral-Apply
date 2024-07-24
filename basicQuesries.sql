-- select * from allData;
-- select * from myQueue;
-- select * from applyQueue;
-- select * from resumeList;

select COUNT(*) from allData;
select COUNT(*) from myQueue;
select COUNT(*) from applyQueue;
select COUNT(*) from resumeList;

-- SAFE!! Delete Table DATA
-- DELETE FROM applyQueue;
-- DELETE FROM myQueue;
-- DELETE FROM allData;
-- DELETE FROM resumeList;

-- LAVDA LAGI JASE!! Delete Whole TABLE
-- DROP TABLE applyQueue;
-- DROP TABLE myQueue;
-- DROP TABLE allData;
-- DROP TABLE resumeList;



-- QUERY TO SHOW ALL THE MYQUEUE DATA
-- select allData.id, allData.title, myQueue.timeOfArrival from allData JOIN myQueue ON allData.id = myQueue.id ORDER BY myQueue.timeOfArrival ASC;
-- SELECT COUNT(*) FROM allData JOIN myQueue ON allData.id = myQueue.id;

-- INSERT INTO allData (id, title, location, company, description, datePosted, dateUpdated, myStatus, decisionTime)
-- VALUES ('11111', 'this Is Title', 'location', 'company', 'description', 1721590526, 1721590528, 'pending', NULL);

-- INSERT INTO myQueue (id, title, timeOfArrival)
-- VALUES ('11111', 'this Is Title', 1721590526);


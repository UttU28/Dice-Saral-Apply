-- select * from allData;
-- select * from myQueue;
-- delete from allData;
-- delete from applyQueue;
-- delete from myQueue;
-- delete from resumeList;
-- truncate TABLE resumeList;
-- select * from resumeList;
select * from applyQueue;
-- select * from myQueue;

-- QUERY TO SHOW ALL THE MYQUEUE DATA
-- select allData.id, allData.title, myQueue.timeOfArrival from allData JOIN myQueue ON allData.id = myQueue.id ORDER BY myQueue.timeOfArrival ASC;
-- SELECT COUNT(*) FROM allData JOIN myQueue ON allData.id = myQueue.id;

-- INSERT INTO allData (id, title, location, company, description, datePosted, dateUpdated, myStatus, decisionTime)
-- VALUES ('11111', 'this Is Title', 'location', 'company', 'description', 1721590526, 1721590528, 'pending', NULL);

-- INSERT INTO myQueue (id, title, timeOfArrival)
-- VALUES ('11111', 'this Is Title', 1721590526);


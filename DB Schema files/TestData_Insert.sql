-- Administrator --
insert into auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
	values ('servicelearning4life', '2016-11-20', 1, 'lisa@servicelearning.com', 'Lisa', 'Service', '', 0, 1, '2016-08-12');

-- Students --
insert into auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
	values ('password123', '2016-11-20', 0, 'barde.s@husky.neu.edu', 'Sameer', 'Barde', '', 0, 1, '2016-09-01' );

insert into auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
	values ('password123', '2016-11-20', 0, 'chen.jo@husky.neu.edu', 'Joe', 'Chen', '', 0, 1, '2016-09-01');

insert into auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
	values ('password123', '2016-11-20', 0, 'starr.l@husky.neu.edu', 'Luke', 'Starr', '', 0, 1, '2016-09-01');
    
insert into auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
	values ('password123', '2016-11-24', 0, 'lough.r@husky.neu.edu', 'Ryan', 'Lough', '', 0, 1, '2016-09-01');

insert into auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
	values ('password123', '2016-11-20', 0, 'tsapakos.t@husky.neu.edu', 'Theodore', 'Tsapakos', '', 0, 1, '2016-09-01');

insert into auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
	values ('password123', '2016-11-10', 0, 'kaasila.e@husky.neu.edu', 'Erik', 'Kaasila', '', 0, 1, '2016-09-01');
    
-- Instructor --
insert into auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
	values ('password123', '2016-11-10', 0, 'weintraub.m@northeastern.edu', 'Michael', 'Weintraub', '', 1, 1, '2016-09-01');

insert into auth_user (password, last_login, is_superuser, username, first_name, last_name, email, is_staff, is_active, date_joined)
	values ('password123', '2016-11-10', 0, 'james.k@northeastern.edu', 'Kevin', 'James', '', 1, 1, '2016-09-01');
    

-- College --
insert into College (name)
	values ('College of Computer and Information Science');
    
insert into College (name)
	values ('D\'Amore-McKim School of Business');
    
insert into College (name)
	values ('College of Science');
    
insert into College (name)
	values ('Bouvé College of Health Sciences');
    
insert into College (name)
	values ('School of Law');

-- Department --
insert into Department (name, college_id)
	values ('Computer Science' , 'College of Computer and Information Science');
    
insert into Department (name, college_id)
	values ('Biology' , 'College of Science');

insert into Department (name, college_id)
	values ('Mathematics' , 'College of Science');
    

-- Course --
insert into Course (id, name, department_id)
	values ('CS4500', 'Software Development', 'Computer Science');

insert into Course (id, name, department_id)
	values ('CS1200', 'Overview 1', 'Computer Science');
    
-- Semester --
insert into Semester (name, start_date, end_date, is_active)
	values ('FALL2016', '2016-08-31', '2016-12-25', true);
    
insert into Semester (name, start_date, end_date, is_active)
	values ('SPRING2017', '2017-01-08', '2017-06-01', false);


-- Enrollment --
insert into Enrollment (user_id, course_id, semester_id, project_id, crn, is_active)
	values (2, 'CS4500', 'FALL2016', null, '12235', true);
	
insert into Enrollment (user_id, course_id, semester_id, project_id, crn, is_active)
	values (3, 'CS1200', 'SPRING2017', null, '44221', false);
	
insert into Enrollment (user_id, course_id, semester_id, project_id, crn, is_active)
	values (8, 'CS4500', 'FALL2016', 2, '56323', true);
	
-- Community Partner --
insert into Community_Partner (name)
	values ('Service Learning');
	
insert into Community_Partner (name)
	values ('America Scores');
	
-- Project --
insert into Project (name, course_id, community_partner_id, start_date, end_date, description, longitude, latitude)
	values ('TimeTracker', 'CS4500', "DS", '2016-09-01', '2016-12-20', 'Time Tracker device for Service Learning', 42.3398, 71.0892);
	
insert into Project (name, course_id, community_partner_id, start_date, end_date, description, longitude, latitude)
	values ('America Scores', 'CS4500', "DS", '2016-01-01', '2017-01-01', null, null, null);
	
-- Record_Category --
insert into Record_Category (name)
	values ('Direct Service');

insert into Record_Category (name)
	values ('Training Events');
	
insert into Record_Category (name)
	values ('Individual Planning/Research/Projects');
	
insert into Record_Category (name)
	values ('Team Planning/Group Work');
	
-- Record --
insert into Record (enrollment_id, project_id, date, start_time, total_hours, longitude, latitude, category_id, is_active, comments, extra_field)
	values (1 , 1001, '2016-08-25', null, 3, null, null, 2, true, 'Worked at Project A', null);
	
insert into Record (enrollment_id, project_id, date, start_time, total_hours, longitude, latitude, category_id, is_active, comments, extra_field)
	values (2, 1001, '2016-08-25', '08:00', 8.3, null, null, 2, true, 'Worked at Project A', null);
	
insert into Record (enrollment_id, project_id, date, start_time, total_hours, longitude, latitude, category_id, is_active, comments, extra_field)
	values (1, 1001, '2016-08-25', '08:00', 10, 42.3399, 71.0891, 2, false, 'Worked at Project A', null);
	
insert into Record (enrollment_id, project_id, date, start_time, total_hours, longitude, latitude, category_id, is_active, comments, extra_field)
	values (1, 1001, '2016-08-28', '08:00', 1.20, 42.3399, 71.0891, 2, true, 'Worked at Project A', null);
	
insert into Record (enrollment_id, project_id, date, start_time, total_hours, longitude, latitude, category_id, is_active, comments, extra_field)
	values (2, 1002, '2016-08-25', '08:00', 5.4, null, null, 2, false, 'Worked at Project B', null);
	
insert into Record (enrollment_id, project_id, date, start_time, total_hours, longitude, latitude, category_id, is_active, comments, extra_field)
	values (1, 1002, '2016-10-25', '11:00', 5, null, null, 2, true, null, null);
	
insert into Record (enrollment_id, project_id, date, start_time, total_hours, longitude, latitude, category_id, is_active, comments, extra_field)
	values (1, 1002, '2016-09-28', '08:00', 4, 42.3399, 71.0881, 2, false, 'Worked at Project B', null);

insert into Record (enrollment_id, project_id, date, start_time, total_hours, longitude, latitude, category_id, is_active, comments, extra_field)
	values (1, 1002, '2016-09-28', '08:00', 10, 42.3299, 71.0884, 2, true, 'Worked at Project B', null);

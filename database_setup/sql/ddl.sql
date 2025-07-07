/*
* Create tables
*/
create table dof.oas (
	code char(2) primary key,
	name varchar(100) not null
);

create table dof.country (
	oas_code char(2) primary key,
	boundary geography(MULTIPOLYGON, 4326),
	foreign key (oas_code) references dof.oas(code)
);

create table dof.us_state (
	oas_code char(2) primary key,
	boundary geography(MULTIPOLYGON, 4326),
	foreign key (oas_code) references dof.oas(code)
);

create table dof.tolerance_uom (
	id smallserial primary key,
	uom varchar(5) not null
);

create table dof.horizontal_acc (
	code smallint primary key,
	tolerance_uom_id smallint not null,
	tolerance numeric(5, 1) not null,
	foreign key (tolerance_uom_id) references dof.tolerance_uom(id)
);

create table dof.vertical_acc (
	code char(1) primary key,
	tolerance_uom_id smallint not null,
	tolerance numeric(5, 1) not null,
	foreign key (tolerance_uom_id) references dof.tolerance_uom(id)
);

create table dof.lighting (
	code char(1) primary key,
	description varchar(35) not null unique
);

create table dof.marking (
	code char(1) primary key,
	description varchar(35) not null unique
);

create table dof.obstacle_type (
	id smallserial primary key,
	type varchar(50) not null unique
);

create table dof.verif_status (
	code char(1) primary key,
	description varchar(20) not null
);

create table dof.obstacle (
	oas_code char(2) not null,
	obst_number char(6) not null,
	verif_status_code char(1) not null,
	type_id smallint not null,
	lighting_code char(1) not null,
	marking_code char(1) not null,
	hor_acc_code smallint not null,
	vert_acc_code char(1) not null,
	city varchar(20) not null,
	quantity smallint null,
	agl numeric(5, 2) null,
	amsl numeric(5, 2) not null,
	faa_study_number char(14) null,
	action char(1) not null,
	julian_date char(7) null,
	valid_from date not null,
	valid_to date not null default '2099-12-31',
	insert_user char(4) not null default current_user,
	mod_user char(4) null,
	insert_timestamp timestamp not null,
	mod_timestamp timestamp null,
	location geography(POINT, 4326),
	foreign key (oas_code) references dof.oas(code),
	foreign key (verif_status_code) references dof.verif_status(code),
	foreign key (type_id) references dof.obstacle_type(id),
	foreign key (lighting_code) references dof.lighting(code),
	foreign key (marking_code) references dof.marking(code),
	foreign key (hor_acc_code) references dof.horizontal_acc(code),
	foreign key (vert_acc_code) references dof.vertical_acc(code)
);


create table dof.dof_conf (
    file_type character(3) primary key,
    revision_date date not null,
    settings json not null
);
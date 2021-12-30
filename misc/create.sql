-- users
CREATE TABLE IF NOT EXISTS "users" (
	"id"	        INTEGER NOT NULL UNIQUE,
	"email"	        TEXT NOT NULL UNIQUE,
	"contact"		TEXT NOT NULL,
	"hash"	        TEXT NOT NULL,
	"role"	        TEXT NOT NULL,
	"first_name"	TEXT NOT NULL,
	"middle_name"	TEXT NOT NULL,
	"last_name"     TEXT NOT NULL,
	"gender"		TEXT NOT NULL,
	"dob"			TEXT NOT NULL,
	"registered"	TEXT NOT NULL,
	"verified"	    NUMERIC NOT NULL DEFAULT 0,
	"approved"	    NUMERIC NOT NULL DEFAULT 0,
	"approved_by"	INTEGER,
	"address_id"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);

-- addresses
CREATE TABLE IF NOT EXISTS "addresses" (
	"id"			INTEGER NOT NULL UNIQUE,
	"line_1"		TEXT NOT NULL,
	"line_2"		TEXT,
	"landmark"		TEXT,
	"city"			TEXT NOT NULL,
	"district"		TEXT NOT NULL,
	"state"			TEXT NOT NULL,
	"pin"			TEXT NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);

-- questions
CREATE TABLE IF NOT EXISTS "questions" (
	"id"			INTEGER NOT NULL UNIQUE,
	"question"		TEXT NOT NULL UNIQUE,
	"option_a"		TEXT NOT NULL,
	"option_b"		TEXT NOT NULL,
	"option_c"		TEXT NOT NULL,
	"option_d"		TEXT NOT NULL,
	"answer"		TEXT NOT NULL,
	"updated_by"	INTEGER NOT NULL,
	PRIMARY KEY("id" AUTOINCREMENT)
);

-- tests
CREATE TABLE IF NOT EXISTS "tests" (
	"id"			INTEGER NOT NULL UNIQUE,
	"taken_by"		INTEGER NOT NULL,
	"max"			INTEGER NOT NULL,
	"attempted"		INTEGER NOT NULL,
	"correct"		INTEGER NOT NULL,
	"start"			TEXT,
	"end"			TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);

-- feedbacks
CREATE TABLE IF NOT EXISTS "feedbacks" (
	"id"				INTEGER NOT NULL UNIQUE,
	"provided_by"		INTEGER NOT NULL,
	"rating"			INTEGER NOT NULL,
	"recommendation"	INTEGER NOT NULL,
	"comments"			TEXT,
	PRIMARY KEY("id" AUTOINCREMENT)
);
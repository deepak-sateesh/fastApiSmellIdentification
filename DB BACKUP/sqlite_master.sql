insert into MY_TABLE (type, name, tbl_name, rootpage, sql) values ('table', 'Rule', 'Rule', 2, 'CREATE TABLE Rule
(
    Rule_name    TEXT default NULL,
    Phrase       TEXT,
    If_Condition TEXT,
    Then_Rule    TEXT
)');
insert into MY_TABLE (type, name, tbl_name, rootpage, sql) values ('table', 'Condition', 'Condition', 3, 'CREATE TABLE "Condition"
(
    Condition_Name TEXT,
    Noun1          TEXT,
    Noun2          TEXT,
    Diagram        TEXT
)');
insert into MY_TABLE (type, name, tbl_name, rootpage, sql) values ('table', 'Noun', 'Noun', 4, 'CREATE TABLE Noun
(
    Noun_Name TEXT
, Known_Noun TEXT, Rule_Name TEXT)');
insert into MY_TABLE (type, name, tbl_name, rootpage, sql) values ('table', 'Known_Noun', 'Known_Noun', 5, 'CREATE TABLE Known_Noun
(
    Noun_Name        TEXT,
    Noun_Description TEXT
)');
insert into MY_TABLE (type, name, tbl_name, rootpage, sql) values ('table', 'Verb', 'Verb', 7, 'CREATE TABLE Verb
(
    Verb_Name        TEXT,
    Verb_Description TEXT
)');
insert into MY_TABLE (type, name, tbl_name, rootpage, sql) values ('table', 'Modal_Verb', 'Modal_Verb', 8, 'CREATE TABLE Modal_Verb
(
    Modal_Verb_Name        TEXT,
    Modal_Verb_Description TEXT,
    Positive_or_Negative   INT
)');
insert into MY_TABLE (type, name, tbl_name, rootpage, sql) values ('table', 'Diagram', 'Diagram', 9, 'CREATE TABLE Diagram
(
    Diagram_Name    TEXT,
    NounOrVerb_Name TEXT
)');
insert into MY_TABLE (type, name, tbl_name, rootpage, sql) values ('table', 'Phrase', 'Phrase', 10, 'CREATE TABLE "Phrase"
(
    Phrase_Name TEXT,
    Noun1       TEXT,
    Modal_Verb  TEXT,
    Verb        TEXT,
    Diagram     TEXT,
    Noun2       TEXT
)');

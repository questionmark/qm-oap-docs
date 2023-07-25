A_Question_Ex
-------------

..  qm:table::  A_Question_Ex

    ..  qm:field::  Question_MID int
        :key:
        :notnull:
    
    ..  qm:field::  Question_LID int
        :key:
        :notnull:

    ..  qm:field::  Revision int
        :notnull:

    ..  qm:field::  Question_Type varchar(10)
    
    ..  qm:field::  Number_Outcomes smallint
    
    ..  qm:field::  Last_Updated datetime
    
    ..  qm:field::  Question_Description varchar(800)
    
    ..  qm:field::  Topic varchar(1020)
        :notnull:

    ..  qm:field::  Question_Wording text
    
    ..  qm:field::  Base bit
        :notnull:

    ..  qm:field::  Lang varchar(10)
        :key:
        :notnull:

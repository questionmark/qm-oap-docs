A_Session_Ex
------------

..  qm:table::  A_Session_Ex

    ..  qm:field::  Session_MID int
        :key:
        :notnull:
    
    ..  qm:field::  Session_LID int
        :key:
        :notnull:
    
    ..  qm:field::  Revision int
        :notnull:
    
    ..  qm:field::  Session_Name varchar(200)
    
    ..  qm:field::  Session_Author varchar(200)
    
    ..  qm:field::  When_Modified datetime
    
    ..  qm:field::  Whether_Time_Limit bit
        :notnull:
    
    ..  qm:field::  Time_Limit int
    
    ..  qm:field::  Number_Sections smallint
    
    ..  qm:field::  Last_Updated datetime
    
    ..  qm:field::  Assessment_Type smallint
    
    ..  qm:field::  Course varchar(1020)
    
    ..  qm:field::  Description varchar(1020)
    
    ..  qm:field::  Base bit
        :notnull:
    
    ..  qm:field::  Lang varchar(10)
        :key:
        :notnull:
    
    ..  qm:field::  Last_Updated_UTC datetime


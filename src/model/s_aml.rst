S_AML
-----

..  qm:table::  S_AML

    ..  qm:field::  Session_MID int
        :key:
        :notnull:
    
    ..  qm:field::  Session_LID int
        :key:
        :notnull:
    

    ..  qm:field::  Revision int
        :key:
        :notnull:
    

    ..  qm:field::  Editor varchar(200)
        :notnull:
    

    ..  qm:field::  Modified_Date datetime
        :notnull:
    

    ..  qm:field::  Comments varchar(4000)
    
    ..  qm:field::  AML_Data text
        :notnull:

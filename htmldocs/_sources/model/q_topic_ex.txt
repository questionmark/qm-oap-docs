Q_Topic_Ex
-----------

..  qm:table::  Q_Topic_Ex

    Basic fields are accessible through the view Q\_Topic.  The
    difference is that the view does not give access to the extended
    fields for topic translation.  These fields following the same
    pattern as other tables, for more information see
    :qm:table:`Q_Question_Ex`.

    ..  qm:field::  Topic_ID int
        :key:
        :notnull:
    
    ..  qm:field::  Parent_ID int
        :notnull:

    ..  qm:field::  Name varchar(200)
        :notnull:

    ..  qm:field::  Description varchar(1020)
    
    ..  qm:field::  Base bit
        :notnull:

    ..  qm:field::  Lang varchar(10)
        :key:
        :notnull:
    
    ..  qm:field::  Source_Lang varchar(10)
        :notnull:
    
    ..  qm:field::  Translation_Status int
        :notnull:

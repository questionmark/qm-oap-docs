Q_Question_Ex
-------------

..  qm:table::  Q_Question_Ex

    Many of these fields are also accessible through an older view
    called simple Q\_Header.  The difference is the way translations are
    handled.  Q\_Header only provides access to untranslated questions
    whereas Q\_Header_Ex introduced additional fields to indicate the
    language and translation status of the question in a similar way to
    :qm:table:`S_Header_Ex`.  Notice also that
    :qm:field:`Q_Question_Ex.Lang` is also part of the table's primary
    key and that queries using the question ID (mid/lid) and revision
    alone will not necessarily return unique records.
    
    ..  qm:field::  Question_MID int
        :key:
        :notnull:
    
    ..  qm:field::  Question_LID int
        :key:
        :notnull:

    ..  qm:field::  Revision int
        :key:
        :notnull:

    ..  qm:field::  Topic_ID int
        :notnull:

    ..  qm:field::  Author varchar(200)
    
    ..  qm:field::  Created_Date datetime
        :notnull:

    ..  qm:field::  Editor varchar(200)
        :notnull:

    ..  qm:field::  Modified_Date datetime
        :notnull:

    ..  qm:field::  Encoded smallint
        :notnull:

    ..  qm:field::  Status smallint
        :notnull:

        0.  Normal
        
        1.  Retired.  These questions are not selected for delivery when
            randomly picking questions (or selecting all) from a topic
            in a block but are delivered if included individually.
        
        2.  Incomplete.  These questions are not selected for delivery
            when randomly picking questions  (or selecting all)  from a
            topic in a block but are delivered if included individually.

        3.  Experimental.  These questions *are* selected for delivery
            but do not contribute to the test or topic score.
        
        4.  Beta.  These questions are treated as 'normal' during
            delivery.  The alternative status value is for information
            and reporting only
                
        5.  Tryout.  Used internally.

    ..  qm:field::  IRT_A float
    
    ..  qm:field::  IRT_B float
    
    ..  qm:field::  IRT_C float
    
    ..  qm:field::  P_Value float
    
    ..  qm:field::  Discrimination float
    
    ..  qm:field::  AngoffW smallint
        :notnull:

    ..  qm:field::  Lock_Question bit
        :notnull:

    ..  qm:field::  Maximum_Score smallint
        :notnull:

    ..  qm:field::  Question_Type char(10)
        :notnull:

    ..  qm:field::  Order_Num int
        :notnull:

    ..  qm:field::  Edited_By char(1)
        :notnull:

    ..  qm:field::  Description varchar(800)
        :notnull:

    ..  qm:field::  Base bit
        :notnull:
    
    ..  qm:field::  Lang varchar(10)
        :key:
        :notnull:
    
    ..  qm:field::  Source_Lang varchar(10)
        :notnull:
    
    ..  qm:field::  Translation_Status int
        :notnull:
    
    ..  qm:field::  Base_Revision int
    
    ..  qm:field::  Question_ID bigint
        :computed:
        :notnull:

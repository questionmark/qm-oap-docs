S_Header_Ex
-----------

..  qm:table::  S_Header_Ex

    Many of these fields are also accessible through an older view
    called simple S\_Header.  The difference is the way translations are
    handled.  S\_Header only provides access to untranslated assessments
    whereas S\_Header_Ex introduced the additional fields to indicate
    the language and translation status of the assessment.  Notice also
    that :qm:field:`S_Header_Ex.Lang` is also part of the table's
    primary key and that queries using the assessment ID (mid/lid) and
    revision alone will not necessarily return unique records.
    
    ..  qm:field::  Session_MID int
        :key:
        :notnull:

    ..  qm:field::  Session_LID  int
        :key:
        :notnull:

    ..  qm:field::  Revision int
        :key:
        :notnull:

    ..  qm:field::  Session_Name varchar(200)
        :notnull:

    ..  qm:field::  Author varchar(200)
    
    ..  qm:field::  Created_Date datetime
        :notnull:

    ..  qm:field::  Editor varchar(200)
        :notnull:

    ..  qm:field::  Modified_Date datetime
        :notnull:

    ..  qm:field::  Version varchar(6)
        :notnull:

    ..  qm:field::  Save_Answers bit
        :notnull:

    ..  qm:field::  Save_Answer_Data bit
        

    ..  qm:field::  Open_Session bit
        :notnull:

    ..  qm:field::  Session_Password varchar(80)
    

    ..  qm:field::  Session_Timed bit
        :notnull:

    ..  qm:field::  Time_Limit int
    

    ..  qm:field::  Template_Name varchar(200)
        :notnull:

    ..  qm:field::  When_Feedback smallint
        :notnull:

    ..  qm:field::  End_Feedback smallint
    

    ..  qm:field::  Exclude_Unscored bit
    

    ..  qm:field::  Permit_External_Call bit
    

    ..  qm:field::  Monitored smallint
    

    ..  qm:field::  Lock_Session bit
        :notnull:

    ..  qm:field::  Assessment_Type smallint
    

    ..  qm:field::  Metadata_ID int
    

    ..  qm:field::  Course_ID int
    

    ..  qm:field::  Run_From smallint
    

    ..  qm:field::  Anonymous bit
    

    ..  qm:field::  Secure bit
    

    ..  qm:field::  SAYG_Option smallint
    

    ..  qm:field::  SAYG_Timer int
    

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

    ..  qm:field::  Base_Revision int
    

    ..  qm:field::  ASSESSMENT_ID bigint
        :notnull:
        :computed:

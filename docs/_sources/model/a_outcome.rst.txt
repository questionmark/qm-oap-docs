A_Outcome_Ex and A_Outcome
--------------------------

..  qm:table::  A_Outcome_Ex

    Many of these fields are also accessible through an older view
    called simple A\_Outcome.  The difference is the way translations
    are handled.  A\_Outcome only provides access to untranslated
    assessments whereas A\_Outcome\_Ex introduced the additional fields
    to indicate the language of the translated outcome.

    ..  qm:field:: Question_MID int
        :notnull:
        :key:

    ..  qm:field:: Question_LID int
        :notnull:
        :key:

    ..  qm:field:: Outcome_Number smallint
        :notnull:
        :key:

    ..  qm:field:: Outcome_Name varchar(200)

    ..  qm:field:: Feedback text

    ..  qm:field:: Base bit
        :notnull:

    ..  qm:field:: Lang varchar(10)
        :notnull:
        :key:

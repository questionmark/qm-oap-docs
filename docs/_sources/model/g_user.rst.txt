G_User
------

..  qm:table::  G_User

    Records all administrators.  An administrator is any user that has a
    role other than the special "Participant" role within the portal.
    The table does not contain the authoritative information about the
    user but is maintained as a mirror of the key fields for backwards
    compatibility.
    
    ..  note::  Perception 5.7 and Questionmark OnDemand Classic, this
                table is authoritative.
   
    ..  qm:field::  User_ID int
        :key:
        :notnull:

        The administrator ID.

    ..  qm:field::  User_Name varchar(200)
        :notnull:

        You should pay particular attention to the issues around the
        storage of information in :ref:`varchar` concerning the encoding
        of user names with characters outside US ASCII.
        
        In addition to this transformation there are a number of further
        restrictions on which graphic characters from US ASCII are
        allowed.  The APIs don't always implement the restrictions
        consistently.  Sometimes *illegal* characters will result in an
        error and sometimes they will be swapped for similar characters
        that are allowed.  Check the documentation for the API for
        further details.        
        
    ..  qm:field::  Password nvarchar(255)
        :notnull:

    ..  qm:field::  Authenticate_Ext int
        :notnull:

    ..  qm:field::  Profile_Record smallint
        :notnull:

    ..  qm:field::  Profile_ID int
        :notnull:

    ..  qm:field::  Authoring1 int
        :notnull:

    ..  qm:field::  Authoring2 int
    
    ..  qm:field::  Admin1 int
        :notnull:

    ..  qm:field::  Admin2 int
        :notnull:

    ..  qm:field::  Admin3 int
    
    ..  qm:field::  Admin4 int
    
    ..  qm:field::  Grading int
        :notnull:

    ..  qm:field::  Reporting1 int
        :notnull:

    ..  qm:field::  Reporting2 int
    
    ..  qm:field::  Misc1 int
    
    ..  qm:field::  Misc2 int
    
    ..  qm:field::  Misc3 int
    
    ..  qm:field::  Misc4 int
    
    ..  qm:field::  Restrict_Host int
    
    ..  qm:field::  Email varchar(255)
    
    ..  qm:field::  URL varchar(255)
    
    ..  qm:field::  First_Name varchar(200)
    
    ..  qm:field::  Last_Name varchar(200)
    
    ..  qm:field::  Department varchar(200)
    
    ..  qm:field::  Alternate_Name varchar(400)
    
    ..  qm:field::  Profile_Description varchar(400)
    
    
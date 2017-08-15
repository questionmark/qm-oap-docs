Groups
------

This part of the guide is under development.  Please refer to the
`Groups <https://www.questionmark.com/content/groups>`_ section of the
old guide.

Group Methods
~~~~~~~~~~~~~

..  qm:meth::   AddGroupAdministratorList

..  qm:meth::   AddGroupParticipantList

..  qm:meth::   CreateGroup

..  qm:meth::   DeleteGroup

..  qm:meth::   DeleteGroupAdministratorList

..  qm:meth::   DeleteGroupParticipantList

..  qm:meth::   GetGroup

..  qm:meth::   GetGroupByName

..  qm:meth::   GetGroupList

..  qm:meth::   SetGroup


Group Types
~~~~~~~~~~~

..  qm:xtype::  Group
    
    ..  qm:xfield:: Group_ID string
        :optional:

    ..  qm:xfield:: Parent_ID string
        :optional:

    ..  qm:xfield:: Group_Name string
        :optional:

    ..  qm:xfield:: Description string
        :optional:

    ..  qm:xfield:: Account_Internal_Ref string
        :optional:

    ..  qm:xfield:: Account_Admin_Email string
        :optional:

    ..  qm:xfield:: Directory_Name string
        :optional:

    ..  qm:xfield:: Account_Status int

    ..  qm:xfield:: Special_1 string
        :optional:

    ..  qm:xfield:: Special_2 string
        :optional:

    ..  qm:xfield:: Special_3 string
        :optional:

    ..  qm:xfield:: Special_4 string
        :optional:

    ..  qm:xfield:: Special_5 string
        :optional:

    ..  qm:xfield:: Special_6 string
        :optional:

    ..  qm:xfield:: Special_7 string
        :optional:

    ..  qm:xfield:: Special_8 string
        :optional:

    ..  qm:xfield:: Special_9 string
        :optional:

    ..  qm:xfield:: Special_10 string
        :optional:

    ..  qm:xfield:: Max_Participants int

    ..  qm:xfield:: Max_Sessions_Attempt int

    ..  qm:xfield:: Session_Taken int

    ..  qm:xfield:: Account_Password string
        :optional:

    ..  qm:xfield:: Account_Type int

    ..  qm:xfield:: Use_Emailing int

    ..  qm:xfield:: Email_Domains string
        :optional:

    ..  qm:xfield:: Account_Finish string
        :optional:


..  qm:xtype::  GroupList

    ..  qm:xfield:: Group Group
        :optional:
        :max: unbounded    

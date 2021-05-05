Topic
-----

..  od:service::    authoringodata


..  od:feed::   Topics Topic

    :method GET: feed is read only
    :filter Id: primary key
    
    :expand QuestionRevisions: the questions in the topic

    The Topics feed contains entities that describe all Topcics within
    the item bank.  There is one entity for each topic.

..  od:type::   Topic
    
    ..  od:prop::   Id  Edm.Int32
        :key:
        :notnull:


    ..  od:prop::   Name    Edm.String

    ..  od:prop::   Path  Edm.String
    
        The full path of the Topic.

    ..  od:prop::   PublishedId  Edm.Int32

    ..  od:prop::   Language  Edm.String

    ..  od:prop::   CreatedDateTime  Edm.DateTimeOffset

        The date and time (in UTC) when the Topic was created.

    ..  od:prop::   Author  Edm.String
    
        The user name of the user that created the question

    ..  od:prop::   ModifiedDateTime  Edm.String

        The date and time (in UTC) when the Topic was last modified. 

    ..  od:prop::   Editor  Edm.String

        The user name of the user that last modified the Topic. 
        Again, this refers to the base language and not any
        translations.

    ..  od:prop::   IsDeleted  Edm.Boolean
        :notnull:
    
        A boolean set to True if the Topic has been *archived*.  In
        versions prior to 2021.05 this action was referred to as
        deletion (though such Topics are still available through the
        API and from 2021.05 can be restored in the user interface
        too).

    ..  od:prop::   QuestionRevisions  QuestionRevision
        :collection:

        

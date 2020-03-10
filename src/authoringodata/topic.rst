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

    ..  od:prop::   Path    Edm.String

    ..  od:prop::   PublishedId  Edm.Int32

    ..  od:prop::   Language  Edm.String

    ..  od:prop::   CreatedDateTime  Edm.DateTimeOffset

        The date and time (in UTC) when the Question was created.

    ..  od:prop::   Author  Edm.String
    
        The user name of the user that created the question

    ..  od:prop::   ModifiedDateTime  Edm.String

        The date and time (in UTC) when the Question was last modified. 
        This revision time refers only to the base language. 
        Modifications to any translations are represented in the related
        :od:prop:`QuestionQMLs` entities.

    ..  od:prop::   Editor  Edm.String

        The user name of the user that last modified the question. 
        Again, this refers to the base language and not any
        translations.

    ..  od:prop::   QuestionRevisions  QuestionRevision
        :collection:

        

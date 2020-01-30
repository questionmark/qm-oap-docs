QuestionRevision
----------------

..  od:service::    authoringodata


..  od:feed::   QuestionRevisions QuestionRevision

    :method GET: feed is read only
    :filter Id: primary key
    :filter QuestionId: the system-wide ID for the Question
    :filter Language: language of the Question
    :filter CreatedDateTime: when the question was created
    :filter Author: the user name of the user creating the Question
    :filter ModifiedDateTime: when the *base language* version of the question was last modified
    :filter Editor: the user name of the last user to edit the *base language* version of the Question
    
    :expand QuestionQMLs: QML entities for each available language  

    The QuestionRevisions feed contains entities that describe all revisions
    of all Questions within the item bank.  There is one entity for each
    revision of each question.

    Example request::
    
        https://ondemand.questionmark.com/authoringapi/123456/odata/QuestionRevisions?$filter=QuestionId eq 100000001323&$orderby=ModifiedDateTime desc&$top=1
    
    This request uses $orderby and $top to get the most recent revision
    of the Question with QuestionId 100000001323.  For clarity spaces
    are show unescaped in the URL.  Example response::
    
        {
            "@odata.context": "https://ondemand.questionmark.com/authoringapi/123456/odata/$metadata#QuestionRevisions",
            "value": [
                {
                    "Id": 10320,
                    "QuestionId": 100000001323,
                    "Language": "-",
                    "CreatedDateTime": "2014-12-23T10:41:29.06Z",
                    "Author": "steve",
                    "ModifiedDateTime": "2014-12-23T10:41:29.107Z",
                    "Editor": "steve",
                    "Status": "Normal",
                    "ReviewStatus": null,
                    "TopicPath": "SubjectiveQuestions",
                    "IsDeleted": false
                }
            ]
        }    


..  od:type::   QuestionRevision

    QuestionRevision entities contain only a subset of the attributes of
    a Question.  The full information about a Question is obtained from
    the associated :od:type:`QuestionQML` entities.
    
    ..  od:prop::   Id  Edm.Int32
        :key:
        :notnull:
        
        The key used within the item bank.  This value will change when
        moving Questions between banks (using QPacks) and should only be
        used in the context of a specific item bank.  A general purpose
        identifier that persists across repositories can be found in
        :od:prop:`QuestionId`.

    ..  od:prop::   QuestionId  Edm.Int64
        
        A 64-bit integer ID, sometimes represented as a string or split
        in to two integers (MID/LID) in other contexts.  When published,
        the same QuestionId is available in the delivery catalog as
        :od:prop:`deliveryodata.Question.ID`

    ..  od:prop::   Language  Edm.String

        The base language of the question.  If the language has not been
        set the string "-" is used.

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

    ..  od:prop::   Status  Edm.String

        The status of this question revision.  One of the values Normal,
        Retired or Experimental.  A change in status, e.g., from Normal
        to Retired results in a new revision.  Therefore, to find the
        *current* status of a question you must read the value from its
        most recent revision.
        
    ..  od:prop::   ReviewStatus  Edm.String

        A free-text field for tracking customer-specific status
        labels.
        
    ..  od:prop::   TopicPath  Edm.String

        The full path of the Question within the Topic hierarchy, for
        example::
        
            "RootTopic/SubTopicB/SubSubTopic1"
        
    ..  od:prop::   IsDeleted  Edm.Boolean

        A flag indicating whether or not the Question has been deleted
        from the item bank.  Deleting Questions *does not* remove them
        from the item bank, it marks them as deleted and removes from
        the user interface only.

    ..  od:prop::   QuestionQMLs  QuestionQML
        :collection:

        A navigation property to the related QuestionQML entities that
        contain detailed information about the question in each
        available language.
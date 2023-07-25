AssessmentRevision
------------------

..  od:service::    authoringodata


..  od:feed::   AssessmentRevisions AssessmentRevision

    :method GET: feed is read only
    :filter Id: primary key
    :filter AssessmentId: the system-wide ID for the Assessment
    :filter Language: language of the Assessment
    :filter CreatedDateTime: when the assessment was created
    :filter Author: the user name of the user creating the Assessment
    :filter ModifiedDateTime: when the *base language* version of the assessment was last modified
    :filter Editor: the user name of the last user to edit the *base language* version of the Assessment
    
    :expand AssessmentAMLs: AML entities for each available language  

    The AssessmentRevisions feed contains entities that describe each
    Assessment within the item bank.  There is one entity for each
    Assessment.

    ..  warning::   although this entity is called an assessment*revision*,
                    the item bank does not retain revision history for
                    assessment entities.  The entity is named in
                    anticipation of a revision history feature in future
                    versions of the Questionmark platform.

    Example request::
    
        https://ondemand.questionmark.com/authoringapi/123456/odata/AssessmentRevisions?$filter=AssessmentId eq 267000000267
    
    This request uses a simple filter to get the Assessment with
    AssessmentId 267000000267.  For clarity spaces are shown unescaped
    in the URL.  Example response::
    
        {
            "@odata.context": "https://ondemand.questionmark.com/authoringapi/123456/odata/$metadata#AssessmentRevisions",
            "value": [
                {
                    "Id": 267,
                    "AssessmentId": 267000000267,
                    "Language": "-",
                    "CreatedDateTime": "2015-03-06T11:02:11.433Z",
                    "Author": "John",
                    "ModifiedDateTime": "2019-06-25T08:24:50.07Z",
                    "Editor": "Sally",
                    "AssessmentFolderPath": "Skills",
                    "IsDeleted": false
                }
            ]
        }

..  od:type::   AssessmentRevision

    AssessmentRevision entities contain only a subset of the attributes
    of an Assessment.  The full information about an Assessment is
    obtained from the associated :od:type:`AssessmentAML` entities.
    
    There is no navigation property between AssessmentRevision and
    :od:type:`QuestionRevision`.  This may seem surprising at first but
    assessments can have a complex structure and Questions are included
    in an assessment through rules defined within this structure.  The
    structure itself is described in XML format and is obtained from the
    related :od:type:`AssessmentAML` entity.
                    
    ..  od:prop::   Id  Edm.Int32
        :key:
        :notnull:
        
        The key used within the item bank.  This value will change when
        moving Assessments between banks (using QPacks) and should only
        be used in the context of a specific item bank.  A general
        purpose identifier that persists across repositories can be
        found in :od:prop:`AssessmentId`.

    ..  od:prop::   AssessmentId  Edm.Int64
        
        A 64-bit integer ID, sometimes represented as a string or split
        in to two integers (MID/LID) in other contexts.  When published,
        the same AssessmentId is available in the delivery catalog as
        :od:prop:`deliveryodata.Assessment.ID`

    ..  od:prop::   Language  Edm.String

        The base language of the assessment.  If the language has not
        been set the string "-" is used.

    ..  od:prop::   CreatedDateTime  Edm.DateTimeOffset

        The date and time (in UTC) when the Assessment was created.

    ..  od:prop::   Author  Edm.String
    
        The user name of the user that created the assessment

    ..  od:prop::   ModifiedDateTime  Edm.String

        The date and time (in UTC) when the Assessment was last
        modified. This revision time refers only to the base language.
        Modifications to any translations are represented in the related
        :od:prop:`AssessmentAMLs` entities.

    ..  od:prop::   Editor  Edm.String

        The user name of the user that last modified the assessment.
        Again, this refers to the base language and not any
        translations.

    ..  od:prop::   AssessmentFolderPath  Edm.String

        The full path of the Assessment's location within the folder
        hierarchy, for example::
        
            "RootFolder/SubFolderB/SubSubFolder1"
        
    ..  od:prop::   IsDeleted  Edm.Boolean

        A flag indicating whether or not the Assessment has been deleted
        from the item bank.  Deleting Assessments *does not* remove them
        from the item bank, it marks them as deleted and removes them
        from the user interface only.

    ..  od:prop::   AssessmentAMLs  AssessmentAML
        :collection:

        A navigation property to the related AssessmentAML entities that
        contain detailed information about the assessment in each
        available language.
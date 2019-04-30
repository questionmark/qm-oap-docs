Question and QuestionTranslation
--------------------------------

..  od:service::    deliveryodata

..  od:feed::   Questions Question

    :method GET: read only
    :filter ID: primary key
    :filter QuestionType: see note in entity type on space padding

    The Questions feed contains records describing all the questions in
    the assessment catalog.


..  od:feed::   QuestionTranslations QuestionTranslation

    An auxiliary feed to :od:feed:`Questions` containing translated
    versions of the Questions.


..  od:type::   Question

    ..  od:prop::   ID  Edm.Int64
        :key:
        :notnull:

    ..  od:prop::   Revision            Edm.Int32
        :notnull:

    ..  od:prop::   Language            Edm.String

    ..  od:prop::   Status              Edm.Int16
        :notnull:

    ..  od:prop::   Description         Edm.String

    ..  od:prop::   Author    	        Edm.String

    ..  od:prop::   Editor              Edm.String

    ..  od:prop::   CreatedDateTime     Edm.DateTime
        :notnull:

    ..  od:prop::   ModifiedDateTime    Edm.DateTime
        :notnull:

    ..  od:prop::   QuestionType    	Edm.String

    ..  od:prop::   QuestionTranslations QuestionTranslation
        :collection:

    ..  od:prop::   Rubric Rubric

    ..  od:prop::   Answers Answer
        :collection:


..  od:type::   QuestionTranslation

    ..  od:prop::   ID                  Edm.Int64
        :key:
        :notnull:

    ..  od:prop::   Language            Edm.String
        :key:
        :notnull:

    ..  od:prop::   Revision            Edm.Int32
        :notnull:

    ..  od:prop::   Status              Edm.Int16
        :notnull:

    ..  od:prop::   Description         Edm.String
    
    ..  od:prop::   Author              Edm.String
    
    ..  od:prop::   Editor              Edm.String
    
    ..  od:prop::   CreatedDateTime     Edm.DateTime
        :notnull:

    ..  od:prop::   ModifiedDateTime    Edm.DateTime
        :notnull:

    ..  od:prop::   Question Question

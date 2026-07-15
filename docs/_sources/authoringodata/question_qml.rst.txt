QuestionQML
-----------

..  od:service::    authoringodata


..  od:feed::   QuestionQMLs QuestionQML

    :method GET: feed is read only
    :filter QuestionRevisionId: part of the composite key
    :filter Language: part of the composite key (translation language)


..  od:type::   QuestionQML

    QuestionQML entities are media-link entities containing the full
    XML description of the Question.

    ..  od:prop::   QuestionRevisionId  Edm.Int32
        :key:
        :notnull:

        The ID of the parent QuestionRevision entity.

    ..  od:prop::   Language  Edm.String
        :key:
        :notnull:

        The language code for this QML translation.

    ..  od:prop::   CreatedDateTime  Edm.DateTimeOffset
        :notnull:

        The date and time (in UTC) when this translation was created.

    ..  od:prop::   Author  Edm.String

        The user name of the user that created this translation.

    ..  od:prop::   ModifiedDateTime  Edm.DateTimeOffset
        :notnull:

        The date and time (in UTC) when this translation was last modified.

    ..  od:prop::   Editor  Edm.String

        The user name of the user that last modified this translation.

    ..  od:prop::   TranslationStatus  Edm.Int32

        Status indicator for the translation.

    ..  od:prop::   IsDeleted  Edm.Boolean
        :notnull:

        A flag indicating whether or not this QML has been deleted.

    ..  od:prop::   QuestionRevision  QuestionRevision

        Navigation property to the parent QuestionRevision entity.

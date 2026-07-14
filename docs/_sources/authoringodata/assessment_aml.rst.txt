AssessmentAML
-------------

..  od:service::    authoringodata


..  od:feed::   AssessmentAMLs AssessmentAML

    :method GET: feed is read only
    :filter Id: primary key


..  od:type::   AssessmentAML

    AssessmentAML entities are media-link entities containing the full
    XML description of the Assessment.

    ..  od:prop::   AssessmentRevisionId  Edm.Int32
        :key:
        :notnull:

        The ID of the parent AssessmentRevision entity.

    ..  od:prop::   Language  Edm.String
        :key:
        :notnull:

        The language code for this AML translation.

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

        A flag indicating whether or not this AML has been deleted.

    ..  od:prop::   AssessmentRevision  AssessmentRevision

        Navigation property to the parent AssessmentRevision entity.

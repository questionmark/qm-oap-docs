Q_QML_Ex
--------

..  qm:table::  Q_QML_Ex

    An auxiliary table with the same structure and primary key as
    :qm:table:`Q_Question_Ex` that contains auxiliary information about
    the question including the serialised (XML) question data.
    
    ..  qm:field::  Question_MID int
        :key:
        :notnull:

    ..  qm:field::  Question_LID int
        :key:
        :notnull:

    ..  qm:field::  Revision int
        :key:
        :notnull:

    ..  qm:field::  Editor varchar(200)
        :notnull:

    ..  qm:field::  Modified_Date datetime
        :notnull:

    ..  qm:field::  Comments varchar(4000)

    ..  qm:field::  QML_Data nvarchar(max)
        
        The data in this field may be encrypted.  The purpose of the
        encryption is to prevent accidental exposure of exam content
        through, for example, database backups.  Newer databases may use
        plain text as transparent data encryption (TDE) is the preferred
        way to encrypt the contents of databases to mitigate this type
        of risk.  For security purposes, details of the encryption
        method used are private to Questionmark and not published in
        documentation.

    ..  qm:field::  Base bit
        :notnull:

    ..  qm:field::  Lang varchar(10)
        :key:
        :notnull:

    ..  qm:field::  Question_ID bigint
        :computed:
        :notnull:


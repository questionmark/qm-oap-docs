ST_RUBRICSCORES
---------------

..  qm:table::  ST_RUBRICSCORES

    ..  qm:field:: ST_RUBRICID int
        :key:
        :notnull:

    ..  qm:field:: ST_RESULTID int
        :key:
        :notnull:

    ..  qm:field:: ST_QLID int
        :key:
        :notnull:

    ..  qm:field:: ST_QMID int
        :key:
        :notnull:

    ..  qm:field:: ST_OCCURRENCE int

    ..  qm:field:: ST_QREVISION int

    ..  qm:field:: ST_SCORE int

    ..  qm:field:: ST_COMMENTS varchar(4000)

    ..  qm:field:: ST_ANNOTATED nvarchar(max)

    ..  qm:field:: ST_AUDIOFEEDBACK varchar(4000)

    ..  qm:field:: ST_STATUS int

    ..  qm:field:: ST_LOCK bit

    ..  qm:field:: ST_AUTHOR int

    ..  qm:field:: ST_CREATED_DATE datetime

    ..  qm:field:: ST_EDITOR int

    ..  qm:field:: ST_MODIFIED_DATE datetime

    ..  qm:field:: QUESTION_ID bigint
        :notnull:
        :computed:

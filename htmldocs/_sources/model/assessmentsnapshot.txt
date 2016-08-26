AssessmentSnapshot & BlockSnapshot
----------------------------------

..  qm:table::  AssessmentSnapshot

    Contains information about assessment snapshots
    
    ..  qm:field:: AssessmentSnapshot_ID int
        :key:
        :notnull:

        The unique ID of the snapshot is automatically allocated.
        
    ..  qm:field:: Assessment_ID bigint
        :notnull:

        The full ID of the assessment (combined MID and LID).  See
        :qm:field:`S_Header_Ex.Session_MID` for details.
        
    ..  qm:field:: Lang varchar(10)
        :notnull:

        The language of the assessment.  See :qm:field:`S_Header_Ex.Lang`
        
    ..  qm:field:: Name nvarchar(200)
        :notnull:

        A human-readable descriptive name for this snapshot.
    
    ..  qm:field:: Revision int
        :notnull:

        The revision of the assessment.  See
        :qm:field:`S_Header_Ex.Revision`.  The snapshot stores all the
        information it needs to deliver and assessment in this table
        (and the associated :qm:table:`BlockSnapshots<BlockSnapshot>`). 
        As a result, it doesn't matter if the assessment that was used
        to create the snapshot is later revised or deleted.  Bear in
        mind that the Revision is also part of the primary key in
        S_Header_Ex.
        
    ..  qm:field:: Created_Date datetime
        :notnull:

        Timestamp recording creation time of snapshot.
        
    ..  qm:field:: Modified_Date datetime
        :notnull:

        Timestamp recording modification time snapshot
        
    ..  qm:field:: Expires_Date datetime
    
        Optional timestamp recording expiry time of snapshot.

    ..  qm:field:: Data varbinary(max)
        :notnull:
        
        Binary data used to describe the snapshot.  You can obtain a
        full XML representation of the snapshot using the
        :od:feed:`deliveryodata.AssessmentSnapshotsData` feed.
        
        
..  qm:table::  BlockSnapshot

    Each AssessmentSnapshot is comprised of some information about the
    assessment as a whole and a set of associated blocks.  The blocks
    are stored separately because, in many cases, they are not subject
    to randomization and so are therefore common to all snapshots of the
    assessment.
    
    ..  qm:field:: BlockSnapshot_ID uniqueidentifier
        :key:
        :notnull:

    ..  qm:field:: Created_Date datetime
        :notnull:

    ..  qm:field:: Data varbinary(max)
        :notnull:

        Binary data used to describe this block within a snapshot. 
        You can obtain a full XML representation of the snapshot using
        the :od:feed:`deliveryodata.AssessmentSnapshotsData` feed.


..  qm:table::  BlocksInAssessmentSnapshot

        Stores the list of blocks for each snapshot.  The Order field is
        used to allow an ordered list of BlockSnapshots to be associated
        with a single AssessmentSnapshot.
        
    ..  qm:field:: AssessmentSnapshot_ID int
        :key:
        :notnull:
        
    ..  qm:field:: BlockSnapshot_ID uniqueidentifier
        :key:
        :notnull:

    ..  qm:field:: Order int
        :notnull:

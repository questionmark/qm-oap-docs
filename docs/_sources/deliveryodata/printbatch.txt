PrintBatch
----------

..  od:service::    deliveryodata


..  od:feed::   PrintBatches PrintBatch

    :method GET: read only
    :filter ID: primary key
    :filter GroupID: the ID of the group associated with this batch

    $orderby is *not* supported.

    The PrintBatches feed contains information about a group of users
    who have been assigned a particular snapshot of an assessment to
    take externally, typically through printing and scanning.


..  od:type::   PrintBatch

    ..  od:prop::   ID  Edm.Int64
        :key:
        :notnull:

        The numeric ID of this batch.

    ..  od:prop::   Name  Edm.String

        The name given to this batch

    ..  od:prop::   SnapshotID  Edm.Int32
        :notnull:

        The ID of the associated :od:type:`AssessmentSnapshot` entity.

    ..  od:prop::   GroupID  Edm.Int32
        :notnull:

        The ID of the associated :od:type:`Group` entity.

    ..  od:prop::   CreatedDateTime  Edm.DateTime
        :notnull:
        
    ..  od:prop::   ModifiedDateTime  Edm.DateTime
        :notnull:

    ..  od:prop::   LastUploadedDateTime  Edm.DateTime
        
        The time at which the last upload for this batch took place.

    ..  od:prop::   AssessmentSnapshot  AssessmentSnapshot

        Navigation property to the associated AssessmentSnapshot.

    ..  od:prop::   Group  Group

        Navigation property to the associated Group.

    ..  od:prop::   PrintBatchUploads  PrintBatchUpload
        :collection:
        
        Navigation property to a collection of PrintBatchUpload entities.


..  od:type::   PrintBatchUpload

    .. versionadded:: 2020.02
    
    With Questionmark OnPremise and certain configurations of
    Questionmark OnDemand, printing and scanning uses an external
    scanning process resulting in CSV files that are uploaded
    representing multiple participants within a print batch.  Typically
    a single batch upload contains the scanned responses for all
    participants within the batch.  In this case, the PrintBatchUpload
    entity is used to represent the uploaded CSV.

    With Questionmark OnDemand, printing and scanning uses scanned
    bubble sheets in PDF format that are uploaded and then processed to
    create individual :od:type:`AnswerUpload` entities.  Print batch
    uploads are not used when uploading PDFs for scanning.


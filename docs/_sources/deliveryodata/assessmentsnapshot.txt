AssessmentSnapshot(Data)
------------------------

..  od:service::    deliveryodata


..  od:type::   AssessmentSnapshot

    AssessmentSnapshot entities are drawn from
    :qm:table:`AssessmentSnapshot`.
    
    ..  od:prop::   ID  Edm.Int32
        :key:
        :notnull:

        The ID of the snapshot
        (:qm:field:`AssessmentSnapshot.AssessmentSnapshot_ID`). The
        value cannot be modified.

    ..  od:prop::   AssessmentID  Edm.Int64
        :notnull:
    
        The ID of the assessment used to create the snapshot.  Along
        with the Language, this is used to find the assessment
        definition. When POSTing to the feed to create a snapshot you
        must specify the AssessmentID, the snapshot is created
        immediately so any subsequent changes to the Assessment will
        not affect the delivery of the snapshot.
        
        You cannot modify this field once the snapshot has been created.

    ..  od:prop::   Language  Edm.String

        The Language of the assessment (if translated).  This field is
        optional.  If unspecified then for assessments that have not
        been translated it will take the value '-', indicating an
        unknown language.  For assessments that have been translated the
        base language is selected.  When specified it must match one
        of the languages the assessment has been translated into.
        
        You cannot modify this field once the snapshot has been created.

    ..  od:prop::   Name  Edm.String

        A human friendly name for the snapshot.  This field can be
        modified using the PATCH method.
    
    ..  od:prop::   ExpiresDateTime  Edm.DateTime

        The time after which new attempts that use this snapshot cannot
        be created.  This value can be modified using the PATH method.
    
    ..  od:prop::   PrintableDocumentSourceUrl  Edm.String
    
        A link to a printable HTML5 version of the snapshot.  This link
        is time-stamped and signed and must be generated immediately
        prior to use.  It is only available when an individual entity is
        queried, whenever a collection of AssessmentSnapshot entities
        can be returned from a query (such as filtering the parent feed)
        this property is set to NULL in the entities returned (for
        security reasons).  For example::
        
            GET /deliveryodata/123456/AssessmentSnapshots
        
            {
                odata.metadata: "https://ondemand.questionmark.com/deliveryodata/123456/$metadata#AssessmentSnapshots",
                value: [
                    {
                        PrintableDocumentSourceUrl: null,
                        ID: 1,
                        AssessmentID: "2185231530264478",
                        Language: "-",
                        Name: "DemoSnap",
                        CreatedDateTime: "2015-11-09T15:48:18.527Z",
                        ModifiedDateTime: "2015-11-09T15:48:18.527Z",
                        ExpiresDateTime: null
                    },
                    {
                        PrintableDocumentSourceUrl: null,
                        ID: 2,
                        ...
        
        To get the printable link to the snapshot you must use a query
        like this::

            GET /deliveryodata/123456/AssessmentSnapshots(1)

            {
                odata.metadata: "https://ondemand.questionmark.com/deliveryodata/123456/$metadata#AssessmentSnapshots/@Element",
                PrintableDocumentSourceUrl: "https://ondemand.questionmark.com/delivery/AssessmentSnapshot.php?customerid=123456&snapshotid=1&timestamp=2015-12-10T16:27:48.9784554Z&signature=63a3ffc4ffdcfdb03280964e1583e8a08a7fe93857d48311c483ad917228d268",
                ID: 1,
                AssessmentID: "2185231530264478",
                Language: "-",
                Name: "DemoSnap",
                CreatedDateTime: "2015-11-09T15:48:18.527Z",
                ModifiedDateTime: "2015-11-09T15:48:18.527Z",
                ExpiresDateTime: null
            }

    ..  od:prop::   CreatedDateTime  Edm.DateTime
        :notnull:
    
        A time stamp of when the snapshot was created.  Set
        automatically, it cannot be modified.
    
    ..  od:prop::   ModifiedDateTime  Edm.DateTime
        :notnull:
    
        A time stamp of when the snapshot was last modified.  Set
        automatically, it cannot be modified directly but a call to the
        PATCH method on the associated feed will cause it to be updated.
    
    
            
..  od:type::   AssessmentSnapshotData


..  _snapshotxml:

Snapshot File Format 
~~~~~~~~~~~~~~~~~~~~

TBC
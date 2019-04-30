AssessmentSnapshot(Data)
------------------------

..  od:service::    deliveryodata


..  od:feed::   AssessmentSnapshots AssessmentSnapshot

    :method GET: reading snapshot entities
    :method POST: creating snapshot entities
    :method PATCH: some properties may be updated, see entity for details
    :filter ID: primary key
    :filter AssessmentID: the assessment used to create the snapshot ($orderby not supported)
    :filter CreatedDateTime: the time the snapshot was created ($orderby only, $filter not supported)
        
    The AssessmentSnapshots feed contains information about snapshots of
    assessments.  Snapshots are versions of an assessment that have
    fixed any randomisation, such as which questions are picked and the
    order they are presented, including the order of any shuffled
    choices.  Snapshots are used for making an exact record of the
    assessment that was delivered to the participant.  At the time of
    writing they are used only for external delivery workflows,
    including printing and scanning.


..  od:feed::   AssessmentSnapshotsData AssessmentSnapshotData
    :mle:

    :method GET: feed is read only
    :filter ID: primary key

    $orderby is *not* supported.

    An auxiliary feed to :od:feed:`AssessmentSnapshots` which contains
    the raw XML data describing the snapshot.  Values are normally
    obtained by navigation from the associated
    :od:type:`deliveryodata.AssessmentSnapshot` rather than directly.


..  od:type::   AssessmentSnapshot

    AssessmentSnapshot entities are drawn from
    :qm:table:`AssessmentSnapshot`.  You can create entities using
    a POST request to the corresponding feed.
    
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
        be created.  This value can be modified using the PATCH method.
    
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

    ..  od:prop::   AssessmentSnapshotData  AssessmentSnapshotData
        :notnull:

        Navigation property to the associated XML data for this
        snapshot. As a single entity you can just append
        /AssessmentSnapshotData/$value to the URL of an
        AssessmentSnapshot entity to obtain the raw XML source of the
        snapshot.
        
    ..  od:prop::   PrintBatches PrintBatch
        :collection:
        
        Navigation property to all PrintBatch entities that use this
        snapshot.  This collection may be empty as PrintBatches are an
        optional grouping structure used to help manage printing and
        scanning workflows..


..  od:type::   AssessmentSnapshotData

        This is a media link entry that describes the XML file
        associated with a snapshot.  You obtain the XML stream by taking
        the value of the identified enity using OData's $value suffix.
        
        The format of the XML data is described in :ref:`snapshotxml`
        below.
        
    ..  od:prop::   ID  Edm.Int32
        :key:
        :notnull:

        The ID of the snapshot for which this is the data.
        
    ..  od:prop::   AssessmentSnapshot  AssessmentSnapshot
        :notnull:

        Navigation property back to the owning AssessmentSnapshot.


..  _snapshotxml:


Snapshot File Format 
~~~~~~~~~~~~~~~~~~~~

TBC
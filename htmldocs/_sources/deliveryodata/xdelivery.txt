External Delivery
-----------------

The Delivery OData API can be used to facilitate delivery through an
external system such as an external printing and scanning process.  The
API does not provide direct access to Questionmark OnDemand's builtin
support for Printing and Scanning but it does provide the data necessary
to integrate an alternate solution.

The following comparison table documents the features supported by this
API and those that are only available through the Questionmark OnDemand
portal.

=====================================   ========================
Process                                 Available through API?
=====================================   ========================
Creating snapshots                      Yes
HTML5 & XML of snapshots                Yes
Create/select bubble sheets             No
Creating PrintBatches                   Yes
Upload scanned PDFs of bubble sheets    No
Upload raw response data for scoring    Yes
=====================================   ========================


Snapshots
~~~~~~~~~

Before an assessment can be delivered a snapshot must be created. The
purpose of the snapshot is to fix any random variation in the assessment
so that anyone referring to the snapshot will know exactly which
questions are to be presented/scored, the order of the questions and the
order of any shuffled choices within those questions.

An application might start by presenting a list of assessments which can
be obtained with a query such as::

    GET /deliveryodata/123456/Assessments

A list of snapshots for a specific assessment might be obtained using
a filter on the :od:feed:`deliveryodata.AssessmentSnapshots` feed::

    GET /deliveryodata/123456/AssessmentSnapshots?$filter=AssessmentID eq 5649284224767710L

..  note:   When obtaining AssessmentSnapshots from list views in this
            way the PrintableDocumentSourceUrl will be null.  To obtain
            a URL for the printable HTML5 view of the assessment you
            must use the ID of the snapshot to query the entity directly.

If none of the snapshots listed meet your needs then you can create a new
snapshot by POSTing to the feed::

     POST /deliveryodata/123456/AssessmentSnapshots

When posting, the ID, CreatedDateTime and ModifiedDateTime values will
be automatically generated and can be set to any value (0 is recommended
for the ID). Use the AssessmentID of the required assessment and choose
a human-readable Name.

On creation, the actual entity is returned (along with the actual ID
allocated to it) and a link to the HTML view of the snapshot in the
:od:prop:`deliveryodata.AssessmentSnapshot.PrintableDocumentSourceUrl`.
This link is time stamped for security so cannot be stored for later
use, instead, you should store the ID of the snapshot entity and
retrieve it immediately prior to use.  For example, if the ID is 34::

    GET /deliveryodata/123456/AssessmentSnapshots(34)

When you create a snapshot, the associated AssessmentSnapshotData entity
is created automatically and linked via a navigation property.  It is a
media-link entity that contains the XML-raw source of the snapshot. The
format is described in :ref:`snapshotxml`.  To retrieve the XML document
use a query such as::

    GET /deliveryodata/123456/AssessmentSnapshots(34)/AssessmentSnapshotData/$value

Note the use of $value to return the document rather than the document's
metadata.

The XML file contains all the information you need to deliver the
assessment to the participant.  For example, for an external printing
and scanning service you can parse this XML to discover the information
required to print a bubble sheet customised to the number of questions
and the expected response types (e.g., number of choices, validation
constraints, etc).


PrintBatches
~~~~~~~~~~~~

A print batch is used to associate a group of participants to a
particular snapshot for external or offline delivery.  Despite the name
it doesn't have to be through a printing and scanning process.  You are
not required to use print batches, it is possible to upload responses
for a participant without an associated PrintBatch if you prefer.

An application might start by presenting a list of groups which can be
obtained with a query such as::

    GET /deliveryodata/123456/Groups

A list of PrintBatches for a specific group might be obtained using a
filter on the :od:feed:`deliveryodata.PrintBatches` feed::

    GET /deliveryodata/123456/PrintBatches?$filter=GroupID eq 335363530

If none of the PrintBatches listed meet your needs then you can create a
new batch by POSTing to the feed::

     POST /deliveryodata/123456/PrintBatches

The ID, CreatedDateTime and ModifiedDateTime properties are assigned
values automatically on creation and dummy values can be specified when
posting.  The GroupID and the SnapshotID are required and the Name
property provides a human-readable name for the batch.  The navigation
property to the associated Group is automatically populated using the
supplied GroupID.

You should store the ID associated your PrintBatch as it can be used
later when uploading responses to automatically associated a group with
the participants result.  You obtain the actual ID allocated by reading
the value from the response.  

Uploading Answers
~~~~~~~~~~~~~~~~~

However you collect the participant responses, ultimately they must be
uploaded through the API to enable scoring and the creation of finalised
results.

The steps to do this are:

    1   Create an Attempt for the participant concerned
    
    2   Prepare an answer upload file with the participant's answers
    
    3   POST the upload file to the AnswerUploads media-link feed

The OData API channels all assessment delivery through an Attempt
entity.  The attempt entity signals the authority for a single
identified participant to take a specific assessment.  Once the attempt
has been used to generate a result it cannot be used again.

It is recommended that you create attempts on a just-in-time basis.  In
other words, create an attempt only when you are ready to upload the
corresponding answers.  Creating an attempt is done by POSTing to the
Attempts feed::

     POST /deliveryodata/123456/Attempts

The ID and LastModifiedDateTime properties are automatically assigned on
creation and dummy values can be supplied.

For this use case, the following properties are required.

    ParticipantID
        
        The ID of the participant authorised to take the assessment.
    
    AssessmentID
        
        The ID of the assessment the participant is taking
    
    AssessmentSnapshotID
    
        The ID of the snapshot the participant was presented with.
        (Although optional when creating Attempts in general it is
        required if the answers are to be uploaded through the
        AnswerUploads feed.)

    ExternalAttemptID
    
        A string identifier that uniquely identifies this attempt in
        your system.  This ID is designed to be used to prevent the
        accidental creation of multiple attempts where one was intended.
        If you POST a new attempt with the same ExternAttemptID as an
        existing one the request will fail.  This helps avoid race
        conditions such as two processes processing the same participant
        responses simultaneously creating an attempt.

    LockStatus, LockRequired
    
        These values are only used during online delivery and can be
        set to False.

The ID of the attempt can be read from the entity returned and should be
used in the next step.

The AnswerUpload file is a JSON file formatted as per
:ref:`answerupload`. Note that the ID of the Attempt is included in the
file format as is the (optional) ID of the associated PrintBatch.

To upload the file you POST it to the AnswerUploads feed::

    POST /deliveryodata/123456/AnswerUploads

If there are any validation errors or formatting problems with the file
the POST will fail with an error code.

There can only ever by one AnswerUpload associated with an attempt, the
metadata for the AnswerUpload entity uses the AttemptID as the key.  You
can review the actual file uploaded at any time using this ID to query
the feed, for example, for attempt ID 75::

    GET /deliveryodata/123456/AnswerUploads(75)/$value

The API processes the uploaded file and creates the corresponding result
associating it with the attempt entity automatically.  On success, you
can therefore use the attempts entity to discover the outcome of the
uploaded assessment::

    GET /deliveryodata/123456/Attempts(75)

The ResultID will have been populated and can be used to get summary
information directly from the Delivery system::

    GET /deliveryodata/601871/Results(304562138)

You can obtain item level scores by expanding the answers in your query::

    GET /deliveryodata/601871/Results(304562138)?$expand=Answers

You can obtain more detailed result information using the QMWISe method
:qm:meth:`GetResult` or by querying the OData feeds from the Results
Warehouse (though in the latter case you will have to wait until the
next scheduled ETL run has completed).


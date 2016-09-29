AnswerUpload
------------

..  od:service::    deliveryodata

..  od:type::   AnswerUpload

    AnswerUpload entities are media link entries that contain the
    response files uploaded for scoring.  Only one format is supported
    and that is application/json with fields as documented below.
        
    ..  od:prop::   AttemptID  Edm.Int32
        :key:
        :notnull:
        
        Each AnswerUpload must be associated with an Attempt.  Due to
        the nature of media link entries the AttemptID cannot be
        specified in the URL on upload as the response file is POSTed to
        the feed URL, however, the AttemptID is contained within the
        file itself and is used as the primary key of the associated
        entity on creation.

    ..  od:prop::   Attempt  Attempt
        
        Navigation property to the associated Attempt.


..  _answerupload:

Answer Upload File Format
~~~~~~~~~~~~~~~~~~~~~~~~~

The answer upload file format is a JSON format (content-type
application/json) file with the following fields.

    BatchID
        A reference to an associated :od:type:`deliveryodata.PrintBatch`
        formatted as a string (optional).  If present, group information
        will be read from the batch and used to set the group
        information in the associated result.
    
    AttemptID
        An integer reference to the associated attempt (required).
        
        The attempt must have an associated snapshot which defines the
        exact version of the assessment that was delivered externally.
        
        An attempt can only ever be taken once, either online or
        externally.  Therefore, you cannot upload a set of results for
        an attempt that is already associated with a result record (see
        :od:prop:`Attempt.ResultID`).  
            
    QuestionAndChoices
        An array of objects describing the response to each question.
        
        QuestionOrderNumber
            Integer index of the question being responded to with 1
            being the first question.  Explanation questions are ignored
            and to not contribute to the numbering.

        UploadedChoices
            A list of records describing the responses given by the
            participant.
            
            ChoiceOrderNumber
                An integer reference to the number of the choice
                (formatted as a string).
            
            Selected
                A boolean (true/false) indicating whether or not the
                choice was actually selected.
            

In future this documentation and file format will be expanded to support
a wider range of choice types.  Here is an example of a simple upload
file::

    {
        AttemptID: 170,
        QuestionAndChoices: [
            {
                QuestionOrderNumber: 1,
                UploadedChoices: [
                    {
                        ChoiceOrderNumber: "5",
                        Selected: true
                    }
                ]
            },
            {
                QuestionOrderNumber: 2,
                UploadedChoices: [
                    {
                        ChoiceOrderNumber: "1",
                        Selected: true
                    }
                ]
            },
            {
                QuestionOrderNumber: 3,
                UploadedChoices: [
                    {
                        ChoiceOrderNumber: "5",
                        Selected: true
                    }
                ]
            }
        ]
    }


Answer
------

..  od:service::    deliveryodata

..  od:feed::   Answers Answer
    :mle:

    :method GET: feed is read only
    :filter QuestionID: ID of the associated Question
    :filter ResultID: ID of the associated Result
    :expand Question: expands the associated Question
    :expand Result: expands the associated Result
    :expand ScoringTask: expands the associated ScoringTask, due to
                         a known issue this expansion will *only* return
                         entities that are associated with a ScoringTask.

    $orderby is *not* supported.

    The Answers feed contains detailed information about the answers
    given by participants.  Each question that a participant answers
    generates a unique record in this feed.


..  od:type::   Answer

    Answer entities are drawn from :qm:table:`A_Answer` in the data
    model but contain only a subset of the properties.  They are read
    only in OData.
    
    The Answer entity is a media link entity.  The value of an Answer
    entity (obtained by appending /$value to the entity's URL) is the
    full answer given by the participant (for constructed response
    questions).  See below for an example of how to obtain this.
    
    ..  od:prop::   QuestionID  Edm.Int64
        :key:
        :notnull:
        
        The fulle ID of the question being answered, see
        :qm:field:`A_Answer.Question_MID`. for more information.

    ..  od:prop::   ResultID  Edm.Int32
        :key:
        :notnull:
        
        The ID of the associated Result, see
        :qm:field:`A_Answer.Result_ID`.

    ..  od:prop::   BlockNumber  Edm.Int16
        :key:
        :notnull:
        
        The sequence number of the block within the which the question
        was presented.  See :qm:field:`A_Answer.Block_Number`.

    ..  od:prop::   Occurrence  Edm.Int16
        :key:
        :notnull:
        
        See :qm:field:`A_Answer.Occurrence`.
    
    ..  od:prop::   QuestionNumber  Edm.Int16
        :notnull:
        
        The sequence number of the question presented within the block. 
        See :qm:field:`A_Answer.Question_Number`.
    
    ..  od:prop::   TimesAnswered  Edm.Int16
        :notnull:

        See :qm:field:`A_Answer.Times_Answered`.

    ..  od:prop::   MaxScore  Edm.Int32
        :notnull:

        See :qm:field:`A_Answer.Max_Score`.

    ..  od:prop::   ActualScore  Edm.Int32
        :notnull:

        See :qm:field:`A_Answer.Actual_Score`.

    ..  od:prop::   AnswerTruncated  Edm.String

        See :qm:field:`A_Answer.Answer_Truncated`.  A truncated
        representation of the answer given by the Participant.  The
        format of this field varies depending on the type of the
        associated question.

        .. versionadded::   2021.05

    ..  od:prop::   Revision Edm.Int32

        Reserved for future use.

    ..  od:prop::   Question  Question

        Navigation property to the a single Question associated with
        this answer.
    
    ..  od:prop::   Result  Result

        Navigation property to the single Result associated with this
        answer.

    ..  od:prop::   ScoringTask  ScoringTask

        Navigation property to an optional ScoringTask associated with
        this answer.  ScoringTasks are only associated with answers that
        require subjective marking.
    
    ..  od:prop::   AnswerAuditLogs  AnswerAuditLog
        :collection:
        
        Navigation property to an audit log of changes to this answer
        record (e.g., with Scoring Editor).

        .. versionadded::   2021.05


..  od:type::   AnswerAuditLog

    Changes to Answer records (other than those made by the participant
    during the assessment itself) are recorded in AnswerAuditLog
    entities.

    .. versionadded::   2021.05
        
    ..  od:prop::   ID  Edm.Int32
        :key:
        :notnull:

        An internal ID for this log entity.

    ..  od:prop::   ResultID  Edm.Int32
        :notnull:

        The ResultID of the associated :od:type:`Result`.  Changes to
        the score given for an answer will result in corresponding
        changes to the result.

    ..  od:prop::   QuestionID  Edm.Int64
        :notnull:

        The QuestionID (used in the association with the corresponding
        Answer entity).
    
    ..  od:prop::   BlockNumber  Edm.Int16
        :notnull:

        The block number in which this answer was given (used in the
        association with the corresponding Answer entity).

    ..  od:prop::   Occurrence  Edm.Int16
        :notnull:

        Deprecated property used in the association with the corresponding
        Answer entity).
            
    ..  od:prop::   RevisionNumber  Edm.Int32
        :notnull:

        A revision number for ordering changes to the associated
        :od:type:`Answer`.

    ..  od:prop::   AdministratorName  Edm.String

        The login name of the Administrator that made the change.  This
        property is set to the name of the logged in user when changes
        are made through the user interface.  Changes made through the
        API can provide any value for this field (e.g., the name of a
        user in a remote system integrated using this API). 

    ..  od:prop::   ActualScoreOld  Edm.Int32
        :notnull:

        The original score awarded for the associated answer.
        
    ..  od:prop::   ActualScoreNew  Edm.Int32
        :notnull:

        The new score awarded for the associated answer.

    ..  od:prop::   AnswerFullOld  Edm.String

        The original Answer provided by the participant.
        
    ..  od:prop::   AnswerFullNew  Edm.String

        The updated Answer *as if* provided by the participant.  These
        fields are provided for compatibility with the classic Score
        Editor tool only.  The modification of participant-provided
        answers is deprecated.
       
    ..  od:prop::   Comment  Edm.String

        A comment describing the reason for the change.

    ..  od:prop::   TimeStampUtc  Edm.DateTime
        :notnull:

        The UTC time and date of the change.
    
    ..  od:prop::   Answer  Answer

        Navigation property to the Answer entity affected by this
        change.


Reading the Participant's Answer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The Answer entity is a media link entity with a corresponding media
stream that contains the participant's full answer.  The stream is
only available when the Question required a constructed response such as
an Essay or File Upload question.

Here is an example::

    <service root>/Results(634445534)/Answers?$expand=Question

    {
        odata.metadata: "<service root>/$metadata#Answers",
        value: [
            {
                odata.mediaReadLink: "<service root>/Answers(QuestionID=5845494007544735L,ResultID=634445534,BlockNumber=1,Occurrence=1)/$value",
                odata.mediaContentType: "application/octet-stream",
                Question: {
                    odata.mediaReadLink: "<service root>/Questions(5845494007544735L)/$value",
                    odata.mediaContentType: "application/xml",
                    ID: "5845494007544735",
                    Revision: 2,
                    Language: "-",
                    Status: 0,
                    Description: "Essay Question",
                    Author: "Jane",
                    Editor: "John",
                    CreatedDateTime: "2016-05-20T09:29:05Z",
                    ModifiedDateTime: "2016-05-20T10:53:44Z",
                    QuestionType: "ESSAY "
                },
                QuestionID: "5845494007544735",
                ResultID: 634445534,
                BlockNumber: 1,
                Occurrence: 1,
                QuestionNumber: 1,
                TimesAnswered: 1,
                MaxScore: 10,
                ActualScore: 0
            },
            {
                odata.mediaReadLink: "<service root>/Answers(QuestionID=1712759025350437L,ResultID=634445534,BlockNumber=1,Occurrence=1)/$value",
                odata.mediaContentType: "application/octet-stream",
                Question: {
                    odata.mediaReadLink: "<service root>/Questions(1712759025350437L)/$value",
                    odata.mediaContentType: "application/xml",
                    ID: "1712759025350437",
                    Revision: 2,
                    Language: "-",
                    Status: 0,
                    Description: "File Upload Question",
                    Author: "Jane",
                    Editor: "John",
                    CreatedDateTime: "2016-05-20T09:59:28Z",
                    ModifiedDateTime: "2016-05-20T10:53:45Z",
                    QuestionType: "UPLOAD "
                },
                QuestionID: "1712759025350437",
                ResultID: 634445534,
                BlockNumber: 1,
                Occurrence: 1,
                QuestionNumber: 2,
                TimesAnswered: 1,
                MaxScore: 1,
                ActualScore: 0
            }
        ]
    }

Notice the media links in each Answer entity, the Questions have been
expanded to make it clearer.  Question number 1 was an essay question
and the media link provides the plain text typed by the candidate. 
Question number 2 is a file upload question and actually returns an
image.

..  warning::   when returning Answer entities the content type encoded
                in the entity's serialised representation is defaulted
                to application/octet-stream for performance reasons (as
                the data model does not contain this information).

                To obtain the true content type you must issue a HEAD
                (or GET) request on the odata.mediaReadLink directly.

Here's a sample HTTP session when retrieving the file uploaded by the
participant::

    <service root>/Answers(QuestionID=1712759025350437L,ResultID=634445534,BlockNumber=1,Occurrence=1)/$value

    GET <service root>/Answers(QuestionID=1712759025350437L,ResultID=634445534,BlockNumber=1,Occurrence=1)/$value HTTP/1.1
    Host: ondemand.questionmark.eu
    User-Agent: Mozilla/5.0 (Macintosh; Intel Mac OS X 10.11; rv:47.0) Gecko/20100101 Firefox/47.0
    Accept: text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8
    Accept-Language: en-US,en;q=0.5
    Accept-Encoding: gzip, deflate, br
    DNT: 1
    Referer: <service root>/Results(634445534)/Answers
    Cookie: language=en
    Connection: keep-alive
    Authorization: Basic <security details removed!>

    HTTP/1.1 200 OK
    Cache-Control: no-cache
    Pragma: no-cache
    Transfer-Encoding: chunked
    Content-Type: image/gif; name="070a2a779af97859f8a0c7342a4068b183db506108b90a660259ce58f964fcaf.gif"
    Expires: -1
    Accept-Ranges: bytes
    Server: Microsoft-IIS/8.5
    Content-Disposition: inline; filename="070a2a779af97859f8a0c7342a4068b183db506108b90a660259ce58f964fcaf.gif"
    X-AspNet-Version: 4.0.30319
    X-Powered-By: ASP.NET
    Date: Tue, 05 Jul 2016 10:56:52 GMT
    Strict-Transport-Security: max-age=31536000; includeSubDomains

    <GIF image data>

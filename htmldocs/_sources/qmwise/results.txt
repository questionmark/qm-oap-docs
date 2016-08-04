Results
-------

Results methods can be used to query the delivery database for
information about assessment results.  There are methods for obtaining
an individual result from a result ID, :qm:meth:`GetResult`, or methods
for obtaining a list of results by filtering, for example
:qm:meth:`GetResultListByAssessment`, :qm:meth:`GetResultListByGroup`
and qm:meth:`GetResultListByParticipant`.

..  warning::
    Questionmark databases may contain many millions of results, some of
    these methods were designed to work with smaller datasets and may
    not be suitable for use when the number of results returned is very
    large.  As a rule of thumb, if the returned result set exceeds
    1,000 results consider using an alternative API.  The
    :od:feed:`Results` OData feed queries the same part of the data
    model and will accept more filters (including date filters) allowing
    you to return more precise result sets.


Result Methods
~~~~~~~~~~~~~~

Getting Result Information
++++++++++++++++++++++++++

..  qm:meth::   GetResult
    :input:     Result_ID   string
    :output:    Result      Result
    
    Returns a single result from the database.  The string type of the
    input parameter is an anomaly, the parameter value is required (See
    :ref:`qmwise_string`) and must be the integer value of a result ID
    present in the database. See :qm:field:`A_Result.Result_ID`.

    The output parameter returned is of type :qm:xtype:`Result2`, which
    is an extension of the basic :qm:xtype:`Result` type declared in the
    WSDL.  (See :ref:`extension_types`.)

    Example::
    
        <SOAP-ENV:Envelope xmlns:SOAP-ENV="http://schemas.xmlsoap.org/soap/envelope/">
            <SOAP-ENV:Header/>
            <SOAP-ENV:Body>
                <GetResult xmlns="http://questionmark.com/QMWISe/">
                    <Result_ID>218475</Result_ID>
                </GetResult>
            </SOAP-ENV:Body>
        </SOAP-ENV:Envelope>

        <?xml version="1.0" encoding="utf-8"?>
        <soap:Envelope xmlns:soap="http://schemas.xmlsoap.org/soap/envelope/"
            xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
            xmlns:xsd="http://www.w3.org/2001/XMLSchema">
            <soap:Body>
                <GetResultResponse xmlns="http://questionmark.com/QMWISe/">
                    <Result xsi:type="Result2">
                        <Result_ID>218475</Result_ID>
                        <Assessment_ID>0009962000009962</Assessment_ID>
                        <Write_Answer_Data>true</Write_Answer_Data>
                        <Participant>miami147</Participant>
                        <Member_Group/>
                        <Participant_Details/>
                        <Hostname/>
                        <IP_Address>10.30.6.5</IP_Address>
                        <Still_Going>false</Still_Going>
                        <Status>9</Status>
                        <Feedback>0</Feedback>
                        <Number_Sections>1</Number_Sections>
                        <Max_Score>3</Max_Score>
                        <Total_Score>3</Total_Score>
                        <Special_1>Customer</Special_1>
                        <Special_2>147</Special_2>
                        <Special_3/>
                        <Special_4/>
                        <Special_5/>
                        <Special_6/>
                        <Special_7/>
                        <Special_8/>
                        <Special_9/>
                        <Special_10/>
                        <Time_Taken>0</Time_Taken>
                        <Score_Band_Title>Thank you!</Score_Band_Title>
                        <Score_Band_Number>2016515</Score_Band_Number>
                        <Percentage_Score>100</Percentage_Score>
                        <Schedule_Name/>
                        <Monitored>true</Monitored>
                        <Monitor_Name/>
                        <TopicScoringList>
                            <TopicScoring>
                                <Topic_ID>58275</Topic_ID>
                                <Topic_Name>Printing and Scanning in Miami</Topic_Name>
                                <Description/>
                                <Percentage_Score>100</Percentage_Score>
                                <Actual_Score>3</Actual_Score>
                                <Maximum_Score>3</Maximum_Score>
                                <Num_Questions>3</Num_Questions>
                            </TopicScoring>
                        </TopicScoringList>
                        <When_Started>2016-04-13T15:28:14</When_Started>
                        <Session_Last_Modified>2016-04-12T23:01:33</Session_Last_Modified>
                        <When_Finished>2016-04-13T15:28:14</When_Finished>
                        <FirstName>Customer</FirstName>
                        <LastName>147</LastName>
                        <PrimaryEmailAddress/>
                        <SubgroupPath/>
                        <CourseProperty>Miami2016</CourseProperty>
                        <ScoreBandIDProperty>663244283</ScoreBandIDProperty>
                    </Result>
                </GetResultResponse>
            </soap:Body>
        </soap:Envelope>


..  qm:meth::   GetResultList
    :output:    ResultList  ResultList

    Returns *all* results in the repository database.  Use of this
    method is no longer recommended due to the number of result records
    in a typical repository.


..  qm:meth::   GetResultListByAssessment
    :input:     Assessment_ID   string
    :output:    ResultList  ResultList

    Returns *all* results in the repository database associated with a
    given assessment.  Use of this method is no longer recommended if
    the number of results for the assessment exceeds 10,000 records.
    
    The input parameter is given as type string but it must be the
    numeric ID of the assessment. 

    
..  qm:meth::   GetResultListByGroup
    :input:     Group_Name   string
    :output:    ResultList  ResultList

    Returns *all* results in the repository database associated with a
    given Group.  Use of this method is no longer recommended if the
    number of results for the group exceeds 10,000 records.

    Notice that the group is identified by *name* and not by a numeric
    ID.  The name must be the name of a top-level group and is matched
    against :qm:field:`A_Result.Member_Group` in the data model.
    
    For backwards compatibility, if the Group_Name input parameter
    contains the single quote character it is replaced with the
    back-quote \` before being used to filter the result set.


..  qm:meth::   GetResultListByParticipant
    :input:     Participant_Name   string
    :output:    ResultList  ResultList

    Returns *all* results in the repository database associated with a
    given Participant.

    Notice that the participant is identified by *name* and not by a
    numeric ID.  The name is matched against
    :qm:field:`A_Result.Participant` in the data model.
    
    For backwards compatibility, if the Participant_Name input parameter
    contains the single quote character it is replaced with the
    back-quote \` before being used to filter the result set.


..  qm:meth::   GetResultListBySubGroup
    :input:     Event   string
    :output:    EventResultList  EventResultList

    Similar to :qm:meth:`GetResultListByGroup`, this returns all results
    in the repository where :qm:field:`A_Result.Member_Sub_Group_1`
    matches the input parameter.  This method imposes the additional
    constraint that the input parameter must be the name of a group as
    recorded in :qm:field:`G_Group_Tree.Group_Name`.
    
    Unlike similar methods, no character transformations are applied to
    the input parameter.


..  qm:meth::   GetAssessmentResult
    :input:     Result_ID   string
    :output:    AssessmentResult  AssessmentResult

    Similar to :qm:meth:`GetResult` but returns additional information
    including the Feedback and the the detailed item-level responses and
    scores.


..  qm:meth::   GetAssessmentResult2
    :input:     Result_ID   string
    :output:    AssessmentResult2  AssessmentResult2

    Similar to :qm:meth:`GetAssessmentResult` but returns some elements
    missing from the original method by using the
    :qm:xtype:`AssessmentResult2` type.


..  qm:meth::   GetAssessmentResultListByAssessment
    :input:     Assessment_ID    string
    :output:    AssessmentResultList AssessmentResultList

    Similar to :qm:meth:`GetResultListByAssessment` but returns
    additional information including the Feedback and the the detailed
    item-level responses and scores.


..  qm:meth::   GetAssessmentResultListByGroup
    :input:     Group_Name    string
    :output:    AssessmentResultList AssessmentResultList

    Similar to :qm:meth:`GetResultListByGroup` but returns additional
    information including the Feedback and the the detailed item-level
    responses and scores.


..  qm:meth::   GetAssessmentResultListByParticipant
    :input:     Participant_Name    string
    :output:    AssessmentResultList AssessmentResultList

    Similar to :qm:meth:`GetResultListByParticipant` but returns
    additional information including the Feedback and the the detailed
    item-level responses and scores.




Creating Results
++++++++++++++++

The following methods can be used to create results in the repository.
The mechanism used by these methods relies on the :qm:table:`A_Session_Ex`
and :qm:table:`A_Question_Ex` tables in the data model.  This is an older
data flow that has some issues with the handling of assessment and question
revisions.  The methods are documented here for backwards compatibility,
new projects should consider using the new snapshot-based 'Attempt' flow
facilitated by the :od:svc:`Delivery OData<deliveryodata>` service.

..  qm:meth::   CreateAssessmentResult
    :input:     AssessmentResult    AssessmentResult
    :output:    Result_ID           string

    Creates a single result in the database from the supplied
    information. This is the base method designed to work with the basic
    :qm:xtype:`Result` and :qm:xtype:`Answer` elements.

    The method creates a record in :qm:table:`A_Result` and optionally
    records in :qm:table:`A_TopicScore`, :qm:table:`A_Answer`,
    :qm:table:`A_ScoreBand` and :qm:table:`A_Comment`. as appropriate.

    On input, the :qm:xfield:`Result.Result_ID` is ignored, it is
    recommended to set it to "0".
    
    The supplied :qm:xfield:`Result.Assessment_ID` must correspond to
    the ID of an assessment in :qm:table:`A_Session_Ex` in the
    repository database.  Similarly, any uploaded answers must have
    corresponding records in :qm:table:`A_Question_Ex`.  Before using
    this method you should familiarise yourself with the purpose of
    these tables in the data model.  It is likely that you will have to
    call :qm:meth:`CreateAssessmentResultInfoList` and
    :qm:meth:`CreateQuestionResultInfoList` when creating results for
    the first time - you can use :qm:meth:`GetAssessmentResultInfo` and
    :qm:meth:`GetQuestionResultInfoList` to test for the existence of
    the required records. 
    
    If :qm:xfield:`AssessmentResult.Feedback` is provided a new record
    is created in :qm:table:`A_ScoreBand` to hold the feebdack.  The
    feedback is not validated against the assessment.  It should record
    the feedback the participant actually saw at the time of delivery.
    If the result has been created following delivery *and scoring* via
    some external system it would be appropriate to set the feedback
    string to the message provided by that system on submission such as
    an indication of pass or fail.

    ..  warning::
        Scored results created with QMWISe are not subject to the same
        level of validation as results created and scored using the
        OData :od:feed:`Attempts` feed.  In particular, care is needed
        to ensure that answers adhere to the correct format for the
        question type, as described by :qm:field:`A_Answer.Answer_Full`.
        Furthermore, these values must validate against the associated
        question.  Using the correct revision number and ensuring that
        the indicated When_Started time is consistent with the revision
        history of the associated questions is important to ensure
        consistent reporting in Questionmark Analytics.

    
..  qm:meth::   CreateAssessmentResult2
    :input:     AssessmentResult2    AssessmentResult2
    :output:    Result_ID           string

    Extends the basic :qm:meth:`CreateAssessmentResult` to use the
    updated :qm:xtype:`AssessmentResult2` type.

    
..  qm:meth::   CreateAssessmentResult3
    :input:     AssessmentResult3    AssessmentResult3
    :output:    Result_ID           string

    Extends the basic :qm:meth:`CreateAssessmentResult` to use the
    language-aware :qm:xtype:`AssessmentResult3` type.


..  qm:meth::   CreateAssessmentResultInfoList
    :input:     AssessmentResultInfoList    AssessmentResultInfoList
    :output:    NumberRecordsCreated        int
    
    Creates an entry in :qm:table:`A_Session_Ex` for each item in the
    input list if there is no existing entry available.  Returns the
    number of records that were actually created as a result.
    
    Before a result can be created for an assessment the assessment must
    have an entry in A_Session_Ex.  This method can be used to force the
    creation of a suitable record enabling subsequent calls to
    :qm:meth:`CreateAssessmentResult` to succeed.  (Though see the
    similar :qm:meth:`CreateQuestionResultInfoList`).
    
    For assessments that have been created using Questionmark tools but
    have been delivered by an external system you should use
    :qm:meth:`GetAssessment` to discover the appropriate information
    to pass.
    
    For assessments that have been created *and* delivered externally
    you must create a unique Assessment ID (see :ref:`midlid` for
    important information about the valid set of IDs) that is not
    currently in use.  You may then fill the fields in appropriately to
    describe the external assessment.


..  qm:meth::   CreateAssessmentResultInfoList2
    :input:     AssessmentResultInfoList2    AssessmentResultInfoList2
    :output:    NumberRecordsCreated        int

    Similar to :qm:meth:`CreateAssessmentResultInfoList` but takes an
    extended set of elements allowing two extra fields to be set in the
    database.

    Note that the :qm:xfield:`AssessmentResultInfo2.CourseProperty`
    field should contain the name of the folder containing the
    assessment.  This is not easy to discover using QMWISe as
    :qm:meth:`GetAssessment` returns the ID of the folder (rather than
    the name) and there is no method to get information about a folder
    itself from its ID.  Given this limitation the field should be
    treated as more general metadata. The value of this field is copied
    to the :qm:field:`A_Result.Course` field for each result created for
    this assessment.
    

..  qm:meth::   CreateAssessmentResultInfoList3
    :input:     AssessmentResultInfoList3    AssessmentResultInfoList3
    :output:    NumberRecordsCreated        int
    
    Similar to :qm:meth:`CreateAssessmentResultInfoList2` but takes an
    extended set of elements allowing language information to be set for
    the assessment.
    

..  qm:meth::   CreateQuestionResultInfoList
    :input:     QuestionResultInfoList    QuestionResultInfoList
    :output:    NumberRecordsCreated        int

    Creates an entry in :qm:table:`A_Question_Ex` for each item in the
    input list if there is no existing entry available.  Returns the
    number of records that were actually created as a result.
    
    Before an answer record can be created for a question the quesitno
    must have an entry in A_Question_Ex.  This method can be used to
    force the creation of a suitable record enabling subsequent calls to
    :qm:meth:`CreateAssessmentResult` to succeed.  (Though see the
    similar :qm:meth:`CreateAssessmentResultInfoList`).
    
    Creating answer records with QMWISe for assessments that have been
    created using Questionmark tools but have been delivered by an
    external system is not simple and is discouraged.  Generating the
    outcome information to pass to this method requires detailed
    knowledge of, and access to, the QML description of the question
    itself.
    
    Consider using snapshots in combination with the newer
    :od:feed:`Attempts` feed for this type of project.  The only
    exception to this use case would be when the result info record is
    known to already exist, for example if you are creating a new result
    after re-scoring an existing one.  In that case you would not need
    to call this method.
    
    For assessments that have been created *and* delivered externally
    you must create a unique Question ID (see :ref:`midlid` for
    important information about the valid set of IDs) for each question
    that is not currently in use.  You may then fill the fields in
    appropriately to describe the externally created question.

    
..  qm:meth::   CreateQuestionResultInfoList2
    :input:     QuestionResultInfoList2    QuestionResultInfoList2
    :output:    NumberRecordsCreated        int

    Similar to :qm:meth:`CreateQuestionResultInfoList` but takes an
    extended set of elements allowing language information to be set for
    the assessment.  For use with
    :qm:meth:`CreateAssessmentResultInfoList3`.


..  qm:meth::   GetAssessmentResultInfo
    :input:     Assessment_ID           string
    :output:    AssessmentResultInfo    AssessmentResultInfo

    Returns information from :qm:table:`A_Session_Ex`.  Can be used to
    check that the required information about an Assessment exists
    before creating results with :qm:meth:`CreateAssessmentResult` and
    similar methods.


..  qm:meth::   GetAssessmentResultInfo2
    :input:     Assessment_ID           string
    :output:    AssessmentResultInfo2   AssessmentResultInfo2

    As per :qm:meth:`GetAssessmentResultInfo` but with extended
    information.


..  qm:meth::   GetAssessmentResultInfo3
    :input:     Assessment_ID string, Base boolean, Language string
    :output:    AssessmentResultInfo3   AssessmentResultInfo3

    As per :qm:meth:`GetAssessmentResultInfo` but can be used with
    translated assessments.  For translated assessments the assessment
    is specified with an additional language code and the flag
    indicating whether or not the language is the base language for the
    assessment.  In fact, the flag is actually ignored, if the correct
    value is not known it may be set to false.


..  qm:meth::   GetAssessmentResultInfoList
    :output:    AssessmentResultInfoList    AssessmentResultInfoList

    Returns all records from :qm:table:`A_Session_Ex`.


..  qm:meth::   GetAssessmentResultInfoList2
    :output:    AssessmentResultInfoList2   AssessmentResultInfoList2

    Returns all records from :qm:table:`A_Session_Ex` with additional
    elements as defined in :qm:xtype:`AssessmentResultInfo2`.  Note
    there is not 'GetAssessmentResultInfoList3'.

..  qm:meth::   GetQuestionResultInfoList
    :output:    QuestionResultInfoList   QuestionResultInfoList

    Returns all records from :qm:table:`A_Question_Ex`.  Can be used to
    check that the required information about a Question exists
    before creating results with :qm:meth:`CreateAssessmentResult` and
    similar methods.
    
    ..  warning::   Some repository databases have thousands of
                    delivered questions. This method is not intended for
                    use on larger repositories.  The use cases for using
                    QMWISe to obtain information from
                    :qm:table:`A_Question_Ex` are limited to legacy
                    applications and are documented here only for
                    completeness.  New applications should use the
                    :od:feed:`Attempts` feed in Delivery OData to create
                    externally generated results.


Result Types
~~~~~~~~~~~~


..  qm:xtype::  AssessmentResult

    The XML datatype that provides complete information about a result.
    
    ..  qm:xfield:: Result Result
        :optional:
        
        The summary information for the result. Although marked as
        optional in the schema this element is always present and must
        be provided when creating results.
    
    ..  qm:xfield:: Feedback string
        :optional:

        If present, and non empty, corresponds to the HTML feedback for
        the result as stored in :qm:field:`A_ScoreBand_Ex.Feedback`.
    
    ..  qm:xfield:: AnswerList AnswerList
        :optional:
        
        The list of answers stored for this result.


..  qm:xtype::  AssessmentResult2

    An alternative type used for complete information about a result.
    
    ..  note::  Despite the name this type is *not* a simple extension
                of the similarly named :qm:xtype:`AssessmentResult` type.

    ..  qm:xfield:: Result Result2
        :optional:
        
        The summary information for the result. Although marked as
        optional in the schema this element is always present and must
        be provided when creating results.
    
    ..  qm:xfield:: Feedback string
        :optional:

        If present, and non empty, corresponds to the HTML feedback for
        the result as stored in :qm:field:`A_ScoreBand_Ex.Feedback`.
    
    ..  qm:xfield:: AnswerList AnswerList2
        :optional:
        
        The list of answers stored for this result.

    ..  qm:xfield:: LMSDetails UnencryptedLMSDetails
        :optional:
        
        Deprecated.  This field was originally intended to allow the
        AICC protocol to notify a learning management system of the new
        result.
        
     
..  qm:xtype::  AssessmentResult3

    An alternative type used for complete information about a result
    that uses the language-aware :qm:xtype:`Result3` type.
    
    ..  note::  Despite the name this type is *not* a simple extension
                of the similarly named :qm:xtype:`AssessmentResult2`
                type.

    ..  qm:xfield:: Result Result3
        :optional:
        
        The summary information for the result. Although marked as
        optional in the schema this element is always present and must
        be provided when creating results.
    
    ..  qm:xfield:: Feedback string
        :optional:

        If present, and non empty, corresponds to the HTML feedback for
        the result as stored in :qm:field:`A_ScoreBand_Ex.Feedback`.
    
    ..  qm:xfield:: AnswerList AnswerList2
        :optional:
        
        The list of answers stored for this result.

    ..  qm:xfield:: LMSDetails UnencryptedLMSDetails
        :optional:
        
        Deprecated.  This field was originally intended to allow the
        AICC protocol to notify a learning management system of the new
        result.


..  qm:xtype::  AssessmentResultList
    
    The element type used for a list of assessment results.
    
    ..  qm:xfield:: AssessmentResult AssessmentResult
        :optional:
        :max: unbounded
        
     
..  qm:xtype::  Result

    The XML datatype representing a result.  This is a base type that is
    extended by :qm:xtype:`Result2` and further by :qm:xtype:`Result3`.

    In most cases the fields returned are simply the values from
    associated record in the :qm:table:`A_Result` table in the
    underlying data model.
    
    ..  qm:xfield:: Result_ID   string
        :optional:
        
        See :qm:field:`A_Result.Result_ID`.
        
    ..  qm:xfield:: Assessment_ID   string
        :optional:
    
        See :qm:field:`A_Result.Session_MID` for more information, the
        field value here is the combined ID, as per
        :qm:field:`A_Result.Assessment_ID`

    ..  qm:xfield:: Write_Answer_Data   boolean

        See :qm:field:`A_Result.Write_Answer_Data`.
    
    ..  qm:xfield:: Participant string
        :optional:

        See :qm:field:`A_Result.Participant`.
    
    ..  qm:xfield:: Member_Group    string
        :optional:
    
        See :qm:field:`A_Result.Member_Group`.

    ..  qm:xfield:: Participant_Details string
        :optional:
    
        See :qm:field:`A_Result.Participant_Details`.
    
    ..  qm:xfield:: Hostname    string
        :optional:
    
        See :qm:field:`A_Result.Hostname`.
    
    ..  qm:xfield:: IP_Address  string
        :optional:
        
        See :qm:field:`A_Result.IP_Address`.
    
    ..  qm:xfield:: Still_Going boolean
        
        See :qm:field:`A_Result.Still_Going`.
    
    ..  qm:xfield:: Status  short
    
        See :qm:field:`A_Result.Status`.
    
    ..  qm:xfield:: Feedback    short
    
        See :qm:field:`A_Result.Feedback`.
    
    ..  qm:xfield:: Number_Sections short
    
        See :qm:field:`A_Result.Number_Sections`.

    ..  qm:xfield:: Max_Score   int

        See :qm:field:`A_Result.Max_Score`.

    ..  qm:xfield:: Total_Score int
    
        See :qm:field:`A_Result.Total_Score`.

    ..  qm:xfield:: Special_1   string
        :optional:

        See :qm:field:`A_Result.Special_1`.

    ..  qm:xfield:: Special_2   string
        :optional:

        See :qm:field:`A_Result.Special_2`.

    ..  qm:xfield:: Special_3   string
        :optional:

        See :qm:field:`A_Result.Special_3`.

    ..  qm:xfield:: Special_4   string
        :optional:

        See :qm:field:`A_Result.Special_4`.

    ..  qm:xfield:: Special_5   string
        :optional:

        See :qm:field:`A_Result.Special_5`.

    ..  qm:xfield:: Special_6   string
        :optional:

        See :qm:field:`A_Result.Special_6`.

    ..  qm:xfield:: Special_7   string
        :optional:

        See :qm:field:`A_Result.Special_7`.

    ..  qm:xfield:: Special_8   string
        :optional:

        See :qm:field:`A_Result.Special_8`.

    ..  qm:xfield:: Special_9   string
        :optional:

        See :qm:field:`A_Result.Special_9`.

    ..  qm:xfield:: Special_10   string
        :optional:

        See :qm:field:`A_Result.Special_10`.

    ..  qm:xfield:: Time_Taken   int
    
        See :qm:field:`A_Result.Time_Taken`.

    ..  qm:xfield:: Score_Band_Title   string
        :optional:

        See :qm:field:`A_Result.Score_Band_Title`.

    ..  qm:xfield:: Score_Band_Number   int

        See :qm:field:`A_Result.Score_Band_Number`.
    
    ..  qm:xfield:: Percentage_Score   short

        See :qm:field:`A_Result.Percentage_Score`.
    
    ..  qm:xfield:: Schedule_Name   string
        :optional:

        See :qm:field:`A_Result.Schedule_Name`.

    ..  qm:xfield:: Monitored   boolean

        See :qm:field:`A_Result.Monitored`.
    
    ..  qm:xfield:: Monitor_Name   string
        :optional:

        See :qm:field:`A_Result.Monitor_Name`.

    ..  qm:xfield:: TopicScoringList    TopicScoringList
        :optional:

        A list of topic scores.

    ..  qm:xfield:: When_Started   string
        :optional:

        See :qm:field:`A_Result.When_Started`.

    ..  qm:xfield:: Session_Last_Modified   string
        :optional:

        See :qm:field:`A_Result.Session_Last_Modified`.

    ..  qm:xfield:: When_Finished   string
        :optional:

        See :qm:field:`A_Result.When_Finished`.


..  qm:xtype::  TopicScoringList

    Element used to return a list of topic scores in :qm:xtype:`Result`.
    and :qm:xtype:`EventResult`.
    
    ..  qm:xfield:: TopicScoring   TopicScoring
        :optional:
        :max: unbounded

        Each topic score is contained in its own TopicScoring element. 


..  qm:xtype::  TopicScoring

    Element representing a topic score.  This information is loaded from
    the :qm:table:`A_TopicScore` in the data model.

    ..  qm:xfield:: Topic_ID   string
        :optional:

        See :qm:field:`A_TopicScore.Topic_ID`
        
    ..  qm:xfield:: Topic_Name   string
        :optional:

        See :qm:field:`A_TopicScore.Topic`

    ..  qm:xfield:: Description   string
        :optional:

        See :qm:field:`A_TopicScore.Description`

    ..  qm:xfield:: Percentage_Score   double

        See :qm:field:`A_TopicScore.Percentage_Score`

    ..  qm:xfield:: Actual_Score   int

        See :qm:field:`A_TopicScore.Actual_Score`

    ..  qm:xfield:: Maximum_Score   int

        See :qm:field:`A_TopicScore.Maximum_Score`

    ..  qm:xfield:: Num_Questions   int
    
        See :qm:field:`A_TopicScore.Num_Questions`


..  qm:xtype::   Result2 Result

    ..  qm:xfield:: FirstName string
        :optional:
        
        See :qm:field:`A_Result.First_Name`.

    ..  qm:xfield:: LastName string
        :optional:

        See :qm:field:`A_Result.Last_Name`.
        
    ..  qm:xfield:: PrimaryEmailAddress string
        :optional:
        
        See :qm:field:`A_Result.Primary_Email`.

    ..  qm:xfield:: SubgroupPath string
        :optional:

        If the result is associated with a sub-group then this field may
        contain the path to the subgroup with the top-level group as the
        first path component.  The path separator is the back-slash
        character.
        
        Whether or not the value of this element is set on a retrieved
        result will depend on the delivery mode used to create it.  See
        :qm:field:`A_Result.Member_Sub_Group_1` for more information.
        
    ..  qm:xfield:: CourseProperty string
        :optional:
        
        See :qm:field:`A_Result.Course`.        
        
    ..  qm:xfield:: ScoreBandIDProperty int

        See :qm:field:`A_Result.ScoreBand_ID`.


..  qm:xtype::  Result3 Result2

    An extension of the result element type that includes information
    about the language of the assessment taken.  Currently used only for
    creating results.
    
    ..  qm:xfield:: Language string
        :optional:
        
        See :qm:field:`A_Result.Lang`.  When creating results there must
        be an entry in :qm:table:`A_Session_Ex` that matches both the
        Assessment_ID (defined by the base Result type) *and* the
        Language.

    ..  qm:xfield:: Base boolean
        
        Indicates if Language is the base language for the assessment or
        a translation. This field is actually used only for the creation
        of feedback and, along with Language, is used to set the
        language information for the ScoreBand (feedback) associated
        with the result.  See :qm:field:`A_ScoreBand.Base` for more
        information.

    
..  qm:xtype::  ResultList
    
    The type used to serialize a list of results.
    
    ..  qm:xfield:: Result Result
        :optional:
        :max: unbounded


..  qm:xtype::  Answer

    Fields largely correspond to the similarly named fields  in
    :qm:table:`A_Answer`.
    
    ..  qm:xfield:: Question_ID string
        :optional:

        The ID of the Question, calculated from the MID and LID, see
        :qm:field:`A_Answer.Question_MID`.
        
    ..  qm:xfield:: Revision int

        See :qm:field:`A_Answer.Revision`.
        
    ..  qm:xfield:: Occurrence short

        See :qm:field:`A_Answer.Occurrence`.
        
    ..  qm:xfield:: Topic_Name string
        :optional:

        See :qm:field:`A_Answer.Topic`.
                
    ..  qm:xfield:: Block_Number short

        See :qm:field:`A_Answer.Block_Number`.
        
    ..  qm:xfield:: Question_Number short

        See :qm:field:`A_Answer.Question_Number`.
        
    ..  qm:xfield:: Status short

        See :qm:field:`A_Answer.Status`.
        
    ..  qm:xfield:: Times_Answered short

        See :qm:field:`A_Answer.Times_Answered`.
        
    ..  qm:xfield:: Max_Score int

        See :qm:field:`A_Answer.Max_Score`.

    ..  qm:xfield:: Actual_Score int

        See :qm:field:`A_Answer.Actual_Score`.

    ..  qm:xfield:: Know_Time_Taken boolean

        See :qm:field:`A_Answer.Know_Time_Taken`.

    ..  qm:xfield:: Time_Taken int

        See :qm:field:`A_Answer.Time_Taken`.

    ..  qm:xfield:: Number_Outcomes short

        See :qm:field:`A_Answer.Number_Outcomes`.

    ..  qm:xfield:: Outcome_Number short

        See :qm:field:`A_Answer.Outcome_Number`.

    ..  qm:xfield:: Outcome_Exponential int

        See :qm:field:`A_Answer.Outcome_Exponential`.  Note that the
        underlying data model allows for 64 outcome bits through the
        provision of a second field
        :qm:field:`A_Answer.Outcome_Exponential_2` but that this field is
        not included in the basic Answer element, this omission was
        corrected with the creation of :qm:xtype:`Answer2`.        

    ..  qm:xfield:: Answer_Truncated string
        :optional:

        See :qm:field:`A_Answer.Answer_Truncated`.
        
    ..  qm:xfield:: Answer_Full string
        :optional:

        See :qm:field:`A_Answer.Answer_Full`.
        
    ..  qm:xfield:: Comment string
        :optional:

        The associated participant comment, obtained from the related
        entity in :qm:field:`A_Comment.Comments` (if present).


..  qm:xtype::  Answer2 Answer

    A small update to the base class to correct the limitation on the
    number of reported outcomes for a question.

    ..  qm:xfield:: Outcome_Exponential2Property int

        Extends QMWISe to support the full 64-outcomes per question when
        performing operations on answer records.  See
        :qm:field:`A_Answer.Outcome_Exponential_2` and the note above in
        :qm:xfield:`Answer.Outcome_Exponential`.
        
        ..  note::
            The name of this element does not conform to the pattern
            in either the data model or the base type being extended.        


..  qm:xtype::  AnswerList
    
    The type used to serialize a list of answers.
    
    ..  qm:xfield:: Answer Answer
        :optional:
        :max: unbounded


..  qm:xtype::  AnswerList2
    
    The type used to serialize a list of answers using the updated
    :qm:xtype:`Answer2` content model.
    
    ..  qm:xfield:: Answer2 Answer2
        :optional:
        :max: unbounded


..  qm:xtype::  AssessmentResultInfo

    Records information about an assessment that has been used to
    generate results - used prior to creating results.  See
    :qm:meth:`CreateAssessmentResultInfoList`.
    
    ..  qm:xfield:: Assessment_ID string
        :optional:

    ..  qm:xfield:: Revision int

    ..  qm:xfield:: Session_Name string
        :optional:

    ..  qm:xfield:: Session_Author string
        :optional:

    ..  qm:xfield:: Whether_Time_Limit boolean

    ..  qm:xfield:: Time_Limit int

    ..  qm:xfield:: Number_Sections short

    ..  qm:xfield:: Description string
        :optional:

    ..  qm:xfield:: Last_Updated string
        :optional:

    ..  qm:xfield:: When_Modified string
        :optional:


..  qm:xtype::  AssessmentResultInfo2   AssessmentResultInfo

    Extends the base class adding the following elements.  For usage see
    :qm:meth:`CreateAssessmentResultInfoList2`.
    
    ..  qm:xfield:: Assessment_TypeProperty int

        Sets the assessment type from one of the constants defined by
        :qm:field:`S_Header_Ex.Assessment_Type`.
        
    ..  qm:xfield:: CourseProperty string
        :optional:
        
        The name of the assessment folder that contains the assessment.


..  qm:xtype::  AssessmentResultInfo3   AssessmentResultInfo2

    Extends the base classes with elements for specifying if the
    assessment has been translated and whether or not this is the base
    language.
    
    ..  qm:xfield:: Base boolean

        True if the language given is the base language.
        
    ..  qm:xfield:: Language string
        :optional:

        The language code of the language the assessment was presented
        in.
        

..  qm:xtype::  AssessmentResultInfoList

    Element that contains a list of AssessmentResultInfo.
    
    ..  qm:xfield:: AssessmentResultInfo AssessmentResultInfo
        :optional:
        :max: unbounded


..  qm:xtype::  AssessmentResultInfoList2

    Element that contains a list of AssessmentResultInfo2.
    
    ..  qm:xfield:: AssessmentResultInfo2 AssessmentResultInfo2
        :optional:
        :max: unbounded


..  qm:xtype::  AssessmentResultInfoList3

    Element that contains a list of AssessmentResultInfo3.
    
    ..  qm:xfield:: AssessmentResultInfo3 AssessmentResultInfo3
        :optional:
        :max: unbounded


..  qm:xtype::  QuestionResultInfo

    Records information about a question that has been used to generate
    answers - used prior to creating results.  See
    :qm:meth:`CreateQuestionResultInfoList`.

    ..  qm:xfield:: Question_ID string
        :optional:

    ..  qm:xfield:: Revision int
    
    ..  qm:xfield:: Question_Description string
        :optional:

    ..  qm:xfield:: Question_Type string
        :optional:

    ..  qm:xfield:: Topic_Name string
        :optional:

    ..  qm:xfield:: Number_Outcomes short

    ..  qm:xfield:: Question_Wording string
        :optional:

    ..  qm:xfield:: OutcomeList OutcomeList
        :optional:

    ..  qm:xfield:: Last_Updated string
        :optional:


..  qm:xtype::  Outcome

    ..  qm:xfield:: Outcome_Number short

    ..  qm:xfield:: Outcome_Name string
        :optional:

    ..  qm:xfield:: Feedback string
        :optional:


..  qm:xtype::  OutcomeList

    Element that contains a list of Outcomes.

    ..  qm:xfield:: Outcome Outcome
        :optional:
        :max: unbounded


..  qm:xtype::  QuestionResultInfo2 QuestionResultInfo

    Extends the base QuestionResultInfo to include support for
    translated questions.

    ..  qm:xfield:: Base boolean

    ..  qm:xfield:: Language string
        :optional:


..  qm:xtype::  QuestionResultInfoList

    Element that contains a list of QuestionResultInfo.

    ..  qm:xfield:: QuestionResultInfo QuestionResultInfo
        :optional:
        :max: unbounded


..  qm:xtype::  QuestionResultInfoList2

    Element that contains a list of QuestionResultInfoList2.

    ..  qm:xfield:: QuestionResultInfoList2 QuestionResultInfoList2
        :optional:
        :max: unbounded


..  qm:xtype::   EventResult

    The XML datatype representing a result as returned by the special
    method :qm:meth:`GetResultListBySubGroup`.
    
    In most cases the fields returned are simply the values from
    associated record in the :qm:table:`A_Result` table in the
    underlying data model.
    
    ..  qm:xfield:: Result_ID   string
        :optional:
        
        See :qm:field:`A_Result.Result_ID`.
        
    ..  qm:xfield:: Assessment_ID   string
        :optional:
    
        See :qm:field:`A_Result.Session_MID` for more information, the
        field value here is the combined ID, as per
        :qm:field:`A_Result.Assessment_ID`

    ..  qm:xfield:: Write_Answer_Data   boolean

        See :qm:field:`A_Result.Write_Answer_Data`.
    
    ..  qm:xfield:: Participant string
        :optional:

        See :qm:field:`A_Result.Participant`.
    
    ..  qm:xfield:: Member_Group    string
        :optional:
    
        See :qm:field:`A_Result.Member_Group`.

    ..  qm:xfield:: Participant_Details string
        :optional:
    
        See :qm:field:`A_Result.Participant_Details`.
    
    ..  qm:xfield:: Hostname    string
        :optional:
    
        See :qm:field:`A_Result.Hostname`.
    
    ..  qm:xfield:: IP_Address  string
        :optional:
        
        See :qm:field:`A_Result.IP_Address`.
    
    ..  qm:xfield:: Still_Going boolean
        
        See :qm:field:`A_Result.Still_Going`.
    
    ..  qm:xfield:: Status  short
    
        See :qm:field:`A_Result.Status`.
    
    ..  qm:xfield:: Feedback    short
    
        See :qm:field:`A_Result.Feedback`.
    
    ..  qm:xfield:: Number_Sections short
    
        See :qm:field:`A_Result.Number_Sections`.

    ..  qm:xfield:: Max_Score   int

        See :qm:field:`A_Result.Max_Score`.

    ..  qm:xfield:: Total_Score int
    
        See :qm:field:`A_Result.Total_Score`.

    ..  qm:xfield:: Special_1   string
        :optional:

        See :qm:field:`A_Result.Special_1`.

    ..  qm:xfield:: Special_2   string
        :optional:

        See :qm:field:`A_Result.Special_2`.

    ..  qm:xfield:: Special_3   string
        :optional:

        See :qm:field:`A_Result.Special_3`.

    ..  qm:xfield:: Special_4   string
        :optional:

        See :qm:field:`A_Result.Special_4`.

    ..  qm:xfield:: Special_5   string
        :optional:

        See :qm:field:`A_Result.Special_5`.

    ..  qm:xfield:: Special_6   string
        :optional:

        See :qm:field:`A_Result.Special_6`.

    ..  qm:xfield:: Special_7   string
        :optional:

        See :qm:field:`A_Result.Special_7`.

    ..  qm:xfield:: Special_8   string
        :optional:

        See :qm:field:`A_Result.Special_8`.

    ..  qm:xfield:: Special_9   string
        :optional:

        See :qm:field:`A_Result.Special_9`.

    ..  qm:xfield:: Special_10   string
        :optional:

        See :qm:field:`A_Result.Special_10`.

    ..  qm:xfield:: Time_Taken   int
    
        See :qm:field:`A_Result.Time_Taken`.

    ..  qm:xfield:: Score_Band_Title   string
        :optional:

        See :qm:field:`A_Result.Score_Band_Title`.

    ..  qm:xfield:: Score_Band_Number   int

        See :qm:field:`A_Result.Score_Band_Number`.
    
    ..  qm:xfield:: Percentage_Score   short

        See :qm:field:`A_Result.Percentage_Score`.
    
    ..  qm:xfield:: Schedule_Name   string
        :optional:

        See :qm:field:`A_Result.Schedule_Name`.

    ..  qm:xfield:: Monitored   boolean

        See :qm:field:`A_Result.Monitored`.
    
    ..  qm:xfield:: Monitor_Name   string
        :optional:

        See :qm:field:`A_Result.Monitor_Name`.

    ..  qm:xfield:: topicScoringList    TopicScoringList
        :optional:

        ..  note::
            The name of this element differs from the corresponding field
            in :qm:xtype:`Result` in the case of the first letter.

    ..  qm:xfield:: ScoreBandID int

        ..  note::
            The name of this element differs from the corresponding field
            in :qm:xtype:`Result2`.

        See :qm:field:`A_Result.ScoreBand_ID`.

    ..  qm:xfield:: Course string
        :optional:
        
        ..  note::
            The name of this element differs from the corresponding field
            in :qm:xtype:`Result2`.

        See :qm:field:`A_Result.Course`.        

    ..  qm:xfield:: Participant_FirstName string
        :optional:
        
        ..  note::
            The name of this element differs from the corresponding field
            in :qm:xtype:`Result2`.

        See :qm:field:`A_Result.First_Name`.

    ..  qm:xfield:: Participant_LastName string
        :optional:

        ..  note::
            The name of this element differs from the corresponding field
            in :qm:xtype:`Result2`.
        
        See :qm:field:`A_Result.Last_Name`.

    ..  qm:xfield:: Result_Value string
        :optional:

        Essentially, this value indicates if the participant achieved
        the best possible assessment outcome (not to be confused with
        the maximum possible score).  For example, if the assessment
        defines two outcomes bands for pass and fail then this value
        would be "1" if the participant passed and "0" if they failed.
        Similarly, if the assessment had 5 outcome bands representing
        grades "A" to "E" with "A" being the highest scoring then this
        field would be "1" if the participant achieved grade A.
                
        "0"
            The percentage score in the result was not in the highest
            scoring outcome band.
        
        "1" 
            The percentage score in the result was in the highest scoring
            outcome band.
        
        ""
            There was no information about outcome bands available.


    ..  qm:xfield:: Member_Sub_Group_1 string
        :optional:

        See :qm:field:`A_Result.Member_Sub_Group_1`.

                    
    ..  qm:xfield:: Assessment_Name string
        :optional:

        The name of the Assessement referenced by
        :qm:xfield:`EventResult.Assessment_ID`.  
                    
        The name is obtained by looking up information in
        :qm:table:`S_AML`.

        
    ..  qm:xfield:: When_Started   string
        :optional:

        See :qm:field:`A_Result.When_Started`.


    ..  qm:xfield:: Session_Last_Modified   string
        :optional:

        See :qm:field:`A_Result.Session_Last_Modified`.


    ..  qm:xfield:: When_Finished   string
        :optional:

        See :qm:field:`A_Result.When_Finished`.


..  qm:xtype::  EventResultList
    
    The type used to serialize a list of results by
    :qm:meth:`GetResultListBySubGroup`.
    
    ..  qm:xfield:: EventResult EventResult
        :optional:
        :max: unbounded


..  qm:xtype::  UnencryptedLMSDetails LMSDetails
    
    Deprecated.
    
    ..  qm:xfield:: Password string
        :optional:


..  qm:xtype::  LMSDetails
    
    Deprecated.
    
    ..  qm:xfield:: SessionId string
        :optional:

    ..  qm:xfield:: LmsUrl string
        :optional:


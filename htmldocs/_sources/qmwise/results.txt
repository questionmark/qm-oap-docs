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
    

Result Types
~~~~~~~~~~~~

..  qm:xtype::   Result

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

    TODO    

    
..  qm:xtype::  ResultList
    
    The type used to serialize a list of results.
    
    ..  qm:xfield:: Result Result
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


Assessments
-----------

This part of the guide is under development.  Please refer to the
`Assessments
<https://support.questionmark.com/content/questionmark-perception-57-qmwise-api-guide-assessments>`_
section of the old guide for more information.


Assessment Methods
~~~~~~~~~~~~~~~~~~

..  qm:meth::   GetAssessment
    :input:     Assessment_ID   string
    :output:    Assessment      Assessment


..  qm:meth::   GetAssessmentList
    :output:    AssessmentList    AssessmentList


..  qm:meth::   GetAssessmentListByAdministrator
    :input:     Administrator_ID        string
    :output:    AssessmentList          AssessmentList


..  qm:meth::   GetAssessmentListByGroup
    :input:     Group_ID            string
    :output:    AssessmentList      AssessmentList


..  qm:meth::   GetAssessmentReportedTopics
    :input:     Assessment_ID    string
    :output:    TopicList        TopicList

    Returns a list with the full details of all the topics that are
    reported on in this assessment.
    

..  qm:meth::   DeleteAssessment
    :input:     Assessment_ID   string


Assessment Folders
~~~~~~~~~~~~~~~~~~    

..  qm:meth::   CreateAssessmentFolder
    :input:     AssessmentFolder    AssessmentFolder
    :output:    Folder_ID           string


..  qm:meth::   GetAssessmentTreeByAdministrator
    :input:     Administrator_ID string, Parent_ID string, OnlyRunFromIntegration int
    :output:    AssessmentTreeItemList  AssessmentTreeItemList
    

Assessment Definitions
~~~~~~~~~~~~~~~~~~~~~~

..  qm:meth::   CreateAssessmentDefinition
    :input:     AssessmentDefinition                AssessmentDefinition
    :output:    CreateAssessmentDefinitionResult    string


..  qm:meth::   GetAssessmentDefinition
    :input:     Assessment_ID           string
    :output:    AssessmentDefinition    AssessmentDefinition


..  qm:meth::   SetAssessmentDefinition
    :input:     AssessmentDefinition    AssessmentDefinition


Misc Methods
~~~~~~~~~~~~

..  qm:meth::   ConfirmAssessmentDownload
    :input:     Schedule_ID                         string
    :output:    ConfirmAssessmentDownloadResponse   int


Assessment Types
~~~~~~~~~~~~~~~~

..  qm:xtype::   Assessment

    ..  qm:xfield:: Assessment_ID string
        :optional:

    ..  qm:xfield:: Revision int

    ..  qm:xfield:: Session_Name string
        :optional:

    ..  qm:xfield:: Author string
        :optional:

    ..  qm:xfield:: Save_Answers boolean

    ..  qm:xfield:: Save_Answer_Data boolean

    ..  qm:xfield:: Open_Session boolean

    ..  qm:xfield:: Session_Password string
        :optional:

    ..  qm:xfield:: Session_Timed boolean

    ..  qm:xfield:: Time_Limit int

    ..  qm:xfield:: Template_Name string
        :optional:

    ..  qm:xfield:: When_Feedback int

    ..  qm:xfield:: End_Feedback int

    ..  qm:xfield:: Exclude_Unscored boolean

    ..  qm:xfield:: Folder_ID int
        :optional:

    ..  qm:xfield:: Lang string
        :optional:

    ..  qm:xfield:: Description string
        :optional:

    ..  qm:xfield:: Monitored int

    ..  qm:xfield:: Editor string
        :optional:

    ..  qm:xfield:: Version string
        :optional:

    ..  qm:xfield:: Permit_External_Call boolean

    ..  qm:xfield:: Created_Date string
        :optional:

    ..  qm:xfield:: Modified_Date string
        :optional:


..  qm:xtype::   AssessmentList

    Element containing a list of Assessment elements.
    
    ..  qm:xfield:: Assessment   Assessment
        :optional:
        :max: unbounded


..  qm:xtype::   AssessmentDefinition

    ..  qm:xfield:: Assessment Assessment
        :optional:

    ..  qm:xfield:: AssessmentBlockList AssessmentBlockList
        :optional:

    ..  qm:xfield:: AssessmentOutcomeList AssessmentOutcomeList
        :optional:


..  qm:xtype::   AssessmentBlock

    ..  qm:xfield:: Block_Name string
        :optional:

    ..  qm:xfield:: Feedback boolean

    ..  qm:xfield:: Shuffle_Questions boolean

    ..  qm:xfield:: Suspend_Time_Limit boolean

    ..  qm:xfield:: Use_Template_File boolean

    ..  qm:xfield:: Template_Name string
        :optional:

    ..  qm:xfield:: Introduction_Text string
        :optional:

    ..  qm:xfield:: ItemList ItemList
        :optional:


..  qm:xtype::   AssessmentBlockList

    ..  qm:xfield:: AssessmentBlock AssessmentBlock
        :optional:
        :max: unbounded    


..  qm:xtype::   Item

    ..  qm:xfield:: Method int

    ..  qm:xfield:: Include_Sub_Topics boolean

    ..  qm:xfield:: Topic_ID string
        :optional:

    ..  qm:xfield:: Number_Of_Questions int

    ..  qm:xfield:: Question_ID string
        :optional:


..  qm:xtype::   ItemList

    ..  qm:xfield:: Item Item
        :optional:
        :max: unbounded    


..  qm:xtype::   AssessmentOutcome

    ..  qm:xfield:: Outcome_Name string
        :optional:

    ..  qm:xfield:: Session_Score boolean

    ..  qm:xfield:: Topic_Scores boolean

    ..  qm:xfield:: Topic_Feedback boolean

    ..  qm:xfield:: Branch int

    ..  qm:xfield:: Assessment_ID string
        :optional:

    ..  qm:xfield:: Destination string
        :optional:

    ..  qm:xfield:: Message string
        :optional:

    ..  qm:xfield:: Min_Percent int

    ..  qm:xfield:: Max_Percent int


..  qm:xtype::   AssessmentOutcomeList

    ..  qm:xfield:: AssessmentOutcome AssessmentOutcome
        :optional:
        :max: unbounded    


..  qm:xtype::   AssessmentFolder

    ..  qm:xfield:: ID string
        :optional:

    ..  qm:xfield:: Name string
        :optional:

    ..  qm:xfield:: Description string
        :optional:

    ..  qm:xfield:: Parent_ID string
        :optional:



..  qm:xtype::   AssessmentTreeItem

    ..  qm:xfield:: ID string
        :optional:

    ..  qm:xfield:: Type int

    ..  qm:xfield:: Name string
        :optional:

    ..  qm:xfield:: Parent_ID string
        :optional:



..  qm:xtype::   AssessmentTreeItemList

    ..  qm:xfield:: AssessmentTreeItem AssessmentTreeItem
        :optional:
        :max: unbounded    



..  qm:xtype::   Topic

    The XML datatype representing a Topic.
    
    In most cases the fields returned are simply the values from
    associated record in the :qm:table:`Q_Topic_Ex` table in the
    underlying data model.
    
    ..  qm:xfield:: Topic_ID   string
        :optional:
        
        See :qm:field:`Q_Topic_Ex.Topic_ID`.
        
    ..  qm:xfield:: Parent_ID   string
        :optional:
    
        See :qm:field:`Q_Topic_Ex.Parent_ID`.

    ..  qm:xfield:: Topic_Name   string
        :optional:

        See :qm:field:`Q_Topic_Ex.Name`.
 
    ..  qm:xfield:: Topic_Description   string
        :optional:

        See :qm:field:`Q_Topic_Ex.Description`.
 
    ..  qm:xfield:: ScoreBandList   ScoreBandList
        :optional:

        Information expanded from the related :qm:table:`Q_ScoreBand_Ex`.
 
 
..  qm:xtype::  TopicList

    Element that contains a list of Topics.
    
    ..  qm:xfield:: Topic Topic
        :optional:
        :max: unbounded    


..  qm:xtype::   ScoreBandList

    Element containing a list of ScoreBand elements.
    
    ..  qm:xfield:: ScoreBand   ScoreBand
        :optional:
        :max: unbounded


..  qm:xtype::   ScoreBand

    The XML datatype representing a ScoreBand.
    
    In most cases the fields returned are simply the values from the
    associated record in the :qm:table:`Q_ScoreBand_Ex` table in the
    underlying data model.

    ..  qm:xfield:: Name   string
        :optional:

        See :qm:field:`Q_ScoreBand_Ex.Name`.

    ..  qm:xfield:: Min_Score   double

        See :qm:field:`Q_ScoreBand_Ex.Min_Score`.

    ..  qm:xfield:: Max_Score   double

        See :qm:field:`Q_ScoreBand_Ex.Max_Score`.

    ..  qm:xfield:: Message   string
        :optional:

        See :qm:field:`Q_ScoreBand_Ex.Message`.


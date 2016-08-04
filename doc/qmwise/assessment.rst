Assessments
-----------

Assessment Methods
~~~~~~~~~~~~~~~~~~

..  qm:meth::   GetAssessmentReportedTopics
    :input:     Assessment_ID    string
    :output:    TopicList        TopicList

    Returns a list with the full details of all the topics that are
    reported on in this assessment.
    

TBC


Assessment Types
~~~~~~~~~~~~~~~~

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


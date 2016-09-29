ScoringTask, ScoringResult and DimensionScore
---------------------------------------------

..  od:service::    deliveryodata

For a worked example of using these entities to set scores for
unscored responses please refer to :doc:`scoring`.

..  od:type::   ScoringTask

    A ScoringTask is created each time a participant submits an answer to
    an unscored question.
    
    ScoringTasks are keyed on a tuple of (:od:prop:`QuestionID`,
    :od:prop:`ResultID`).  On their own these values are insufficient to
    identify an answer record uniquely because a participant may answer
    the same question multiple times in a single assessment (but not
    twice in the same block).  The lack of an
    :od:prop:`Answer.BlockNumber` property means that, for the purposes
    of subjective scoring, an assessment must contain no more than one
    instance of each unscored question. Assessments that do not satisfy
    this constraint cannot be subjectively marked.  In practice, this is
    not a significant limitation.
 
    ..  od:prop::   QuestionID    Edm.Int64
        :key:
        :notnull:

        The identifier of the question that the participant's answer was
        a response to.  The :od:prop:`Question` navigation property
        provides a more convenient way to obtain the associated question
        entity.

    ..  od:prop::   ResultID    Edm.Int32
        :key:
        :notnull:

        The identifier of the result record that contains the answer. 
        The
        :od:prop:`Result` navigation property provides a more convenient
        way to obtain the associated result entity.
        
    ..  od:prop::   Status    Edm.Int32
        :notnull:

        The status of this task:
        
            0   Unscored
            
            1   Locked: in this state the task cannot be scored in the
                native scoring tool in Enterprise Manager
            
            2   Saved: indicates that some scores have been recorded but
                the scoring process is not yet complete.
            
            3   Scored: indicates that the scores have been finalised
                for this task.

        The value of this property can be updated using the PUT method
        on the entity.
                
    ..  od:prop::   Question    Question
    
        A navigation property to the question the participant answered.

    ..  od:prop::   Result    Result
    
        A navigation property to the result associated with the
        participant's answer.
    
    ..  od:prop::   Group    Group
    
        A navigation property to the optional group that provides a
        context for the participant's result.  For example, if the
        result was generated from an assessment scheduled to a group of
        participants the group will be available here.
    
    ..  od:prop::   Assessment    Assessment
    
        A navigation property to the assessment the participant was
        taking when they answered the question.
            
    ..  od:prop::   ScoringResult    ScoringResult
        :collection:
    
        A navigation property to the entity representing the scores
        awarded to the participant by the external marking process.
        Although this navigation property yields a collection there can
        be at most one scoring result associated with a scoring task.
        
        The ScoringResult is created automatically the first time this
        collection is retrieved.
        
        ..  warning::   if you expand this navigation property the API
                        will yield an empty collection if the
                        ScoringResult has not yet been created.  To
                        ensure that the entity is created you must load
                        this collection directly, e.g.::
                      
                            deliveryodata/123456/ScoringTask(...)/ScoringResult
                    
                        The brackets would contain the key identifying
                        the ScoringTask entity and have been omitted in
                        the example to improve readability.

                        The Question that generated the answer *MUST* be
                        associated with a rubric before any
                        ScoringResults can be created.  Failure to
                        obtain a ScoringResult entity for a ScoringTask
                        usually indicates that the Question has not yet
                        been associated with a Rubric.
                        
    ..  od:prop::   Answer  Answer
        :collection:
        
        A navigation property to the entity representing the participant's
        answer.  Although defined as a collection there will always
        be a single Answer entity associated with each ScoringTask.  
        

..  od:type::   ScoringResult

    Results are scored using ScoringResult entities.  These entities are
    created automatically as required when the navigation collection of
    the associated ScoringTask is retrieved.  See
    :od:prop:`ScoringTask.ScoringResult` for details.
    
    The data exposed by this entity is stored in the
    :qm:table:`ST_RUBRICSCORES` table in the data model.
    
    ..  od:prop::   QuestionID    Edm.Int64
        :key:
        :notnull:

        The identifier of the question - used as part of the key
        required to identify the associated ScoringTask.

    ..  od:prop::   ResultID    Edm.Int32
        :key:
        :notnull:

        The identifier of the result - used as part of the key required
        to identify the associated ScoringTask.

    ..  od:prop::   RubricID    Edm.Int32
        :key:
        :notnull:

        The identifier of the Rubric that defines the rules for scoring
        the participants response.  This property is part of the key of
        the entity and, hence, the question that generated a ScoringTask
        must have an associated rubric before a ScoringResult entity can
        be created to score it.
        
    ..  od:prop::   Score    Edm.Int32

        The total score for the question awarded to the participant.
        This property can be updated using the PUT method on the entity.
        The score must be calculated externally and should be equal to
        the sum of the individual :od:prop:`DimensionScores`.  This
        constraint is not checked by the API, it is recommended that
        when updating scores you use the PUT method to update individual
        DimensionScores first and then calculate the total and update
        this property of the ScoringTask.
        
        When the ScoringTask is finalised (status is set to Scored) then
        this is the value that is used to update the score in the Answer
        entity and the corresponding result.
        
    ..  od:prop::   Comments    Edm.String

        A text string containing comments from the person or system
        doing the scoring.
        
    ..  od:prop::   Annotated    Edm.String

        An annotated version of the participant's answer as an HTML
        fragment.  See :qm:field:`ST_RUBRICSCORES.ST_ANNOTATED` for more
        information about this field.

    ..  od:prop::   CreatedDateTime  Edm.DateTime
        :notnull:
    
        A time stamp of when the entity was created.  Set automatically,
        it cannot be modified.
        
    ..  od:prop::   ModifiedDateTime  Edm.DateTime
        :notnull:
    
        A time stamp of when the entity was last modified.
        
        ..  note::  when updating the score, you must PUT the updated
                    entity with the same ModifiedDateTime value as you
                    received when you retrieved the entity. If the
                    ModifiedDateTime date on the server has changed,
                    then you'll get a contention error and the update
                    will fail (with a 400 series error).  In that case
                    you'll have to retrieve the record again and compare
                    the current values to determine whether to retry or
                    abort. This procedure replaces the concept of
                    "locking" a result for scoring with a form of
                    optimistic concurrency control.

    ..  od:prop::   ScoringTask ScoringTask
    
        The ScoringTask that this entity is providing scores for.
                 
    ..  od:prop::   Rubric Rubric
    
        The Rubric used to score the participant's answer.
                 
    ..  od:prop::   DimensionScores DimensionScore
        :collection:
        
        A collection of DimensionScores, one per dimension defined by the
        Rubric.


..  od:type::   DimensionScore

    A DimensionScore is an instance of a score for a specific
    participant's result.  The entity is created automatically with the
    associated :od:type:`ScoringResult`.
    
    ..  od:prop::   QuestionID    Edm.Int64
        :key:
        :notnull:

        The identifier of the question that this score relates to.
        
    ..  od:prop::   ResultID    Edm.Int32
        :key:
        :notnull:

        The identifier of the result that was being scored.  Together
        with the :od:prop:`QuestionID` this identifies the
        :od:type:`ScoringTask` associated with this score.
        
    ..  od:prop::   RubricID    Edm.Int32
        :key:
        :notnull:

        The identifier of the rubric containing the dimension being
        scored.
        
    ..  od:prop::   Order    Edm.Int32
        :key:
        :notnull:

        The order number of the dimension being scored within the
        defining rubric.  Together with the :od:prop:`RubricID` this
        uniquely identifies the :od:type:`Dimension` being scored.
        
    ..  od:prop::   Score    Edm.Int16

        The score being awarded to this participant for this dimension.
        This value can be updated using the PUT method on the entity.
        
    ..  od:prop::   Comment    Edm.String

    ..  od:prop::   ScoringResult    Edm.ScoringResult

    ..  od:prop::   Dimension    Edm.Dimension

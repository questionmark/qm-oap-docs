Rubric and Dimension
--------------------

..  od:service::    deliveryodata

..  od:feed::   Rubrics Rubric

    :method GET: read only

    The Rubrics feed contains the scoring rules for subjective questions.


..  od:feed::   Dimensions Dimension

    :method GET: this feed is read only
    :filter ID: primary key
    :expand Rubric: expands the associated Rubric    
    :expand DimensionScores: expands the associated collection of scores    
    
    The Dimensions feed contains information about the scoring
    dimensions associated with a rubric and is used for subjective
    marking.


..  od:type::   Rubric

    ..warning:: the Scoring Tool in Enterprise Manager provides some
                additional security by allowing users to specify
                separate passwords that protect access to a rubric (for
                viewing and editing) and the associated rubric scores.
                These passwords are not supported by the Delivery OData
                API.

    The term 'Rubric' can be open to confusion.  In this context it
    refers to the instructions to graders (scorers) for grading answers.
    Rubrics may be shared by multiple questions.
        
    ..  od:prop::   ID    Edm.Int32
        :key:
        :notnull:

    ..  od:prop::   Name    Edm.String

        The name of this Rubric.
        
    ..  od:prop::   CreatedDateTime    Edm.DateTime
        :notnull:

    ..  od:prop::   ModifiedDateTime    Edm.DateTime
        :notnull:

    ..  od:prop::   Instructions    Edm.String

    ..  od:prop::   MaxScore    Edm.Int16
        :notnull:

        The maximum score associated with the Rubric.
                
    ..  od:prop::   ShowParticipant    Edm.String
        :notnull:

    ..  od:prop::   Dimensions    Dimension
        :collection:
        
        The scoring for the Question is divided into separate Dimensions
        that represent different aspects of the scoring.  For example,
        an essay might be scored separately on relevance, organization
        and style of language.  Each dimension of the rubric is
        represented by separate Dimension entity in this collection.

    ..  od:prop::   Questions    Question
        :collection:

        Each Rubric may be associated with multiple Questions.  This
        allows standardized rubrics to be created and associated with
        all similar tasks.  Rubrics and Questions are associated using
        Enterprise Manager.

    ..  od:prop::   ScoringResults    ScoringResult
        :collection:

        The combined results of all scoring tasks associated with this
        rubric.

                 
..  od:type::   Dimension

    ..  od:prop::   ID    Edm.Int32
        :key:
        :notnull:
    
        The unique ID of this dimension.

    ..  od:prop::   RubricID    Edm.Int32
        :notnull:

        The ID of the associated rubric.  You may also use the
        navigation property :od:prop:`Rubric` to obtain this entity
        directly.
        
    ..  od:prop::   Order    Edm.Int32
        :notnull:

        The order of this dimension (for presentation to human markers).
        
    ..  od:prop::   Name    Edm.String

        The human-readable name of this dimension.
        
    ..  od:prop::   Instructions    Edm.String

        The human-readable instructions for scoring this dimension.
        
    ..  od:prop::   MaxScore    Edm.Int16
        :notnull:

        The maximum permitted score for this dimension.  Scores may
        range from 0 up to and including MaxScore.
        
    ..  od:prop::   Rubric    Rubric
        :notnull:

        The navigation property to the associated :od:type:`Rubric`.
        
    ..  od:prop::   DimensionScores    DimensionScore
        :collection:

        A navigation property to all scores (for all participants) that
        are associated with this dimension of this rubric.

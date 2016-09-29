Rubric and Dimension
--------------------

..  od:service::    deliveryodata

..  od:type::   Rubric

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

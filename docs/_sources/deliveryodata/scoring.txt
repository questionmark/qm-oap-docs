Subjective Scoring
------------------

One application of this API is the integration of external scoring tools
and scoring workflows with Questionmark software.

This scenario requires that the rubrics for an assessment to be created
and associated with Questions using the existing `Scoring Tool`_
available through Enterprise Manager.

..  _Scoring Tool:  https://www.questionmark.com/content/what-scoring-tool

A rubric is a set of instructions to a scorer, including a maximum score
to award for a response (which must always match the maximum score of
the question assigned to it). The rubric is broken down into various
dimensions; individual facets of the rubric score that can be set and
commented on separately by the scorer.  The overall score for the
participant's response is obtained by adding up the scores for the
individual dimensions.

The existing Scoring Tool uses a locking feature to prevent two scorers
from marking the same question at the same time. This mechanism is not
modeled directly in the API, though the same workflow states are
available to external tools allowing them to emulate this behaviour. It
is assumed that an external tool will have its own workflow rules that
are mapped on to the limited set of status values defined here.


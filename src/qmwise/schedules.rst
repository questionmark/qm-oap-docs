Schedules
---------

This part of the guide is under development.  Please refer to the
`Schedule <https://www.questionmark.com/content/schedule>`_
section of the old guide.

Schedule Methods
~~~~~~~~~~~~~~~~


..  qm:meth::   CreateAndScheduleParticipant

..  qm:meth::   CreateDisconnectedScheduleGroup

..  qm:meth::   CreateDisconnectedScheduleParticipant

..  qm:meth::   CreateScheduleGroup

..  qm:meth::   CreateScheduleGroupV42

..  qm:meth::   CreateScheduleParticipant

..  qm:meth::   CreateScheduleParticipantV42

..  qm:meth::   CreateScheduleWithParticipantGroupTestCenter

..  qm:meth::   DeleteDisconnectedSchedule

..  qm:meth::   DeleteSchedule

..  qm:meth::   DeleteScheduleList

..  qm:meth::   DeleteScheduleListByParticipant

..  qm:meth::   DeleteScheduleV42

..  qm:meth::   GetDisconnectedSchedule

..  qm:meth::   GetDisconnectedScheduleListByGroup

..  qm:meth::   GetDisconnectedScheduleListByParticipant

..  qm:meth::   GetSchedule

..  qm:meth::   GetScheduleList

..  qm:meth::   GetScheduleListByAssessment

..  qm:meth::   GetScheduleListByAssessmentV42

..  qm:meth::   GetScheduleListByGroup

..  qm:meth::   GetScheduleListByGroupV42

..  qm:meth::   GetScheduleListByParticipant
    :input:     Participant_ID    string
    :output:    ScheduleList      ScheduleList

    Returns a list of schedules for a specified participant.

..  qm:meth::   GetScheduleListByParticipantV42

..  qm:meth::   GetScheduleListV42

..  qm:meth::   GetScheduleV42

..  qm:meth::   SendEmailsScheduledEvent

..  qm:meth::   SetSchedule

..  qm:meth::   SetScheduleV42


Schedule Types
~~~~~~~~~~~~~~

..  qm:xtype::  ScheduleList

    ..  qm:xfield:: Schedule Schedule
        :optional:
        :max: unbounded    


..  qm:xtype::  Schedule

    ..  qm:xfield:: Schedule_ID string
        :optional:

    ..  qm:xfield:: Assessment_ID string
        :optional:

    ..  qm:xfield:: Participant_ID string
        :optional:

    ..  qm:xfield:: Group_ID string
        :optional:

    ..  qm:xfield:: Schedule_Name string
        :optional:

    ..  qm:xfield:: Restrict_Times boolean

    ..  qm:xfield:: Restrict_Attempts boolean

    ..  qm:xfield:: Max_Attempts int

    ..  qm:xfield:: Monitored int
        :optional:
        :default: 0
        
        ..  warning::   schedule elements returned in methods responses
                        will omit this element when the value is 0 due
                        to the default designation in the XML schema.

    ..  qm:xfield:: Schedule_Starts string
        :optional:

    ..  qm:xfield:: Schedule_Stops string
        :optional:


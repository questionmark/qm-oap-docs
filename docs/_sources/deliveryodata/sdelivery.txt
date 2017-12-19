Scheduled Delivery
------------------

.. versionadded::   2017.07

.. warning::    This page documents parts of the API that should be
                considered to be of 'beta' quality.  The details *are*
                subject to minor changes in future versions.
                
The Delivery OData API contains a brand new schedule entity to enable
the scheduling of assessments from third-party applications, including
the scheduling of assessments that require special procotring.

Classic vs Next Generation Schedules
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Classic schedules are described by the database tables
:qm:table:`G_Schedule` and :qm:table:`G_Schedule_Details` and by the
QMWISe schema type :qm:xtype:`Schedule`.

Classic schedules are the *only* way to schedule assessments in
Perception 5.

Next-generations schedules are being introduced with OnDemand 2017.07
and will gradually become the preferred way to schedule assessments in
Questionmark OnDemand and OnPremise.


Scheduling Permissions
~~~~~~~~~~~~~~~~~~~~~~

Permission to schedule an assessment is controlled by Group.  An
association exists between :od:type:`deliveryodata.Assessment` and
:od:type:`deliveryodata.Group` entities.  This association indicates
that *only* administrators that are owners of (one of) the associated
groups may schedule that assessment.  In the Questionmark portal the
types of action that a particular administrator may perform are further
limited by role and the permissions associated with that role.  Role
information is not exposed by the APIs.

To obtain a list of assessments that a given Administrator is associated
with you need to look at the Groups associated with that administrator
*and* the SchedulableAssessments associated with those groups::

    GET /deliveryodata/<customer_id>/Administrators(12345)/Groups?$expand=SchedulableAssessments

    {
        "odata.metadata": "https://ondemand.questionmark.com/deliveryodata/<customer-id>/$metadata#Groups",
        "value": [
            {
                "SchedulableAssessments": [
                    {
                        "ID": "92761000092761",
                        "Revision": 1,
                        "Name": "Sample Test",
                        "Language": "-",
                        "Description": null,
                        "Author": "Manager",
                        "CreatedDateTime": "2017-03-14T18:04:39Z",
                        "Editor": "Manager",
                        "ModifiedDateTime": "2017-04-06T09:16:22Z",
                        "Base": true
                    }
                ],
                "ID": 587413784,
                "Name": "Test_Group",
                "Description": "",
                "RootGroupID": 587413784
            }
        ]
    }

In the above response the administrator is associated with a single
Group (called "Test_Group" and that group is associated with a single
"Sample Test" assessment.

Bear in mind that it is possible for the same assessment to show up
multiple times (associated with different groups) so if you are
processing a response to this message to create a flat list you will
have to remove duplicates.

For very long lists the Groups themselves may prove a useful way to
hierarchically present the assessment list to the end user for selection.


Creating a Schedule
~~~~~~~~~~~~~~~~~~~

To create a schedule you POST to the Schedules feed endpoint.  There are
only a few required pieces of information.  A human-readable Name for
the schedule, the AssessmentID of the assessment to be scheduled, one of
GroupID or ParticipantID to identify who the schedule is for and the ID
of a monitoring type that describes how the assessment will be monitored
(e.g., proctored versus unproctored).

You can obtain a list of MonitoringTypes directly from the API::

    GET /deliveryodata/<customer-id>/MonitoringTypes

Monitoring types do not have human-friendly names, they have symbolic
names that are designed to be used as keys to translated text for a
multi-lingual user interface.  Once you have selected a monotring type
use its ID when creating a schedule. We'll create a simple
unmonitored test that does not require Questionmark Secure::

    POST /deliveryodata/<customer-id>/Schedules

    {
        "Name": "Demo Schedule",
        "AssessmentID": "92761000092761",
        "GroupID": 587413784,
        "MonitoringTypeID": 1
    }

The response is "201 Created" and the Schedule is reflected back::

    {
        "odata.metadata": "https://ondemand.questionmark.eu/deliveryodata/<customer-id>/$metadata#Schedules/@Element",
        "ID": 1,
        "ParentScheduleID": null,
        "ExternalID": null,
        "Name": "Demo Schedule",
        "AssessmentID": "92761000092761",
        "Language": null,
        "GroupID": 587413784,
        "ParticipantID": null,
        "StartFrom": null,
        "StartTo": null,
        "ResumeTo": null,
        "ReportFrom": null,
        "ReportTo": null,
        "ExtraTime": null,
        "MaxAttempts": null,
        "MonitoringTypeID": 1,
        "ObserverID": null,
        "Created": "2017-11-23T17:12:22.5894683Z",
        "Modified": "2017-11-23T17:12:22.5894683Z",
        "Hidden": false,
        "Disabled": false,
        "ResumeAllowed": false,
        "ObserverInitiated": false,
        "TestCenterID": null
    }

This creates a schedule for the Sample Test returned in the previous
example for all members of the group with ID 587413784 (the "Test_Group"
also returned in the previous example).  There are no time limits on
when the participants can start the test and no limit on the number of
attempts.

In future, creating a schedule will be all that is required for a third
party integration as the schedule will then show up in the Questionmark
portal when the participant logs in and they'll be able to launch the
test from there.  That functionality is not available yet (as of
2017.11) and so this API assumes that the external system will go on to
create its own user interface for the participant.

If you do not want the Schedule to show up in the Questionmark portal,
in other words, if you want to control the schedule entirely from your
own external system you can hide the schedule.  By default schedules are
*not* hidden.


Active Schedules
~~~~~~~~~~~~~~~~

A third-party user interface for a participant needs to know which
schedules are active for that participant.  A schedule is active if
there is some action that the participant may take (such as starting or
resuming the test).

To discover the list of active schedules for a participant you invoke
an action on that Participant's entity.  For the Participant with ID
1459320309 you can call the ActionableSchedules action as follows::

    POST /deliveryodata/<customer-id>/Participants(1459320309)/ActionableSchedules
    
    {
    }

In this case we POST an empty JSON object in the body (Content-Type:
application/json) as there are no parameters.

The response will look like this::

    {
        "odata.metadata": "https://ondemand.questionmark.eu/deliveryodata/<customer-id>/$metadata#Collection(QM.DeliveryODataService.DTO.ActionableSchedule)",
        "value": [
            {
                "ScheduleID": 1,
                "Name": "Demo Schedule",
                "ParticipantID": 1459320309,
                "ParticipantName": "Adrian Hurst",
                "Hidden": false,
                "AttemptsRemaining": null,
                "Actions": [
                    "start"
                ]
            }
        ]
    }

The result is a list of ActionableSchedule objects.  You can see the ID
of the schedule, the name (for display to the user when there are
multiple assessments available) and information about the number of
attempts remaining which is null here as there is no limit.

The Actions list is just a list of strings containing the names of
actions that are allowed.  In this case just one: "start".


Launching a Scheduled Test
~~~~~~~~~~~~~~~~~~~~~~~~~~

If a schedule is active for a participant then there will be a non-empty
list of actions in the associated AcitonableSchedule returned by the
previous request.

To enable the participant to launch the test you need to convert the
action into a URL that can be passed to the user's browser to invoke the
action.  You do this using the InvokeAction action::

    POST /deliveryodata/<customer-id>/Schedules(1)/InvokeAction

    {
        "Action": "start",
        "ParticipantID": 1459320309
    }

The response will look something like this::

    {
        "odata.metadata": "https://ondemand.questionmark.eu/deliveryodata/<customer-id>/$metadata#Edm.String",
        "value": "https://ondemand.questionmark.eu/lobby/<customer-id>/lobby/SystemCheck/201?nonce=d22bdd49-4d35-4265-b9e7-3bbb8b7a9fab&timestamp=2017-11-23T17:28:02.0181676Z&role=participant&signature=58db3754e595701731b8468775a4e0ce1d7686e3fca9d29f7920f1261f3a45ac"
    }

The URL obtained in the value of the result can be passed to the
participant's browser to enable them to launch the test.  The link is
time-limited, you should ensure that your application redirects the
participant to this link while processing a request from a suitable
action such as a button press.  If the participant is too slow to load
the URL it will expire and you'll have to generate another one by
invoking the action again.



Modiyfing a Schedule
~~~~~~~~~~~~~~~~~~~~

Schedules may be patched, though some properties may not be changed.
(E.g., the AssessmentID is fixed on creation).  The following call will
update the Schedule created in the previous example so that it can be
resumed::

    PATCH /deliveryodata/<customer-id>/Schedules(1)

    {
        "ResumeAllowed": true
    }

If the participant has started an assessment but has not completed it
and the schedule is resumable then the test may be resumed.  This is
indicated using the "resume" action::

    POST /deliveryodata/<customer-id>/Schedules/ActionableSchedulesForParticipant
    
    {
        "ParticipantID": 1459320309
    }

Responds with::

    {
        "odata.metadata": "https://ondemand.questionmark.com/deliveryodata/<customer-id>/$metadata#Collection(QM.DeliveryODataService.DTO.ActionableSchedule)",
        "value":
        [
            {
            "ScheduleID": 1,
            "Name": "Demo Schedule",
            "ParticipantID": 1459320309,
            "ParticipantName": "Adrian Hurst",
            "Hidden": false,
            "AttemptsRemaining": null,
            "Actions": [
                "resume"
            ]
        }
        ]
    }
 
A schedule is never marked with both "start" and "resume" actions. 
(This is a significant departure from classic schedules where multiple
attempts can be started simultaneously.  In next-generation schedules
the participant must complete the current attempt before progressing to
the next one if the schedule is resumable.)


Managing Attempts: Schedule Reporting
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Next generation schedules use the Attempt entity which can also be used
standalone for non-scheduled delivery.   The difference that is for
scheduled delivery, the actions described above take care of creating
the associated Attempts at the correct time. You may still use the
Attempts to discover detailed information about who has attempted the
assessment and what results have been completed or are in progress::

    GET /deliveryodata/<customer-id>/Schedules(1)?$expand=Attempts/Result

This query returns all Attempts for a schedule using expansion of the
Attempt navigation property.  By expanding the Result associated with
each Attempt we can see the status and outcome too.

This data could be used to construct a dashboard report for the schedule::

    {
        "odata.metadata": "https://ondemand.questionmark.com/deliveryodata/<customer-id>/$metadata#Attempts",
        "value": [
            {
                "Result": {
                    "ID": 390765738,
                    "AssessmentID": "92761000092761",
                    "ParticipantName": "a.hurst",
                    "GroupName": null,
                    "ParticipantDetails": null,
                    "Status": 2,
                    "MaxScore": 3,
                    "TotalScore": 3,
                    "ScoreBandTitle": "Pass",
                    "PercentageScore": 100,
                    "WhenFinished": "2017-08-21T13:59:41.347",
                    "WhenStarted": "2017-08-21T13:48:20.123",
                    "ExtraTime": null
                },
                "ID": 17897,
                "ExternalAttemptID": "72f2b164084748ac835802f329bdadf2",
                "ParticipantFacingQMLobbyUrl": null,
                "ProctorFacingQMControlsWidgetUrl": null,
                "UnlockCodeExpiresDateTime": null,
                "ParticipantID": 1459320309,
                "AssessmentID": "92761000092761",
                "AssessmentSnapshotID": null,
                "ScheduleID": 11887,
                "AttemptNumber": 1,
                "ResultID": 390765738,
                "LockStatus": false,
                "LockRequired": false,
                "ParticipantFacingProctorSystemWidgetUrl": null,
                "LastModifiedDateTime": "2017-08-21T12:48:20.157Z",
                "Language": null,
                "ParticipantSystemCheckUrl": "null",
                "UnlockCode": null,
                "AttemptListID": null,
                "MonitoringTypeID": 1
            }
        ]
    }


**API Restful**
===============

This API try to offer a good and simple way to interact with the microservice, doing possible a lot of this more than the basic CRUD with the items of this with simple and powerful idiomatic calls based on HTTP verbs.



General considerations
---------------------- 
 - This API Rest work only with JSON data format, to send and receive data.
 - In spite of exists another tables in data model like *Impart*, *Association*, and *Enrollment* that represent different kinds of relations between entities this aren't accessible directly like nested resources from the API, but yes like unique. ::
 
        ../teacher/n/impart
        ...
        400 Bad Request
        ...


    To see examples of use and chcking please review the code of test in dbms_api_test.py

**Teacher** Resource
--------------------

A teacher is a person that impart class to students and with our model it is possible only when is related with a subject that is associated with a class. This are the basic operations with their methods:


GET
***

To get all info about a teacher:::

   GET ../teacher/n   

It will return all info about this item, included the metadata like 
the user that created the resource or when happens this.

To get list of teachers:::

   GET ../teacher

It will return all info about all teachers saved, but if we don't
want all info, and for example only want the names we can pass
params:::

    GET ../teacher?params=name

That return only the names of teachers. Take a look that always will
be returned the id of item in all request, in this case teacherId, this
isn't optional.

The list of params always together with a colon between: ::

    GET ../teacher?params=name,surname

If the kind haven't the param passed it will return a ``400 Bad Request``.
It means that the model haven't this attribute in his definition.

Post
****

You can insert a new item in the data base of microservice using the same resource with ``POST`` method. The data is needed to pass in JSON format.

An example with curl would be: ::

    curl -H "Content-Type: application/json" -X POST -d '{"name": "Martha"}' localhost:8002/entities/teacher

A post call with `success` always return the data that have been saved, with some metadata values, the response that last call will be: ::

    {"name": "Martha", "createdBy": 1, "createdAt": "2016-12-13T13:02:41", "teacherId": 6}


Here the important metadata are the values ``createdBy`` and ``createdAt`` that show *who* and *when* the item was created. The minimal params that the method require depend of the kind on entity, in this case the only required params is ``name``.

There are some **errors** that you can see in some cases:

- If you pass an empty dictionary or one without the require values or some on attributes name are wrong you will receive an ``400 Bad Request``
- If the name of resource is write wrong, like 'teachsk' instead of teacher the response will be ``404 Not found``

Put
******

To *update* a resource only is necessary call itself with ``PUT`` method. For example: ::

    curl -H "Content-Type: application/json" -X PUT -d '{"name": "Eduard"}' localhost:8002/entities/teacher/25
    {"modifiedBy": 1, "createdBy": 1, "teacherId": 6, "modifiedAt": "2016-12-13T18:26:55", "name": "Eduard", "createdAt": "2016-12-13T13:02:41"}

The update of this resource retrieve all data from this item, now including the ``modifiedAt`` and ``modifiedBy``. 

The erros that this method can be produce with this resource are the same that with ``POST``.

Delete
******

We can delete a resource using the DELETE HTTP method, for example: ::

    curl  -i -X  DELETE localhost:8002/entities/teacher/1

If the call have success always return a ``200`` status code without body content. 

This way to proceed can present a problem, on the one hand if we delete a item that are related with other in another table (like a student with a pair subject-class) we can broke the consistency of the model but on the other hand if we want erase all dependencies of a item we need search them in all tables. 
To solve we can delete item with the default way, but the api implements another option to **delete the dependencies** in cascade: ::

 curl  -i -X  DELETE localhost:8002/entities/subject/1?action=dd

We only need specific the param **action** set to *dd* (delete dependencies) in the call to say to system that delete the item and all relations that exists with others items. 

Even so if we use the traditional way we can see errors if we try to do something that broke the consistency of data relations:

This is an example: ::

 curl  -i -X  DELETE localhost:8002/entities/subject/1

With the body response: ::

<title>409 Conflict</title>
<h1>Conflict</h1>
<p>Impossible delete the subject, this is related with some class , and this broke the consistency.</p>

If we execute the same with ``?action=dd`` the system will retrieve a ``200 OK`` status code.





Related resources
*****************

Teacher like another resources have a nested/related resources, in this case
the basic are: *subject*, *class*, *student*. Each one give a list of 
the items of the kind related with the teacher with `200` status code or in
case of the it doesn't exists yet a `204` code without content in body.

 
 Related resources calls examples: ::
 
    GET .../teacher/n/student 
    List of student which the teacher n impart class.
    
    GET .../teacher/n/class
    List of class where the teacher n impart class.
    
    GET .../teacher/n/subject
    List of subject that impart the teacher n.

Special case
*************

There are a special resource to teacher resources, it is ``teaching`` ::

    GET .../teacher/n/teaching  
 
It return a list with the teaching related with this teacher, perfect to build his profile in the UI. The data retrieved have the follow format: :: 
    
    [{"subject":{"subjectId": n, "name": "..."},
      "classes": [
                  {"classId": n,
                   "impartId": n,
                   "level": "...",
                   "course": "...",
                   "word": "..."},
                   {...},
                   {...}
                  ]
     },
     {"subject": {......},
      "classes": [{...},{...}...]
     }, 
     ...
     ]       
              
The JSON received is a list of subjects that the teacher impart when a list nested with the classes when each subject is imparted, with the basic info (ids) to jump to anyplace, subject, class, etc.

This resource is thinking to retrieve the maximal academic info about one teacher in a only call.

If the resource exists, but it hasn't teaching related this call will return a ``204`` status code that means *Success Call without content*.       


**Student** Resource
--------------------

This resource has the same behaviour that teacher, with the same management of the calls and errors except the method ``teaching``.

Special case
*************

The call is similar ::

    GET ../student/n/teaching 

It return a list with the teaching related with this student, perfect to build his profile in the UI. The data retrieved have the follow format: a list of  pairs **class and list of subjects** :: 

   [
    {"subjects": [
         {"subjectId": 1, "name": "Special Subject", "enrollmentId": 2}
     ], 
    "class": {"course": 1, "word": "A", "level": "Primary", "classId": 1}
    }, 

    {"subjects": [
         {"subjectId": 1, "name": "Special Subject", "enrollmentId": 4}
     ], 
    "class": {"course": 1, "word": "B", "level": "Primary", "classId": 2}
    }
   ]

The JSON received is class which the student are enrollment with a nested list with the subjects that are imparted in each class, with the basic info (ids) to jump to anyplace, subject, class, etc.
This resource is thinking to retrieve the maximal academic info about one student in a only call.
                  
**Subject** Resource
--------------------

This resource has the same behaviour that the rest, with the same management of the calls and errors except the method ``teaching``.

Special case
*************

The call is similar ::

    GET ../subject/n/teaching 

It return a list with the teaching related with the subject, perfect to build his profile in the UI. The data retrieved have the follow format: :: 

 [
  {
    "class": {
      "level": "Primary",
      "word": "B",
      "associationId": 3,
      "course": 1,
      "classId": 2
    },
    "teachers": [
      {
        "name": "Sophie",
        "impartId": 3,
        "teacherId": 3
      }
    ]
  }
 ]

**Class** Resource
--------------------

This resource has the same behaviour that the rest, with the same management of the calls and errors except the method ``teaching`` and the concept of **optional classes**.


Delete
******

We can delete a resource using the DELETE HTTP method, as in the other resoureces, for example: ::

    curl  -i -X  DELETE localhost:8002/entities/class/1

But in this case we have an **special delete method** with entities nested, and this is the reason: must be easy
delete an estudent fron all the subjects that are associated with this class, so we can do this:

    curl  -i -X  DELETE localhost:8002/entities/class/1/student/3

This method will delete all the enrollements items that exists beween the student and any association of the any subject
with the class related. *This special delete method with nested item is only available in **Class resource** *.

Optional classes
****************
This resource can be store two kind of items, a normal class that are items with three values, *course*, *level* and *word* but in some cases can be exists (because of the domain of problem) classes that are optional for all words of a course-level. For example if we have 1º Primary A, 1º Primary B and 1º Primary C but we can offer a common group 1º Primary Optional the call is made by other way with other values besides of these, see some examples: ::

 POST  '{"course": 1, "word": "B", "level": "ESO"}' /entities/class
     Insert a standard group in the system.

 POST  '{"course": 1, "level": "ESO", "group": 1, "subgroup": 1 }' /entities/class

Insert a optional group to a subject that will be shared between students from some groups un the level, like 1ALevel1, 1BLevel2..
We could be develop another implementation more implicit but we prefer that the insertions will be more explicit.

The program control the numeration of groups and you can't insert a group number 3 without insert before the group 2 and in the same way win the subgroups, and return an error in the cases if not satisfy this conditions.

The detele or update actions follow the same philosophy.



Further of this, this kind of classes have a own rules and errors due his own nature.



Special case
********************************

The call is similar ::

    GET ../class/n/teaching 

It return a list with the teaching related with the subject, perfect to build his profile in the UI. The data retrieved have the follow format: :: 

 [
  {
    "subject": {
      "subjectId": 1,
      "associationId": 2,
      "subjectName": "Special Subject"
    },
    "teachers": [
      {
        "teacherName": "Andrew",
        "impartId": 2,
        "teacherId": 2
      }
    ]
  },
  {
    "subject": {
      "subjectId": 2,
      "associationId": 3,
      "subjectName": "Super Special Subject"
    },
    "teachers": [
      {
        "teacherName": "Sophie",
        "impartId": 3,
        "teacherId": 3
      }
    ]
  }
 ]

All the block of data of this special *teaching* resources have all identifiers needed to make any action, to jump to other info or to delete some item.



**Association** Resource
------------------------

An association is a relation between a subject and a class in the domain of 
the problem:


This resource has a special GET response to a specific item, `` GET ../association/n ``. This return a special
data block with all info about this pair of subject-class, like the name and id of subject and class and two list with
the teachers that imparts this couple and another list with the students that are enrollment in this pair, in spite of
the own data of the association entity, like metadata and id.

**This resource hasn't related resources**, for example: ::

 curl -i -X GET localhost:8002/entities/association/1/class
 ...
 400 Bad Request
 ...
 <h1>Bad Request</h1>
 <p>class is not a valid nested resource.</p>


GET
***

To get all info about a association:::

   GET .../association/n   

This is the aspect of the common response:

   {
     "createdAt": "2016-12-15T10:51:12",
     "createdBy": 1,
     "subject": {
       "name": "1",
       "subjectId": 1
     },
     "associationId": 2,
     "teachers": [
       {
         "teacherId": 1,
         "teacherName": "1"
       }
     ],
     "students": [
       {
         "studentName": "3",
         "studentId": 3
       }
     ],
     "class": {
       "classId": 2,
       "course": 2,
       "word": "B",
       "level": "2"
     }
   }
    
    

**Enrollment** Resource
------------------------

An enrollment item is a relation between a subject and an association between a  class and a subject.



PUT
***

To put a new enrollment relation in the sistem you need use the PUT method, and it can be used
two diferents ways.

   curl -H "Content-Type: application/json" -X POST -d '{"associationId": 16, "studentId": 1}' localhost:8002/entities/enrollment

But is easy to need save mulitple relations with the same student, when it is enrolled to all subject of
a class or in any other process that we can imagine, because of this you can pass, instead of *associationId*,
*associationsIds* where the value must be an array of identificators of associations.

Something like this:

   '{"associationsIds": [16,17,18,19], "studentId": 1}'

To this way we focus the complexity of this kind of  processes in the server.





    
    

Flask APIRest
-----------------

.. toctree::
   :maxdepth: 2
   
   dbms_api
                   
    
    
    
    
    
    

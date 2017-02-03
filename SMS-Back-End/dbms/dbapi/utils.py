from termcolor import colored
import inspect

def logger(func):
    def real_loger(*args, **kwargs):
        print colored('LOGGER')
        print colored('Function: '+func.__name__, 'green')
        print colored(args[1:], 'green')

    return real_loger

class sorters(object):

    @classmethod
    def special_sort(cls, list):
        """
        Sort with a special way the items of the list.
        :param list:
        :return:
        See example in newTest.py test file.
        """

        sorted_list = []

        for list_element in list:

            if len(sorted_list) == 0:
                new_subject = {'subjectId': list_element.get('subjectId'),
                               'name': list_element.get('name')
                               }
                new_class = {'classId': list_element.get('classId'),
                             'course': list_element.get('course'),
                             'level': list_element.get('level'),
                             'word': list_element.get('word'),
                             'impartId': list_element.get('impartId')}

                sorted_list.append({'subject': new_subject, 'classes': [new_class]})

            else:
                index = -1
                for item in sorted_list:
                    if item["subject"]["subjectId"] == list_element.get("subjectId"):
                        index = sorted_list.index(item)

                if index != -1:
                    new_class = {'classId': list_element.get('classId'),
                                 'course': list_element.get('course'),
                                 'level': list_element.get('level'),
                                 'word': list_element.get('word'),
                                 'impartId': list_element.get('impartId')}

                    sorted_list[index]["classes"].append(new_class)

                else:
                    new_subject = {'subjectId': list_element.get('subjectId'),
                                   'name': list_element.get('name')
                                   }
                    new_class = {'classId': list_element.get('classId'),
                                 'course': list_element.get('course'),
                                 'level': list_element.get('level'),
                                 'word': list_element.get('word'),
                                 'impartId': list_element.get('impartId')}

                    sorted_list.append({'subject': new_subject, 'classes': [new_class]})

        return sorted_list

    @classmethod
    def special_sort_2(cls, list):
        """
        Sort with a special way the items of the list.
        :param list:
        :return:
        See example in newTest.py test file.
        """

        sorted_list = []

        for list_element in list:

            if len(sorted_list) == 0:
                new_class = {'classId': list_element.get('classId'),
                             'course': list_element.get('course'),
                             'level': list_element.get('level'),
                             'word': list_element.get('word')}

                new_subject = {'subjectId': list_element.get('subjectId'),
                               'name': list_element.get('name'),
                               'enrollmentId': list_element.get('enrollmentId')
                               }

                sorted_list.append({'class': new_class, 'subjects': [new_subject]})

            else:
                index = -1
                for item in sorted_list:
                    if item["class"]["classId"] == list_element.get("classId"):
                        index = sorted_list.index(item)

                if index != -1:
                    new_subject = {'subjectId': list_element.get('subjectId'),
                                   'name': list_element.get('name'),
                                   'enrollmentId': list_element.get('enrollmentId')
                                   }
                    sorted_list[index]["subjects"].append(new_subject)

                else:
                    new_class = {'classId': list_element.get('classId'),
                                 'course': list_element.get('course'),
                                 'level': list_element.get('level'),
                                 'word': list_element.get('word')}

                    new_subject = {'subjectId': list_element.get('subjectId'),
                                   'name': list_element.get('name'),
                                   'enrollmentId': list_element.get('enrollmentId')
                                   }

                    sorted_list.append({'class': new_class, 'subjects': [new_subject]})

        return sorted_list

    @classmethod
    def special_sort_3(cls, list):
        #print ('print input in special_sort')

        #print type(list)

        # First it cleaned the list with repeated elements.
        to_delete = []
        for element in list:
            if not element.get('teacherId', None):
                for item in list:
                    # If the item a have teacher and is the same association
                    if item.get('teacherId', None) and item.get('associationId', None) == element.get('associationId', None):
                        index = list.index(element)
                        if index not in to_delete:
                            to_delete.append(index)

        list = [i for j, i in enumerate(list) if j not in to_delete]




        sorted_list = []
        for list_element in list:

            if len(sorted_list) == 0:

                new_class = {'classId': list_element.get('classId'),
                             'course': list_element.get('course'),
                             'level': list_element.get('level'),
                             'word': list_element.get('word'),
                             'associationId': list_element.get('associationId')}

                if list_element.get('teacherId', None):

                    new_teacher = {'teacherId': list_element.get('teacherId'),
                                   'name': list_element.get('name'),
                                   'impartId': list_element.get('impartId')
                                   }

                    sorted_list.append({'class': new_class, 'teachers': [new_teacher]})

                else:
                    sorted_list.append({'class': new_class})

            else:

                index = -1
                for item in sorted_list:
                    if item['class']['classId'] == list_element['classId']:
                        index = sorted_list.index(item)

                if index == -1: # The element class-teachers doesn't exists still.
                    new_class = {'classId': list_element.get('classId'),
                                 'course': list_element.get('course'),
                                 'level': list_element.get('level'),
                                 'word': list_element.get('word'),
                                 'associationId': list_element.get('associationId')}

                    if list_element.get('teacherId', None):

                        new_teacher = {'teacherId': list_element.get('teacherId'),
                                       'name': list_element.get('name'),
                                       'impartId': list_element.get('impartId')
                                       }

                        sorted_list.append({'class': new_class, 'teachers': [new_teacher]})

                    else:
                        sorted_list.append({'class': new_class})

                else:

                    if list_element.get('teacherId', None):

                        new_teacher = {'teacherId': list_element.get('teacherId'),
                                       'name': list_element.get('name'),
                                       'impartId': list_element.get('impartId')
                                       }
                        sorted_list[index]['teachers'].append(new_teacher)

        return sorted_list


    @classmethod
    def special_sort_4(cls, list):

        # First it cleaned the list with repeated elements.
        to_delete = []
        for element in list:
            if not element.get('teacherId', None):
                for item in list:
                    # If the item a have teacher and is the same association
                    if item.get('teacherId', None) and item.get('associationId', None) == element.get('associationId', None):
                        index = list.index(element)
                        if index not in to_delete:
                            to_delete.append(index)

        list = [i for j, i in enumerate(list) if j not in to_delete]




        sorted_list = []
        for list_element in list:

            if len(sorted_list) == 0:

                new_subject = {'subjectId': list_element.get('subjectId'),
                             'subjectName': list_element.get('subjectName'),
                             'associationId': list_element.get('associationId')}

                if list_element.get('teacherId', None):

                    new_teacher = {'teacherId': list_element.get('teacherId'),
                                   'teacherName': list_element.get('teacherName'),
                                   'impartId': list_element.get('impartId')
                                   }

                    sorted_list.append({'subject': new_subject, 'teachers': [new_teacher]})

                else:
                    sorted_list.append({'subject': new_subject})

            else:

                index = -1
                for item in sorted_list:
                    if item['subject']['subjectId'] == list_element['subjectId']:
                        index = sorted_list.index(item)

                if index == -1: # The element subject-teachers doesn't exists still.
                    new_subject = {'subjectId': list_element.get('subjectId'),
                                   'subjectName': list_element.get('subjectName'),
                                   'associationId': list_element.get('associationId')}

                    if list_element.get('teacherId', None):

                        new_teacher = {'teacherId': list_element.get('teacherId'),
                                       'teacherName': list_element.get('teacherName'),
                                       'impartId': list_element.get('impartId')
                                       }

                        sorted_list.append({'subject': new_subject, 'teachers': [new_teacher]})

                    else:
                        sorted_list.append({'subject': new_subject})

                else:

                    if list_element.get('teacherId', None):
                        new_teacher = {'teacherId': list_element.get('teacherId'),
                                       'teacherName': list_element.get('teacherName'),
                                       'impartId': list_element.get('impartId')
                                       }
                        sorted_list[index]['teachers'].append(new_teacher)

        return sorted_list
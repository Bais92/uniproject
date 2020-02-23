from uniproject.fragebogen.models import Question


def calculate_absulte_error(answer_tuple, experiment_id):
    absolute_error = 0
    for answer, question_id in answer_tuple:
        correct_answer = Question.objects.get(question_id=question_id)
        answer = answer
        error = correct_answer - answer
        absolute_error += error
    return absolute_error

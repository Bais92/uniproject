from uniproject.fragebogen.models import Question

# grundsätzlich ist hier der richtige Ort, um Erweiterungen, die an verschiedenen Stellen benötigt werden, anzulegen.
# Grundsätzlich kann dieser Code aber auch in jedem anderen Skript geschieben werden (Stichwort ist hier allerdings
# best practices).

def calculate_absulte_error(answer_tuple, experiment_id):
    absolute_error = 0
    for answer, question_id in answer_tuple:
        correct_answer = Question.objects.get(question_id=question_id)
        answer = answer
        error = correct_answer - answer
        absolute_error += error
    return absolute_error

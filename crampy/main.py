from pathlib import Path

from crampy.exporting import QuizExporter
from crampy.models import OpenAnswerQuestionModel, QuizModel


def run():
    path = Path("C:\\Development\\Projects\\crampy\\exports\\new_template.html")
    quiz = QuizModel("Sum", "Mathematics", [
        OpenAnswerQuestionModel("A", "A"),
        OpenAnswerQuestionModel("B", "B"),
        OpenAnswerQuestionModel("C", "C"),
        OpenAnswerQuestionModel("D", "D"),
        OpenAnswerQuestionModel("E", "E"),
        OpenAnswerQuestionModel("F", "F"),
        OpenAnswerQuestionModel("G", "G"),
        OpenAnswerQuestionModel("H", "H"),
        OpenAnswerQuestionModel("I", "I"),
        OpenAnswerQuestionModel("J", "J"),
        OpenAnswerQuestionModel("K", "K"),
        OpenAnswerQuestionModel("L", "L"),
        OpenAnswerQuestionModel("M", "M")
    ])
    QuizExporter().as_notecards(quiz, "html", path)


if __name__ == "__main__":
    print("CramPy!")
    run()

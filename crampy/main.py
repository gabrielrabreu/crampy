from pathlib import Path

from crampy.exporting import QuizExporter
from crampy.models import MultipleChoiceQuestionModel, OpenAnswerQuestionModel, QuizModel, CompositeQuestionModel


def run():
    """
    math_quiz = QuizModel("Contas e problemas", "Matemática", [
        MultipleChoiceQuestionModel(
            "1. Quanto é cinco vezes sete",
            [
                "a) 48", "b) 12", "c) 35", "d) 36"
            ], 3
        ),
        CompositeQuestionModel(
            "2. Resolvas as operações abaixo", [
                OpenAnswerQuestionModel("a) 59.475 + 40.780 = ", ""),
                OpenAnswerQuestionModel("b) 90.560 + 48.780 = ", ""),
                OpenAnswerQuestionModel("c) 99.979 - 41.971 = ", ""),
                OpenAnswerQuestionModel("d) 70.241 - 77.401 = ", ""),
                OpenAnswerQuestionModel("e) 8.987 * 4 = ", ""),
                OpenAnswerQuestionModel("f) 6.788 * 8 = ", ""),
                OpenAnswerQuestionModel("g) 29.782 / 2 = ", ""),
                OpenAnswerQuestionModel("h) 4.790 / 4 = ", ""),
                MultipleChoiceQuestionModel(
                    "i) Quanto é cinco vezes sete",
                    [
                        "a) 48", "b) 12", "c) 35", "d) 36"
                    ], 3
                ),
            ]
        ),
        OpenAnswerQuestionModel(
            "3. Maria tem duzentos e setenta gibis e o Carlos tem trezentos e trinta. Quantos eles tem juntos?",
            "600"
        ),
        OpenAnswerQuestionModel(
            "4. Mariana tem quatrocentos e noventa livros e Miguel tem trezentos e noventa. Quantos livros Mariana "
            "tem a mais que Miguel?",
            "100"
        )
    ])
    QuizExporter().as_practice_test(math_quiz, "html",
                                    Path("C:\\Development\\Projects\\crampy\\exports\\practice_test.html"))
    QuizExporter().as_notecards(math_quiz, "html",
                                Path("C:\\Development\\Projects\\crampy\\exports\\notecards.html"))"""

    portuguese_quiz = QuizModel("Plural/Singular", "Português", [
        OpenAnswerQuestionModel("Televisão", "Televisões"),
        OpenAnswerQuestionModel("Camaleão", "Camaleões"),
        OpenAnswerQuestionModel("Barril", "Barris"),
        OpenAnswerQuestionModel("Anzol", "Anzois"),
        OpenAnswerQuestionModel("Camisa", "Camisas"),
        OpenAnswerQuestionModel("Costas", "Costas"),
        OpenAnswerQuestionModel("Canal", "Canais"),
        OpenAnswerQuestionModel("Youtuber", "Youtubers"),
        OpenAnswerQuestionModel("Casa", "Casas"),
        OpenAnswerQuestionModel("Janela", "Janelas"),
        OpenAnswerQuestionModel("Mesa", "Mesas"),
        OpenAnswerQuestionModel("Plural", "Plurais")
    ])
    QuizExporter().as_notecards(portuguese_quiz, "html",
                                Path("C:\\Development\\Projects\\crampy\\exports\\notecards2.html"))


if __name__ == "__main__":
    print("CramPy!")
    run()

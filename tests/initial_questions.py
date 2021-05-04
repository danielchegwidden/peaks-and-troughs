from app import app
from app import db
from app.models import Questions


def add_question(question_id, question_text, answers, correct_answer):
    question = Questions(
        question_id=question_id,
        question_text=question_text,
        answer_1=answers[0][1],
        answer_2=answers[1][1],
        answer_3=answers[2][1],
        answer_4=answers[3][1],
        correct_answer=correct_answer,
    )
    db.session.add(question)
    db.session.commit()


def main():
    add_question(
        question_id=1,
        question_text="In 2001 when Enron collapsed under a $40 billion accounting scandal, shareholders had to pay which of the following?",
        answers=[
            ("A", "Up to the value of the shares they held at the time"),
            ("B", "Up to the value of the debts Enron had oustanding"),
            ("C", "$1,000 per shareholder"),
            ("D", "Nothing, they had no liability"),
        ],
        correct_answer="D",
    )

    add_question(
        question_id=2,
        question_text="Which of the following is not an example of a derivative product?",
        answers=[
            ("A", "Put Option"),
            ("B", "Oil Future"),
            ("C", "Currency Swap"),
            ("D", "Index Fund"),
        ],
        correct_answer="D",
    )

    add_question(
        question_id=3,
        question_text="In which of the following cryptocurrencies can you find the Nyan Cat animation embedded on the blockchain?",
        answers=[
            ("A", "Bitcoin"),
            ("B", "Ethereum"),
            ("C", "Dogecoin"),
            ("D", "Litecoin"),
        ],
        correct_answer="B",
    )

    add_question(
        question_id=4,
        question_text="The people who had their entire savings wiped out by Bernie Madoff faced which of the following risks?",
        answers=[
            ("A", "Concentration Risk"),
            ("B", "Market Risk"),
            ("C", "Liquidity Risk"),
            ("D", "Inflation Risk"),
        ],
        correct_answer="A",
    )

    add_question(
        question_id=5,
        question_text="Which of the following did not contribute to the 2008 Financial Crisis?",
        answers=[
            ("A", "Subprime mortgages being signed to people who could not repay them"),
            ("B", "Lack of regulation and oversight by government entities and agencies"),
            ("C", "The volatile nature of cryptocurrencies"),
            (
                "D",
                "Bonuses and incentives rewarding traders and bankers for risky investment decisions",
            ),
        ],
        correct_answer="C",
    )


if __name__ == "__main__":
    main()

"""Competition entry point.

The organizer runs this file non-interactively.
"""

import argparse
import json

from agent.agent import run_agent


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Run the payment investigation AI assistant."
    )

    parser.add_argument(
        "--questions",
        required=True,
        help="Path to the official questions.json.",
    )

    parser.add_argument(
        "--output",
        required=True,
        help="Path for generated submission.json.",
    )

    args = parser.parse_args()

    with open(args.questions, "r", encoding="utf-8") as file:
        questions = json.load(file)

    results = []

    for question in questions:
        result = run_agent(
            question=question["question"],
            payment_id=question["payment_id"],
        )

        # These fields make the candidate output traceable to the exact
        # official evaluation question.
        result["question_id"] = question["question_id"]
        result["payment_id"] = question["payment_id"]
        result["question"] = question["question"]

        results.append(result)

    with open(args.output, "w", encoding="utf-8") as file:
        json.dump(results, file, indent=2)


if __name__ == "__main__":
    main()

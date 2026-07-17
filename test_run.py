from app.core.crew import run_market_scout


def main():
    target_topic = "Clean Beauty & Preventive Wellness"
    print(f"Intializing CrewAI Market Scout Loop for : '{target_topic}' \n")

    # Trigger execution
    output = run_market_scout(target_topic=target_topic)

    print("\n" + "=" * 40)
    print("Stage 2: Instrumentation logic:")
    print("=" * 40)

    # Extract total token metrics from the CrewOutput object
    try:
        if hasattr(output, "token_usage") and output.token_usage:  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue]
            metrics = output.token_usage  # pyright: ignore[reportUnknownMemberType, reportAttributeAccessIssue]
            print(f"Prompt token: {metrics.prompt_tokens}")
            print(f"Completion token: {metrics.completion_tokens}")
            print(f"Total token: {metrics.total_tokens}")

            # Calculate approximate cost using reference price guidelines ($2.50 in / $10 out per 1M)
            input_cost = (metrics.prompt_tokens / 1_000_000) * 2.50
            output_cost = (metrics.completion_tokens / 1_000_000) * 10.0
            total_cost = input_cost + output_cost

            print(f"Estimated cost: {total_cost:.5f}")
        else:
            print("No token usage metrics returned.")
            raise Exception(
                "No toke usage metrics returned. Ensure your LLM configuration supports usage tracking."
            )
        print("\n" + "=" * 40)
        print("Final Report Generated")
        print("=" * 40)
        print(output.raw)  # pyright: ignore[reportAttributeAccessIssue, reportUnknownArgumentType, reportUnknownMemberType]
        with open("output.md", "x") as file:
            status: int = file.write(output.raw)
            print(f"Output written to output.md (status: {status})")

    except Exception as e:
        print(f"Error: {e}")


if __name__ == "__main__":
    main()

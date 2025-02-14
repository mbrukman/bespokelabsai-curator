import json
import re

from datasets import load_dataset

from bespokelabs import curator


class TACOCodeExecutor(curator.CodeExecutor):
    """TACO Code Executor."""

    def code(self, row):
        """Extract code string from a dataset row."""
        try:
            code = re.search(r"```python\n(.*?)\n```", row["deepseek_solution"], re.DOTALL).group(1)
        except (AttributeError, IndexError):
            code = ""
        return code

    def code_input(self, row):
        """Extract single input from a dataset row."""
        inputs_outputs = row["input_output_x"]
        try:
            inputs_outputs = json.loads(inputs_outputs)
            inputs = inputs_outputs["inputs"][0]

        except Exception as e:
            print("Error parsing input output", e)

        if isinstance(inputs, list):
            inputs = "\n".join([str(i) for i in inputs])

        return inputs

    def code_output(self, row, execution_output):
        """Parse execution results."""
        inputs_outputs = row["input_output_x"]
        try:
            inputs_outputs = json.loads(inputs_outputs)
            output = inputs_outputs["outputs"][0]
        except Exception as e:
            print("Error parsing input output", e)
            return row

        # Compare the output with execution stdout, stripping whitespace to handle formatting differences
        if isinstance(output, str) and isinstance(execution_output.stdout, str):
            row["correct"] = output.strip() == execution_output.stdout.strip()
        else:
            row["correct"] = output == execution_output.stdout

        return row


if __name__ == "__main__":
    executor = TACOCodeExecutor(backend="e2b")
    dataset = load_dataset("bespokelabs/sky-t1-taco-test-rejection-sampled-shreyas")
    execution_output = executor(dataset["train"].select(range(10)))

    print("================")
    print(execution_output)

    print(execution_output["correct"])
    print("================")

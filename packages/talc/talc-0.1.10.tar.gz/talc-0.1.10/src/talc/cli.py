import os
import csv as csvmod
import time
from typing import Literal
import click
import random
from pdfminer.high_level import extract_text
from talc.evals import Document, EvalsClient, TestCaseResponse, TestCaseWithRubric


talc_api_key: str | None = os.getenv("TALC_API_KEY", None)
talc_base_url: str | None = os.getenv(
    "TALC_BASE_URL", "http://evals-webserver-webapp.azurewebsites.net"
)


def poll_results(
    client: EvalsClient, run_id: str, print_failed: bool, outfile: str | None
):
    while True:
        run_info = client.get_results()
        print(f"Progress: {run_info.completion_progress * 100}%")
        if run_info.completion_progress >= 1:
            print("\n=============================================")
            print("Grading complete.")
            print(f"Accuracy: {run_info.grade_accuracy}")
            print("=============================================\n")
            if print_failed and run_info.test_cases is not None:
                print("Failed cases:")
                for case in run_info.test_cases:
                    if case.grade_accuracy < 0.5:
                        print(
                            f"{case.id}: {case.question} -> {case.response} ({case.grade_accuracy}{case.grade_reason})"
                        )
            if outfile is not None and run_info.test_cases is not None:
                with open(outfile, "w", newline="") as csvfile:
                    writer = csvmod.writer(csvfile)
                    writer.writerow(
                        ["id", "question", "response", "grade", "grade_reason"]
                    )
                    for case in run_info.test_cases:
                        writer.writerow(
                            [
                                case.id,
                                case.question,
                                case.response,
                                case.grade_accuracy,
                                case.grade_reason,
                            ]
                        )
                print("Results written to " + outfile)
            if run_info.grade_accuracy is not None and run_info.grade_accuracy < 1:
                return 1
            else:
                return 0
        time.sleep(2)


@click.group()
def evals():
    pass


@evals.command()
@click.option("--count", default=0, help="Number of cases to sample (0 for all).")
@click.option("--api_key", default=talc_api_key, help="Talc API key")
@click.option("--dataset", prompt="Dataset ID", help="The ID of the dataset to load.")
@click.option(
    "--outfile",
    default=None,
    help="Path to CSV file to save results to.",
    required=False,
)
def get_dataset(count: int, dataset: str, api_key: str, outfile: str) -> None:
    """Download or pretty print a test dataset from the server."""

    if api_key is None:
        raise click.UsageError(
            "No API key provided. Please set the TALC_API_KEY environment variable or provide the --api_key option."
        )

    client = EvalsClient(api_key, talc_base_url)
    data = client.get_dataset(dataset)

    if count == 0:
        count = len(dataset)

    random.shuffle(data)

    if outfile is not None:
        with open(outfile, "w", newline="") as csvfile:
            writer = csvmod.writer(csvfile)
            writer.writerow(["id", "question", "expected_answer"])
            for case in data[:count]:
                writer.writerow([case.id, case.question, case.expected_response])

    for case in data[:count]:
        print(case.question)


@evals.command()
@click.option("--api_key", default=talc_api_key, help="Talc API key")
@click.option(
    "--infile",
    prompt="Results CSV path",
    help="Path to CSV file to load results from. Columns should be 'id', 'result'. Header row is required and case sensitive.",
)
@click.option("--print_failed", is_flag=True, help="Print the failed test cases.")
@click.option("--outfile", default=None, help="Optionally save output as CSV.")
@click.option(
    "--fail_on_error",
    is_flag=True,
    help="Exit with a non-zero status if any test cases fail.",
)
def eval(
    api_key: str, infile: str, print_failed: bool, outfile: str, fail_on_error: bool
):
    """Grade a test run from a csv. Columns should be 'id', question, and 'result'. CSV should have a header row."""

    if api_key is None:
        raise click.UsageError(
            "No API key provided. Please set the TALC_API_KEY environment variable or provide the --api_key option."
        )

    client = EvalsClient(api_key, talc_base_url)

    with open(infile, newline="") as csvfile:
        reader = csvmod.DictReader(csvfile)

        results = [
            TestCaseResponse(id=row["id"], response=row["result"]) for row in reader
        ]

    run_info = client.start_run()
    client.submit_responses(results)
    print("Submitted results. Beginning grading for run ID: " + run_info.id)

    res = poll_results(client, run_info.id, print_failed, outfile)
    if fail_on_error and res != 0:
        exit(res)


@evals.command()
@click.option("--api_key", default=talc_api_key, help="Talc API key")
@click.option("--run_id", prompt="Run ID", help="The ID of the run to get results for.")
@click.option("--print_failed", is_flag=True, help="Print the failed test cases.")
@click.option(
    "--fail_on_error",
    is_flag=True,
    help="Exit with a non-zero status if any test cases fail.",
)
def get_results(api_key: str, run_id: str, print_failed: bool, fail_on_error: bool):
    """Get the grades for a test run."""

    if api_key is None:
        raise click.UsageError(
            "No API key provided. Please set the TALC_API_KEY environment variable or provide the --api_key option."
        )

    client = EvalsClient(api_key, talc_base_url, run_id)

    res = poll_results(client, run_id, print_failed, None)
    if fail_on_error and res != 0:
        exit(res)


@evals.command()
@click.option("--api_key", default=talc_api_key, help="Talc API key")
@click.option(
    "--csv",
    prompt="CSV path",
    help="Path to CSV file to upload. Column headers should be 'question' and 'expected_answer'. An optional source_text column can be included as well.",
)
@click.option("--name", prompt="Dataset name", help="The name of the dataset.")
def upload_manual_testset(api_key: str, csv: str, name: str):
    """Add a new dataset to the server."""

    if api_key is None:
        raise click.UsageError(
            "No API key provided. Please set the TALC_API_KEY environment variable or provide the --api_key option."
        )

    client = EvalsClient(api_key, talc_base_url)

    with open(csv, newline="") as csvfile:
        reader = csvmod.DictReader(csvfile)

        try:
            dataset = [
                TestCaseWithRubric(
                    question=row["question"],
                    expected_response=row["expected_answer"],
                    scenario_data={},
                    id=None,
                    source_content=(
                        [row["source_text"]] if "source_text" in row else []
                    ),
                )
                for row in reader
            ]
        except KeyError:
            raise click.UsageError(
                "CSV file must have columns 'question' and 'expected_answer'. A header is required. An optional source_text column can be included."
            )

    dataset_id = client.upload_dataset(name, dataset)
    print(f"Dataset created with ID: {dataset_id}")


@evals.command()
@click.option("--api_key", default=talc_api_key, help="Talc API key")
@click.option(
    "--csv",
    prompt="CSV path",
    help="Path to CSV file to upload. Columns should be 'question', 'expected_answer' and 'user_answer'. An optional source_text column can be included as well.",
)
@click.option(
    "--name",
    help="The name of the dataset.",
    default="Temp Dataset",
    required=False,
)
@click.option(
    "--outfile",
    help="Name of the output file",
    required=False,
)
@click.option(
    "--fail_on_error",
    is_flag=True,
    help="Exit with a non-zero status if any test cases fail.",
)
def upload_and_grade(
    api_key: str, csv: str, name: str, outfile: str | None, fail_on_error: bool
):
    """Upload a CSV with questions, reference answers, and user answers. Grade the user answers and return the grade. Column names must be 'question', 'expected_answer', and 'user_answer'."""

    if api_key is None:
        raise click.UsageError(
            "No API key provided. Please set the TALC_API_KEY environment variable or provide the --api_key option."
        )

    client = EvalsClient(api_key, talc_base_url)

    with open(csv, newline="") as csvfile:
        reader = csvmod.DictReader(csvfile)

        rows = [row for row in reader]

        assert "question" in rows[0]
        assert "expected_answer" in rows[0]
        assert "user_answer" in rows[0]

    dataset = [
        TestCaseWithRubric(
            question=row["question"],
            expected_response=row["expected_answer"],
            scenario_data={},
            id=None,
            source_content=([row["source_text"]] if "source_text" in row else []),
        )
        for row in rows
    ]

    dataset = client.upload_dataset(name, dataset)

    # Download the dataset to get the IDs
    data = client.get_dataset(dataset.id)

    # Map the IDs to the actual responses using the questions as a key

    id_map = {case.question: case.id for case in data}

    results = [
        TestCaseResponse(
            id=id_map[row["question"]],
            response=row["user_answer"] if "user_answer" in row else "",
        )
        for row in rows
    ]

    # Create a run and submit the results
    run_info = client.start_run()
    client.submit_responses(results)
    print("Submitted results. Beginning grading for run ID: " + run_info.id)

    res = poll_results(client, run_info.id, True, outfile)

    if fail_on_error and res != 0:
        exit(res)


@evals.command()
@click.option("--api_key", default=talc_api_key, help="Talc API key")
@click.option(
    "--file",
    prompt="Input folder, single file path, or URL.",
    help="Input folder, single file path, or URL. Multiple allowed.",
    multiple=True,
)
@click.option("--out", prompt="Output path", help="Path to save the output to.")
@click.option("--dataset_name", prompt="Dataset name", help="The name of the dataset.")
@click.option(
    "--sampling_mode",
    help="The sampling mode to use.",
    type=click.Choice(["main_file", "all_files", "random", "ranked"]),
    default="all_files",
)
@click.option(
    "--generation_modes",
    help="The generation modes to use.",
    type=click.Choice(["simple", "complex", "sweep"]),
    default=["simple"],
    multiple=True,
)
def generate(
    api_key: str,
    file: list[str],
    out: str,
    dataset_name: str,
    sampling_mode: Literal["main_file", "all_files", "random", "ranked"],
    generation_modes: list[Literal["simple"] | Literal["complex"] | Literal["sweep"]],
):
    """Generate a dataset from a set of documents."""

    if api_key is None:
        raise click.UsageError(
            "No API key provided. Please set the TALC_API_KEY environment variable or provide the --api_key option."
        )

    client = EvalsClient(api_key, talc_base_url)

    documents: list[Document] = []

    # Figure out what kind of document each file is, and load it into a list of Document objects
    # If it's a URL, send the URL and the server will load it (might want to make this local in the future)
    # If it's a directory, load all the markdown files in the directory
    # If it's a file, load the file
    for f in file:
        if f.startswith("http") or f.startswith("https"):
            documents.append(Document(url=f, title=f))
        elif os.path.isdir(f):
            for root, _, files in os.walk(f):
                for path in files:
                    if path.endswith(".md"):
                        with open(os.path.join(root, path), "r") as f:
                            documents.append(Document(content=f.read(), title=f.name))
                    elif path.endswith(".pdf"):
                        documents.append(
                            Document(content=extract_text(os.path.join(root, path)))
                        )
                    else:
                        print(
                            f"Skipping file with unknown extension {path} in directory {root}."
                        )
        elif os.path.isfile(f):
            if f.endswith(".pdf"):
                documents.append(Document(content=extract_text(f), title=f))
            elif f.endswith(".md"):
                with open(f, "r") as f:
                    documents.append(Document(content=f.read(), title=f.name))
            else:
                raise click.UsageError(
                    "Unsupported file type. Only .md and .pdf files are supported."
                )

    dataset_job = client.start_generate_dataset(
        dataset_name, documents, sampling_mode, generation_modes
    )

    while True:
        dataset_job = client.get_dataset_creation_job(dataset_job.id)
        print("Generating: " + dataset_job.status)
        if dataset_job.status == "COMPLETE":
            break
        if dataset_job.status == "ERROR":
            print("Generation failed.")
            exit(1)
        time.sleep(2)

    dataset = client.get_dataset(dataset_job.dataset_id)

    with open(out, "w", newline="") as csvfile:
        writer = csvmod.writer(csvfile)
        writer.writerow(["id", "question", "expected_answer"])
        for case in dataset:
            writer.writerow([case.id, case.question, case.expected_response])

    print(f"Dataset created with ID: {dataset_job.dataset_id}")
    print(f"Dataset written to {out}")


def main():
    evals()

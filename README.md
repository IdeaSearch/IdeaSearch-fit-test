# IdeaSearch-fit-test

This repository provides a demonstration project for the `IdeaSearch-fit` package. To run this project, follow the steps below.

---

## 1\. Configure API Keys

Create an `api_keys.json` file in the root directory of this project. You can do this by copying the `api_keys_template.json` file and populating it with your own valid API keys.

---

## 2\. Create Directories

Create two empty directories in the project root:

- `database`
- `fit_results`

These directories are required because the `IdeaSearch` framework writes its output to `database`, and the `IdeaSearchFitter` class saves its results to `fit_results`.

---

## 3\. Run the Program

Execute the following command from the project's root directory to start the program:

```bash
python -m run
```

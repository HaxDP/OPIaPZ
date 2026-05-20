from pathlib import Path

from verificationService import buildReport, checkCodeStyle, runDynamicTests


def mainFunction():
    codePath = Path(__file__).resolve().parent / "verificationService.py"
    codeText = codePath.read_text(encoding="utf-8")
    results = []
    results.extend(checkCodeStyle(codeText))
    results.extend(runDynamicTests())
    print(buildReport(results))


if __name__ == "__main__":
    mainFunction()
from abc import ABC, abstractmethod
#також дотримувався SOLID для практики
class DataSourceInterface(ABC):
    @abstractmethod
    def loadDataFunction(self):
        pass

class StatusCalculatorInterface(ABC):
    @abstractmethod
    def calculateStatusFunction(self, items):
        pass

class ReportBuilderInterface(ABC):
    @abstractmethod
    def buildReportFunction(self, stats):
        pass

class StaticDataSource(DataSourceInterface):
    def loadDataFunction(self):
        return [
            {"назва": "API", "стан": "готово"},
            {"назва": "БД", "стан": "готово"},
            {"назва": "UI", "стан": "помилка"}
        ]

class DefaultStatusCalculator(StatusCalculatorInterface):
    def calculateStatusFunction(self, items):
        allCount = len(items)
        okCount = sum(1 for item in items if item["стан"] == "готово")
        return {"всього": allCount, "успіх": okCount, "помилки": allCount - okCount}

class UkrainianReportBuilder(ReportBuilderInterface):
    def buildReportFunction(self, stats):
        return (
            "звіт інтеграції:\n"
            f"компонентів: {stats['всього']}\n"
            f"успішно: {stats['успіх']}\n"
            f"помилок: {stats['помилки']}"
        )

class IntegrationService:
    def __init__(self, dataSource, calculator, reportBuilder):
        self.dataSource = dataSource
        self.calculator = calculator
        self.reportBuilder = reportBuilder

    def runIntegrationFunction(self):
        data = self.dataSource.loadDataFunction()
        stats = self.calculator.calculateStatusFunction(data)
        return self.reportBuilder.buildReportFunction(stats)

def loadDataFunction():
    return StaticDataSource().loadDataFunction()

def calculateStatusFunction(items):
    return DefaultStatusCalculator().calculateStatusFunction(items)

def buildReportFunction(stats):
    return UkrainianReportBuilder().buildReportFunction(stats)

def runIntegrationFunction():
    service = IntegrationService(
        StaticDataSource(),
        DefaultStatusCalculator(),
        UkrainianReportBuilder()
    )
    return service.runIntegrationFunction()
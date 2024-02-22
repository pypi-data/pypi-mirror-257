import abc
import uuid


class AbstractEvent(abc.ABC):
    def __init__(self):
        self.event_id = str(uuid.uuid4()).replace("-", "")
        self.task_thread = None

    @abc.abstractmethod
    def action(self): ...

    def call_back(self):
        """
        定义回调函数
        :return:
        :rtype:
        """
        ...

    def criteria_desc(self):
        """
        默认的为 空的字典
        :return:
        :rtype:
        """
        return dict()

    def fall_back(self, e):
        """
        如果有异常发生的时候的错误处理
        :param: e 系统捕获的异常
        :return:
        :rtype:
        """
        ...

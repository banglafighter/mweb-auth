from abc import ABC, abstractmethod


class MWebAuthBaseInterceptor(ABC):

    @abstractmethod
    async def intercept(self): ...
from calculator_pb2_grpc import CalculatorServicer

from calculator_pb2 import SumRequest
from calculator_pb2 import SumReply
from calculator_pb2 import MultiplyRequest
from calculator_pb2 import MultiplyReply       
from calculator_pb2 import ReturnBiggerRequest
from calculator_pb2 import ReturnBiggerReply     
from calculator_pb2 import QuotientRequest
from calculator_pb2 import QuotientReply

from grpc import ServicerContext


class Calculator(CalculatorServicer):

    def Sum(self, request: SumRequest, context: ServicerContext) -> SumReply:
        return SumReply(s=request.a + request.b)
    def Multiply(self, request: MultiplyRequest, context: ServicerContext) -> MultiplyReply:
        return MultiplyReply(result=request.a * request.b)
    def ReturnBigger(self, request: ReturnBiggerRequest, context: ServicerContext) -> ReturnBiggerReply:
        return ReturnBiggerReply(result=max(request.a, request.b, request.c))
    def Quotient(self, request: QuotientRequest, context: ServicerContext) -> QuotientReply: 
        return QuotientReply(quotient=int(request.numerator / request.denominator), rest=request.numerator % request.denominator)

    

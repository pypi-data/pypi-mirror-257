from jsonargparse import CLI 
from logging import getLogger
from .io import ParserOutput, HealthCheckOutput, DomainOutput, NLUInput
from .language import NLU
import uvicorn
from .utils import print_spent_time


logger = getLogger(__name__)


def serve(checkpoint: str, example: str = '你好', port: int = 18000, host: str = "localhost"):
    
    nlu = NLU.from_checkpoint(checkpoint)
    
    domain = nlu.domain
    
    
    logger.info(f"loading model {domain}")
    
    from fastapi import FastAPI
    app = FastAPI(description="NLU Inference API")
    
    @app.post("/parser", response_model=ParserOutput)
    def parse(inputs: NLUInput):
        
        with print_spent_time("parser"):
            output: ParserOutput = nlu.predict_parser(inputs.rawText)
            
        return output
    
    
    @app.post("/domain", response_model=DomainOutput)
    def domain(inputs: NLUInput):
        
        with print_spent_time("domain"):
            output =  nlu.predict_domain(inputs.rawText)
        return output
    
    
    @app.post("/health", response_model=HealthCheckOutput)
    def health():
        try:
            domain_results = nlu.predict_domain(example)
            parser_results = nlu.predict_parser(example)
            return HealthCheckOutput(code=0, message="success")
        except Exception as e:
            return HealthCheckOutput(code=1, message=str(e))
        
    uvicorn.run(app, host=host, port=port)


def run():
    CLI(serve)
from logging import DEBUG as logLevelDebug
import MyUtils as MU
import MyLogger as myLogger



MU.readYaml('lsu1proxy-3346.yaml')


global w6fLog
wf6Log:myLogger.SyxLogger

localLogger = myLogger.SyxLogger('web6test.log', level=logLevelDebug)
MU.setLogger(localLogger)
print('Initing')

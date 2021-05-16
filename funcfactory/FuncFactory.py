# standard lib imports
from inspect import getmembers, isfunction
import glob
import os
import traceback
import logging

# custom imports
from funcfactory.enums.severity_level import SeverityLevel
from funcfactory.enums.check_result import CheckResult
import funcfactory.utils.utils as ff_utils
import funcfactory.logging.logging as ff_log

class FunFactory:
    """A.k.a FunctionFactory: class that "uns" dynamic python pipelines

    What are dynamic pipelines you ask?
    Pipelines that basically change very often. The FunFactory enables you to configure highly dynamic
    pipelines specified by the standard library ConfigParser package. Users only need to make trivial
    changes to config files instead of changing lines of production code.

    All the typical production code matters are taken care of
    (read: logging, error handeling, result generation). Users simply define functions, load these and
    specify in what order these needs to be ran/what result one expects.

    example usage:
    """
    def __init__(self, folder_results ='./logs', list_modules_functions=None, func_logging_format=None):

        self.list_function_files = [] # placeholder yaml input files
        self.list_configs = []
        self.config_factory = {}
        self.dict_factory_objects={}

        os.makedirs(folder_results, exist_ok=True)
        self.folder_results=folder_results
        self.logging_formatter = self.func_logging_format if func_logging_format else ff_log.logging_formatter()

        if list_modules_functions:
            # self.list_check_modules=list_check_modules
            for mod in list_modules_functions:
                print(f"Info - Loading functions from {mod}")
                self.load_functions(mod)

    def read_file(self, file):
        print(f"Loading Fun from: {file} into Factory")
        assert os.path.isfile(file)
        if not file.endswith((".yaml", ".yml")):
            print("Not implemented error: Only yaml/yml files supported")
            return None

        config = ff_utils.read_yaml(file)
        self.config_factory.update({file:config})

    def read_config_folder(self, folder):
        assert os.path.isdir(folder)
        for file in glob.glob(os.path.join(folder,"*.*"), recursive=True):
            self.read_file(file)

    # do the problem is that every config file can have its own defaults.. we need to take care of this
    def run_fun(self):
        print("Creating Fun")
        for file, conf in self.config_factory.items():
            print(f"Running checks in functions in: {file}")
            try:
                conf_default = conf.pop('DEFAULT', {})

                if not conf_default:
                    print("Warning - Error no default settings found -> Attempting to run fun.")
                if not conf:
                    print("Error - no steps found -> Continuing")
                    continue

                if conf_default.get(DefaultKeys.SKIP, None):
                    print(f"Skipping functions in: {file}")
                    continue

                self.run_fun_single_config_file(conf_default, conf)

            except Exception as ex:
                traceback.print_exc()
                print(f"error occured in file: {file} -> {ex}")

    def run_fun_single_config_file(self, conf_default, conf_steps):
        """Function that actually runs the checks
        """
        assert isinstance(conf_default, dict)
        assert isinstance(conf_steps, dict)

        significance = conf_default.pop("significance", 2)
        check_name = conf_default.pop("check_name", "General Checks")
        logger_name = conf_default.pop("logger", "ResultsFunFactory")

        # todo set in utils function -> Implement basicConfig.. (reload logging mod)
        if logger_name in logging.root.manager.loggerDict:
            logger = logging.getLogger(logger_name) # get existing logger
        else:
            logger = logging.getLogger(logger_name) # creates new logger and adds file handler
            logger = self.logging_formatter(logger, logger_name)

        # logger.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
        logger.info(f"\n\n Running: {check_name}\n")

        for step_name, conf_step in conf_steps.items():

            try:
                print(f"Info - Running: {step_name}")
                func_left = getattr(self, conf_step.pop("func_left"))
                func_right = getattr(self, conf_step.pop("func_right"))
                kwargs_left = conf_step.pop("kwargs_left")
                kwargs_right = conf_step.pop("kwargs_right")

                value_left, log_left = func_left(**kwargs_left, **self.dict_factory_objects)
                value_right, log_right = func_right(**kwargs_right, **self.dict_factory_objects)

                # get the severity level corresponding to the check
                severity_lvl = SeverityLevel(conf_step["severity_level"])

                # Do the actual check and return the checkresult enum class
                check_result = CheckResult.get_check_result(
                    value_left, value_right, significance=significance
                )

                # We basically just form the 1 line of log per check here.
                m = f"{step_name.ljust(9)} - {str(check_result.name).ljust(7)}"

                # print severity if check result val in 4,3,0 and make sure rest of
                # the logs is evenly spaced
                m += (
                    f" - Severity: {severity_lvl.name}".ljust(24)
                    if check_result.value in [4, 3, 0]
                    else "".ljust(24)
                )
                m += f" - {log_left} - {log_right}"

                # if a explain function is passed add to log.
                # if func_explainer:
                #     log_additional = func_explainer(
                #         **eval(kwargs_right),
                #         **eval(kwargs_left),
                #         wb=wb,
                #         folder_protos=folder_zip,
                #     )
                #
                #     m += f" - Additional Logs: {log_additional}".ljust(70)

                print(f"writing to log for check: {step_name}\n")
                logger.info(m)

            # bit more info in logger if its a asserted error
            except AssertionError as ex:
                m = f"{step_name.ljust(9)} - {str(CheckResult(-1).name).ljust(7)} - Severity: {SeverityLevel(3).name.ljust(11)} - Assertion error occured "
                traceback.print_exc()
                logger.error(m + f"{ex}")

            except Exception as ex:
                m = f"{step_name.ljust(9)} Uncaught error occured for check "
                traceback.print_exc()
                logger.error(m)

    def load_functions(self, module):
        for name_func, func in getmembers(module, isfunction):
            # check if attribute doesnt already exist! otherwise error!
            if getattr(self, name_func, None):
                print(f"Error - {name_func} already loaded -> skipping")
                continue
            setattr(self, name_func, func)

    def load_factory_objects(self, *args, **kwargs):
        if kwargs:
            for k,v in kwargs.items():
                if k in self.__dict__.keys():
                    print(f"Warning - Object: {k} already loaded -> Overwritting")
                self.dict_factory_objects.update({k:v})
                # locals()[k] = v # aaah so locals keeps track of the class methods in scope, adding this here
        else:
            print("Please load object as kwargs: key=value pair")
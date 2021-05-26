# standard lib imports
from inspect import getmembers, isfunction
import glob
import os
import traceback
import logging
from importlib import reload

# custom imports
from .enums import (SeverityLevel, CheckResult, ConfigKeys)
from .utils import read_yaml


class FuncFactory:
    """A.k.a FunctionFactory: class that "runs" dynamic python pipelines

    What are dynamic pipelines you ask?
    Pipelines that basically change very often. The FunFactory enables you to configure
    highly dynamic pipelines specified by the standard library ConfigParser package.
    Users only need to make trivial changes to config files instead of changing lines of
     production code.

    All the typical production code matters are taken care of
    (read: logging, error handeling, result generation). Users simply define functions,
     load these and specify in what order these needs to be ran/what result one expects.

    example usage:
    """
    def __init__(
        self, folder_results="./logs", list_modules_functions=None, get_logger=None
    ):
        self.list_function_files = []  # placeholder yaml input files
        self.list_configs = []
        self.config_factory = {}
        self.dict_factory_objects = {}

        os.makedirs(folder_results, exist_ok=True)
        self.folder_results = folder_results
        self.get_logger = get_logger if get_logger else self.get_logger_default

        if list_modules_functions:
            # self.list_check_modules=list_check_modules
            for mod in list_modules_functions:
                print(f"Info - Loading functions from {mod}")
                self.load_functions(mod)

    def get_logger_default(self, logger_name):

        logger = logging.getLogger(
            logger_name
        )  # creates new logger and adds file handler
        fh = logging.FileHandler(
            os.path.join(self.folder_results, f"{logger_name}.log")
        )
        fh.setFormatter(
            logging.Formatter(
                "%(asctime)s - %(levelname)s - %(message)s", "%Y-%m-%d %H:%M:%S"
            )
        )
        logger.addHandler(fh)
        logger.setLevel(logging.INFO)
        logger.name = logger_name
        return logger

    def read_file(self, file):
        assert os.path.isfile(file)
        if not file.endswith((".yaml", ".yml")):
            return None

        print(f"Loading Fun from: {file} into Factory")
        self.config_factory.update({file: read_yaml(file)})

    def read_config_folder(self, folder):
        assert os.path.isdir(folder)
        for file in glob.glob(os.path.join(folder, "*.*"), recursive=True):
            self.read_file(file)

    # do the problem is that every config file can have its own defaults..
    # we need to take care of this
    def run_func(self):
        print("Creating Fun")
        for file, conf in self.config_factory.items():
            try:
                conf_default = conf.pop(ConfigKeys.DEFAULT, {})
                if not conf_default:
                    print("Warning - No default settings found -> Running Func..")

                if not conf:
                    print("Error - no steps found -> Continuing")
                    continue

                if conf_default.get(ConfigKeys.SKIP, None):
                    print(f"Skipping functions in: {file}")
                    continue
                print(f"Running checks in functions in: {file}")
                self.run_fun_single_config_file(conf_default, conf)

            except Exception as ex:
                traceback.print_exc()
                print(f"error occured in file: {file} -> {ex}")

        # finally flush result and remove loggers
        print("Shutting down loggers")
        self.flush_loggers()

    def flush_loggers(self):
        print("Flushing loggers")
        logging.shutdown()  # typical
        # very a typical, logging keeps the already created loggers in memory..
        # so if we run this a second time. the loggers are already there.. removing
        # is very problematic so we simply reset after flushing.
        reload(logging)
        return None

    def run_fun_single_config_file(self, conf_default, conf_steps):
        """Function that actually runs the checks"""
        assert isinstance(conf_default, dict)
        assert isinstance(conf_steps, dict)

        significance = conf_default.pop(ConfigKeys.SIGNIFICANCE, 2)
        check_name = conf_default.pop(ConfigKeys.CHECK_NAME, "General Checks")
        logger_name = conf_default.pop(ConfigKeys.LOGGER, "ResultsFunFactory")
        bStop_on_fail = conf_default.pop(ConfigKeys.STOP_RUN, False)

        logger = (
            logging.getLogger(logger_name)
            if logger_name in logging.root.manager.loggerDict
            else self.get_logger(logger_name)
        )

        # logger.setFormatter(logging.Formatter('%(asctime)s - %(message)s'))
        logger.info(f"\n\n Running: {check_name}\n")

        for step_name, conf_step in conf_steps.items():

            try:
                print(f"Info - Running: {step_name}")
                func_left = getattr(self, conf_step.pop("func_left"))
                func_right = getattr(self, conf_step.pop("func_right"))
                kwargs_left = conf_step.pop("kwargs_left")
                kwargs_right = conf_step.pop("kwargs_right")

                value_left, log_left = func_left(
                    **kwargs_left, **self.dict_factory_objects
                )
                value_right, log_right = func_right(
                    **kwargs_right, **self.dict_factory_objects
                )

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

                print(f"writing to log for check: {step_name}\n")
                logger.info(m)

                if bStop_on_fail and (
                    check_result == CheckResult.FAILED
                    or check_result == CheckResult.ERROR
                ):
                    logger.critical("Run aborted")
                    print("Run aborted")
                    break

            # bit more info in logger if its a asserted error
            except AssertionError as ex:
                m = f"{step_name.ljust(9)} " \
                    f"- {str(CheckResult(-1).name).ljust(7)} " \
                    f"- Severity: {SeverityLevel(3).name.ljust(11)} " \
                    f"- Assertion error occured "

                traceback.print_exc()
                logger.error(m + f"{ex}")
                if bStop_on_fail:
                    print("Run aborted")
                    break

            except Exception:
                m = f"{step_name.ljust(9)} Uncaught error occured for check "
                traceback.print_exc()
                logger.error(m)
                if bStop_on_fail:
                    print("Run aborted")
                    break

    def load_functions(self, module):
        for name_func, func in getmembers(module, isfunction):
            # check if attribute doesnt already exist! otherwise error!
            if getattr(self, name_func, None):
                print(f"Error - {name_func} already loaded -> skipping")
                continue
            setattr(self, name_func, func)

    def load_factory_objects(self, **kwargs):
        if kwargs:
            for k, v in kwargs.items():
                if k in self.__dict__.keys():
                    print(f"Warning - Object: {k} already loaded -> Overwritting")
                self.dict_factory_objects.update({k: v})
        else:
            print("Please load object as kwargs: key=value pair")
